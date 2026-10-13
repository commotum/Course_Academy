# Template extraction

For each source below, the exact captured record is retained in source.json/source.edn. All choices are assigned to their field and mapped to a complete bank, without pooling recipes. Recipe triples denote amplitude × inverse-function(argument-slope × x) + C. These are observed expression patterns; their psychological mistake interpretation is unresolved and is not shown to learners.

## Shared mathematics

For positive n and real x with |nx|>1, d arcsec(nx)/dx = 1/(|x| sqrt(n²x²−1)). A normalized integral c/(|x|sqrt(n²x²−1)) therefore has primitive c arcsec(nx)+C on each connected interval. Moderate keeps |nx| and (nx)² explicit. Hard expands n²x² and/or writes an outside denominator prefactor. Each source retains its substitution u=nx, dx=du/n, cancellation, primitive and back-substitution sequence.

## Fixed, variable, and conditional components

Fixed: variable x, constant C, principal real inverse secant, denominator square-root minus one, exact source prose/Markdown layout, one selection field and five choices. Variable: positive slope n, numerator a, n², initial normalization a*n where needed, reduced final coefficient. Conditional: numerator-one omission, reciprocal prefactors, source bank profile, equal/proportional scales, perfect-square versus nonsquare slope forms. No new distractors or feedback. All numerical source tokens are changed simultaneously; exponent two is fixed. Source wording is retained exactly at replay. The selection placeholder is an explicit UI placement addition. Canonicalized answer notation is tested separately from algebraic equivalence.

## Proposed bounds

t is a positive integer from 2 through 24. Each bank imposes the observed equal/proportional/square relationship from its source. Root profiles use nonsquare t. Colliding banks are ineligible. These are intentionally narrow finite sampling bounds; all observed values are included. Negative slopes are not observed and are deferred. Bank/order/seed changes never establish a new mathematical task. Identity includes profile to avoid authored-bank collisions; inventory deduplication uses normalized integrand, independently of identity.

## Per-source components and complete banks

### q-69476: m-prefactor (moderate)

EDB question 17592186064941; field ae92fcf7-e93b-597c-a9c2-a8feb16ae56b, key selection. Observed t=8, slope n=8, numerator a=8, normalized amplitude c=1. All parameters are positive; the real domain is |8x|>1.

$\int \frac{8\,\text{d}x}{|8x|\sqrt{(8x)^{2}-1}}=$

| Source answer UUID | Exact captured value | Observed recipe at source parameters | Correct |
|---|---|---|---|
| 33cf2d14-d04d-51e3-b76e-64b8e1a665b6 | `4\text{arcsec}(8x)+C` | 4 × arcsec(8x)+C | False |
| 3dc9dd34-b284-58b6-84db-345e4e630da9 | `\text{arcsec}(64x)+C` | 1 × arcsec(64x)+C | False |
| 8f11fd04-9fa8-5d58-b9c9-6ab52adba008 | `\text{arcsec}(8x)+C` | 1 × arcsec(8x)+C | True |
| d2244dec-f6d2-5e94-8b71-32f7eabc6720 | `\frac{\text{arcsec}(8x)}{8}+C` | 1/8 × arcsec(8x)+C | False |
| d66dc866-442a-59b0-ad6e-365d928672f6 | `\frac{\text{arcsec}(4x)}{4}+C` | 1/4 × arcsec(4x)+C | False |

Exact source worked solution:

Note that we can rewrite this integral as

$$
\int \frac{8\,\text{d}x}{|8x|\sqrt{(8x)^{2}-1}}=8\int \frac{\text{d}x}{|8x|\sqrt{(8x)^{2}-1}}.
$$

This integral now resembles the basic one for $\text{arcsec},$

$$
\int \frac{1}{|u|\sqrt{{u}^{2}-1}}\text{d}u=\text{arcsec}(u)+C.
$$

The only difference is that instead of $u$ as the variable, we have $8x.$

So, let's substitute $u=8x.$ Differentiating, we get

$$
\frac{\text{d}u}{\text{d}x}=8\,⟹\,\text{d}x=\frac{1}{8}\text{d}u.
$$

Using the above, we can write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}\begin{aligned}8\int \frac{1}{|8x|\sqrt{(8x)^{2}-1}}\text{d}x & =8\int \frac{1}{|u|\sqrt{{u}^{2}-1}}\cdot (\frac{1}{8}\text{d}u) \\  & =\int \frac{\text{d}u}{|u|\sqrt{{u}^{2}-1}} \\  & =\text{arcsec }u+C \\  & =\text{arcsec}(8x)+C\end{aligned}\end{aligned}
$$

### q-69475: m-prefactor (moderate)

EDB question 17592186335976; field ebde86f4-5f82-5ab1-8866-0726b82f2be1, key selection. Observed t=7, slope n=7, numerator a=7, normalized amplitude c=1. All parameters are positive; the real domain is |7x|>1.

$\int \frac{7\,\text{d}x}{|7x|\sqrt{(7x)^{2}-1}}=$

| Source answer UUID | Exact captured value | Observed recipe at source parameters | Correct |
|---|---|---|---|
| 4c842fc6-bdb7-5fd1-95ec-a8a6c5c213af | `\text{arcsec}(7x)+C` | 1 × arcsec(7x)+C | True |
| 8817bce9-1d12-59f6-a5d1-e12cf7bf9ea0 | `\frac{\text{arcsec}(7x)}{7}+C` | 1/7 × arcsec(7x)+C | False |
| d4994be2-56ea-5429-8d7d-0f2980d19115 | `\frac{\text{arcsec}(49x)}{7}+C` | 1/7 × arcsec(49x)+C | False |
| d5ef86d7-cffa-55cc-8343-9157ea5e011e | `\frac{\text{arcsec}(7x)}{49}+C` | 1/49 × arcsec(7x)+C | False |
| eff32ea7-4fa2-5bab-91d2-777e88bff4bf | `\text{arcsec}(49x)+C` | 1 × arcsec(49x)+C | False |

Exact source worked solution:

Note that we can rewrite this integral as

$$
\int \frac{7\,\text{d}x}{|7x|\sqrt{(7x)^{2}-1}}=7\int \frac{\text{d}x}{|7x|\sqrt{(7x)^{2}-1}}.
$$

This integral now resembles the basic one for $\text{arcsec},$

