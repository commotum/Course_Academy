# Original MA evidence and generated variants

Raw evidence is ineligible; every normal question has one fixed complete worked solution. Source IDs, parameters and profiles are review metadata, not learner content.

## original MA evidence — q-15717 / source / {"n": 8}

What is the antiderivative of $\frac{8}{3x}?$

- $\frac{8}{3}\operatorname{ln}⁡(|x|+K)$
- $\frac{8}{3}\operatorname{ln}⁡(K|x|)$
- $\frac{1}{3}\operatorname{ln}⁡(8|x|+K)$
- $\operatorname{ln}⁡(\frac{8}{3}K|x|)$
- $\frac{1}{3}\operatorname{ln}⁡(8K|x|)$

First, we apply the constant factor rule and take the coefficient $\frac{8}{3}$ out of the integral. Then we compute the integral of $\frac{1}{x},$ and get

$$
\begin{aligned}\int \frac{8}{3x}\text{d}x & =\frac{8}{3}\int \frac{1}{x}\text{d}x \\  & =\frac{8}{3}\operatorname{ln}⁡|x|+C.\end{aligned}
$$

Lastly, let's rewrite the constant so that we can combine it with the natural logarithm. For any constant $C,$ we can always write $C=\frac{8}{3}\operatorname{ln}⁡K$ where $K$ is some other positive constant. Doing this allows us to combine the constant with $\frac{8}{3}\operatorname{ln}⁡|x|$ term, and we get

$$
\begin{aligned}\int \frac{8}{3x}\text{d}x & =\frac{8}{3}\operatorname{ln}⁡|x|+C \\  & =\frac{8}{3}\operatorname{ln}⁡|x|+\frac{8}{3}\operatorname{ln}⁡K \\  & =\frac{8}{3}(\operatorname{ln}⁡|x|+\operatorname{ln}⁡K) \\  & =\frac{8}{3}\operatorname{ln}⁡(K|x|).\end{aligned}
$$

## normal original-parameter presentation / documented repair — q-15717 / normal / {"n": 8}

What is the antiderivative of $\frac{8}{3x}?$

- $\frac{8}{3}\ln(|x|+K)$
- $\frac{8}{3}\ln(K|x|)$
- $\frac{1}{3}\ln(8|x|+K)$
- $\ln(\frac{8}{3}K|x|)$
- $\frac{1}{3}\ln(8K|x|)$

First, we apply the constant factor rule and take the coefficient $\frac{8}{3}$ out of the integral. Then we compute the integral of $\frac{1}{x},$ and get

$$
\begin{aligned}\int \frac{8}{3x}\text{d}x & =\frac{8}{3}\int \frac{1}{x}\text{d}x \\  & =\frac{8}{3}\ln|x|+C.\end{aligned}
$$

Lastly, let's rewrite the constant so that we can combine it with the natural logarithm. For any constant $C,$ we can always write $C=\frac{8}{3}\ln K$ where $K$ is some other positive constant. Doing this allows us to combine the constant with $\frac{8}{3}\ln|x|$ term, and we get

$$
\begin{aligned}\int \frac{8}{3x}\text{d}x & =\frac{8}{3}\ln|x|+C \\  & =\frac{8}{3}\ln|x|+\frac{8}{3}\ln K \\  & =\frac{8}{3}(\ln|x|+\ln K) \\  & =\frac{8}{3}\ln(K|x|).\end{aligned}
$$

## original MA evidence — q-103375 / source / {"n": 3}

What is the antiderivative of ${(1+\frac{3}{2x})}^{2}?$

- $1-\frac{3}{2x}+3ln⁡(K|x|)$
- $1-\frac{3}{2x}+ln⁡(3K|x|)$
- $x-\frac{3}{2x}+3ln⁡(K|x|)$
- $x-\frac{9}{4x}+ln⁡(3K|x|)$
- $x-\frac{9}{4x}+3ln⁡(K|x|)$

Expanding the binomial and applying the sum and constant factor rules, we get

$$
\begin{aligned}\int {(1+\frac{3}{2x})}^{2}\text{d}x & =\int (1+\frac{3}{x}+\frac{9}{4{x}^{2}})\text{d}x \\  & =\int \text{d}x+3\int \frac{1}{x}\,\text{d}x+\frac{9}{4}\int \frac{1}{{x}^{2}}\,\text{d}x \\  & =x+3ln⁡|x|+\frac{9{x}^{-2+1}}{4(-2+1)}+C \\  & =x+3ln⁡|x|-\frac{9}{4x}+C.\end{aligned}
$$

Lastly, let's rewrite the constant so that we can combine it with the natural logarithm. For any constant $C,$ we can always write $C=3ln⁡K$ where $K$ is some other positive constant. Doing this allows us to combine the constant with $3ln⁡|x|$ term, and we get

$$
\begin{aligned}\int {(1+\frac{3}{2x})}^{2}\text{d}x & =x-\frac{9}{4x}+3ln⁡|x|+3ln⁡K \\  & =x-\frac{9}{4x}+3(ln⁡|x|+ln⁡K) \\  & =x-\frac{9}{4x}+3ln⁡(K|x|).\end{aligned}
$$

## normal original-parameter presentation / documented repair — q-103375 / normal / {"n": 3}

What is the antiderivative of ${(1+\frac{3}{2x})}^{2}?$

- $1-\frac{3}{2x}+3\ln(K|x|)$
- $1-\frac{3}{2x}+\ln(3K|x|)$
- $x-\frac{3}{2x}+3\ln(K|x|)$
- $x-\frac{9}{4x}+\ln(3K|x|)$
- $x-\frac{9}{4x}+3\ln(K|x|)$

Expanding the binomial and applying the sum and constant factor rules, we get

$$
\begin{aligned}\int {(1+\frac{3}{2x})}^{2}\text{d}x & =\int (1+\frac{3}{x}+\frac{9}{4{x}^{2}})\text{d}x \\  & =\int \text{d}x+3\int \frac{1}{x}\,\text{d}x+\frac{9}{4}\int \frac{1}{{x}^{2}}\,\text{d}x \\  & =x+3\ln|x|+\frac{9{x}^{-2+1}}{4(-2+1)}+C \\  & =x+3\ln|x|-\frac{9}{4x}+C.\end{aligned}
$$

Lastly, let's rewrite the constant so that we can combine it with the natural logarithm. For any constant $C,$ we can always write $C=3\ln K$ where $K$ is some other positive constant. Doing this allows us to combine the constant with $3\ln|x|$ term, and we get

$$
\begin{aligned}\int {(1+\frac{3}{2x})}^{2}\text{d}x & =x-\frac{9}{4x}+3\ln|x|+3\ln K \\  & =x-\frac{9}{4x}+3(\ln|x|+\ln K) \\  & =x-\frac{9}{4x}+3\ln(K|x|).\end{aligned}
$$

## original MA evidence — q-103605 / source / {"n": 2}

What is the antiderivative of $\frac{2x-1}{x}?$

- $2x+\operatorname{ln}⁡(K|x|)$
- ${x}^{2}-\operatorname{ln}⁡(K|x|)$
- ${x}^{2}+\operatorname{ln}⁡(K|x|)$
- $2x-\operatorname{ln}⁡(K|x|)$
- $2x+\operatorname{ln}⁡(|x|+K)$

We separate the integrand into the sum of two fractions so that we can simplify each term. So, we get

$$
\begin{aligned}\int \frac{2x-1}{x}\,\text{d}x & =\int (\frac{2x}{x}-\frac{1}{x})\,\text{d}x \\  & =\int (2-\frac{1}{x})\,\text{d}x \\  & =2\int \,\text{d}x-\int \frac{1}{x}\,\text{d}x \\  & =2x-\operatorname{ln}⁡|x|+C.\end{aligned}
$$

Lastly, let's rewrite the constant so that we can combine it with the natural logarithm. For any constant $C,$ we can always write $C=-\operatorname{ln}⁡K$ where $K$ is some other positive constant. Doing this allows us to combine the constant with $-\operatorname{ln}⁡|x|$ term, and we get

$$
\begin{aligned}\int \frac{2x-1}{x}\,\text{d}x & =2x-\operatorname{ln}⁡|x|+C \\  & =2x-\operatorname{ln}⁡|x|-\operatorname{ln}⁡K \\  & =2x-(\operatorname{ln}⁡|x|+\operatorname{ln}⁡K) \\  & =2x-\operatorname{ln}⁡(K|x|).\end{aligned}
$$

## normal original-parameter presentation / documented repair — q-103605 / normal / {"n": 2}

What is the antiderivative of $\frac{2x-1}{x}?$

- $2x+\ln(K|x|)$
- ${x}^{2}-\ln(K|x|)$
- ${x}^{2}+\ln(K|x|)$
- $2x-\ln(K|x|)$
- $2x+\ln(|x|+K)$

