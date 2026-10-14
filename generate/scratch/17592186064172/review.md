# General-base exponential integral review — basis 2275

Raw originals preserve omissions; generated examples use completed authored normal records. No plots required.

## Original q-31248 — raw observed evidence

What is $\displaystyle \int4 \cdot 5^{x}dx$?

- $2 \cdot \frac{4^{x}}{\ln 5} + C$

- $\frac{\ln x}{\ln 5} + C$

- $\frac{5}{\ln x} + C$

- $4 \cdot \frac{5^{x}}{\ln 5} + C$

- $4 \cdot \frac{5^{\ln x}}{\ln 5} + C$

## Original q-66139 — raw observed evidence

Calculate $\int {3}^{x}\,\text{d}x.$

- ${3}^{x}ln⁡3+C$

- $ln⁡({3}^{x})+C$

- $\frac{{3}^{x}}{ln⁡3}+C$

- $\frac{ln⁡x}{ln⁡3}+C$

- ${3}^{x}+C$

To compute the integral of a general exponential function, we just need to divide by the natural logarithm of the base of the exponential function:

$$
\begin{aligned}\int {3}^{x}\,\text{d}x & =\frac{{3}^{x}}{ln⁡3}+C\end{aligned}
$$

## Original q-113887 — raw observed evidence

Calculate $\int {5}^{x}\,\text{d}x.$

- $\frac{ln⁡x}{ln⁡5}+C$

- ${5}^{x}+C$

- ${5}^{x}ln⁡5+C$

- $5ln⁡x+C$

- $\frac{{5}^{x}}{ln⁡5}+C$

To compute the integral of a general exponential function, we just need to divide by the natural logarithm of the base of the exponential function:

$$
\begin{aligned}\int {5}^{x}\,\text{d}x & =\frac{{5}^{x}}{ln⁡5}+C\end{aligned}
$$

## Original q-113890 — raw observed evidence

$\int 2\cdot {9}^{x}\,\text{d}x=$

- $\frac{{9}^{x}}{ln⁡2}+C$

- $\frac{ln⁡9}{{9}^{x}}+C$

- $2\cdot {9}^{x}+C$

- $2\cdot \frac{{9}^{x}}{ln⁡9}+C$

- $\frac{ln⁡2}{9ln⁡x}+C$

First, we factor out the constant $2.$ Then, we integrate the exponential function and get

$$
\begin{aligned}\int 2\cdot {9}^{x}\,\text{d}x & =2\int {9}^{x}\,\text{d}x \\  & =2\cdot \frac{{9}^{x}}{ln⁡9}+C.\end{aligned}
$$

## Original q-113893 — raw observed evidence

Calculate $\int {(\frac{1}{8})}^{x}\,\text{d}x.$

- $\frac{ln⁡x}{ln⁡8}+C$

- $-\frac{{(\frac{1}{8})}^{x}}{ln⁡8}+C$

- ${(\frac{1}{8})}^{x}ln⁡8+C$

- $\frac{{8}^{x}}{ln⁡8}+C$

- $-\frac{ln⁡x}{{8}^{x}}+C$

To compute the integral of a general exponential function, we just need to divide by the natural logarithm of the base of the exponential function:

$$
\begin{aligned}\int {(\frac{1}{8})}^{x}\,\text{d}x & =\frac{{(\frac{1}{8})}^{x}}{ln⁡(\frac{1}{8})}+C\end{aligned}
$$

Using the laws of logarithms, we have that

$$
\begin{aligned}ln⁡(\frac{1}{8}) & =ln⁡1-ln⁡8 \\  & =0-ln⁡8 \\  & =-ln⁡8.\end{aligned}
$$

So, we can simplify our final answer as follows:

$$
\begin{aligned}\frac{{(\frac{1}{8})}^{x}}{ln⁡(\frac{1}{8})}+C=-\frac{{(\frac{1}{8})}^{x}}{ln⁡8}+C\end{aligned}
$$

## Original q-31249 — raw observed evidence

$\int 3\cdot {2}^{x}\,\text{d}x=$

- $3\cdot \frac{{2}^{x}}{ln⁡2}+C$

- $\frac{ln⁡x}{ln⁡2}+C$

- $2\cdot \frac{{3}^{ln⁡x}}{ln⁡2}+C$

- $\frac{2}{ln⁡x}+C$