$$
\int \frac{1}{|u|\sqrt{{u}^{2}-1}}\text{d}u=\text{arcsec}(u)+C.
$$

The only difference is that instead of $u$ as the variable, we have $7x.$

So, let's substitute $u=7x.$ Differentiating, we get

$$
\frac{\text{d}u}{\text{d}x}=7\,⟹\,\text{d}x=\frac{1}{7}\text{d}u.
$$

Using the above, we can write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}\begin{aligned}7\int \frac{1}{|7x|\sqrt{(7x)^{2}-1}}\text{d}x & =7\int \frac{1}{|u|\sqrt{{u}^{2}-1}}\cdot (\frac{1}{7}\text{d}u) \\  & =\int \frac{\text{d}u}{|u|\sqrt{{u}^{2}-1}} \\  & =\text{arcsec }u+C \\  & =\text{arcsec}(7x)+C\end{aligned}\end{aligned}
$$

### q-69477: m-prefactor (moderate)

EDB question 17592186335977; field 2ae037e8-4b57-5061-96fb-95244295292c, key selection. Observed t=3, slope n=9, numerator a=3, normalized amplitude c=1/3. All parameters are positive; the real domain is |9x|>1.

$\int \frac{3\,\text{d}x}{|9x|\sqrt{(9x)^{2}-1}}=$

| Source answer UUID | Exact captured value | Observed recipe at source parameters | Correct |
|---|---|---|---|
| 48ed7e88-42a3-5874-867c-a70eb196b8de | `\text{arcsec}(9x)+C` | 1 × arcsec(9x)+C | False |
| 8bc52df5-2130-5724-8f9a-3900402db0a3 | `\frac{\text{arcsec}(9x)}{3}+C` | 1/3 × arcsec(9x)+C | True |
| 961ad6bb-bcc5-55c8-bf62-b1d0251abaec | `\frac{\text{arcsec}(9x)}{9}+C` | 1/9 × arcsec(9x)+C | False |
| d33c5bc0-c46c-505d-825e-d5fb312cca88 | `\frac{\text{arcsec}(3x)}{81}+C` | 1/81 × arcsec(3x)+C | False |
| d9456840-7b87-506e-b8e7-b50a98cb1b55 | `\text{arcsec}(3x)+C` | 1 × arcsec(3x)+C | False |

Exact source worked solution:

Note that we can rewrite this integral as

$$
\int \frac{3\,\text{d}x}{|9x|\sqrt{(9x)^{2}-1}}=3\int \frac{\text{d}x}{|9x|\sqrt{(9x)^{2}-1}}.
$$

This integral now resembles the basic one for $\text{arcsec},$

$$
\int \frac{1}{|u|\sqrt{{u}^{2}-1}}\text{d}u=\text{arcsec}(u)+C.
$$

The only difference is that instead of $u$ as the variable, we have $9x.$

So, let's substitute $u=9x.$ Differentiating, we get

$$
\frac{\text{d}u}{\text{d}x}=9\,⟹\,\text{d}x=\frac{1}{9}\text{d}u.
$$

Using the above, we can write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}\begin{aligned}3\int \frac{1}{|9x|\sqrt{(9x)^{2}-1}}\text{d}x & =3\int \frac{1}{|u|\sqrt{{u}^{2}-1}}\cdot (\frac{1}{9}\text{d}u) \\  & =\frac{1}{3}\int \frac{\text{d}u}{|u|\sqrt{{u}^{2}-1}} \\  & =\frac{1}{3}\text{arcsec }u+C \\  & =\frac{\text{arcsec}(9x)}{3}+C\end{aligned}\end{aligned}
$$

### q-73715: m-prefactor (moderate)

EDB question 17592186342066; field c6e02fde-8f73-598e-a892-0518e56b81c6, key selection. Observed t=3, slope n=6, numerator a=3, normalized amplitude c=1/2. All parameters are positive; the real domain is |6x|>1.

$\int \frac{3\,\text{d}x}{|6x|\sqrt{(6x)^{2}-1}}=$

| Source answer UUID | Exact captured value | Observed recipe at source parameters | Correct |
|---|---|---|---|
| 12a76728-b839-5d06-89f1-9934eae3f027 | `\frac{\text{arcsec}(6x)}{6}+C` | 1/6 × arcsec(6x)+C | False |
| 665fe7b3-58d5-51b3-a6e6-d098ccd5df2d | `\frac{\text{arcsec}(6x)}{36}+C` | 1/36 × arcsec(6x)+C | False |
| 689ac8e4-68fd-56b3-a68a-d04dadd83f44 | `\frac{\text{arcsec}(6x)}{2}+C` | 1/2 × arcsec(6x)+C | True |
| 926a2dfc-a131-5563-ba53-5afa24278c9d | `\frac{\text{arcsec}(36x)}{6}+C` | 1/6 × arcsec(36x)+C | False |
| e3ae6232-f8ce-5ece-a30d-6e27d814267f | `\text{arcsec}(36x)+C` | 1 × arcsec(36x)+C | False |

Exact source worked solution:

Note that we can rewrite this integral as

$$
\int \frac{3\,\text{d}x}{|6x|\sqrt{(6x)^{2}-1}}=3\int \frac{\text{d}x}{|6x|\sqrt{(6x)^{2}-1}}.
$$

This integral now resembles the basic one for $\text{arcsec},$

$$
\int \frac{1}{|u|\sqrt{{u}^{2}-1}}\text{d}u=\text{arcsec}(u)+C.
$$

The only difference is that instead of $u$ as the variable, we have $6x.$

So, let's substitute $u=6x.$ Differentiating, we get

$$
\frac{\text{d}u}{\text{d}x}=6\,⟹\,\text{d}x=\frac{1}{6}\text{d}u.
$$

Using the above, we can write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}\begin{aligned}3\int \frac{1}{|6x|\sqrt{(6x)^{2}-1}}\text{d}x & =3\int \frac{1}{|u|\sqrt{{u}^{2}-1}}\cdot (\frac{1}{6}\text{d}u) \\  & =\frac{1}{2}\int \frac{\text{d}u}{|u|\sqrt{{u}^{2}-1}} \\  & =\frac{1}{2}\text{arcsec }u+C \\  & =\frac{\text{arcsec}(6x)}{2}+C\end{aligned}\end{aligned}
$$

### q-73716: m-unit (moderate)