We separate the integrand into the sum of two fractions so that we can simplify each term. So, we get

$$
\begin{aligned}\int \frac{2x-1}{x}\,\text{d}x & =\int (\frac{2x}{x}-\frac{1}{x})\,\text{d}x \\  & =\int (2-\frac{1}{x})\,\text{d}x \\  & =2\int \,\text{d}x-\int \frac{1}{x}\,\text{d}x \\  & =2x-\ln|x|+C.\end{aligned}
$$

Lastly, let's rewrite the constant so that we can combine it with the natural logarithm. For any constant $C,$ we can always write $C=-\ln K$ where $K$ is some other positive constant. Doing this allows us to combine the constant with $-\ln|x|$ term, and we get

$$
\begin{aligned}\int \frac{2x-1}{x}\,\text{d}x & =2x-\ln|x|+C \\  & =2x-\ln|x|-\ln K \\  & =2x-(\ln|x|+\ln K) \\  & =2x-\ln(K|x|).\end{aligned}
$$

## original MA evidence — q-15710 / source / {"n": 5}

What is the antiderivative of $\frac{5}{2x}?$

- $ln⁡(\frac{5}{2}|x|+K)$
- $\frac{5}{2}ln⁡(|x|+K)$
- $ln⁡(\frac{5}{2}K|x|)$
- $\frac{1}{2}ln⁡(5K|x|)$
- $\frac{5}{2}ln⁡(K|x|)$

First, we apply the constant factor rule and take the coefficient $\frac{5}{2}$ out of the integral. Then we compute the integral of $\frac{1}{x},$ and get

$$
\begin{aligned}\int \frac{5}{2x}\text{d}x & =\frac{5}{2}\int \frac{1}{x}\text{d}x \\  & =\frac{5}{2}ln⁡|x|+C.\end{aligned}
$$

Lastly, let's rewrite the constant so that we can combine it with the natural logarithm. For any constant $C,$ we can always write $C=\frac{5}{2}ln⁡K$ where $K$ is some other positive constant. Doing this allows us to combine the constant with $\frac{5}{2}ln⁡|x|$ term, and we get

$$
\begin{aligned}\int \frac{5}{2x}\text{d}x & =\frac{5}{2}ln⁡|x|+\frac{5}{2}ln⁡K \\  & =\frac{5}{2}(ln⁡|x|+ln⁡K) \\  & =\frac{5}{2}ln⁡(K|x|).\end{aligned}
$$

## normal original-parameter presentation / documented repair — q-15710 / normal / {"n": 5}

What is the antiderivative of $\frac{5}{2x}?$

- $\ln(\frac{5}{2}|x|+K)$
- $\frac{5}{2}\ln(|x|+K)$
- $\ln(\frac{5}{2}K|x|)$
- $\frac{1}{2}\ln(5K|x|)$
- $\frac{5}{2}\ln(K|x|)$

First, we apply the constant factor rule and take the coefficient $\frac{5}{2}$ out of the integral. Then we compute the integral of $\frac{1}{x},$ and get

$$
\begin{aligned}\int \frac{5}{2x}\text{d}x & =\frac{5}{2}\int \frac{1}{x}\text{d}x \\  & =\frac{5}{2}\ln|x|+C.\end{aligned}
$$

Lastly, let's rewrite the constant so that we can combine it with the natural logarithm. For any constant $C,$ we can always write $C=\frac{5}{2}\ln K$ where $K$ is some other positive constant. Doing this allows us to combine the constant with $\frac{5}{2}\ln|x|$ term, and we get

$$
\begin{aligned}\int \frac{5}{2x}\text{d}x & =\frac{5}{2}\ln|x|+\frac{5}{2}\ln K \\  & =\frac{5}{2}(\ln|x|+\ln K) \\  & =\frac{5}{2}\ln(K|x|).\end{aligned}
$$

## original MA evidence — q-29834 / source / {"n": 5}

What is the antiderivative of $-\frac{5}{2x}?$

- $-\frac{5}{2}ln⁡(K|x|)$
- $\frac{5}{2}ln⁡(K|x|)$
- $\frac{1}{2}ln⁡(5K|x|)$
- $-\frac{5}{2}ln⁡(|x|+K)$
- $-ln⁡(\frac{5}{2}K|x|)$

First, we apply the constant factor rule and take the coefficient $-\frac{5}{2}$ out of the integral. Then we compute the integral of $\frac{1}{x},$ and get

$$
\begin{aligned}\int -\frac{5}{2x}\,\text{d}x & =-\frac{5}{2}\int \frac{1}{x}\,\text{d}x \\  & =-\frac{5}{2}ln⁡|x|+C.\end{aligned}
$$

Lastly, let's rewrite the constant so that we can combine it with the natural logarithm. For any constant $C,$ we can always write $C=-\frac{5}{2}ln⁡K$ where $K$ is some other positive constant. Doing this allows us to combine the constant with $-\frac{5}{2}ln⁡|x|$ term, and we get

$$
\begin{aligned}\int -\frac{5}{2x}\,\text{d}x & =-\frac{5}{2}ln⁡|x|-\frac{5}{2}ln⁡K \\  & =-\frac{5}{2}(ln⁡|x|+ln⁡K) \\  & =-\frac{5}{2}ln⁡(K|x|).\end{aligned}
$$

## normal original-parameter presentation / documented repair — q-29834 / normal / {"n": 5}

What is the antiderivative of $-\frac{5}{2x}?$

- $-\frac{5}{2}\ln(K|x|)$
- $\frac{5}{2}\ln(K|x|)$
- $\frac{1}{2}\ln(5K|x|)$
- $-\frac{5}{2}\ln(|x|+K)$
- $-\ln(\frac{5}{2}K|x|)$

First, we apply the constant factor rule and take the coefficient $-\frac{5}{2}$ out of the integral. Then we compute the integral of $\frac{1}{x},$ and get

$$
\begin{aligned}\int -\frac{5}{2x}\,\text{d}x & =-\frac{5}{2}\int \frac{1}{x}\,\text{d}x \\  & =-\frac{5}{2}\ln|x|+C.\end{aligned}
$$

Lastly, let's rewrite the constant so that we can combine it with the natural logarithm. For any constant $C,$ we can always write $C=-\frac{5}{2}\ln K$ where $K$ is some other positive constant. Doing this allows us to combine the constant with $-\frac{5}{2}\ln|x|$ term, and we get

$$
\begin{aligned}\int -\frac{5}{2x}\,\text{d}x & =-\frac{5}{2}\ln|x|-\frac{5}{2}\ln K \\  & =-\frac{5}{2}(\ln|x|+\ln K) \\  & =-\frac{5}{2}\ln(K|x|).\end{aligned}
$$

## original MA evidence — q-103603 / source / {"n": 2}

What is the antiderivative of $2{x}^{-1}?$

- $2ln⁡(K|x|)$
- $ln⁡(\frac{K|x|}{2})$
- $\frac{ln⁡(K|x|)}{2}$
- $ln⁡(2K|x|)$
- $\frac{2}{ln⁡(K|x|)}$

First, we apply the constant factor rule and take the coefficient $2$ out of the integral. Then we compute the integral of $\frac{1}{x},$ and get

$$
\begin{aligned}\int 2{x}^{-1}\,\text{d}x & =2\int \frac{1}{x}\,\text{d}x \\  & =2ln⁡|x|+C.\end{aligned}
$$

Lastly, let's rewrite the constant so that we can combine it with the natural logarithm. For any constant $C,$ we can always write $C=2ln⁡K$ where $K$ is some other positive constant. Doing this allows us to combine the constant with $2ln⁡|x|$ term, and we get

$$
\begin{aligned}\int 2{x}^{-1}\,\text{d}x & =2ln⁡|x|+2ln⁡K \\  & =2(ln⁡|x|+ln⁡K) \\  & =2ln⁡(K|x|).\end{aligned}
$$

## normal original-parameter presentation / documented repair — q-103603 / normal / {"n": 2}

What is the antiderivative of $2{x}^{-1}?$

- $2\ln(K|x|)$
- $\ln(\frac{K|x|}{2})$
- $\frac{\ln(K|x|)}{2}$
- $-\ln(K|x|)$
- $\frac{2}{\ln(K|x|)}$

First, we apply the constant factor rule and take the coefficient $2$ out of the integral. Then we compute the integral of $\frac{1}{x},$ and get

$$
\begin{aligned}\int 2{x}^{-1}\,\text{d}x & =2\int \frac{1}{x}\,\text{d}x \\  & =2\ln|x|+C.\end{aligned}
$$

Lastly, let's rewrite the constant so that we can combine it with the natural logarithm. For any constant $C,$ we can always write $C=2\ln K$ where $K$ is some other positive constant. Doing this allows us to combine the constant with $2\ln|x|$ term, and we get

