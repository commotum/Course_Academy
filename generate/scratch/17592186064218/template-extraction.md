# Template extraction

Shared pattern: recognize the inverse-sine integral, normalize the quadratic radicand if its constant is not one, set u=kx, convert dx, integrate, and back-substitute. The response is one full antiderivative family including +C. Each source bank remains an indivisible profile; numerical slot transforms retain complete compound mistakes without adding inferred error feedback.

General forms: easy a/sqrt(1-b*x^2), with k=sqrt(b), primitive (a/k)asin(k*x)+C; moderate a/sqrt(n^2-x^2), with k=1/n, primitive a*asin(x/n)+C. All radicands must be strictly positive. Slopes are positive; negative coefficients/slopes are unobserved and deferred.

Numeric tokens are simultaneous slots. Exponents of x and u are fixed. Every prose sentence, display block, and solution stage comes from its observed template. Parameter relationships and bounds are source-related policy extensions, not independent random coefficient pools. No banks are mixed.

Source error q-49535: the first integral in the final aligned display has numerator 1 although its prompt and all following steps require 2. Exact replay retains the error; generated completion changes only that numerator. Numerically repeated 2 has incompatible variable roles, so this profile is restricted to its original t=4; it supplies no fresh variants.

Ambiguous q-2506 arcsec superscript: retain full literal expression and unresolved interpretation in evidence. This profile is excluded from generated practice. q-4334 arcsec and q-114032 sqrt(x) are complete observed alternative objects; their author intent is unresolved and no psychological recipe is invented.

The source question and choices, corresponding field, correct designation, solution, parameters, every numeric slot recipe, and transformed whole-value pattern are in components.json. Original choice UUIDs are evidence only; generated answers belong to their generated fields.

## q-2505

$\int \frac{1}{\sqrt{1-4{x}^{2}}}\,\text{d}x=$

Observed t=2; slots {"2": "t", "4": "t^2"}; bounded t=(2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12).

- \frac{\operatorname{arcsin}⁡(2x)}{2}+C → \frac{\operatorname{arcsin}⁡(tx)}{t}+C (correct)

- 2\operatorname{arcsin}⁡(2x)+C → t\operatorname{arcsin}⁡(tx)+C (observed alternative)

- \frac{\operatorname{arccos}⁡(4x)}{4}+C → \frac{\operatorname{arccos}⁡(t^2x)}{t^2}+C (observed alternative)

- \frac{\operatorname{arccos}⁡(2x)}{2}+C → \frac{\operatorname{arccos}⁡(tx)}{t}+C (observed alternative)

- \frac{\operatorname{arcsin}⁡(4x)}{4}+C → \frac{\operatorname{arcsin}⁡(t^2x)}{t^2}+C (observed alternative)

## q-2506

$\int \frac{1}{\sqrt{1-9{x}^{2}}}\,\text{d}x=$

Observed t=3; slots {"3": "t", "9": "t^2"}; bounded t=(2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12).

- \frac{\operatorname{arcsin}⁡(9x)}{9}+C → \frac{\operatorname{arcsin}⁡(t^2x)}{t^2}+C (observed alternative)

- \frac{\operatorname{arctan}⁡(3x)}{3}+C → \frac{\operatorname{arctan}⁡(tx)}{t}+C (observed alternative)

- \frac{\operatorname{arcsin}⁡(3x)}{3}+C → \frac{\operatorname{arcsin}⁡(tx)}{t}+C (correct)

- \frac{\text{arcsec}{(9x)}^{2}}{9}+C → \frac{\text{arcsec}{(t^2x)}^{2}}{t^2}+C (observed alternative)

- 3\operatorname{arcsin}⁡(3x)+C → t\operatorname{arcsin}⁡(tx)+C (observed alternative)

## q-49535

$\int \frac{2}{\sqrt{1-16{x}^{2}}}\,\text{d}x=$

Observed t=4; slots {"2": "2", "4": "4", "16": "16"}; bounded t=(4,).

- \frac{\operatorname{arcsin}⁡(4x)}{4}+C → \frac{\operatorname{arcsin}⁡(4x)}{4}+C (observed alternative)