EDB question 17592186342067; field d91ba1e9-1dd8-5d35-a35f-ac59fd9e8143, key selection. Observed t=4, slope n=4, numerator a=1, normalized amplitude c=1/4. All parameters are positive; the real domain is |4x|>1.

$\int \frac{\text{d}x}{|4x|\sqrt{(4x)^{2}-1}}=$

| Source answer UUID | Exact captured value | Observed recipe at source parameters | Correct |
|---|---|---|---|
| 5be9359f-ea8b-563c-9bb9-6b1a6826176f | `\frac{\text{arcsec}(4x)}{4}+C` | 1/4 × arcsec(4x)+C | True |
| 64bf2439-df5c-5f13-8e13-540b1d44c9d9 | `\text{arcsec}(4x)+C` | 1 × arcsec(4x)+C | False |
| 81d073cc-887d-5b6a-aeab-6cecc28a4382 | `4\,\text{arcsec}(4x)+C` | 4 × arcsec(4x)+C | False |
| 95b7f420-0b28-5282-a657-40d893b628dd | `\frac{\text{arctan}(4x)}{4}+C` | 1/4 × arctan(4x)+C | False |
| d5244b0b-6f4f-5504-8207-05f6294fbb10 | `\text{arctan}(4x)+C` | 1 × arctan(4x)+C | False |

Exact source worked solution:

This integral resembles the basic one for $\text{arcsec},$

$$
\int \frac{1}{|u|\sqrt{{u}^{2}-1}}\text{d}u=\text{arcsec}(u)+C.
$$

The only difference is that instead of $u$ as the variable, we have $4x.$

So, let's substitute $u=4x.$ Differentiating, we get

$$
\frac{\text{d}u}{\text{d}x}=4\,⟹\,\text{d}x=\frac{1}{4}\text{d}u.
$$

Using the above, we can write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}\begin{aligned}\int \frac{1}{|4x|\sqrt{(4x)^{2}-1}}\text{d}x & =\int \frac{1}{|u|\sqrt{{u}^{2}-1}}\cdot (\frac{1}{4}\text{d}u) \\  & =\frac{1}{4}\int \frac{\text{d}u}{|u|\sqrt{{u}^{2}-1}} \\  & =\frac{1}{4}\text{arcsec }u+C \\  & =\frac{\text{arcsec}(4x)}{4}+C\end{aligned}\end{aligned}
$$

### q-73717: h-prefactor (hard)

EDB question 17592186064952; field 79900759-4114-5519-b212-5c813256836c, key selection. Observed t=2, slope n=2, numerator a=2, normalized amplitude c=2. All parameters are positive; the real domain is |2x|>1.

$\int \frac{2}{|x|\sqrt{4{x}^{2}-1}}\,\text{d}x=$

| Source answer UUID | Exact captured value | Observed recipe at source parameters | Correct |
|---|---|---|---|
| 17153736-08a5-511b-8d66-3076de3a56f5 | `4\,\text{arcsec}(2x)+C` | 4 × arcsec(2x)+C | False |
| 287af432-ac1d-5bb0-9cce-df095ab56481 | `\frac{\text{arcsec}(2x)}{4}+C` | 1/4 × arcsec(2x)+C | False |
| 3031610e-8402-5eae-b837-b04a952ccb28 | `2\,\text{arcsec}(2x)+C` | 2 × arcsec(2x)+C | True |
| 741561ed-033d-5aff-8ad7-766c99be57a0 | `\,\text{arcsec}(2x)+C` | 1 × arcsec(2x)+C | False |
| c8a5cb98-9b11-5ca7-8b96-437d604616ef | `\frac{\text{arcsec}(2x)}{2}+C` | 1/2 × arcsec(2x)+C | False |

Exact source worked solution:

Note that we can rewrite this integral as

$$
\int \frac{2\,\text{d}x}{|x|\sqrt{4{x}^{2}-1}}=4\int \frac{\text{d}x}{|2x|\sqrt{(2x)^{2}-1}}.
$$

This integral now resembles the basic one for $\text{arcsec},$

$$
\int \frac{1}{|u|\sqrt{{u}^{2}-1}}\text{d}u=\text{arcsec}(u)+C.
$$

The only difference is that instead of $u$ as the variable, we have $2x.$

So, let's substitute $u=2x.$ Differentiating, we get

$$
\frac{\text{d}u}{\text{d}x}=2\,⟹\,\text{d}x=\frac{1}{2}\text{d}u.
$$

Using the above, we can write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}\begin{aligned}\int \frac{2}{|x|\sqrt{4{x}^{2}-1}}\,\text{d}x & =4\int \frac{1}{|2x|\sqrt{(2x)^{2}-1}}\,\text{d}x \\  & =4\int \frac{1}{|u|\sqrt{{u}^{2}-1}}\cdot (\frac{1}{2}\text{d}u) \\  & =2\int \frac{\text{d}u}{|u|\sqrt{{u}^{2}-1}} \\  & =2\,\text{arcsec}\,u+C \\  & =2\,\text{arcsec}(2x)+C\end{aligned}\end{aligned}
$$

### q-114051: h-root-unit (hard)

EDB question 17592186250173; field 5bb9394d-1677-5845-bcf1-c7fd75b784b5, key selection. Observed t=5, slope n=sqrt(5), numerator a=1, normalized amplitude c=1. All parameters are positive; the real domain is |sqrt(5)x|>1.

Calculate $\int \frac{1}{|x|\sqrt{5{x}^{2}-1}}\,\text{d}x.$

| Source answer UUID | Exact captured value | Observed recipe at source parameters | Correct |
|---|---|---|---|
| 2557c8c9-61d4-546a-b12e-2149e3cb0784 | `\text{arcsec}(\sqrt{5}x)+C` | 1 × arcsec(sqrt(5)x)+C | True |
| 4b9ffc95-a0ae-5868-bc4f-b4a2ff82ae20 | `5\,\text{arcsec}(\sqrt{5}x)+C` | 5 × arcsec(sqrt(5)x)+C | False |
| 90d77fc7-cc8f-513f-84a7-ae393b51759b | `5\,\text{arcsec}(5x)+C` | 5 × arcsec(5x)+C | False |
| da3de159-0af1-5109-a432-7a259afa945f | `\sqrt{5}\,\text{arcsec}(\sqrt{5}x)+C` | sqrt(5) × arcsec(sqrt(5)x)+C | False |
| f5ce8cb5-8424-5bdb-b48e-afc1856f992f | `\text{arcsec}(5x)+C` | 1 × arcsec(5x)+C | False |