$$
\begin{aligned}\int 2{x}^{-1}\,\text{d}x & =2\ln|x|+2\ln K \\  & =2(\ln|x|+\ln K) \\  & =2\ln(K|x|).\end{aligned}
$$

## original MA evidence — q-49067 / source / {"n": 1}

What is the antiderivative of ${(1+\frac{1}{x})}^{2}?$

- $1+2ln⁡(|K|x)$
- $1-\frac{1}{x}+2ln⁡(|K|x)$
- $x-\frac{1}{x}+2ln⁡(K|x|)$
- $x+(1+ln⁡(K|x|))^{2}$
- $x-\frac{1}{x}+ln⁡(2K|x|)$

Expanding the binomial and applying the sum and constant factor rules, we get

$$
\begin{aligned}\int {(1+\frac{1}{x})}^{2}\text{d}x & =\int (1+\frac{2}{x}+\frac{1}{{x}^{2}})\text{d}x \\  & =\int \text{d}x+2\int \frac{1}{x}\,\text{d}x+\int \frac{1}{{x}^{2}}\,\text{d}x \\  & =x+2ln⁡|x|+\frac{{x}^{-2+1}}{-2+1}+C \\  & =x+2ln⁡|x|-\frac{1}{x}+C.\end{aligned}
$$

Lastly, let's rewrite the constant so that we can combine it with the natural logarithm. For any constant $C,$ we can always write $C=2ln⁡K$ where $K$ is some other positive constant. Doing this allows us to combine the constant with $2ln⁡|x|$ term, and we get

$$
\begin{aligned}\int {(1+\frac{1}{x})}^{2}\text{d}x & =x-\frac{1}{x}+2ln⁡|x|+2ln⁡K \\  & =x-\frac{1}{x}+2(ln⁡|x|+ln⁡K) \\  & =x-\frac{1}{x}+2ln⁡(K|x|).\end{aligned}
$$

## normal original-parameter presentation / documented repair — q-49067 / normal / {"n": 1}

What is the antiderivative of ${(1+\frac{1}{x})}^{2}?$

- $1+2\ln(K|x|)$
- $1-\frac{1}{x}+2\ln(K|x|)$
- $x-\frac{1}{x}+2\ln(K|x|)$
- $x+(1+\ln(K|x|))^{2}$
- $x-\frac{1}{x}+\ln(2K|x|)$

Expanding the binomial and applying the sum and constant factor rules, we get

$$
\begin{aligned}\int {(1+\frac{1}{x})}^{2}\text{d}x & =\int (1+\frac{2}{x}+\frac{1}{{x}^{2}})\text{d}x \\  & =\int \text{d}x+2\int \frac{1}{x}\,\text{d}x+\int \frac{1}{{x}^{2}}\,\text{d}x \\  & =x+2\ln|x|+\frac{{x}^{-2+1}}{-2+1}+C \\  & =x+2\ln|x|-\frac{1}{x}+C.\end{aligned}
$$

Lastly, let's rewrite the constant so that we can combine it with the natural logarithm. For any constant $C,$ we can always write $C=2\ln K$ where $K$ is some other positive constant. Doing this allows us to combine the constant with $2\ln|x|$ term, and we get

$$
\begin{aligned}\int {(1+\frac{1}{x})}^{2}\text{d}x & =x-\frac{1}{x}+2\ln|x|+2\ln K \\  & =x-\frac{1}{x}+2(\ln|x|+\ln K) \\  & =x-\frac{1}{x}+2\ln(K|x|).\end{aligned}
$$

## original MA evidence — q-49096 / source / {"a": 6, "b": 7}

What is the antiderivative of $\frac{6 + 7x}{x}$?

- $6\ln (K \mid x \mid) - 7x$
- $6\ln (K \mid x \mid + 7)$
- $\ln (K(6 + 7 \mid x \mid))$
- $6\ln (K \mid x \mid) + 7x$
- $\ln (7K \mid x \mid + 6)$

[Captured source omits a worked solution.]

## normal original-parameter presentation / documented repair — q-49096 / normal / {"a": 6, "b": 7}

What is the antiderivative of $\frac{6 + 7x}{x}$?

- $6\ln (K \mid x \mid) - 7x$
- $6\ln (K \mid x \mid + 7)$
- $\ln (K(6 + 7 \mid x \mid))$
- $6\ln (K \mid x \mid) + 7x$
- $\ln (7K \mid x \mid + 6)$

We separate the integrand into the sum of two fractions so that we can simplify each term. So, we get

$$
\begin{aligned}\int \frac{6 + 7x}{x}\,\text{d}x & =\int (\frac{6}{x}+\frac{7x}{x})\,\text{d}x \\ & =\int (\frac{6}{x}+7)\,\text{d}x \\ & =6\int \frac{1}{x}\,\text{d}x+7\int \,\text{d}x \\ & =6\ln|x|+7x+C.\end{aligned}
$$

Lastly, let's rewrite the constant so that we can combine it with the natural logarithm. For any constant $C,$ we can always write $C=6\ln K$ where $K$ is some other positive constant. Doing this allows us to combine the constant with $6\ln|x|$ term, and we get

$$
\begin{aligned}\int \frac{6 + 7x}{x}\,\text{d}x & =6\ln|x|+7x+C \\ & =6\ln|x|+7x+6\ln K \\ & =6\ln(K|x|)+7x.\end{aligned}
$$

## generated variant; authored missing-level easy — easy_integer / normal / {"n": -24}

What is the antiderivative of $-\frac{24}{x}?$

- $-24\ln(|x|+K)$
- $24\ln(K|x|)$
- $\ln(K|x|)$
- $-24\ln(K|x|)$
- $\frac{1}{-24}\ln(K|x|)$

First, we apply the constant factor rule and take the coefficient $-24$ out of the integral. Then we compute the integral of $\frac{1}{x},$ and get

$$
\begin{aligned}\int -\frac{24}{x}\,\text{d}x & =-24\int \frac{1}{x}\,\text{d}x \\ & =-24\ln|x|+C.\end{aligned}
$$

Lastly, let's rewrite the constant so that we can combine it with the natural logarithm. For any constant $C,$ we can always write $C=-24\ln K$ where $K$ is some other positive constant. Doing this allows us to combine the constant with $-24\ln|x|$ term, and we get

$$
\begin{aligned}\int -\frac{24}{x}\,\text{d}x & =-24\ln|x|+C \\ & =-24\ln|x|+(-24)\ln K \\ & =-24(\ln|x|+\ln K) \\ & =-24\ln(K|x|).\end{aligned}
$$

## generated variant; authored missing-level easy — easy_integer / normal / {"n": 24}

What is the antiderivative of $\frac{24}{x}?$

- $24\ln(|x|+K)$
- $-24\ln(K|x|)$
- $\ln(K|x|)$
- $24\ln(K|x|)$
- $\frac{1}{24}\ln(K|x|)$

First, we apply the constant factor rule and take the coefficient $24$ out of the integral. Then we compute the integral of $\frac{1}{x},$ and get

$$
\begin{aligned}\int \frac{24}{x}\,\text{d}x & =24\int \frac{1}{x}\,\text{d}x \\ & =24\ln|x|+C.\end{aligned}
$$

Lastly, let's rewrite the constant so that we can combine it with the natural logarithm. For any constant $C,$ we can always write $C=24\ln K$ where $K$ is some other positive constant. Doing this allows us to combine the constant with $24\ln|x|$ term, and we get

$$
\begin{aligned}\int \frac{24}{x}\,\text{d}x & =24\ln|x|+C \\ & =24\ln|x|+24\ln K \\ & =24(\ln|x|+\ln K) \\ & =24\ln(K|x|).\end{aligned}
$$

## generated variant; source-family normal — q-15717 / normal / {"n": 4}

What is the antiderivative of $\frac{4}{3x}?$

- $\ln(\frac{4}{3}K|x|)$
- $\frac{4}{3}\ln(K|x|)$
- $\frac{1}{3}\ln(4K|x|)$
- $\frac{1}{3}\ln(4|x|+K)$
- $\frac{4}{3}\ln(|x|+K)$

First, we apply the constant factor rule and take the coefficient $\frac{4}{3}$ out of the integral. Then we compute the integral of $\frac{1}{x},$ and get

$$
\begin{aligned}\int \frac{4}{3x}\text{d}x & =\frac{4}{3}\int \frac{1}{x}\text{d}x \\  & =\frac{4}{3}\ln|x|+C.\end{aligned}
$$

Lastly, let's rewrite the constant so that we can combine it with the natural logarithm. For any constant $C,$ we can always write $C=\frac{4}{3}\ln K$ where $K$ is some other positive constant. Doing this allows us to combine the constant with $\frac{4}{3}\ln|x|$ term, and we get