- $3\cdot \frac{{3}^{2x}}{ln⁡3}+C$

First, we factor out the constant $3.$ Then, we integrate the exponential function and get

$$
\begin{aligned}\int 3\cdot {2}^{x}\,\text{d}x & =3\int {2}^{x}\,\text{d}x \\  & =3\cdot \frac{{2}^{x}}{ln⁡2}+C.\end{aligned}
$$

## Generated easy — integer_base / base_ln_power (authored bounded variation)

Calculate $\int {3}^{x}\,\text{d}x.$

- $\frac{{3}^{x}}{\ln 3}+C$

- $\frac{\ln x}{\ln 3}+C$

- ${3}^{x}+C$

- $\ln ({3}^{x})+C$

- ${3}^{x}\ln 3+C$

To compute the integral of a general exponential function, we just need to divide by the natural logarithm of the base of the exponential function:

$$
\begin{aligned}\int {3}^{x}\,\text{d}x & =\frac{{3}^{x}}{\ln 3}+C\end{aligned}
$$

## Generated easy — integer_base / base_ln_power (authored bounded variation)

Calculate $\int {20}^{x}\,\text{d}x.$

- $\frac{{20}^{x}}{\ln 20}+C$

- $\frac{\ln x}{\ln 20}+C$

- ${20}^{x}+C$

- $\ln ({20}^{x})+C$

- ${20}^{x}\ln 20+C$

To compute the integral of a general exponential function, we just need to divide by the natural logarithm of the base of the exponential function:

$$
\begin{aligned}\int {20}^{x}\,\text{d}x & =\frac{{20}^{x}}{\ln 20}+C\end{aligned}
$$

## Generated easy — integer_base / base_scaled_ln_x (authored bounded variation)

Calculate $\int {3}^{x}\,\text{d}x.$

- $\frac{\ln x}{\ln 3}+C$

- ${3}^{x}+C$

- $\frac{{3}^{x}}{\ln 3}+C$

- ${3}^{x}\ln 3+C$

- $3\ln x+C$

To compute the integral of a general exponential function, we just need to divide by the natural logarithm of the base of the exponential function:

$$
\begin{aligned}\int {3}^{x}\,\text{d}x & =\frac{{3}^{x}}{\ln 3}+C\end{aligned}
$$

## Generated easy — integer_base / base_scaled_ln_x (authored bounded variation)

Calculate $\int {20}^{x}\,\text{d}x.$

- $\frac{\ln x}{\ln 20}+C$

- ${20}^{x}+C$

- $\frac{{20}^{x}}{\ln 20}+C$

- ${20}^{x}\ln 20+C$

- $20\ln x+C$

To compute the integral of a general exponential function, we just need to divide by the natural logarithm of the base of the exponential function:

$$
\begin{aligned}\int {20}^{x}\,\text{d}x & =\frac{{20}^{x}}{\ln 20}+C\end{aligned}
$$

## Generated moderate — scalar_base / scalar_log_coefficient (authored bounded variation)

$\int -2\cdot {5}^{x}\,\text{d}x=$

- $-2\cdot \frac{{5}^{x}}{\ln 5}+C$

- $-2\cdot \frac{{5}^{x}}{\ln 2}+C$

- $-2\cdot {5}^{x}\ln 5+C$

- $\frac{{5}^{x}}{\ln 5}+C$

- $-2\cdot {5}^{x}+C$

First, we factor out the constant $-2.$ Then, we integrate the exponential function and get

$$
\begin{aligned}\int -2\cdot {5}^{x}\,\text{d}x & =-2\int {5}^{x}\,\text{d}x \\  & =-2\cdot \frac{{5}^{x}}{\ln 5}+C.\end{aligned}
$$

## Generated moderate — scalar_base / scalar_log_coefficient (authored bounded variation)

$\int 12\cdot {19}^{x}\,\text{d}x=$

- $12\cdot \frac{{19}^{x}}{\ln 19}+C$

- $12\cdot \frac{{19}^{x}}{\ln 12}+C$

- $12\cdot {19}^{x}\ln 19+C$

- $\frac{{19}^{x}}{\ln 19}+C$

- $12\cdot {19}^{x}+C$

First, we factor out the constant $12.$ Then, we integrate the exponential function and get

