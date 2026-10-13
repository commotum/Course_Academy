# Template extraction

General pattern: integrate 1/(ax+b)+1/(dx+c), then combine the two logarithms into one. Equal slopes use a product; opposite slopes use a quotient. Answers are antiderivatives on each connected real domain interval, with K>0. Source conditions are carried in generation metadata.

Fixed components: exact prompt/solution prose, five-choice radio field selection, source-specific complete bank, positive arbitrary K. Variable components: slopes/shifts, denominator strings, coefficient 1/a, intermediate logarithms, combined product/quotient. Templates preserve the original four-row solution: split integral; individual antiderivatives; combine logs and set C=(1/a)ln K; absorb K.

Observed values are recorded below and in contract.json. Proposed bounded extension: integer slopes 2..6 and shifts 1..6, unit-slope families retain a=1; same-unit shift 2..6; opposite-asymmetric first shift -6..-2, second shift 1..6 with b+c != 0. q-113540 requires b>=2 and a!=b to avoid collisions. q-49360 retains observed fixed distractor coefficients 2 and 1/4 while extending only its common shift b. No cross-profile banks.

Recipe notation: a is the positive slope magnitude; b is the first shift (positive in shift-dependent banks). inv_a=1/a, neg_inv_a=-1/a, inv_b=1/b, neg_inv_b=-1/b, neg_a=-a, neg_b=-b; one=1, two=2, quarter=1/4. product means (D1)(D2); quotient means D1/D2. The displayed mathematical value is coefficient*ln(K|argument|). These describe the observed transformations; cognitive-error interpretations are unresolved and are not added to learner feedback.

## q-49524

Source DB entity 17592186064873; field b93fc135-aa70-532a-b97e-cd7a1123a184, selection/radio; parameters [a,b,c]=[4, 2, 2]; family opposite-symmetric. Exact prompt:

Calculate $\int (\frac{1}{2+4x}+\frac{1}{2-4x})\,\text{d}x.$ Assume that $K$ is an arbitrary positive constant.

Complete source bank and parameterized recipes:

- 1. `$\frac{1}{4}\operatorname{ln}⁡(K|(2+4x)(2-4x)|)$` → inv_a:product.
- 2. `$-\frac{1}{4}\operatorname{ln}⁡(K|\frac{2+4x}{2-4x}|)$` → neg_inv_a:quotient.
- 3. `$4\operatorname{ln}⁡(K|\frac{2+4x}{2-4x}|)$` → a:quotient.
- 4. `$-4\operatorname{ln}⁡(K|(2+4x)(2-4x)|)$` → neg_a:product.
- 5. `$\frac{1}{4}\operatorname{ln}⁡(K|\frac{2+4x}{2-4x}|)$` → inv_a:quotient (correct).

Exact source solution (template components in contract.json):

Let's solve this using the general formula:

$$
\begin{aligned}\int (\frac{1}{2+4x}+\frac{1}{2-4x})\,\text{d}x & =\int \frac{1}{2+4x}\,\text{d}x+\int \frac{1}{2-4x}\,\text{d}x \\  & =\frac{1}{4}\operatorname{ln}⁡|2+4x|-\frac{1}{4}\operatorname{ln}⁡|2-4x|+C \\  & =\frac{1}{4}\operatorname{ln}⁡|\frac{2+4x}{2-4x}|+\frac{1}{4}\operatorname{ln}⁡K \\  & =\frac{1}{4}\operatorname{ln}⁡(K|\frac{2+4x}{2-4x}|)\end{aligned}
$$

Notice that we used the laws of logarithms to write the result as a single logarithm.

## q-113540

Source DB entity 17592186247369; field 5b7ee80e-437d-599e-8d92-09c467d8e2c3, selection/radio; parameters [a,b,c]=[3, 2, -2]; family same-symmetric. Exact prompt:

Calculate $\int (\frac{1}{3x+2}+\frac{1}{3x-2})\,\text{d}x.$ Assume that $K$ is an arbitrary positive constant.

Complete source bank and parameterized recipes:

- 1. `$\frac{1}{2}\operatorname{ln}⁡(K|(3x+2)(3x-2)|)$` → inv_b:product.
- 2. `$\frac{1}{3}\operatorname{ln}⁡(K|(3x+2)(3x-2)|)$` → inv_a:product (correct).
- 3. `$\operatorname{ln}⁡(K|(3x+2)(3x-2)|)$` → one:product.
- 4. `$\frac{1}{2}\operatorname{ln}⁡(K|\frac{3x+2}{3x-2}|)$` → inv_b:quotient.
- 5. `$\frac{1}{3}\operatorname{ln}⁡(K|\frac{3x+2}{3x-2}|)$` → inv_a:quotient.

Exact source solution (template components in contract.json):

Let's solve this using the general formula:

$$
\begin{aligned}\int (\frac{1}{3x+2}+\frac{1}{3x-2})\,\text{d}x & =\int \frac{1}{3x+2}\,\text{d}x+\int \frac{1}{3x-2}\,\text{d}x \\  & =\frac{1}{3}\operatorname{ln}⁡|3x+2|+\frac{1}{3}\operatorname{ln}⁡|3x-2|+C \\  & =\frac{1}{3}\operatorname{ln}⁡|(3x+2)(3x-2)|+\frac{1}{3}\operatorname{ln}⁡K \\  & =\frac{1}{3}\operatorname{ln}⁡(K|(3x+2)(3x-2)|)\end{aligned}
$$

Notice that we used the laws of logarithms to write the result as a single logarithm.

## q-113544

Source DB entity 17592186247370; field ead91955-0524-574f-a8fe-8b351aad7ed3, selection/radio; parameters [a,b,c]=[1, 3, -3]; family same-unit. Exact prompt:

Calculate $\int (\frac{1}{x+3}+\frac{1}{x-3})\,\text{d}x.$ Assume that $K$ is an arbitrary positive constant.

Complete source bank and parameterized recipes:

- 1. `$-\frac{1}{3}\operatorname{ln}⁡(K|(x+3)(x-3)|)$` → neg_inv_b:product.
- 2. `$\operatorname{ln}⁡(K|(x+3)(x-3)|)$` → one:product (correct).
- 3. `$3\operatorname{ln}⁡(K|(x+3)(x-3)|)$` → b:product.
- 4. `$-3\operatorname{ln}⁡(K|(x+3)(x-3)|)$` → neg_b:product.
- 5. `$\frac{1}{3}\operatorname{ln}⁡(K|(x+3)(x-3)|)$` → inv_b:product.

Exact source solution (template components in contract.json):

Let's solve this using the general formula:

$$
\begin{aligned}\int (\frac{1}{x+3}+\frac{1}{x-3})\,\text{d}x & =\int \frac{1}{x+3}\,\text{d}x+\int \frac{1}{x-3}\,\text{d}x \\  & =\operatorname{ln}⁡|x+3|+\operatorname{ln}⁡|x-3|+C \\  & =\operatorname{ln}⁡|(x+3)(x-3)|+\operatorname{ln}⁡K \\  & =\operatorname{ln}⁡(K|(x+3)(x-3)|)\end{aligned}
$$

Notice that we used the laws of logarithms to write the result as a single logarithm.

## q-49360

Source DB entity 17592186332706; field d573eb9f-5b4a-5c4d-be89-c86d1a19944c, selection/radio; parameters [a,b,c]=[1, 1, 1]; family opposite-unit. Exact prompt:

Calculate $\int (\frac{1}{1+x}+\frac{1}{1-x})\,\text{d}x.$ Assume that $K$ is an arbitrary positive constant.

Complete source bank and parameterized recipes:

- 1. `$2\operatorname{ln}⁡(K|(1+x)(1-x)|)$` → two:product.
- 2. `$\frac{1}{4}\operatorname{ln}⁡(K|(1+x)(1-x)|)$` → quarter:product.
- 3. `$\frac{1}{4}\operatorname{ln}⁡(K|\frac{1+x}{1-x}|)$` → quarter:quotient.
- 4. `$2\operatorname{ln}⁡(K|\frac{1+x}{1-x}|)$` → two:quotient.
- 5. `$\operatorname{ln}⁡(K|\frac{1+x}{1-x}|)$` → one:quotient (correct).

Exact source solution (template components in contract.json):

Let's solve this using the general formula:

$$
\begin{aligned}\int (\frac{1}{1+x}+\frac{1}{1-x})\,\text{d}x & =\int \frac{1}{1+x}\,\text{d}x+\int \frac{1}{1-x}\,\text{d}x \\  & =\operatorname{ln}⁡|1+x|-\operatorname{ln}⁡|1-x|+C \\  & =\operatorname{ln}⁡|\frac{1+x}{1-x}|+\operatorname{ln}⁡K \\  & =\operatorname{ln}⁡(K|\frac{1+x}{1-x}|)\end{aligned}
$$

Notice that we used the laws of logarithms to write the result as a single logarithm.

## q-49520

Source DB entity 17592186332730; field d099d8e6-9f09-5bcb-9f4f-b030a1bc2edf, selection/radio; parameters [a,b,c]=[2, 3, 3]; family opposite-symmetric. Exact prompt:

Calculate $\int (\frac{1}{3+2x}+\frac{1}{3-2x})\,\text{d}x.$ Assume that $K$ is an arbitrary positive constant.

Complete source bank and parameterized recipes:

- 1. `$\frac{1}{2}\operatorname{ln}⁡(K|\frac{3+2x}{3-2x}|)$` → inv_a:quotient (correct).
- 2. `$2\operatorname{ln}⁡(K|(3+2x)(3-2x)|)$` → a:product.
- 3. `$\frac{1}{2}\operatorname{ln}⁡(K|(3+2x)(3-2x)|)$` → inv_a:product.
- 4. `$-2\operatorname{ln}⁡(K|\frac{3+2x}{3-2x}|)$` → neg_a:quotient.
- 5. `$2\operatorname{ln}⁡(K|\frac{3+2x}{3-2x}|)$` → a:quotient.

Exact source solution (template components in contract.json):

Let's solve this using the general formula:

$$
\begin{aligned}\int (\frac{1}{3+2x}+\frac{1}{3-2x})\,\text{d}x & =\int \frac{1}{3+2x}\,\text{d}x+\int \frac{1}{3-2x}\,\text{d}x \\  & =\frac{1}{2}\operatorname{ln}⁡|3+2x|-\frac{1}{2}\operatorname{ln}⁡|3-2x|+C \\  & =\frac{1}{2}\operatorname{ln}⁡|\frac{3+2x}{3-2x}|+\frac{1}{2}\operatorname{ln}⁡K \\  & =\frac{1}{2}\operatorname{ln}⁡(K|\frac{3+2x}{3-2x}|)\end{aligned}
$$

Notice that we used the laws of logarithms to write the result as a single logarithm.

## q-49522

Source DB entity 17592186332731; field 4eba1835-2339-5271-b0e0-a782f45a652e, selection/radio; parameters [a,b,c]=[5, 1, 1]; family opposite-symmetric. Exact prompt:

Calculate $\int (\frac{1}{1+5x}+\frac{1}{1-5x})\,\text{d}x.$ Assume that $K$ is an arbitrary positive constant.

Complete source bank and parameterized recipes:

- 1. `$5\operatorname{ln}⁡(K|\frac{1+5x}{1-5x}|)$` → a:quotient.
- 2. `$-\frac{1}{5}\operatorname{ln}⁡(K|\frac{1+5x}{1-5x}|)$` → neg_inv_a:quotient.
- 3. `$\frac{1}{5}\operatorname{ln}⁡(K|\frac{1+5x}{1-5x}|)$` → inv_a:quotient (correct).
- 4. `$-5\operatorname{ln}⁡(K|\frac{1+5x}{1-5x}|)$` → neg_a:quotient.
- 5. `$5\operatorname{ln}⁡(K|(1+5x)(1-5x)|)$` → a:product.

Exact source solution (template components in contract.json):

Let's solve this using the general formula:

$$
\begin{aligned}\int (\frac{1}{1+5x}+\frac{1}{1-5x})\,\text{d}x & =\int \frac{1}{1+5x}\,\text{d}x+\int \frac{1}{1-5x}\,\text{d}x \\  & =\frac{1}{5}\operatorname{ln}⁡|1+5x|-\frac{1}{5}\operatorname{ln}⁡|1-5x|+C \\  & =\frac{1}{5}\operatorname{ln}⁡|\frac{1+5x}{1-5x}|+\frac{1}{5}\operatorname{ln}⁡K \\  & =\frac{1}{5}\operatorname{ln}⁡(K|\frac{1+5x}{1-5x}|)\end{aligned}
$$

Notice that we used the laws of logarithms to write the result as a single logarithm.

## q-72448

Source DB entity 17592186339118; field c92d692c-9833-5c19-b571-ff45ea45171f, selection/radio; parameters [a,b,c]=[4, -5, 1]; family opposite-asymmetric. Exact prompt:

Calculate $\int (\frac{1}{4x-5}+\frac{1}{1-4x})\,\text{d}x.$ Assume that $K$ is an arbitrary positive constant.

Complete source bank and parameterized recipes:

- 1. `$\frac{1}{4}\operatorname{ln}⁡(K|(4x-5)(1-4x)|)$` → inv_a:product.
- 2. `$\operatorname{ln}⁡(K|\frac{4x-5}{1-4x}|)$` → one:quotient.
- 3. `$4\operatorname{ln}⁡(K|\frac{4x-5}{1-4x}|)$` → a:quotient.
- 4. `$4\operatorname{ln}⁡(K|(4x-5)(1-4x)|)$` → a:product.
- 5. `$\frac{1}{4}\operatorname{ln}⁡(K|\frac{4x-5}{1-4x}|)$` → inv_a:quotient (correct).

Exact source solution (template components in contract.json):

Let's solve this using the general formula:

$$
\begin{aligned}\int (\frac{1}{4x-5}+\frac{1}{1-4x})\,\text{d}x & =\int \frac{1}{4x-5}\,\text{d}x+\int \frac{1}{1-4x}\,\text{d}x \\  & =\frac{1}{4}\operatorname{ln}⁡|4x-5|-\frac{1}{4}\operatorname{ln}⁡|1-4x|+C \\  & =\frac{1}{4}\operatorname{ln}⁡|\frac{4x-5}{1-4x}|+\frac{1}{4}\operatorname{ln}⁡K \\  & =\frac{1}{4}\operatorname{ln}⁡(K|\frac{4x-5}{1-4x}|)\end{aligned}
$$

Notice that we used the laws of logarithms to write the result as a single logarithm.

## q-72449

Source DB entity 17592186339119; field dd143701-6720-5620-9d38-200cfec896ea, selection/radio; parameters [a,b,c]=[2, 1, -1]; family same-symmetric. Exact prompt:

Calculate $\int (\frac{1}{2x+1}+\frac{1}{2x-1})\,\text{d}x.$ Assume that $K$ is an arbitrary positive constant.

Complete source bank and parameterized recipes:

- 1. `$\frac{1}{2}\operatorname{ln}⁡(K|(2x+1)(2x-1)|)$` → inv_a:product (correct).
- 2. `$\operatorname{ln}⁡(K|\frac{2x+1}{2x-1}|)$` → one:quotient.
- 3. `$2\operatorname{ln}⁡(K|(2x+1)(2x-1)|)$` → a:product.
- 4. `$2\operatorname{ln}⁡(K|\frac{2x+1}{2x-1}|)$` → a:quotient.
- 5. `$\frac{1}{2}\operatorname{ln}⁡(K|\frac{2x+1}{2x-1}|)$` → inv_a:quotient.

Exact source solution (template components in contract.json):

Let's solve this using the general formula:

$$
\begin{aligned}\int (\frac{1}{2x+1}+\frac{1}{2x-1})\,\text{d}x & =\int \frac{1}{2x+1}\,\text{d}x+\int \frac{1}{2x-1}\,\text{d}x \\  & =\frac{1}{2}\operatorname{ln}⁡|2x+1|+\frac{1}{2}\operatorname{ln}⁡|2x-1|+C \\  & =\frac{1}{2}\operatorname{ln}⁡|(2x+1)(2x-1)|+\frac{1}{2}\text{ }\operatorname{ln}⁡K \\  & =\frac{1}{2}\operatorname{ln}⁡(K|(2x+1)(2x-1)|)\end{aligned}
$$

Notice that we used the laws of logarithms to write the result as a single logarithm.

## q-72450

Source DB entity 17592186339120; field 4e2bab5c-f6f6-520b-81c3-9f397f7cf935, selection/radio; parameters [a,b,c]=[5, 2, -2]; family same-symmetric. Exact prompt:

Calculate $\int (\frac{1}{5x+2}+\frac{1}{5x-2})\,\text{d}x.$ Assume that $K$ is an arbitrary positive constant.

Complete source bank and parameterized recipes:

- 1. `$5\operatorname{ln}⁡(K|(5x+2)(5x-2)|)$` → a:product.
- 2. `$5\operatorname{ln}⁡(K|\frac{5x+2}{5x-2}|)$` → a:quotient.
- 3. `$\frac{1}{5}\operatorname{ln}⁡(K|\frac{5x+2}{5x-2}|)$` → inv_a:quotient.
- 4. `$\frac{1}{5}\operatorname{ln}⁡(K|(5x+2)(5x-2)|)$` → inv_a:product (correct).
- 5. `$\operatorname{ln}⁡(K|\frac{5x+2}{5x-2}|)$` → one:quotient.

Exact source solution (template components in contract.json):

Let's solve this using the general formula:

$$
\begin{aligned}\int (\frac{1}{5x+2}+\frac{1}{5x-2})\,\text{d}x & =\int \frac{1}{5x+2}\,\text{d}x+\int \frac{1}{5x-2}\,\text{d}x \\  & =\frac{1}{5}\operatorname{ln}⁡|5x+2|+\frac{1}{5}\operatorname{ln}⁡|5x-2|+C \\  & =\frac{1}{5}\operatorname{ln}⁡|(5x+2)(5x-2)|+\frac{1}{5}\operatorname{ln}⁡K \\  & =\frac{1}{5}\operatorname{ln}⁡(K|(5x+2)(5x-2)|)\end{aligned}
$$

Notice that we used the laws of logarithms to write the result as a single logarithm.

## Incomplete source

q-49521: equal positive shifts 3, opposite unit slopes; five-choice radio bank, missing rating, correct designation and solution. No supported bank replay claim is made for this source. All original values remain in source.json/source.edn.

Source fidelity is separate from mathematical correctness and native grading: source-replay.json records each complete bank; validation.json records displayed mathematics; native-grading.json records the actual learner grader. review.md places originals, exact replay and fresh variants together. No plots or assets need extraction or publication.