- \frac{\operatorname{arcsin}⁡(2x)}{4}+C → \frac{\operatorname{arcsin}⁡(2x)}{4}+C (observed alternative)

- 2\operatorname{arcsin}⁡(4x)+C → 2\operatorname{arcsin}⁡(4x)+C (observed alternative)

- \frac{\operatorname{arctan}⁡(4x)}{4}+C → \frac{\operatorname{arctan}⁡(4x)}{4}+C (observed alternative)

- \frac{\operatorname{arcsin}⁡(4x)}{2}+C → \frac{\operatorname{arcsin}⁡(4x)}{2}+C (correct)

## q-114022

Calculate $\int \frac{5}{\sqrt{1-25{x}^{2}}}\,\text{d}x.$

Observed t=5; slots {"5": "t", "25": "t^2"}; bounded t=(2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12).

- \frac{\operatorname{arcsin}⁡(5x)}{5}+C → \frac{\operatorname{arcsin}⁡(tx)}{t}+C (observed alternative)

- \operatorname{arcsin}⁡(5x)+C → \operatorname{arcsin}⁡(tx)+C (correct)

- 5\operatorname{arcsin}⁡(5x)+C → t\operatorname{arcsin}⁡(tx)+C (observed alternative)

- \operatorname{arcsin}⁡(\frac{x}{5})+C → \operatorname{arcsin}⁡(\frac{x}{t})+C (observed alternative)

- \frac{\operatorname{arcsin}⁡(x)}{5}+C → \frac{\operatorname{arcsin}⁡(x)}{t}+C (observed alternative)

## q-114023

Calculate $\int \frac{1}{6\sqrt{1-36{x}^{2}}}\,\text{d}x.$

Observed t=6; slots {"6": "t", "36": "t^2"}; bounded t=(2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12).

- \frac{1}{6}\operatorname{arcsin}⁡(x)+C → \frac{1}{t}\operatorname{arcsin}⁡(x)+C (observed alternative)

- 6\operatorname{arcsin}⁡(6x)+C → t\operatorname{arcsin}⁡(tx)+C (observed alternative)

- \frac{1}{36}\operatorname{arcsin}⁡(6x)+C → \frac{1}{t^2}\operatorname{arcsin}⁡(tx)+C (correct)

- 36\operatorname{arcsin}⁡(6x)+C → t^2\operatorname{arcsin}⁡(tx)+C (observed alternative)

- \frac{1}{6}\operatorname{arcsin}⁡(6x)+C → \frac{1}{t}\operatorname{arcsin}⁡(tx)+C (observed alternative)

## q-114025

Calculate $\int \frac{1}{9\sqrt{1-81{x}^{2}}}\,\text{d}x.$

Observed t=9; slots {"9": "t", "81": "t^2"}; bounded t=(2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12).

- \frac{1}{81}\operatorname{arcsin}⁡(9x)+C → \frac{1}{t^2}\operatorname{arcsin}⁡(tx)+C (correct)

- \frac{1}{9}\operatorname{arcsin}⁡(x)+C → \frac{1}{t}\operatorname{arcsin}⁡(x)+C (observed alternative)

- \frac{1}{9}\operatorname{arcsin}⁡(9x)+C → \frac{1}{t}\operatorname{arcsin}⁡(tx)+C (observed alternative)

- 81\operatorname{arcsin}⁡(9x)+C → t^2\operatorname{arcsin}⁡(tx)+C (observed alternative)

- 9\operatorname{arcsin}⁡(9x)+C → t\operatorname{arcsin}⁡(tx)+C (observed alternative)

## q-114024

Calculate $\int \frac{4}{\sqrt{1-2{x}^{2}}}\,\text{d}x.$

Observed t=2; slots {"2": "t", "4": "t^2"}; bounded t=(2, 3, 5, 6, 7, 8, 10, 11, 12).

- \sqrt{2}\operatorname{arcsin}⁡(x)+C → \sqrt{t}\operatorname{arcsin}⁡(x)+C (observed alternative)

- 2\operatorname{arcsin}⁡(\sqrt{2}x)+C → t\operatorname{arcsin}⁡(\sqrt{t}x)+C (observed alternative)

- 2\sqrt{2}\operatorname{arcsin}⁡(2x)+C → t\sqrt{t}\operatorname{arcsin}⁡(tx)+C (observed alternative)