$$
\begin{aligned}\int 12\cdot {19}^{x}\,\text{d}x & =12\int {19}^{x}\,\text{d}x \\  & =12\cdot \frac{{19}^{x}}{\ln 19}+C.\end{aligned}
$$

## Generated moderate — scalar_base / scalar_reciprocal (authored bounded variation)

$\int -2\cdot {5}^{x}\,\text{d}x=$

- $-2\cdot {5}^{x}+C$

- $\frac{{5}^{x}}{\ln 5}+C$

- $\frac{{5}^{x}}{-2\ln 5}+C$

- $-2\cdot \frac{{5}^{x}}{\ln 5}+C$

- $-2\cdot \frac{{5}^{-x}}{\ln 5}+C$

First, we factor out the constant $-2.$ Then, we integrate the exponential function and get

$$
\begin{aligned}\int -2\cdot {5}^{x}\,\text{d}x & =-2\int {5}^{x}\,\text{d}x \\  & =-2\cdot \frac{{5}^{x}}{\ln 5}+C.\end{aligned}
$$

## Generated moderate — scalar_base / scalar_reciprocal (authored bounded variation)

$\int 12\cdot {19}^{x}\,\text{d}x=$

- $12\cdot {19}^{x}+C$

- $\frac{{19}^{x}}{\ln 19}+C$

- $\frac{{19}^{x}}{12\ln 19}+C$

- $12\cdot \frac{{19}^{x}}{\ln 19}+C$

- $12\cdot \frac{{19}^{-x}}{\ln 19}+C$

First, we factor out the constant $12.$ Then, we integrate the exponential function and get

$$
\begin{aligned}\int 12\cdot {19}^{x}\,\text{d}x & =12\int {19}^{x}\,\text{d}x \\  & =12\cdot \frac{{19}^{x}}{\ln 19}+C.\end{aligned}
$$

## Generated moderate — what_integral / scalar_log_coefficient (authored bounded variation)

What is $\displaystyle \int-2 \cdot 5^{x}dx$?

- $-2\cdot {5}^{x}+C$

- $-2\cdot \frac{{5}^{x}}{\ln 5}+C$

- $\frac{{5}^{x}}{\ln 5}+C$

- $-2\cdot \frac{{5}^{x}}{\ln 2}+C$

- $-2\cdot {5}^{x}\ln 5+C$

First, we factor out the constant $-2.$ Then, we integrate the exponential function and get

$$
\begin{aligned}\int -2\cdot {5}^{x}\,\text{d}x & =-2\int {5}^{x}\,\text{d}x \\  & =-2\cdot \frac{{5}^{x}}{\ln 5}+C.\end{aligned}
$$

## Generated moderate — what_integral / scalar_log_coefficient (authored bounded variation)

What is $\displaystyle \int12 \cdot 19^{x}dx$?

- $12\cdot {19}^{x}+C$

- $12\cdot \frac{{19}^{x}}{\ln 19}+C$

- $\frac{{19}^{x}}{\ln 19}+C$

- $12\cdot \frac{{19}^{x}}{\ln 12}+C$

- $12\cdot {19}^{x}\ln 19+C$

First, we factor out the constant $12.$ Then, we integrate the exponential function and get

$$
\begin{aligned}\int 12\cdot {19}^{x}\,\text{d}x & =12\int {19}^{x}\,\text{d}x \\  & =12\cdot \frac{{19}^{x}}{\ln 19}+C.\end{aligned}
$$

## Generated moderate — what_integral / scalar_reciprocal (authored bounded variation)

What is $\displaystyle \int-2 \cdot 5^{x}dx$?

- $\frac{{5}^{x}}{\ln 5}+C$

- $-2\cdot \frac{{5}^{-x}}{\ln 5}+C$

- $-2\cdot {5}^{x}+C$

- $-2\cdot \frac{{5}^{x}}{\ln 5}+C$

- $\frac{{5}^{x}}{-2\ln 5}+C$

First, we factor out the constant $-2.$ Then, we integrate the exponential function and get

$$
\begin{aligned}\int -2\cdot {5}^{x}\,\text{d}x & =-2\int {5}^{x}\,\text{d}x \\  & =-2\cdot \frac{{5}^{x}}{\ln 5}+C.\end{aligned}
$$

## Generated moderate — what_integral / scalar_reciprocal (authored bounded variation)

What is $\displaystyle \int12 \cdot 19^{x}dx$?

- $\frac{{19}^{x}}{\ln 19}+C$