Exact source worked solution:

Note that we can rewrite this integral as

$$
\int \frac{\text{d}x}{|x|\sqrt{5{x}^{2}-1}}=\int \frac{\sqrt{5}}{|\sqrt{5}x|\sqrt{(\sqrt{5}x)^{2}-1}}\text{d}x.
$$

This integral now resembles the basic one for $\text{arcsec},$

$$
\int \frac{1}{|u|\sqrt{{u}^{2}-1}}\text{d}u=\text{arcsec}(u)+C.
$$

The only difference is that instead of $u$ as the variable, we have $\sqrt{5}x.$

So, let's substitute $u=\sqrt{5}x.$ Differentiating, we get

$$
\frac{\text{d}u}{\text{d}x}=\sqrt{5}\,⟹\,\text{d}x=\frac{1}{\sqrt{5}}\text{d}u.
$$

Using the above, we can write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}\begin{aligned}\int \frac{1}{|x|\sqrt{5{x}^{2}-1}}\,\text{d}x & =\int \frac{\sqrt{5}}{|\sqrt{5}x|\sqrt{(\sqrt{5}x)^{2}-1}}\,\text{d}x \\  & =\sqrt{5}\int \frac{1}{|u|\sqrt{{u}^{2}-1}}\cdot (\frac{1}{\sqrt{5}}\text{d}u) \\  & =\sqrt{5}\cdot \frac{1}{\sqrt{5}}\int \frac{\text{d}u}{|u|\sqrt{{u}^{2}-1}} \\  & =\text{arcsec }u+C \\  & =\text{arcsec}(\sqrt{5}x)+C\end{aligned}\end{aligned}
$$

### q-114052: h-root-unit (hard)

EDB question 17592186250174; field 1add6643-9b56-5600-a0e9-cb809f1a9078, key selection. Observed t=2, slope n=sqrt(2), numerator a=1, normalized amplitude c=1. All parameters are positive; the real domain is |sqrt(2)x|>1.

Calculate $\int \frac{1}{|x|\sqrt{2{x}^{2}-1}}\,\text{d}x.$

| Source answer UUID | Exact captured value | Observed recipe at source parameters | Correct |
|---|---|---|---|
| 4d1c680b-da3e-532e-b768-23a73eed1830 | `\sqrt{2}\,\text{arcsec}(x)+C` | sqrt(2) × arcsec(1x)+C | False |
| 76b64e00-cc9d-56bb-96a5-6ed308000d0f | `\text{arcsec}(\frac{x}{\sqrt{2}})+C` | 1 × arcsec(sqrt(2)/2x)+C | False |
| 81a2d087-34bd-5b98-b3f9-540414b7de9a | `\text{arcsec}(\sqrt{2}x)+C` | 1 × arcsec(sqrt(2)x)+C | True |
| a16a9266-9795-55dc-8015-252092435b4f | `\sqrt{2}\,\text{arcsec}(\sqrt{2}x)+C` | sqrt(2) × arcsec(sqrt(2)x)+C | False |
| f738a875-32bb-5a84-9c85-9b96cb51105b | `2\,\text{arcsec}(\sqrt{2}x)+C` | 2 × arcsec(sqrt(2)x)+C | False |

Exact source worked solution:

Note that we can rewrite this integral as

$$
\int \frac{\text{d}x}{|x|\sqrt{2{x}^{2}-1}}=\int \frac{\sqrt{2}}{|\sqrt{2}x|\sqrt{(\sqrt{2}x)^{2}-1}}\text{d}x.
$$

This integral now resembles the basic one for $\text{arcsec},$

$$
\int \frac{1}{|u|\sqrt{{u}^{2}-1}}\text{d}u=\text{arcsec}(u)+C.
$$

The only difference is that instead of $u$ as the variable, we have $\sqrt{2}x.$

So, let's substitute $u=\sqrt{2}x.$ Differentiating, we get

$$
\frac{\text{d}u}{\text{d}x}=\sqrt{2}\,⟹\,\text{d}x=\frac{1}{\sqrt{2}}\text{d}u.
$$

Using the above, we can write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}\begin{aligned}\int \frac{1}{|x|\sqrt{2{x}^{2}-1}}\,\text{d}x & =\int \frac{\sqrt{2}}{|\sqrt{2}x|\sqrt{(\sqrt{2}x)^{2}-1}}\,\text{d}x \\  & =\sqrt{2}\int \frac{1}{|u|\sqrt{{u}^{2}-1}}\cdot (\frac{1}{\sqrt{2}}\text{d}u) \\  & =\sqrt{2}\cdot \frac{1}{\sqrt{2}}\int \frac{\text{d}u}{|u|\sqrt{{u}^{2}-1}} \\  & =\text{arcsec }u+C \\  & =\text{arcsec}(\sqrt{2}x)+C\end{aligned}\end{aligned}
$$

### q-114053: h-root-unit (hard)

EDB question 17592186250175; field ad6f5e31-fa19-5c0b-8277-0506de476581, key selection. Observed t=3, slope n=sqrt(3), numerator a=1, normalized amplitude c=1. All parameters are positive; the real domain is |sqrt(3)x|>1.

Calculate $\int \frac{1}{|x|\sqrt{3{x}^{2}-1}}\,\text{d}x.$

| Source answer UUID | Exact captured value | Observed recipe at source parameters | Correct |
|---|---|---|---|
| 30f7223b-3eec-5940-8deb-7bc6e19cac0d | `\text{arcsec}(\frac{x}{\sqrt{3}})+C` | 1 × arcsec(sqrt(3)/3x)+C | False |
| 3d76b2e3-b64f-5ff7-9e80-9f8479c9c899 | `\text{arcsec}(\sqrt{3}x)+C` | 1 × arcsec(sqrt(3)x)+C | True |
| 9bd42595-09d2-528a-bd27-8cbc87ecbf1d | `\frac{\sqrt{3}}{3}\text{arcsec}(x)+C` | sqrt(3)/3 × arcsec(1x)+C | False |
| def281e2-ae26-5545-95a5-a8332aa49347 | `\text{arcsec}(3x)+C` | 1 × arcsec(3x)+C | False |
| f9f3a636-5c31-5b0d-9342-5cf8e8d5dd79 | `\sqrt{3}\,\text{arcsec}(x)+C` | sqrt(3) × arcsec(1x)+C | False |