- \sqrt{2}\operatorname{arcsin}⁡(\sqrt{2}x)+C → \sqrt{t}\operatorname{arcsin}⁡(\sqrt{t}x)+C (observed alternative)

- 2\sqrt{2}\operatorname{arcsin}⁡(\sqrt{2}x)+C → t\sqrt{t}\operatorname{arcsin}⁡(\sqrt{t}x)+C (correct)

## q-114027

Calculate $\int \frac{8}{\sqrt{1-3{x}^{2}}}\,\text{d}x.$

Observed t=3; slots {"3": "t"}; bounded t=(2, 3, 5, 6, 7, 8, 10, 11, 12).

- \frac{8\sqrt{3}}{3}\operatorname{arcsin}⁡(\sqrt{3}x)+C → \frac{8\sqrt{t}}{t}\operatorname{arcsin}⁡(\sqrt{t}x)+C (correct)

- \frac{\sqrt{3}}{8}\operatorname{arcsin}⁡(\sqrt{3}x)+C → \frac{\sqrt{t}}{8}\operatorname{arcsin}⁡(\sqrt{t}x)+C (observed alternative)

- \frac{8}{3}\operatorname{arcsin}⁡(3x)+C → \frac{8}{t}\operatorname{arcsin}⁡(tx)+C (observed alternative)

- \frac{8}{3}\operatorname{arcsin}⁡(\sqrt{3}x)+C → \frac{8}{t}\operatorname{arcsin}⁡(\sqrt{t}x)+C (observed alternative)

- \frac{\sqrt{3}}{8}\operatorname{arcsin}⁡(3x)+C → \frac{\sqrt{t}}{8}\operatorname{arcsin}⁡(tx)+C (observed alternative)

## q-114032

Calculate $\int \frac{3}{\sqrt{1-3{x}^{2}}}\,\text{d}x.$

Observed t=3; slots {"3": "t"}; bounded t=(2, 3, 5, 6, 7, 8, 10, 11, 12).

- 3\operatorname{arcsin}⁡(\sqrt{3}x)+C → t\operatorname{arcsin}⁡(\sqrt{t}x)+C (observed alternative)

- \sqrt{3}\operatorname{arcsin}⁡(\sqrt{3}x)+C → \sqrt{t}\operatorname{arcsin}⁡(\sqrt{t}x)+C (correct)

- 3\sqrt{3}\operatorname{arcsin}⁡(\sqrt{3}x)+C → t\sqrt{t}\operatorname{arcsin}⁡(\sqrt{t}x)+C (observed alternative)

- \sqrt{3}\operatorname{arcsin}⁡(\sqrt{x})+C → \sqrt{t}\operatorname{arcsin}⁡(\sqrt{x})+C (observed alternative)

- \frac{\sqrt{3}}{3}\operatorname{arcsin}⁡(\sqrt{3}x)+C → \frac{\sqrt{t}}{t}\operatorname{arcsin}⁡(\sqrt{t}x)+C (observed alternative)

## q-2503

$\int \frac{1}{\sqrt{9-{x}^{2}}}\text{d}x=$

Observed t=3; slots {"3": "t", "9": "t^2"}; bounded t=(2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12).

- \frac{1}{3}\,\operatorname{arccos}⁡(\frac{x}{3})+C → \frac{1}{t}\,\operatorname{arccos}⁡(\frac{x}{t})+C (observed alternative)

- \operatorname{arcsin}⁡(\frac{x}{3})+C → \operatorname{arcsin}⁡(\frac{x}{t})+C (correct)

- \operatorname{arccos}⁡({x}^{2})+C → \operatorname{arccos}⁡({x}^{2})+C (observed alternative)

- 9\operatorname{arcsin}⁡({x}^{2})+C → t^2\operatorname{arcsin}⁡({x}^{2})+C (observed alternative)

- 9\operatorname{arcsin}⁡(\frac{{x}^{2}}{9})+C → t^2\operatorname{arcsin}⁡(\frac{{x}^{2}}{t^2})+C (observed alternative)

## q-4334

$\int \frac{1}{\sqrt{36-{x}^{2}}}\text{d}x\,=$