- $12\cdot \frac{{19}^{-x}}{\ln 19}+C$

- $12\cdot {19}^{x}+C$

- $12\cdot \frac{{19}^{x}}{\ln 19}+C$

- $\frac{{19}^{x}}{12\ln 19}+C$

First, we factor out the constant $12.$ Then, we integrate the exponential function and get

$$
\begin{aligned}\int 12\cdot {19}^{x}\,\text{d}x & =12\int {19}^{x}\,\text{d}x \\  & =12\cdot \frac{{19}^{x}}{\ln 19}+C.\end{aligned}
$$

## Generated hard — reciprocal_base / reciprocal_method (authored bounded variation)

Calculate $\int {(\frac{1}{3})}^{x}\,\text{d}x.$

- $-\frac{{(\frac{1}{3})}^{x}}{\ln 3}+C$

- ${(\frac{1}{3})}^{x}+C$

- $\frac{{3}^{x}}{\ln 3}+C$

- $\frac{{(\frac{1}{3})}^{x}}{\ln 3}+C$

- ${(\frac{1}{3})}^{x}\ln 3+C$

To compute the integral of a general exponential function, we just need to divide by the natural logarithm of the base of the exponential function:

$$
\begin{aligned}\int {(\frac{1}{3})}^{x}\,\text{d}x & =\frac{{(\frac{1}{3})}^{x}}{\ln (\frac{1}{3})}+C\end{aligned}
$$

Using the laws of logarithms, we have that

$$
\begin{aligned}\ln (\frac{1}{3}) & =\ln 1-\ln 3 \\  & =0-\ln 3 \\  & =-\ln 3.\end{aligned}
$$

So, we can simplify our final answer as follows:

$$
\begin{aligned}\frac{{(\frac{1}{3})}^{x}}{\ln (\frac{1}{3})}+C=-\frac{{(\frac{1}{3})}^{x}}{\ln 3}+C\end{aligned}
$$

## Generated hard — reciprocal_base / reciprocal_method (authored bounded variation)

Calculate $\int {(\frac{1}{20})}^{x}\,\text{d}x.$

- $-\frac{{(\frac{1}{20})}^{x}}{\ln 20}+C$

- ${(\frac{1}{20})}^{x}+C$

- $\frac{{20}^{x}}{\ln 20}+C$

- $\frac{{(\frac{1}{20})}^{x}}{\ln 20}+C$

- ${(\frac{1}{20})}^{x}\ln 20+C$

To compute the integral of a general exponential function, we just need to divide by the natural logarithm of the base of the exponential function:

$$
\begin{aligned}\int {(\frac{1}{20})}^{x}\,\text{d}x & =\frac{{(\frac{1}{20})}^{x}}{\ln (\frac{1}{20})}+C\end{aligned}
$$

Using the laws of logarithms, we have that

$$
\begin{aligned}\ln (\frac{1}{20}) & =\ln 1-\ln 20 \\  & =0-\ln 20 \\  & =-\ln 20.\end{aligned}
$$

So, we can simplify our final answer as follows:

$$
\begin{aligned}\frac{{(\frac{1}{20})}^{x}}{\ln (\frac{1}{20})}+C=-\frac{{(\frac{1}{20})}^{x}}{\ln 20}+C\end{aligned}
$$


## Generated evidence replay q-31248 — changed parameters, raw complete bank (ineligible for normal learning)

What is $\displaystyle \int4 \cdot 3^{x}dx$?

- $2 \cdot \frac{2^{x}}{\ln 3} + C$

- $\frac{\ln x}{\ln 3} + C$

- $4 \cdot \frac{3^{x}}{\ln 3} + C$

- $4 \cdot \frac{3^{\ln x}}{\ln 3} + C$

- $\frac{3}{\ln x} + C$


## Generated evidence replay q-31248 — changed parameters, raw complete bank (ineligible for normal learning)

What is $\displaystyle \int6 \cdot 19^{x}dx$?

- $3 \cdot \frac{18^{x}}{\ln 19} + C$

- $\frac{\ln x}{\ln 19} + C$

- $6 \cdot \frac{19^{x}}{\ln 19} + C$

- $6 \cdot \frac{19^{\ln x}}{\ln 19} + C$

- $\frac{19}{\ln x} + C$


## Generated evidence replay q-66139 — changed parameters, raw complete bank (ineligible for normal learning)