$$
\begin{aligned}\int \frac{4}{3x}\text{d}x & =\frac{4}{3}\ln|x|+C \\  & =\frac{4}{3}\ln|x|+\frac{4}{3}\ln K \\  & =\frac{4}{3}(\ln|x|+\ln K) \\  & =\frac{4}{3}\ln(K|x|).\end{aligned}
$$

## generated variant; source-family source — q-15717 / source / {"n": 4}

What is the antiderivative of $\frac{4}{3x}?$

- $\operatorname{ln}⁡(\frac{4}{3}K|x|)$
- $\frac{4}{3}\operatorname{ln}⁡(K|x|)$
- $\frac{1}{3}\operatorname{ln}⁡(4K|x|)$
- $\frac{1}{3}\operatorname{ln}⁡(4|x|+K)$
- $\frac{4}{3}\operatorname{ln}⁡(|x|+K)$

First, we apply the constant factor rule and take the coefficient $\frac{4}{3}$ out of the integral. Then we compute the integral of $\frac{1}{x},$ and get

$$
\begin{aligned}\int \frac{4}{3x}\text{d}x & =\frac{4}{3}\int \frac{1}{x}\text{d}x \\  & =\frac{4}{3}\operatorname{ln}⁡|x|+C.\end{aligned}
$$

Lastly, let's rewrite the constant so that we can combine it with the natural logarithm. For any constant $C,$ we can always write $C=\frac{4}{3}\operatorname{ln}⁡K$ where $K$ is some other positive constant. Doing this allows us to combine the constant with $\frac{4}{3}\operatorname{ln}⁡|x|$ term, and we get

$$
\begin{aligned}\int \frac{4}{3x}\text{d}x & =\frac{4}{3}\operatorname{ln}⁡|x|+C \\  & =\frac{4}{3}\operatorname{ln}⁡|x|+\frac{4}{3}\operatorname{ln}⁡K \\  & =\frac{4}{3}(\operatorname{ln}⁡|x|+\operatorname{ln}⁡K) \\  & =\frac{4}{3}\operatorname{ln}⁡(K|x|).\end{aligned}
$$

## generated variant; source-family normal — q-15717 / normal / {"n": 31}

What is the antiderivative of $\frac{31}{3x}?$

- $\ln(\frac{31}{3}K|x|)$
- $\frac{31}{3}\ln(K|x|)$
- $\frac{1}{3}\ln(31K|x|)$
- $\frac{1}{3}\ln(31|x|+K)$
- $\frac{31}{3}\ln(|x|+K)$

First, we apply the constant factor rule and take the coefficient $\frac{31}{3}$ out of the integral. Then we compute the integral of $\frac{1}{x},$ and get

$$
\begin{aligned}\int \frac{31}{3x}\text{d}x & =\frac{31}{3}\int \frac{1}{x}\text{d}x \\  & =\frac{31}{3}\ln|x|+C.\end{aligned}
$$

Lastly, let's rewrite the constant so that we can combine it with the natural logarithm. For any constant $C,$ we can always write $C=\frac{31}{3}\ln K$ where $K$ is some other positive constant. Doing this allows us to combine the constant with $\frac{31}{3}\ln|x|$ term, and we get

$$
\begin{aligned}\int \frac{31}{3x}\text{d}x & =\frac{31}{3}\ln|x|+C \\  & =\frac{31}{3}\ln|x|+\frac{31}{3}\ln K \\  & =\frac{31}{3}(\ln|x|+\ln K) \\  & =\frac{31}{3}\ln(K|x|).\end{aligned}
$$

## generated variant; source-family source — q-15717 / source / {"n": 31}

What is the antiderivative of $\frac{31}{3x}?$

- $\operatorname{ln}⁡(\frac{31}{3}K|x|)$
- $\frac{31}{3}\operatorname{ln}⁡(K|x|)$
- $\frac{1}{3}\operatorname{ln}⁡(31K|x|)$
- $\frac{1}{3}\operatorname{ln}⁡(31|x|+K)$
- $\frac{31}{3}\operatorname{ln}⁡(|x|+K)$

First, we apply the constant factor rule and take the coefficient $\frac{31}{3}$ out of the integral. Then we compute the integral of $\frac{1}{x},$ and get

$$
\begin{aligned}\int \frac{31}{3x}\text{d}x & =\frac{31}{3}\int \frac{1}{x}\text{d}x \\  & =\frac{31}{3}\operatorname{ln}⁡|x|+C.\end{aligned}
$$

Lastly, let's rewrite the constant so that we can combine it with the natural logarithm. For any constant $C,$ we can always write $C=\frac{31}{3}\operatorname{ln}⁡K$ where $K$ is some other positive constant. Doing this allows us to combine the constant with $\frac{31}{3}\operatorname{ln}⁡|x|$ term, and we get

$$
\begin{aligned}\int \frac{31}{3x}\text{d}x & =\frac{31}{3}\operatorname{ln}⁡|x|+C \\  & =\frac{31}{3}\operatorname{ln}⁡|x|+\frac{31}{3}\operatorname{ln}⁡K \\  & =\frac{31}{3}(\operatorname{ln}⁡|x|+\operatorname{ln}⁡K) \\  & =\frac{31}{3}\operatorname{ln}⁡(K|x|).\end{aligned}
$$

## generated variant; source-family normal — q-103605 / normal / {"n": 2}

What is the antiderivative of $\frac{2x-1}{x}?$

- $2x-\ln(K|x|)$
- ${x}^{2}-\ln(K|x|)$
- $2x+\ln(|x|+K)$
- ${x}^{2}+\ln(K|x|)$
- $2x+\ln(K|x|)$

We separate the integrand into the sum of two fractions so that we can simplify each term. So, we get

$$
\begin{aligned}\int \frac{2x-1}{x}\,\text{d}x & =\int (\frac{2x}{x}-\frac{1}{x})\,\text{d}x \\  & =\int (2-\frac{1}{x})\,\text{d}x \\  & =2\int \,\text{d}x-\int \frac{1}{x}\,\text{d}x \\  & =2x-\ln|x|+C.\end{aligned}
$$

Lastly, let's rewrite the constant so that we can combine it with the natural logarithm. For any constant $C,$ we can always write $C=-\ln K$ where $K$ is some other positive constant. Doing this allows us to combine the constant with $-\ln|x|$ term, and we get

$$
\begin{aligned}\int \frac{2x-1}{x}\,\text{d}x & =2x-\ln|x|+C \\  & =2x-\ln|x|-\ln K \\  & =2x-(\ln|x|+\ln K) \\  & =2x-\ln(K|x|).\end{aligned}
$$

## generated variant; source-family source — q-103605 / source / {"n": 2}

What is the antiderivative of $\frac{2x-1}{x}?$

- $2x-\operatorname{ln}⁡(K|x|)$
- ${x}^{2}-\operatorname{ln}⁡(K|x|)$
- $2x+\operatorname{ln}⁡(|x|+K)$
- ${x}^{2}+\operatorname{ln}⁡(K|x|)$
- $2x+\operatorname{ln}⁡(K|x|)$

We separate the integrand into the sum of two fractions so that we can simplify each term. So, we get

$$
\begin{aligned}\int \frac{2x-1}{x}\,\text{d}x & =\int (\frac{2x}{x}-\frac{1}{x})\,\text{d}x \\  & =\int (2-\frac{1}{x})\,\text{d}x \\  & =2\int \,\text{d}x-\int \frac{1}{x}\,\text{d}x \\  & =2x-\operatorname{ln}⁡|x|+C.\end{aligned}
$$

Lastly, let's rewrite the constant so that we can combine it with the natural logarithm. For any constant $C,$ we can always write $C=-\operatorname{ln}⁡K$ where $K$ is some other positive constant. Doing this allows us to combine the constant with $-\operatorname{ln}⁡|x|$ term, and we get

$$
\begin{aligned}\int \frac{2x-1}{x}\,\text{d}x & =2x-\operatorname{ln}⁡|x|+C \\  & =2x-\operatorname{ln}⁡|x|-\operatorname{ln}⁡K \\  & =2x-(\operatorname{ln}⁡|x|+\operatorname{ln}⁡K) \\  & =2x-\operatorname{ln}⁡(K|x|).\end{aligned}
$$

## generated variant; source-family normal — q-103605 / normal / {"n": 31}

What is the antiderivative of $\frac{31x-1}{x}?$

- $31x-\ln(K|x|)$
- ${x}^{2}-\ln(K|x|)$
- $31x+\ln(|x|+K)$
- ${x}^{2}+\ln(K|x|)$
- $31x+\ln(K|x|)$

We separate the integrand into the sum of two fractions so that we can simplify each term. So, we get

$$
\begin{aligned}\int \frac{31x-1}{x}\,\text{d}x & =\int (\frac{31x}{x}-\frac{1}{x})\,\text{d}x \\  & =\int (31-\frac{1}{x})\,\text{d}x \\  & =31\int \,\text{d}x-\int \frac{1}{x}\,\text{d}x \\  & =31x-\ln|x|+C.\end{aligned}
$$