Exact source worked solution:

Note that we can rewrite this integral as

$$
\int \frac{\text{d}x}{|x|\sqrt{3{x}^{2}-1}}=\int \frac{\sqrt{3}}{|\sqrt{3}x|\sqrt{(\sqrt{3}x)^{2}-1}}\text{d}x.
$$

This integral now resembles the basic one for $\text{arcsec},$

$$
\int \frac{1}{|u|\sqrt{{u}^{2}-1}}\text{d}u=\text{arcsec}(u)+C.
$$

The only difference is that instead of $u$ as the variable, we have $\sqrt{3}x.$

So, let's substitute $u=\sqrt{3}x.$ Differentiating, we get

$$
\frac{\text{d}u}{\text{d}x}=\sqrt{3}\,⟹\,\text{d}x=\frac{1}{\sqrt{3}}\text{d}u.
$$

Using the above, we can write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}\begin{aligned}\int \frac{1}{|x|\sqrt{3{x}^{2}-1}}\,\text{d}x & =\int \frac{\sqrt{3}}{|\sqrt{3}x|\sqrt{(\sqrt{3}x)^{2}-1}}\,\text{d}x \\  & =\sqrt{3}\int \frac{1}{|u|\sqrt{{u}^{2}-1}}\cdot (\frac{1}{\sqrt{3}}\text{d}u) \\  & =\sqrt{3}\cdot \frac{1}{\sqrt{3}}\int \frac{\text{d}u}{|u|\sqrt{{u}^{2}-1}} \\  & =\text{arcsec }u+C \\  & =\text{arcsec}(\sqrt{3}x)+C\end{aligned}\end{aligned}
$$

### q-114054: h-root-unit (hard)

EDB question 17592186250176; field 8b28b499-c249-529d-8a2e-50e60f8a5000, key selection. Observed t=6, slope n=sqrt(6), numerator a=1, normalized amplitude c=1. All parameters are positive; the real domain is |sqrt(6)x|>1.

Calculate $\int \frac{1}{|x|\sqrt{6{x}^{2}-1}}\,\text{d}x.$

| Source answer UUID | Exact captured value | Observed recipe at source parameters | Correct |
|---|---|---|---|
| 00c4a36b-1ea2-5c73-8a8e-897727eb8f12 | `\frac{\sqrt{6}}{6}\,\text{arcsec}(x)+C` | sqrt(6)/6 × arcsec(1x)+C | False |
| 1a99f5d4-adb5-558f-ab9d-871641a6895a | `\text{arcsec}(\sqrt{6}x)+C` | 1 × arcsec(sqrt(6)x)+C | True |
| 473a1c85-0e25-55e8-9960-af9d6576e38d | `6\,\text{arcsec}(\sqrt{6}x)+C` | 6 × arcsec(sqrt(6)x)+C | False |
| 612053c7-5fa5-581e-863a-77db7fe44da7 | `\text{arcsec}(\frac{x}{\sqrt{6}})+C` | 1 × arcsec(sqrt(6)/6x)+C | False |
| 96a16219-09aa-5a3c-a6f7-b42ee02e1ec9 | `\sqrt{6}\,\text{arcsec}(x)+C` | sqrt(6) × arcsec(1x)+C | False |

Exact source worked solution:

Note that we can rewrite this integral as

$$
\int \frac{\text{d}x}{|x|\sqrt{6{x}^{2}-1}}=\int \frac{\sqrt{6}}{|\sqrt{6}x|\sqrt{(\sqrt{6}x)^{2}-1}}\text{d}x.
$$

This integral now resembles the basic one for $\text{arcsec},$

$$
\int \frac{1}{|u|\sqrt{{u}^{2}-1}}\text{d}u=\text{arcsec}(u)+C.
$$

The only difference is that instead of $u$ as the variable, we have $\sqrt{6}x.$

So, let's substitute $u=\sqrt{6}x.$ Differentiating, we get

$$
\frac{\text{d}u}{\text{d}x}=\sqrt{6}\,⟹\,\text{d}x=\frac{1}{\sqrt{6}}\text{d}u.
$$

Using the above, we can write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}\begin{aligned}\int \frac{1}{|x|\sqrt{6{x}^{2}-1}}\,\text{d}x & =\int \frac{\sqrt{6}}{|\sqrt{6}x|\sqrt{(\sqrt{6}x)^{2}-1}}\,\text{d}x \\  & =\sqrt{6}\int \frac{1}{|u|\sqrt{{u}^{2}-1}}\cdot (\frac{1}{\sqrt{6}}\text{d}u) \\  & =\sqrt{6}\cdot \frac{1}{\sqrt{6}}\int \frac{\text{d}u}{|u|\sqrt{{u}^{2}-1}} \\  & =\text{arcsec }u+C \\  & =\text{arcsec}(\sqrt{6}x)+C\end{aligned}\end{aligned}
$$

### q-114055: h-root-prefactor (hard)

EDB question 17592186250177; field ae56369a-9dc7-56a8-9b42-9abf878339d0, key selection. Observed t=7, slope n=sqrt(7), numerator a=7, normalized amplitude c=7. All parameters are positive; the real domain is |sqrt(7)x|>1.

Calculate $\int \frac{7}{|x|\sqrt{7{x}^{2}-1}}\,\text{d}x.$

| Source answer UUID | Exact captured value | Observed recipe at source parameters | Correct |
|---|---|---|---|
| 345d0dd8-1722-50e6-996a-3145ed9fa4cc | `\text{arcsec}(\sqrt{7}x)+C` | 1 × arcsec(sqrt(7)x)+C | False |
| 795dfd60-9293-54b9-a133-af67359f3625 | `\text{arcsec}(7x)+C` | 1 × arcsec(7x)+C | False |
| a6deadf7-ef59-56ac-a86b-d7bdb56e7adc | `7\sqrt{7}\,\text{arcsec}(x)+C` | 7*sqrt(7) × arcsec(1x)+C | False |
| afa04312-a9ee-53e6-8294-76266301a3a4 | `\frac{\sqrt{7}}{7}\,\text{arcsec}(x)+C` | sqrt(7)/7 × arcsec(1x)+C | False |
| d0c6dca0-cfeb-5ddf-b8cf-96bba1eee175 | `7\,\text{arcsec}(\sqrt{7}x)+C` | 7 × arcsec(sqrt(7)x)+C | True |