Calculate $\int {2}^{x}\,\text{d}x.$

- ${2}^{x}ln⁡2+C$

- $ln⁡({2}^{x})+C$

- $\frac{ln⁡x}{ln⁡2}+C$

- ${2}^{x}+C$

- $\frac{{2}^{x}}{ln⁡2}+C$

To compute the integral of a general exponential function, we just need to divide by the natural logarithm of the base of the exponential function:

$$
\begin{aligned}\int {2}^{x}\,\text{d}x & =\frac{{2}^{x}}{ln⁡2}+C\end{aligned}
$$


## Generated evidence replay q-66139 — changed parameters, raw complete bank (ineligible for normal learning)

Calculate $\int {20}^{x}\,\text{d}x.$

- ${20}^{x}ln⁡20+C$

- $ln⁡({20}^{x})+C$

- $\frac{ln⁡x}{ln⁡20}+C$

- ${20}^{x}+C$

- $\frac{{20}^{x}}{ln⁡20}+C$

To compute the integral of a general exponential function, we just need to divide by the natural logarithm of the base of the exponential function:

$$
\begin{aligned}\int {20}^{x}\,\text{d}x & =\frac{{20}^{x}}{ln⁡20}+C\end{aligned}
$$


## Generated evidence replay q-113887 — changed parameters, raw complete bank (ineligible for normal learning)

Calculate $\int {2}^{x}\,\text{d}x.$

- $\frac{ln⁡x}{ln⁡2}+C$

- ${2}^{x}+C$

- $2ln⁡x+C$

- $\frac{{2}^{x}}{ln⁡2}+C$

- ${2}^{x}ln⁡2+C$

To compute the integral of a general exponential function, we just need to divide by the natural logarithm of the base of the exponential function:

$$
\begin{aligned}\int {2}^{x}\,\text{d}x & =\frac{{2}^{x}}{ln⁡2}+C\end{aligned}
$$


## Generated evidence replay q-113887 — changed parameters, raw complete bank (ineligible for normal learning)

Calculate $\int {20}^{x}\,\text{d}x.$

- $\frac{ln⁡x}{ln⁡20}+C$

- ${20}^{x}+C$

- $20ln⁡x+C$

- $\frac{{20}^{x}}{ln⁡20}+C$

- ${20}^{x}ln⁡20+C$

To compute the integral of a general exponential function, we just need to divide by the natural logarithm of the base of the exponential function:

$$
\begin{aligned}\int {20}^{x}\,\text{d}x & =\frac{{20}^{x}}{ln⁡20}+C\end{aligned}
$$


## Generated evidence replay q-113890 — changed parameters, raw complete bank (ineligible for normal learning)

$\int 4\cdot {3}^{x}\,\text{d}x=$

- $\frac{{3}^{x}}{ln⁡4}+C$

- $\frac{ln⁡3}{{3}^{x}}+C$

- $4\cdot \frac{{3}^{x}}{ln⁡3}+C$

- $\frac{ln⁡4}{3ln⁡x}+C$

- $4\cdot {3}^{x}+C$

First, we factor out the constant $4.$ Then, we integrate the exponential function and get

$$
\begin{aligned}\int 4\cdot {3}^{x}\,\text{d}x & =4\int {3}^{x}\,\text{d}x \\  & =4\cdot \frac{{3}^{x}}{ln⁡3}+C.\end{aligned}
$$


## Generated evidence replay q-113890 — changed parameters, raw complete bank (ineligible for normal learning)

$\int 6\cdot {19}^{x}\,\text{d}x=$

- $\frac{{19}^{x}}{ln⁡6}+C$

- $\frac{ln⁡19}{{19}^{x}}+C$

- $6\cdot \frac{{19}^{x}}{ln⁡19}+C$

- $\frac{ln⁡6}{19ln⁡x}+C$

- $6\cdot {19}^{x}+C$

First, we factor out the constant $6.$ Then, we integrate the exponential function and get

$$
\begin{aligned}\int 6\cdot {19}^{x}\,\text{d}x & =6\int {19}^{x}\,\text{d}x \\  & =6\cdot \frac{{19}^{x}}{ln⁡19}+C.\end{aligned}
$$


## Generated evidence replay q-113893 — changed parameters, raw complete bank (ineligible for normal learning)