Observed t=6; slots {"2": "t/3", "3": "t/2", "6": "t", "36": "t^2"}; bounded t=(6, 12, 18, 24).

- 36\operatorname{arcsin}⁡(\frac{x}{6})+C → t^2\operatorname{arcsin}⁡(\frac{x}{t})+C (observed alternative)

- \text{arcsec}(\frac{x}{2})+C → \text{arcsec}(\frac{x}{t/3})+C (observed alternative)

- \operatorname{arcsin}⁡(\frac{x}{6})+C → \operatorname{arcsin}⁡(\frac{x}{t})+C (correct)

- 3\,\text{arcsin}(\frac{x}{6})+C → t/2\,\text{arcsin}(\frac{x}{t})+C (observed alternative)

- \operatorname{arcsin}⁡x+C → \operatorname{arcsin}⁡x+C (observed alternative)

## q-49547

$\int \frac{3}{\sqrt{49-{x}^{2}}}\,\text{d}x=$

Observed t=7; slots {"7": "t", "49": "t^2"}; bounded t=(2, 3, 4, 5, 6, 7, 8, 10, 11, 12).

- 3\operatorname{arctan}⁡(7x)+C → 3\operatorname{arctan}⁡(tx)+C (observed alternative)

- 3\operatorname{arctan}⁡(\frac{x}{7})+C → 3\operatorname{arctan}⁡(\frac{x}{t})+C (observed alternative)

- \frac{3\operatorname{arcsin}⁡(\frac{x}{7})}{7}+C → \frac{3\operatorname{arcsin}⁡(\frac{x}{t})}{t}+C (observed alternative)

- 3\operatorname{arcsin}⁡(\frac{x}{7})+C → 3\operatorname{arcsin}⁡(\frac{x}{t})+C (correct)

- \frac{\operatorname{arcsin}⁡(\frac{x}{7})}{3}+C → \frac{\operatorname{arcsin}⁡(\frac{x}{t})}{3}+C (observed alternative)

## q-114030

Calculate $\int \frac{2}{\sqrt{25-{x}^{2}}}\,\text{d}x.$

Observed t=5; slots {"5": "t", "25": "t^2"}; bounded t=(2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12).

- 2\operatorname{arcsin}⁡(5x)+C → 2\operatorname{arcsin}⁡(tx)+C (observed alternative)

- \operatorname{arcsin}⁡(\frac{x}{5})+C → \operatorname{arcsin}⁡(\frac{x}{t})+C (observed alternative)

- \frac{2}{25}\operatorname{arcsin}⁡(\frac{x}{5})+C → \frac{2}{t^2}\operatorname{arcsin}⁡(\frac{x}{t})+C (observed alternative)

- 25\operatorname{arcsin}⁡(5x)+C → t^2\operatorname{arcsin}⁡(tx)+C (observed alternative)

- 2\operatorname{arcsin}⁡(\frac{x}{5})+C → 2\operatorname{arcsin}⁡(\frac{x}{t})+C (correct)

## q-73712

$\int \frac{8}{3\sqrt{4-{x}^{2}}}\text{d}x=$

Observed t=2; slots {"2": "t", "4": "t^2", "8": "t^3"}; bounded t=(2, 3, 4).

- \frac{3}{4}\operatorname{arcsin}⁡(2x)+C → \frac{3}{t^2}\operatorname{arcsin}⁡(tx)+C (observed alternative)

- \frac{4}{3}\operatorname{arcsin}⁡(2x)+C → \frac{t^2}{3}\operatorname{arcsin}⁡(tx)+C (observed alternative)

- \frac{3}{4}\operatorname{arcsin}⁡(\frac{x}{2})+C → \frac{3}{t^2}\operatorname{arcsin}⁡(\frac{x}{t})+C (observed alternative)

- \frac{4}{3}\operatorname{arcsin}⁡(\frac{x}{2})+C → \frac{t^2}{3}\operatorname{arcsin}⁡(\frac{x}{t})+C (observed alternative)

- \frac{8}{3}\operatorname{arcsin}⁡(\frac{x}{2})+C → \frac{t^3}{3}\operatorname{arcsin}⁡(\frac{x}{t})+C (correct)