Lastly, let's rewrite the constant so that we can combine it with the natural logarithm. For any constant $C,$ we can always write $C=-\ln K$ where $K$ is some other positive constant. Doing this allows us to combine the constant with $-\ln|x|$ term, and we get

$$
\begin{aligned}\int \frac{31x-1}{x}\,\text{d}x & =31x-\ln|x|+C \\  & =31x-\ln|x|-\ln K \\  & =31x-(\ln|x|+\ln K) \\  & =31x-\ln(K|x|).\end{aligned}
$$

## generated variant; source-family source — q-103605 / source / {"n": 31}

What is the antiderivative of $\frac{31x-1}{x}?$

- $31x-\operatorname{ln}⁡(K|x|)$
- ${x}^{2}-\operatorname{ln}⁡(K|x|)$
- $31x+\operatorname{ln}⁡(|x|+K)$
- ${x}^{2}+\operatorname{ln}⁡(K|x|)$
- $31x+\operatorname{ln}⁡(K|x|)$

We separate the integrand into the sum of two fractions so that we can simplify each term. So, we get

$$
\begin{aligned}\int \frac{31x-1}{x}\,\text{d}x & =\int (\frac{31x}{x}-\frac{1}{x})\,\text{d}x \\  & =\int (31-\frac{1}{x})\,\text{d}x \\  & =31\int \,\text{d}x-\int \frac{1}{x}\,\text{d}x \\  & =31x-\operatorname{ln}⁡|x|+C.\end{aligned}
$$

Lastly, let's rewrite the constant so that we can combine it with the natural logarithm. For any constant $C,$ we can always write $C=-\operatorname{ln}⁡K$ where $K$ is some other positive constant. Doing this allows us to combine the constant with $-\operatorname{ln}⁡|x|$ term, and we get

$$
\begin{aligned}\int \frac{31x-1}{x}\,\text{d}x & =31x-\operatorname{ln}⁡|x|+C \\  & =31x-\operatorname{ln}⁡|x|-\operatorname{ln}⁡K \\  & =31x-(\operatorname{ln}⁡|x|+\operatorname{ln}⁡K) \\  & =31x-\operatorname{ln}⁡(K|x|).\end{aligned}
$$

## generated variant; source-family normal — q-15710 / normal / {"n": 3}

What is the antiderivative of $\frac{3}{2x}?$

- $\frac{1}{2}\ln(3K|x|)$
- $\frac{3}{2}\ln(|x|+K)$
- $\frac{3}{2}\ln(K|x|)$
- $\ln(\frac{3}{2}K|x|)$
- $\ln(\frac{3}{2}|x|+K)$

First, we apply the constant factor rule and take the coefficient $\frac{3}{2}$ out of the integral. Then we compute the integral of $\frac{1}{x},$ and get

$$
\begin{aligned}\int \frac{3}{2x}\text{d}x & =\frac{3}{2}\int \frac{1}{x}\text{d}x \\  & =\frac{3}{2}\ln|x|+C.\end{aligned}
$$

Lastly, let's rewrite the constant so that we can combine it with the natural logarithm. For any constant $C,$ we can always write $C=\frac{3}{2}\ln K$ where $K$ is some other positive constant. Doing this allows us to combine the constant with $\frac{3}{2}\ln|x|$ term, and we get

$$
\begin{aligned}\int \frac{3}{2x}\text{d}x & =\frac{3}{2}\ln|x|+\frac{3}{2}\ln K \\  & =\frac{3}{2}(\ln|x|+\ln K) \\  & =\frac{3}{2}\ln(K|x|).\end{aligned}
$$

## generated variant; source-family source — q-15710 / source / {"n": 3}

What is the antiderivative of $\frac{3}{2x}?$

- $\frac{1}{2}ln⁡(3K|x|)$
- $\frac{3}{2}ln⁡(|x|+K)$
- $\frac{3}{2}ln⁡(K|x|)$
- $ln⁡(\frac{3}{2}K|x|)$
- $ln⁡(\frac{3}{2}|x|+K)$

First, we apply the constant factor rule and take the coefficient $\frac{3}{2}$ out of the integral. Then we compute the integral of $\frac{1}{x},$ and get

$$
\begin{aligned}\int \frac{3}{2x}\text{d}x & =\frac{3}{2}\int \frac{1}{x}\text{d}x \\  & =\frac{3}{2}ln⁡|x|+C.\end{aligned}
$$

Lastly, let's rewrite the constant so that we can combine it with the natural logarithm. For any constant $C,$ we can always write $C=\frac{3}{2}ln⁡K$ where $K$ is some other positive constant. Doing this allows us to combine the constant with $\frac{3}{2}ln⁡|x|$ term, and we get

$$
\begin{aligned}\int \frac{3}{2x}\text{d}x & =\frac{3}{2}ln⁡|x|+\frac{3}{2}ln⁡K \\  & =\frac{3}{2}(ln⁡|x|+ln⁡K) \\  & =\frac{3}{2}ln⁡(K|x|).\end{aligned}
$$

## generated variant; source-family normal — q-15710 / normal / {"n": 31}

What is the antiderivative of $\frac{31}{2x}?$

- $\frac{1}{2}\ln(31K|x|)$
- $\frac{31}{2}\ln(|x|+K)$
- $\frac{31}{2}\ln(K|x|)$
- $\ln(\frac{31}{2}K|x|)$
- $\ln(\frac{31}{2}|x|+K)$

First, we apply the constant factor rule and take the coefficient $\frac{31}{2}$ out of the integral. Then we compute the integral of $\frac{1}{x},$ and get

$$
\begin{aligned}\int \frac{31}{2x}\text{d}x & =\frac{31}{2}\int \frac{1}{x}\text{d}x \\  & =\frac{31}{2}\ln|x|+C.\end{aligned}
$$

Lastly, let's rewrite the constant so that we can combine it with the natural logarithm. For any constant $C,$ we can always write $C=\frac{31}{2}\ln K$ where $K$ is some other positive constant. Doing this allows us to combine the constant with $\frac{31}{2}\ln|x|$ term, and we get

$$
\begin{aligned}\int \frac{31}{2x}\text{d}x & =\frac{31}{2}\ln|x|+\frac{31}{2}\ln K \\  & =\frac{31}{2}(\ln|x|+\ln K) \\  & =\frac{31}{2}\ln(K|x|).\end{aligned}
$$

## generated variant; source-family source — q-15710 / source / {"n": 31}

What is the antiderivative of $\frac{31}{2x}?$

- $\frac{1}{2}ln⁡(31K|x|)$
- $\frac{31}{2}ln⁡(|x|+K)$
- $\frac{31}{2}ln⁡(K|x|)$
- $ln⁡(\frac{31}{2}K|x|)$
- $ln⁡(\frac{31}{2}|x|+K)$

First, we apply the constant factor rule and take the coefficient $\frac{31}{2}$ out of the integral. Then we compute the integral of $\frac{1}{x},$ and get

$$
\begin{aligned}\int \frac{31}{2x}\text{d}x & =\frac{31}{2}\int \frac{1}{x}\text{d}x \\  & =\frac{31}{2}ln⁡|x|+C.\end{aligned}
$$

Lastly, let's rewrite the constant so that we can combine it with the natural logarithm. For any constant $C,$ we can always write $C=\frac{31}{2}ln⁡K$ where $K$ is some other positive constant. Doing this allows us to combine the constant with $\frac{31}{2}ln⁡|x|$ term, and we get

$$
\begin{aligned}\int \frac{31}{2x}\text{d}x & =\frac{31}{2}ln⁡|x|+\frac{31}{2}ln⁡K \\  & =\frac{31}{2}(ln⁡|x|+ln⁡K) \\  & =\frac{31}{2}ln⁡(K|x|).\end{aligned}
$$

## generated variant; source-family normal — q-29834 / normal / {"n": 3}

What is the antiderivative of $-\frac{3}{2x}?$

- $-\frac{3}{2}\ln(|x|+K)$
- $\frac{3}{2}\ln(K|x|)$
- $-\ln(\frac{3}{2}K|x|)$
- $\frac{1}{2}\ln(3K|x|)$
- $-\frac{3}{2}\ln(K|x|)$

First, we apply the constant factor rule and take the coefficient $-\frac{3}{2}$ out of the integral. Then we compute the integral of $\frac{1}{x},$ and get

$$
\begin{aligned}\int -\frac{3}{2x}\,\text{d}x & =-\frac{3}{2}\int \frac{1}{x}\,\text{d}x \\  & =-\frac{3}{2}\ln|x|+C.\end{aligned}
$$

Lastly, let's rewrite the constant so that we can combine it with the natural logarithm. For any constant $C,$ we can always write $C=-\frac{3}{2}\ln K$ where $K$ is some other positive constant. Doing this allows us to combine the constant with $-\frac{3}{2}\ln|x|$ term, and we get