Exact source worked solution:

Note that we can rewrite this integral as

$$
\int \frac{7}{|x|\sqrt{7{x}^{2}-1}}\text{d}x=\int \frac{7\sqrt{7}}{|\sqrt{7}x|\sqrt{(\sqrt{7}x)^{2}-1}}\text{d}x.
$$

This integral now resembles the basic one for $\text{arcsec},$

$$
\int \frac{1}{|u|\sqrt{{u}^{2}-1}}\text{d}u=\text{arcsec}(u)+C.
$$

The only difference is that instead of $u$ as the variable, we have $\sqrt{7}x.$

So, let's substitute $u=\sqrt{7}x.$ Differentiating, we get

$$
\frac{\text{d}u}{\text{d}x}=\sqrt{7}\,⟹\,\text{d}x=\frac{1}{\sqrt{7}}\text{d}u.
$$

Using the above, we can write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}\begin{aligned}\int \frac{7}{|x|\sqrt{7{x}^{2}-1}}\,\text{d}x & =\int \frac{7\sqrt{7}}{|\sqrt{7}x|\sqrt{(\sqrt{7}x)^{2}-1}}\,\text{d}x \\  & =7\sqrt{7}\int \frac{1}{|u|\sqrt{{u}^{2}-1}}\cdot (\frac{1}{\sqrt{7}}\text{d}u) \\  & =7\sqrt{7}\cdot \frac{1}{\sqrt{7}}\int \frac{\text{d}u}{|u|\sqrt{{u}^{2}-1}} \\  & =7\,\text{arcsec }u+C \\  & =7\,\text{arcsec}(\sqrt{7}x)+C\end{aligned}\end{aligned}
$$

### q-114056: h-root-prefactor (hard)

EDB question 17592186250178; field f124bfeb-924c-5974-b5d6-5bac9d8b7458, key selection. Observed t=8, slope n=2*sqrt(2), numerator a=8, normalized amplitude c=8. All parameters are positive; the real domain is |2*sqrt(2)x|>1.

Calculate $\int \frac{8}{|x|\sqrt{8{x}^{2}-1}}\,\text{d}x.$

| Source answer UUID | Exact captured value | Observed recipe at source parameters | Correct |
|---|---|---|---|
| 06349d8e-8391-574b-b6ee-d09717af159e | `8\sqrt{8}\,\text{arcsec}(x)+C` | 16*sqrt(2) × arcsec(1x)+C | False |
| 28b08c9d-77c7-5bea-8de3-24e47c4a6b22 | `8\,\text{arcsec}(\sqrt{8}x)+C` | 8 × arcsec(2*sqrt(2)x)+C | True |
| 4b4c8ae4-b8b1-5ed2-b232-73c90f37ed26 | `\text{arcsec}(\sqrt{8}x)+C` | 1 × arcsec(2*sqrt(2)x)+C | False |
| 97ffb8aa-ac92-5db2-a3d4-4a6b34576f59 | `\frac{\sqrt{8}}{8}\,\text{arcsec}(x)+C` | sqrt(2)/4 × arcsec(1x)+C | False |
| b9b1dd01-2ffe-53eb-9456-1dfad676593b | `8\,\text{arcsec}(\frac{x}{\sqrt{8}})+C` | 8 × arcsec(sqrt(2)/4x)+C | False |

Exact source worked solution:

Note that we can rewrite this integral as

$$
\int \frac{8}{|x|\sqrt{8{x}^{2}-1}}\text{d}x=\int \frac{8\sqrt{8}}{|\sqrt{8}x|\sqrt{(\sqrt{8}x)^{2}-1}}\text{d}x.
$$

This integral now resembles the basic one for $\text{arcsec},$

$$
\int \frac{1}{|u|\sqrt{{u}^{2}-1}}\text{d}u=\text{arcsec}(u)+C.
$$

The only difference is that instead of $u$ as the variable, we have $\sqrt{8}x.$

So, let's substitute $u=\sqrt{8}x.$ Differentiating, we get

$$
\frac{\text{d}u}{\text{d}x}=\sqrt{8}\,⟹\,\text{d}x=\frac{1}{\sqrt{8}}\text{d}u.
$$

Using the above, we can write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}\begin{aligned}\int \frac{8}{|x|\sqrt{8{x}^{2}-1}}\,\text{d}x & =\int \frac{8\sqrt{8}}{|\sqrt{8}x|\sqrt{(\sqrt{8}x)^{2}-1}}\,\text{d}x \\  & =8\sqrt{8}\int \frac{1}{|u|\sqrt{{u}^{2}-1}}\cdot (\frac{1}{\sqrt{8}}\text{d}u) \\  & =8\sqrt{8}\cdot \frac{1}{\sqrt{8}}\int \frac{\text{d}u}{|u|\sqrt{{u}^{2}-1}} \\  & =8\,\text{arcsec }u+C \\  & =8\,\text{arcsec}(\sqrt{8}x)+C\end{aligned}\end{aligned}
$$

### q-114057: h-square-calculate-prefactor (hard)

EDB question 17592186250179; field 1249c5e2-b95a-56a8-9562-7cfa27416496, key selection. Observed t=5, slope n=10, numerator a=5, normalized amplitude c=5. All parameters are positive; the real domain is |10x|>1.

Calculate $\int \frac{5}{|x|\sqrt{100{x}^{2}-1}}\,\text{d}x.$

| Source answer UUID | Exact captured value | Observed recipe at source parameters | Correct |
|---|---|---|---|
| 20eeed43-06fc-5a51-a569-cc359295eeb2 | `\text{arcsec}(50x)+C` | 1 × arcsec(50x)+C | False |
| 23a4faf6-7048-5692-877b-730a3aa48b44 | `\text{arcsec}(10x)+C` | 1 × arcsec(10x)+C | False |
| 860a98b5-c89e-5a98-a319-70c942ace928 | `\frac{1}{5}\,\text{arcsec}(10x)+C` | 1/5 × arcsec(10x)+C | False |
| c1ea824c-8f8e-5257-ae08-86f03dfd7210 | `5\,\text{arcsec}(10x)+C` | 5 × arcsec(10x)+C | True |
| d7024181-5209-53f4-9e77-1d70e6a37869 | `5\,\text{arcsec}(x)+C` | 5 × arcsec(1x)+C | False |