Calculate $\int {(\frac{1}{2})}^{x}\,\text{d}x.$

- $\frac{ln⁡x}{ln⁡2}+C$

- $-\frac{{(\frac{1}{2})}^{x}}{ln⁡2}+C$

- $\frac{{2}^{x}}{ln⁡2}+C$

- $-\frac{ln⁡x}{{2}^{x}}+C$

- ${(\frac{1}{2})}^{x}ln⁡2+C$

To compute the integral of a general exponential function, we just need to divide by the natural logarithm of the base of the exponential function:

$$
\begin{aligned}\int {(\frac{1}{2})}^{x}\,\text{d}x & =\frac{{(\frac{1}{2})}^{x}}{ln⁡(\frac{1}{2})}+C\end{aligned}
$$

Using the laws of logarithms, we have that

$$
\begin{aligned}ln⁡(\frac{1}{2}) & =ln⁡1-ln⁡2 \\  & =0-ln⁡2 \\  & =-ln⁡2.\end{aligned}
$$

So, we can simplify our final answer as follows:

$$
\begin{aligned}\frac{{(\frac{1}{2})}^{x}}{ln⁡(\frac{1}{2})}+C=-\frac{{(\frac{1}{2})}^{x}}{ln⁡2}+C\end{aligned}
$$


## Generated evidence replay q-113893 — changed parameters, raw complete bank (ineligible for normal learning)

Calculate $\int {(\frac{1}{20})}^{x}\,\text{d}x.$

- $\frac{ln⁡x}{ln⁡20}+C$

- $-\frac{{(\frac{1}{20})}^{x}}{ln⁡20}+C$

- $\frac{{20}^{x}}{ln⁡20}+C$

- $-\frac{ln⁡x}{{20}^{x}}+C$

- ${(\frac{1}{20})}^{x}ln⁡20+C$

To compute the integral of a general exponential function, we just need to divide by the natural logarithm of the base of the exponential function:

$$
\begin{aligned}\int {(\frac{1}{20})}^{x}\,\text{d}x & =\frac{{(\frac{1}{20})}^{x}}{ln⁡(\frac{1}{20})}+C\end{aligned}
$$

Using the laws of logarithms, we have that

$$
\begin{aligned}ln⁡(\frac{1}{20}) & =ln⁡1-ln⁡20 \\  & =0-ln⁡20 \\  & =-ln⁡20.\end{aligned}
$$

So, we can simplify our final answer as follows:

$$
\begin{aligned}\frac{{(\frac{1}{20})}^{x}}{ln⁡(\frac{1}{20})}+C=-\frac{{(\frac{1}{20})}^{x}}{ln⁡20}+C\end{aligned}
$$


## Generated evidence replay q-31249 — changed parameters, raw complete bank (ineligible for normal learning)

$\int 4\cdot {3}^{x}\,\text{d}x=$

- $4\cdot \frac{{3}^{x}}{ln⁡3}+C$

- $\frac{ln⁡x}{ln⁡3}+C$

- $\frac{3}{ln⁡x}+C$

- $4\cdot \frac{{4}^{3x}}{ln⁡4}+C$

- $3\cdot \frac{{4}^{ln⁡x}}{ln⁡3}+C$

First, we factor out the constant $4.$ Then, we integrate the exponential function and get

$$
\begin{aligned}\int 4\cdot {3}^{x}\,\text{d}x & =4\int {3}^{x}\,\text{d}x \\  & =4\cdot \frac{{3}^{x}}{ln⁡3}+C.\end{aligned}
$$


## Generated evidence replay q-31249 — changed parameters, raw complete bank (ineligible for normal learning)

$\int 6\cdot {19}^{x}\,\text{d}x=$

- $6\cdot \frac{{19}^{x}}{ln⁡19}+C$

- $\frac{ln⁡x}{ln⁡19}+C$

- $\frac{19}{ln⁡x}+C$

- $6\cdot \frac{{6}^{19x}}{ln⁡6}+C$

- $19\cdot \frac{{6}^{ln⁡x}}{ln⁡19}+C$

First, we factor out the constant $6.$ Then, we integrate the exponential function and get

$$
\begin{aligned}\int 6\cdot {19}^{x}\,\text{d}x & =6\int {19}^{x}\,\text{d}x \\  & =6\cdot \frac{{19}^{x}}{ln⁡19}+C.\end{aligned}
$$