$$
\begin{aligned}\int -\frac{3}{2x}\,\text{d}x & =-\frac{3}{2}\ln|x|-\frac{3}{2}\ln K \\  & =-\frac{3}{2}(\ln|x|+\ln K) \\  & =-\frac{3}{2}\ln(K|x|).\end{aligned}
$$

## generated variant; source-family source — q-29834 / source / {"n": 3}

What is the antiderivative of $-\frac{3}{2x}?$

- $-\frac{3}{2}ln⁡(|x|+K)$
- $\frac{3}{2}ln⁡(K|x|)$
- $-ln⁡(\frac{3}{2}K|x|)$
- $\frac{1}{2}ln⁡(3K|x|)$
- $-\frac{3}{2}ln⁡(K|x|)$

First, we apply the constant factor rule and take the coefficient $-\frac{3}{2}$ out of the integral. Then we compute the integral of $\frac{1}{x},$ and get

$$
\begin{aligned}\int -\frac{3}{2x}\,\text{d}x & =-\frac{3}{2}\int \frac{1}{x}\,\text{d}x \\  & =-\frac{3}{2}ln⁡|x|+C.\end{aligned}
$$

Lastly, let's rewrite the constant so that we can combine it with the natural logarithm. For any constant $C,$ we can always write $C=-\frac{3}{2}ln⁡K$ where $K$ is some other positive constant. Doing this allows us to combine the constant with $-\frac{3}{2}ln⁡|x|$ term, and we get

$$
\begin{aligned}\int -\frac{3}{2x}\,\text{d}x & =-\frac{3}{2}ln⁡|x|-\frac{3}{2}ln⁡K \\  & =-\frac{3}{2}(ln⁡|x|+ln⁡K) \\  & =-\frac{3}{2}ln⁡(K|x|).\end{aligned}
$$

## generated variant; source-family normal — q-29834 / normal / {"n": 31}

What is the antiderivative of $-\frac{31}{2x}?$

- $-\frac{31}{2}\ln(|x|+K)$
- $\frac{31}{2}\ln(K|x|)$
- $-\ln(\frac{31}{2}K|x|)$
- $\frac{1}{2}\ln(31K|x|)$
- $-\frac{31}{2}\ln(K|x|)$

First, we apply the constant factor rule and take the coefficient $-\frac{31}{2}$ out of the integral. Then we compute the integral of $\frac{1}{x},$ and get

$$
\begin{aligned}\int -\frac{31}{2x}\,\text{d}x & =-\frac{31}{2}\int \frac{1}{x}\,\text{d}x \\  & =-\frac{31}{2}\ln|x|+C.\end{aligned}
$$

Lastly, let's rewrite the constant so that we can combine it with the natural logarithm. For any constant $C,$ we can always write $C=-\frac{31}{2}\ln K$ where $K$ is some other positive constant. Doing this allows us to combine the constant with $-\frac{31}{2}\ln|x|$ term, and we get

$$
\begin{aligned}\int -\frac{31}{2x}\,\text{d}x & =-\frac{31}{2}\ln|x|-\frac{31}{2}\ln K \\  & =-\frac{31}{2}(\ln|x|+\ln K) \\  & =-\frac{31}{2}\ln(K|x|).\end{aligned}
$$

## generated variant; source-family source — q-29834 / source / {"n": 31}

What is the antiderivative of $-\frac{31}{2x}?$

- $-\frac{31}{2}ln⁡(|x|+K)$
- $\frac{31}{2}ln⁡(K|x|)$
- $-ln⁡(\frac{31}{2}K|x|)$
- $\frac{1}{2}ln⁡(31K|x|)$
- $-\frac{31}{2}ln⁡(K|x|)$

First, we apply the constant factor rule and take the coefficient $-\frac{31}{2}$ out of the integral. Then we compute the integral of $\frac{1}{x},$ and get

$$
\begin{aligned}\int -\frac{31}{2x}\,\text{d}x & =-\frac{31}{2}\int \frac{1}{x}\,\text{d}x \\  & =-\frac{31}{2}ln⁡|x|+C.\end{aligned}
$$

Lastly, let's rewrite the constant so that we can combine it with the natural logarithm. For any constant $C,$ we can always write $C=-\frac{31}{2}ln⁡K$ where $K$ is some other positive constant. Doing this allows us to combine the constant with $-\frac{31}{2}ln⁡|x|$ term, and we get

$$
\begin{aligned}\int -\frac{31}{2x}\,\text{d}x & =-\frac{31}{2}ln⁡|x|-\frac{31}{2}ln⁡K \\  & =-\frac{31}{2}(ln⁡|x|+ln⁡K) \\  & =-\frac{31}{2}ln⁡(K|x|).\end{aligned}
$$

## generated variant; source-family normal — q-103603 / normal / {"n": 2}

What is the antiderivative of $2{x}^{-1}?$

- $-\ln(K|x|)$
- $\ln(\frac{K|x|}{2})$
- $\frac{2}{\ln(K|x|)}$
- $\frac{\ln(K|x|)}{2}$
- $2\ln(K|x|)$

First, we apply the constant factor rule and take the coefficient $2$ out of the integral. Then we compute the integral of $\frac{1}{x},$ and get

$$
\begin{aligned}\int 2{x}^{-1}\,\text{d}x & =2\int \frac{1}{x}\,\text{d}x \\  & =2\ln|x|+C.\end{aligned}
$$

Lastly, let's rewrite the constant so that we can combine it with the natural logarithm. For any constant $C,$ we can always write $C=2\ln K$ where $K$ is some other positive constant. Doing this allows us to combine the constant with $2\ln|x|$ term, and we get

$$
\begin{aligned}\int 2{x}^{-1}\,\text{d}x & =2\ln|x|+2\ln K \\  & =2(\ln|x|+\ln K) \\  & =2\ln(K|x|).\end{aligned}
$$

## generated variant; source-family source — q-103603 / source / {"n": 2}

What is the antiderivative of $2{x}^{-1}?$

- $ln⁡(2K|x|)$
- $ln⁡(\frac{K|x|}{2})$
- $\frac{2}{ln⁡(K|x|)}$
- $\frac{ln⁡(K|x|)}{2}$
- $2ln⁡(K|x|)$

First, we apply the constant factor rule and take the coefficient $2$ out of the integral. Then we compute the integral of $\frac{1}{x},$ and get

$$
\begin{aligned}\int 2{x}^{-1}\,\text{d}x & =2\int \frac{1}{x}\,\text{d}x \\  & =2ln⁡|x|+C.\end{aligned}
$$

Lastly, let's rewrite the constant so that we can combine it with the natural logarithm. For any constant $C,$ we can always write $C=2ln⁡K$ where $K$ is some other positive constant. Doing this allows us to combine the constant with $2ln⁡|x|$ term, and we get

$$
\begin{aligned}\int 2{x}^{-1}\,\text{d}x & =2ln⁡|x|+2ln⁡K \\  & =2(ln⁡|x|+ln⁡K) \\  & =2ln⁡(K|x|).\end{aligned}
$$

## generated variant; source-family normal — q-103603 / normal / {"n": 31}

What is the antiderivative of $31{x}^{-1}?$

- $-\ln(K|x|)$
- $\ln(\frac{K|x|}{31})$
- $\frac{31}{\ln(K|x|)}$
- $\frac{\ln(K|x|)}{31}$
- $31\ln(K|x|)$

First, we apply the constant factor rule and take the coefficient $31$ out of the integral. Then we compute the integral of $\frac{1}{x},$ and get

$$
\begin{aligned}\int 31{x}^{-1}\,\text{d}x & =31\int \frac{1}{x}\,\text{d}x \\  & =31\ln|x|+C.\end{aligned}
$$

Lastly, let's rewrite the constant so that we can combine it with the natural logarithm. For any constant $C,$ we can always write $C=31\ln K$ where $K$ is some other positive constant. Doing this allows us to combine the constant with $31\ln|x|$ term, and we get

$$
\begin{aligned}\int 31{x}^{-1}\,\text{d}x & =31\ln|x|+31\ln K \\  & =31(\ln|x|+\ln K) \\  & =31\ln(K|x|).\end{aligned}
$$

## generated variant; source-family source — q-103603 / source / {"n": 31}

What is the antiderivative of $31{x}^{-1}?$

- $ln⁡(31K|x|)$
- $ln⁡(\frac{K|x|}{31})$
- $\frac{31}{ln⁡(K|x|)}$
- $\frac{ln⁡(K|x|)}{31}$
- $31ln⁡(K|x|)$

First, we apply the constant factor rule and take the coefficient $31$ out of the integral. Then we compute the integral of $\frac{1}{x},$ and get

$$
\begin{aligned}\int 31{x}^{-1}\,\text{d}x & =31\int \frac{1}{x}\,\text{d}x \\  & =31ln⁡|x|+C.\end{aligned}
$$