Exact source worked solution:

Note that we can rewrite this integral as

$$
\int \frac{5}{|x|\sqrt{100{x}^{2}-1}}\text{d}x=\int \frac{50}{|10x|\sqrt{(10x)^{2}-1}}\text{d}x.
$$

This integral now resembles the basic one for $\text{arcsec},$

$$
\int \frac{1}{|u|\sqrt{{u}^{2}-1}}\text{d}u=\text{arcsec}(u)+C.
$$

The only difference is that instead of $u$ as the variable, we have $10x.$

So, let's substitute $u=10x.$ Differentiating, we get

$$
\frac{\text{d}u}{\text{d}x}=10\,⟹\,\text{d}x=\frac{1}{10}\text{d}u.
$$

Using the above, we can write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}\begin{aligned}\int \frac{5}{|x|\sqrt{100{x}^{2}-1}}\,\text{d}x & =\int \frac{50}{|10x|\sqrt{(10x)^{2}-1}}\,\text{d}x \\  & =50\int \frac{1}{|u|\sqrt{{u}^{2}-1}}\cdot (\frac{1}{10}\text{d}u) \\  & =50\cdot \frac{1}{10}\int \frac{\text{d}u}{|u|\sqrt{{u}^{2}-1}} \\  & =5\,\text{arcsec }u+C \\  & =5\,\text{arcsec}(10x)+C\end{aligned}\end{aligned}
$$

### q-49519: h-denominator (hard)

EDB question 17592186332729; field 2ed515ce-b125-59ef-ba87-1982f7680cc3, key selection. Observed t=4, slope n=4, numerator a=1/4, normalized amplitude c=1/4. All parameters are positive; the real domain is |4x|>1.

$\int \frac{1}{4|x|\sqrt{16{x}^{2}-1}}\,\text{d}x=$

| Source answer UUID | Exact captured value | Observed recipe at source parameters | Correct |
|---|---|---|---|
| 26bff1d2-1a1f-5568-b606-c926ad4e222e | `\frac{\operatorname{arcsin}⁡(4x)}{4}+C` | 1/4 × arcsin(4x)+C | False |
| 38f382b6-b9e0-5d37-bb15-bf2017958200 | `\frac{\operatorname{arctan}⁡(4x)}{4}+C` | 1/4 × arctan(4x)+C | False |
| 88b1a168-dccc-5c24-aa5c-58eef11e4b53 | `4\text{arcsec}(4x)+C` | 4 × arcsec(4x)+C | False |
| 8a671a08-acf6-51a4-a4b1-a79a1a8a1a19 | `\frac{\text{arcsec}(16x)}{2}+C` | 1/2 × arcsec(16x)+C | False |
| c1c62bda-b0cb-5477-843f-9e7f08c270e5 | `\frac{\text{arcsec}(4x)}{4}+C` | 1/4 × arcsec(4x)+C | True |

Exact source worked solution:

Note that we can rewrite this integral as

$$
\int \frac{\text{d}x}{4|x|\sqrt{16{x}^{2}-1}}=\int \frac{\text{d}x}{|4x|\sqrt{(4x)^{2}-1}}.
$$

This integral now resembles the basic one for $\text{arcsec},$

$$
\int \frac{1}{|u|\sqrt{{u}^{2}-1}}\text{d}u=\text{arcsec}(u)+C.
$$

The only difference is that instead of $u$ as the variable, we have $4x.$

So, let's substitute $u=4x.$ Differentiating, we get

$$
\frac{\text{d}u}{\text{d}x}=4\,⟹\,\text{d}x=\frac{1}{4}\text{d}u.
$$

Using the above, we can write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}\begin{aligned}\int \frac{1}{4|x|\sqrt{16{x}^{2}-1}}\,\text{d}x & =\int \frac{1}{|4x|\sqrt{(4x)^{2}-1}}\,\text{d}x \\  & =\int \frac{1}{|u|\sqrt{{u}^{2}-1}}\cdot (\frac{1}{4}\text{d}u) \\  & =\frac{1}{4}\int \frac{\text{d}u}{|u|\sqrt{{u}^{2}-1}} \\  & =\frac{1}{4}\text{arcsec }u+C \\  & =\frac{\text{arcsec}(4x)}{4}+C\end{aligned}\end{aligned}
$$

### q-49554: h-denominator (hard)

EDB question 17592186332740; field b3ccce72-f1f2-5395-8899-d57e02ead31c, key selection. Observed t=3, slope n=3, numerator a=1/3, normalized amplitude c=1/3. All parameters are positive; the real domain is |3x|>1.

$\int \frac{1}{3|x|\sqrt{9{x}^{2}-1}}\,\text{d}x=$

| Source answer UUID | Exact captured value | Observed recipe at source parameters | Correct |
|---|---|---|---|
| 4b0edf81-9914-5a0f-b9b6-d58d70540093 | `\frac{\text{arcsec}(x)}{3}+C` | 1/3 × arcsec(1x)+C | False |
| 70cf07b2-a48c-5c20-b1ad-493648041c3b | `\frac{\text{arcsec}(9x)}{3}+C` | 1/3 × arcsec(9x)+C | False |
| 9a56a3d4-f0db-5dee-8e1b-e1e7174dd979 | `\frac{\operatorname{arcsin}⁡(3x)}{3}+C` | 1/3 × arcsin(3x)+C | False |
| a43c7a93-7056-56e0-adc4-8cc368c5eac5 | `\frac{\operatorname{arcsin}⁡(9x)}{3}+C` | 1/3 × arcsin(9x)+C | False |
| e8c453d1-3b22-5ee0-8261-9dc453f931aa | `\frac{\text{arcsec}(3x)}{3}+C` | 1/3 × arcsec(3x)+C | True |

Exact source worked solution:

Note that we can rewrite this integral as

$$
\int \frac{\text{d}x}{3|x|\sqrt{9{x}^{2}-1}}=\int \frac{\text{d}x}{|3x|\sqrt{(3x)^{2}-1}}.
$$

This integral now resembles the basic one for $\text{arcsec},$

$$
\int \frac{1}{|u|\sqrt{{u}^{2}-1}}\text{d}u=\text{arcsec}(u)+C.
$$

The only difference is that instead of $u$ as the variable, we have $3x.$

So, let's substitute $u=3x.$ Differentiating, we get