Lastly, let's rewrite the constant so that we can combine it with the natural logarithm. For any constant $C,$ we can always write $C=31ln⁡K$ where $K$ is some other positive constant. Doing this allows us to combine the constant with $31ln⁡|x|$ term, and we get

$$
\begin{aligned}\int 31{x}^{-1}\,\text{d}x & =31ln⁡|x|+31ln⁡K \\  & =31(ln⁡|x|+ln⁡K) \\  & =31ln⁡(K|x|).\end{aligned}
$$

## generated variant; source-family normal — q-49096 / normal / {"a": 2, "b": 2}

What is the antiderivative of $\frac{2 + 2x}{x}$?

- $2\ln (K \mid x \mid) + 2x$
- $2\ln (K \mid x \mid + 2)$
- $\ln (2K \mid x \mid + 2)$
- $\ln (K(2 + 2 \mid x \mid))$
- $2\ln (K \mid x \mid) - 2x$

We separate the integrand into the sum of two fractions so that we can simplify each term. So, we get

$$
\begin{aligned}\int \frac{2 + 2x}{x}\,\text{d}x & =\int (\frac{2}{x}+\frac{2x}{x})\,\text{d}x \\ & =\int (\frac{2}{x}+2)\,\text{d}x \\ & =2\int \frac{1}{x}\,\text{d}x+2\int \,\text{d}x \\ & =2\ln|x|+2x+C.\end{aligned}
$$

Lastly, let's rewrite the constant so that we can combine it with the natural logarithm. For any constant $C,$ we can always write $C=2\ln K$ where $K$ is some other positive constant. Doing this allows us to combine the constant with $2\ln|x|$ term, and we get

$$
\begin{aligned}\int \frac{2 + 2x}{x}\,\text{d}x & =2\ln|x|+2x+C \\ & =2\ln|x|+2x+2\ln K \\ & =2\ln(K|x|)+2x.\end{aligned}
$$

## generated variant; source-family source — q-49096 / source / {"a": 2, "b": 2}

What is the antiderivative of $\frac{2 + 2x}{x}$?

- $2\ln (K \mid x \mid) + 2x$
- $2\ln (K \mid x \mid + 2)$
- $\ln (2K \mid x \mid + 2)$
- $\ln (K(2 + 2 \mid x \mid))$
- $2\ln (K \mid x \mid) - 2x$

[Captured source omits a worked solution.]

## generated variant; source-family normal — q-49096 / normal / {"a": 12, "b": 12}

What is the antiderivative of $\frac{12 + 12x}{x}$?

- $12\ln (K \mid x \mid) + 12x$
- $12\ln (K \mid x \mid + 12)$
- $\ln (12K \mid x \mid + 12)$
- $\ln (K(12 + 12 \mid x \mid))$
- $12\ln (K \mid x \mid) - 12x$

We separate the integrand into the sum of two fractions so that we can simplify each term. So, we get

$$
\begin{aligned}\int \frac{12 + 12x}{x}\,\text{d}x & =\int (\frac{12}{x}+\frac{12x}{x})\,\text{d}x \\ & =\int (\frac{12}{x}+12)\,\text{d}x \\ & =12\int \frac{1}{x}\,\text{d}x+12\int \,\text{d}x \\ & =12\ln|x|+12x+C.\end{aligned}
$$

Lastly, let's rewrite the constant so that we can combine it with the natural logarithm. For any constant $C,$ we can always write $C=12\ln K$ where $K$ is some other positive constant. Doing this allows us to combine the constant with $12\ln|x|$ term, and we get

$$
\begin{aligned}\int \frac{12 + 12x}{x}\,\text{d}x & =12\ln|x|+12x+C \\ & =12\ln|x|+12x+12\ln K \\ & =12\ln(K|x|)+12x.\end{aligned}
$$

## generated variant; source-family source — q-49096 / source / {"a": 12, "b": 12}

What is the antiderivative of $\frac{12 + 12x}{x}$?

- $12\ln (K \mid x \mid) + 12x$
- $12\ln (K \mid x \mid + 12)$
- $\ln (12K \mid x \mid + 12)$
- $\ln (K(12 + 12 \mid x \mid))$
- $12\ln (K \mid x \mid) - 12x$

[Captured source omits a worked solution.]

## generated variant; source-family normal — q-103375 / normal / {"n": 3}

What is the antiderivative of ${(1+\frac{3}{2x})}^{2}?$

- $x-\frac{9}{4x}+\ln(3K|x|)$
- $1-\frac{3}{2x}+\ln(3K|x|)$
- $x-\frac{9}{4x}+3\ln(K|x|)$
- $x-\frac{3}{2x}+3\ln(K|x|)$
- $1-\frac{3}{2x}+3\ln(K|x|)$

Expanding the binomial and applying the sum and constant factor rules, we get

$$
\begin{aligned}\int {(1+\frac{3}{2x})}^{2}\text{d}x & =\int (1+\frac{3}{x}+\frac{9}{4{x}^{2}})\text{d}x \\  & =\int \text{d}x+3\int \frac{1}{x}\,\text{d}x+\frac{9}{4}\int \frac{1}{{x}^{2}}\,\text{d}x \\  & =x+3\ln|x|+\frac{9{x}^{-2+1}}{4(-2+1)}+C \\  & =x+3\ln|x|-\frac{9}{4x}+C.\end{aligned}
$$

Lastly, let's rewrite the constant so that we can combine it with the natural logarithm. For any constant $C,$ we can always write $C=3\ln K$ where $K$ is some other positive constant. Doing this allows us to combine the constant with $3\ln|x|$ term, and we get

$$
\begin{aligned}\int {(1+\frac{3}{2x})}^{2}\text{d}x & =x-\frac{9}{4x}+3\ln|x|+3\ln K \\  & =x-\frac{9}{4x}+3(\ln|x|+\ln K) \\  & =x-\frac{9}{4x}+3\ln(K|x|).\end{aligned}
$$

## generated variant; source-family source — q-103375 / source / {"n": 3}

What is the antiderivative of ${(1+\frac{3}{2x})}^{2}?$

- $x-\frac{9}{4x}+ln⁡(3K|x|)$
- $1-\frac{3}{2x}+ln⁡(3K|x|)$
- $x-\frac{9}{4x}+3ln⁡(K|x|)$
- $x-\frac{3}{2x}+3ln⁡(K|x|)$
- $1-\frac{3}{2x}+3ln⁡(K|x|)$

Expanding the binomial and applying the sum and constant factor rules, we get

$$
\begin{aligned}\int {(1+\frac{3}{2x})}^{2}\text{d}x & =\int (1+\frac{3}{x}+\frac{9}{4{x}^{2}})\text{d}x \\  & =\int \text{d}x+3\int \frac{1}{x}\,\text{d}x+\frac{9}{4}\int \frac{1}{{x}^{2}}\,\text{d}x \\  & =x+3ln⁡|x|+\frac{9{x}^{-2+1}}{4(-2+1)}+C \\  & =x+3ln⁡|x|-\frac{9}{4x}+C.\end{aligned}
$$

Lastly, let's rewrite the constant so that we can combine it with the natural logarithm. For any constant $C,$ we can always write $C=3ln⁡K$ where $K$ is some other positive constant. Doing this allows us to combine the constant with $3ln⁡|x|$ term, and we get

$$
\begin{aligned}\int {(1+\frac{3}{2x})}^{2}\text{d}x & =x-\frac{9}{4x}+3ln⁡|x|+3ln⁡K \\  & =x-\frac{9}{4x}+3(ln⁡|x|+ln⁡K) \\  & =x-\frac{9}{4x}+3ln⁡(K|x|).\end{aligned}
$$

## generated variant; source-family normal — q-103375 / normal / {"n": 31}

What is the antiderivative of ${(1+\frac{31}{2x})}^{2}?$

- $x-\frac{961}{4x}+\ln(31K|x|)$
- $1-\frac{31}{2x}+\ln(31K|x|)$
- $x-\frac{961}{4x}+31\ln(K|x|)$
- $x-\frac{31}{2x}+31\ln(K|x|)$
- $1-\frac{31}{2x}+31\ln(K|x|)$

Expanding the binomial and applying the sum and constant factor rules, we get

$$
\begin{aligned}\int {(1+\frac{31}{2x})}^{2}\text{d}x & =\int (1+\frac{31}{x}+\frac{961}{4{x}^{2}})\text{d}x \\  & =\int \text{d}x+31\int \frac{1}{x}\,\text{d}x+\frac{961}{4}\int \frac{1}{{x}^{2}}\,\text{d}x \\  & =x+31\ln|x|+\frac{961{x}^{-2+1}}{4(-2+1)}+C \\  & =x+31\ln|x|-\frac{961}{4x}+C.\end{aligned}
$$