$$
\frac{\text{d}u}{\text{d}x}=3\,⟹\,\text{d}x=\frac{1}{3}\text{d}u.
$$

Using the above, we can write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}\begin{aligned}\int \frac{1}{3|x|\sqrt{9{x}^{2}-1}}\,\text{d}x & =\int \frac{1}{|3x|\sqrt{(3x)^{2}-1}}\,\text{d}x \\  & =\int \frac{1}{|u|\sqrt{{u}^{2}-1}}\cdot (\frac{1}{3}\text{d}u) \\  & =\frac{1}{3}\int \frac{\text{d}u}{|u|\sqrt{{u}^{2}-1}} \\  & =\frac{1}{3}\text{arcsec }u+C \\  & =\frac{\text{arcsec}(3x)}{3}+C\end{aligned}\end{aligned}
$$

### q-49555: h-denominator (hard)

EDB question 17592186332741; field 89604dd1-6f4e-5479-bb62-31a5924f3f5e, key selection. Observed t=6, slope n=6, numerator a=1/6, normalized amplitude c=1/6. All parameters are positive; the real domain is |6x|>1.

$\int \frac{1}{6|x|\sqrt{36{x}^{2}-1}}\,\text{d}x=$

| Source answer UUID | Exact captured value | Observed recipe at source parameters | Correct |
|---|---|---|---|
| 1afb9d8c-3f67-5355-93d6-a9093bad7dae | `\frac{\operatorname{arcsin}⁡(6x)}{6}+C` | 1/6 × arcsin(6x)+C | False |
| 3226e3a9-ff07-580d-875b-1db26197856a | `\frac{\text{arcsec}(36x)}{6}+C` | 1/6 × arcsec(36x)+C | False |
| d697edf8-7533-5458-807b-5604ad7429ef | `\text{arcsec}(6x)+C` | 1 × arcsec(6x)+C | False |
| d72cc629-030b-503a-b49e-63c0be8afa3b | `\frac{\text{arcsec}(6x)}{6}+C` | 1/6 × arcsec(6x)+C | True |
| d885db49-c6b0-5c70-8dc4-c09546b4b009 | `\text{arcsec}(36x)+C` | 1 × arcsec(36x)+C | False |

Exact source worked solution:

Note that we can rewrite this integral as

$$
\int \frac{\text{d}x}{6|x|\sqrt{36{x}^{2}-1}}=\int \frac{\text{d}x}{|6x|\sqrt{(6x)^{2}-1}}.
$$

This integral now resembles the basic one for $\text{arcsec},$

$$
\int \frac{1}{|u|\sqrt{{u}^{2}-1}}\text{d}u=\text{arcsec}(u)+C.
$$

The only difference is that instead of $u$ as the variable, we have $6x.$

So, let's substitute $u=6x.$ Differentiating, we get

$$
\frac{\text{d}u}{\text{d}x}=6\,⟹\,\text{d}x=\frac{1}{6}\text{d}u.
$$

Using the above, we can write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}\begin{aligned}\int \frac{1}{6|x|\sqrt{36{x}^{2}-1}}\,\text{d}x & =\int \frac{1}{|6x|\sqrt{(6x)^{2}-1}}\,\text{d}x \\  & =\int \frac{1}{|u|\sqrt{{u}^{2}-1}}\cdot (\frac{1}{6}\text{d}u) \\  & =\frac{1}{6}\int \frac{\text{d}u}{|u|\sqrt{{u}^{2}-1}} \\  & =\frac{1}{6}\text{arcsec }u+C \\  & =\frac{\text{arcsec}(6x)}{6}+C\end{aligned}\end{aligned}
$$

### q-73718: h-denominator (hard)

EDB question 17592186342068; field 0d389694-7fb3-5b9c-b985-67d93a5095c2, key selection. Observed t=5, slope n=5, numerator a=1/5, normalized amplitude c=1/5. All parameters are positive; the real domain is |5x|>1.

$\int \frac{1}{5|x|\sqrt{25{x}^{2}-1}}\,\text{d}x=$

| Source answer UUID | Exact captured value | Observed recipe at source parameters | Correct |
|---|---|---|---|
| 14690a52-f522-5cec-90d3-9f420e7fc080 | `5\,\text{arctan}(5x)+C` | 5 × arctan(5x)+C | False |
| 5da47576-8911-5b68-868f-555462fcef8e | `\frac{\text{arcsec}(5x)}{5}+C` | 1/5 × arcsec(5x)+C | True |
| 6ec5d84f-e713-5832-b748-a0e4c715f798 | `\frac{\text{arctan}(5x)}{5}+C` | 1/5 × arctan(5x)+C | False |
| 7b9a50aa-ecbb-5989-afe3-1d8c3cdb9d07 | `\text{arcsec}(5x)+C` | 1 × arcsec(5x)+C | False |
| 99ab830d-95ff-5734-ab2f-bab2f3570815 | `5\,\text{arcsec}(5x)+C` | 5 × arcsec(5x)+C | False |

Exact source worked solution:

Note that we can rewrite this integral as

$$
\int \frac{\text{d}x}{5|x|\sqrt{25{x}^{2}-1}}=\int \frac{\text{d}x}{|5x|\sqrt{(5x)^{2}-1}}.
$$

This integral now resembles the basic one for $\text{arcsec},$

$$
\int \frac{1}{|u|\sqrt{{u}^{2}-1}}\text{d}u=\text{arcsec}(u)+C.
$$

The only difference is that instead of $u$ as the variable, we have $5x.$

So, let's substitute $u=5x.$ Differentiating, we get

$$
\frac{\text{d}u}{\text{d}x}=5\,⟹\,\text{d}x=\frac{1}{5}\text{d}u.
$$

Using the above, we can write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}\begin{aligned}\int \frac{1}{5|x|\sqrt{25{x}^{2}-1}}\,\text{d}x & =\int \frac{1}{|5x|\sqrt{(5x)^{2}-1}}\,\text{d}x \\  & =\int \frac{1}{|u|\sqrt{{u}^{2}-1}}\cdot (\frac{1}{5}\text{d}u) \\  & =\frac{1}{5}\int \frac{\text{d}u}{|u|\sqrt{{u}^{2}-1}} \\  & =\frac{1}{5}\text{arcsec }u+C \\  & =\frac{\text{arcsec}(5x)}{5}+C\end{aligned}\end{aligned}
$$