Lastly, let's rewrite the constant so that we can combine it with the natural logarithm. For any constant $C,$ we can always write $C=31\ln K$ where $K$ is some other positive constant. Doing this allows us to combine the constant with $31\ln|x|$ term, and we get

$$
\begin{aligned}\int {(1+\frac{31}{2x})}^{2}\text{d}x & =x-\frac{961}{4x}+31\ln|x|+31\ln K \\  & =x-\frac{961}{4x}+31(\ln|x|+\ln K) \\  & =x-\frac{961}{4x}+31\ln(K|x|).\end{aligned}
$$

## generated variant; source-family source — q-103375 / source / {"n": 31}

What is the antiderivative of ${(1+\frac{31}{2x})}^{2}?$

- $x-\frac{961}{4x}+ln⁡(31K|x|)$
- $1-\frac{31}{2x}+ln⁡(31K|x|)$
- $x-\frac{961}{4x}+31ln⁡(K|x|)$
- $x-\frac{31}{2x}+31ln⁡(K|x|)$
- $1-\frac{31}{2x}+31ln⁡(K|x|)$

Expanding the binomial and applying the sum and constant factor rules, we get

$$
\begin{aligned}\int {(1+\frac{31}{2x})}^{2}\text{d}x & =\int (1+\frac{31}{x}+\frac{961}{4{x}^{2}})\text{d}x \\  & =\int \text{d}x+31\int \frac{1}{x}\,\text{d}x+\frac{961}{4}\int \frac{1}{{x}^{2}}\,\text{d}x \\  & =x+31ln⁡|x|+\frac{961{x}^{-2+1}}{4(-2+1)}+C \\  & =x+31ln⁡|x|-\frac{961}{4x}+C.\end{aligned}
$$

Lastly, let's rewrite the constant so that we can combine it with the natural logarithm. For any constant $C,$ we can always write $C=31ln⁡K$ where $K$ is some other positive constant. Doing this allows us to combine the constant with $31ln⁡|x|$ term, and we get

$$
\begin{aligned}\int {(1+\frac{31}{2x})}^{2}\text{d}x & =x-\frac{961}{4x}+31ln⁡|x|+31ln⁡K \\  & =x-\frac{961}{4x}+31(ln⁡|x|+ln⁡K) \\  & =x-\frac{961}{4x}+31ln⁡(K|x|).\end{aligned}
$$

## generated variant; source-family normal — q-49067 / normal / {"n": 1}

What is the antiderivative of ${(1+\frac{1}{x})}^{2}?$

- $x+(1+\ln(K|x|))^{2}$
- $1-\frac{1}{x}+2\ln(K|x|)$
- $x-\frac{1}{x}+\ln(2K|x|)$
- $x-\frac{1}{x}+2\ln(K|x|)$
- $1+2\ln(K|x|)$

Expanding the binomial and applying the sum and constant factor rules, we get

$$
\begin{aligned}\int {(1+\frac{1}{x})}^{2}\text{d}x & =\int (1+\frac{2}{x}+\frac{1}{{x}^{2}})\text{d}x \\  & =\int \text{d}x+2\int \frac{1}{x}\,\text{d}x+\int \frac{1}{{x}^{2}}\,\text{d}x \\  & =x+2\ln|x|+\frac{{x}^{-2+1}}{-2+1}+C \\  & =x+2\ln|x|-\frac{1}{x}+C.\end{aligned}
$$

Lastly, let's rewrite the constant so that we can combine it with the natural logarithm. For any constant $C,$ we can always write $C=2\ln K$ where $K$ is some other positive constant. Doing this allows us to combine the constant with $2\ln|x|$ term, and we get

$$
\begin{aligned}\int {(1+\frac{1}{x})}^{2}\text{d}x & =x-\frac{1}{x}+2\ln|x|+2\ln K \\  & =x-\frac{1}{x}+2(\ln|x|+\ln K) \\  & =x-\frac{1}{x}+2\ln(K|x|).\end{aligned}
$$

## generated variant; source-family source — q-49067 / source / {"n": 1}

What is the antiderivative of ${(1+\frac{1}{x})}^{2}?$

- $x+(1+ln⁡(K|x|))^{2}$
- $1-\frac{1}{x}+2ln⁡(|K|x)$
- $x-\frac{1}{x}+ln⁡(2K|x|)$
- $x-\frac{1}{x}+2ln⁡(K|x|)$
- $1+2ln⁡(|K|x)$

Expanding the binomial and applying the sum and constant factor rules, we get

$$
\begin{aligned}\int {(1+\frac{1}{x})}^{2}\text{d}x & =\int (1+\frac{2}{x}+\frac{1}{{x}^{2}})\text{d}x \\  & =\int \text{d}x+2\int \frac{1}{x}\,\text{d}x+\int \frac{1}{{x}^{2}}\,\text{d}x \\  & =x+2ln⁡|x|+\frac{{x}^{-2+1}}{-2+1}+C \\  & =x+2ln⁡|x|-\frac{1}{x}+C.\end{aligned}
$$

Lastly, let's rewrite the constant so that we can combine it with the natural logarithm. For any constant $C,$ we can always write $C=2ln⁡K$ where $K$ is some other positive constant. Doing this allows us to combine the constant with $2ln⁡|x|$ term, and we get

$$
\begin{aligned}\int {(1+\frac{1}{x})}^{2}\text{d}x & =x-\frac{1}{x}+2ln⁡|x|+2ln⁡K \\  & =x-\frac{1}{x}+2(ln⁡|x|+ln⁡K) \\  & =x-\frac{1}{x}+2ln⁡(K|x|).\end{aligned}
$$

## generated variant; source-family normal — q-49067 / normal / {"n": 15}

What is the antiderivative of ${(1+\frac{15}{x})}^{2}?$

- $x+(1+15\ln(K|x|))^{2}$
- $1-\frac{225}{x}+30\ln(K|x|)$
- $x-\frac{225}{x}+\ln(30K|x|)$
- $x-\frac{225}{x}+30\ln(K|x|)$
- $1+30\ln(K|x|)$

Expanding the binomial and applying the sum and constant factor rules, we get

$$
\begin{aligned}\int {(1+\frac{15}{x})}^{2}\text{d}x & =\int (1+\frac{30}{x}+\frac{225}{{x}^{2}})\text{d}x \\  & =\int \text{d}x+30\int \frac{1}{x}\,\text{d}x+225\int \frac{1}{{x}^{2}}\,\text{d}x \\  & =x+30\ln|x|+\frac{225{x}^{-2+1}}{-2+1}+C \\  & =x+30\ln|x|-\frac{225}{x}+C.\end{aligned}
$$

Lastly, let's rewrite the constant so that we can combine it with the natural logarithm. For any constant $C,$ we can always write $C=30\ln K$ where $K$ is some other positive constant. Doing this allows us to combine the constant with $30\ln|x|$ term, and we get

$$
\begin{aligned}\int {(1+\frac{15}{x})}^{2}\text{d}x & =x-\frac{225}{x}+30\ln|x|+30\ln K \\  & =x-\frac{225}{x}+30(\ln|x|+\ln K) \\  & =x-\frac{225}{x}+30\ln(K|x|).\end{aligned}
$$

## generated variant; source-family source — q-49067 / source / {"n": 15}

What is the antiderivative of ${(1+\frac{15}{x})}^{2}?$

- $x+(1+15ln⁡(K|x|))^{2}$
- $1-\frac{225}{x}+30ln⁡(|K|x)$
- $x-\frac{225}{x}+ln⁡(30K|x|)$
- $x-\frac{225}{x}+30ln⁡(K|x|)$
- $1+30ln⁡(|K|x)$

Expanding the binomial and applying the sum and constant factor rules, we get

$$
\begin{aligned}\int {(1+\frac{15}{x})}^{2}\text{d}x & =\int (1+\frac{30}{x}+\frac{225}{{x}^{2}})\text{d}x \\  & =\int \text{d}x+30\int \frac{1}{x}\,\text{d}x+225\int \frac{1}{{x}^{2}}\,\text{d}x \\  & =x+30ln⁡|x|+\frac{225{x}^{-2+1}}{-2+1}+C \\  & =x+30ln⁡|x|-\frac{225}{x}+C.\end{aligned}
$$

Lastly, let's rewrite the constant so that we can combine it with the natural logarithm. For any constant $C,$ we can always write $C=30ln⁡K$ where $K$ is some other positive constant. Doing this allows us to combine the constant with $30ln⁡|x|$ term, and we get

$$
\begin{aligned}\int {(1+\frac{15}{x})}^{2}\text{d}x & =x-\frac{225}{x}+30ln⁡|x|+30ln⁡K \\  & =x-\frac{225}{x}+30(ln⁡|x|+ln⁡K) \\  & =x-\frac{225}{x}+30ln⁡(K|x|).\end{aligned}
$$
