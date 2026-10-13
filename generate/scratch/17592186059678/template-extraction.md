# Template extraction

Basis 1925. Exact individual prompt, solution, fields and every source choice are in source-cases.json and source-choice-mapping.json.

The generalized task is to differentiate the displayed y twice, first computing dy/dx, then d²y/dx². Each source keeps its own row sequence, field key and complete bank.

A common positive scalar k scales the entire function, every intermediate row and every bank value. Differentiation is linear: (k f)′ = k f′ and (k f)″ = k f″. k=1 replays the source byte-for-byte. k=2..6 is an explicit conservative extension with a factored scalar; independent coefficient changes are not inferred. Signed terms, fractional exponents, fixed exponents, logarithm arguments, trigonometric arguments and domains stay fixed. k=0, negative, fractional and >6 are rejected.

This bounded family has 36 easy and 12 moderate mathematical tasks before source/history exclusions. Seed and choice order do not define identity. Mathematical fingerprints use the expanded second derivative; linear and constant terms cannot create fake variants. Question UUIDs are deterministic for version, source profile and k; answer UUIDs belong to their field.

Fixed: instructional prose, Leibniz notation, Markdown, operator and row sequence, source field layout, bank size. Variable: common factor k, all derivative and choice values, partial-blank suffix. Conditional: k=1 preserves source notation; k>1 uses a factored scalar. The single worked solution for each instance is deterministic.

No source errors were found in the eight complete banks. q-342970 is a fragment, not an erroneous canonical answer: expected field = full second derivative + 6k/x⁴, while −6k/x⁴ is already supplied after the blank. Whole-derivative input must be rejected for this field.

Every radio distractor is retained as its complete observed expression pattern. The recipe is k times that mathematical object; transformations and complete values appear in source-choice-mapping.json. Specific error interpretation is unresolved where not established by sources. All options are reproduced exactly at k=1, and pairwise inequality and unique correctness are checked at every k. No mixed or pooled bank is used.

## q-10903 — easy

Source 17592186059986. Function: `5*x**4 + 4*x**2`. Domain: real x.

Field selection, :answer-field.type/radio, 5 values. Shared pattern: scale this complete source function and its two derivative phases by k.

Source solution:

Computing the first derivative, we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =\frac{\text{d}}{\text{d}x}(5{x}^{4}+4{x}^{2}) \\  & =4\cdot 5{x}^{3}+2\cdot 4x \\  & =20{x}^{3}+8x\,.\end{aligned}
$$

Computing the second derivative, we get

$$
\begin{aligned}\frac{{\text{d}}^{2}y}{\text{d}{x}^{2}} & =\frac{\text{d}}{\text{d}x}(20{x}^{3}+8x) \\  & =3\cdot 20{x}^{2}+8 \\  & =60{x}^{2}+8.\end{aligned}
$$

## q-342868 — moderate

Source 17592186233938. Function: `x**8/4 + x - 4/sqrt(x)`. Domain: x>0.

Field field-1, :answer-field.type/blank, 1 values. Shared pattern: scale this complete source function and its two derivative phases by k.

Source solution:

Computing the first derivative, we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =\frac{\text{d}}{\text{d}x}(\frac{{x}^{8}}{4}+x-\frac{4}{\sqrt{x}}) \\  & =\frac{\text{d}}{\text{d}x}(\frac{{x}^{8}}{4}+x-4{x}^{-1/2}) \\  & =8\cdot \frac{{x}^{7}}{4}+1-(-\frac{1}{2})\cdot 4{x}^{-3/2} \\  & =2{x}^{7}+1+2{x}^{-3/2}.\end{aligned}
$$

Computing the second derivative, we get

$$
\begin{aligned}\frac{{\text{d}}^{2}y}{\text{d}{x}^{2}} & =\frac{\text{d}}{\text{d}x}(2{x}^{7}+1+2{x}^{-3/2}) \\  & =7\cdot 2{x}^{6}+0+(-\frac{3}{2})\cdot 2{x}^{-5/2} \\  & =14{x}^{6}-3{x}^{-5/2} \\  & =14{x}^{6}-\frac{3}{\sqrt{{x}^{5}}}.\end{aligned}
$$

## q-104191 — moderate

Source 17592186240821. Function: `log(x) + 1/(6*x**2)`. Domain: x>0.

Field selection, :answer-field.type/radio, 5 values. Shared pattern: scale this complete source function and its two derivative phases by k.

Source solution:

Computing the first derivative, we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =\frac{\text{d}}{\text{d}x}(ln⁡x+\frac{1}{6{x}^{2}}) \\  & =\frac{\text{d}}{\text{d}x}(ln⁡x+\frac{1}{6}{x}^{-2}) \\  & =\frac{1}{x}+\frac{1}{6}\cdot (-2){x}^{-2-1} \\  & ={x}^{-1}-\frac{1}{3}{x}^{-3}.\end{aligned}
$$

Computing the second derivative, we get

$$
\begin{aligned}\frac{{\text{d}}^{2}y}{\text{d}{x}^{2}} & =\frac{\text{d}}{\text{d}x}({x}^{-1}-\frac{1}{3}{x}^{-3}) \\  & =(-1){x}^{-1-1}-\frac{1}{3}\cdot (-3){x}^{-3-1} \\  & =\frac{1}{{x}^{4}}-\frac{1}{{x}^{2}}.\end{aligned}
$$

## q-104192 — easy

Source 17592186240822. Function: `2*sin(x) + 4/sqrt(x)`. Domain: x>0.

Field selection, :answer-field.type/radio, 5 values. Shared pattern: scale this complete source function and its two derivative phases by k.

Source solution:

Computing the first derivative, we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =\frac{\text{d}}{\text{d}x}(\frac{4}{\sqrt{x}}+2sin⁡x) \\  & =\frac{\text{d}}{\text{d}x}(4{x}^{-1/2}+2sin⁡x) \\  & =4(-\frac{1}{2}){x}^{-1/2-1}+2cos⁡x \\  & =-2{x}^{-3/2}+2cos⁡x.\end{aligned}
$$

Computing the second derivative, we get

$$
\begin{aligned}\frac{{\text{d}}^{2}y}{\text{d}{x}^{2}} & =\frac{\text{d}}{\text{d}x}(-2{x}^{-3/2}+2cos⁡x) \\  & =-2(-\frac{3}{2}){x}^{-3/2-1}-2sin⁡x \\  & =\frac{3}{\sqrt{{x}^{5}}}-2sin⁡x.\end{aligned}
$$

## q-10884 — easy

Source 17592186244175. Function: `3*x**5 + 4*x**3 - 10*x**2`. Domain: real x.

Field selection, :answer-field.type/radio, 5 values. Shared pattern: scale this complete source function and its two derivative phases by k.

Source solution:

Computing the first derivative, we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =\frac{\text{d}}{\text{d}x}(3{x}^{5}+4{x}^{3}-10{x}^{2}) \\  & =5\cdot 3{x}^{4}+3\cdot 4{x}^{2}-2\cdot 10x \\  & =15{x}^{4}+12{x}^{2}-20x\,.\end{aligned}
$$

Computing the second derivative, we get

$$
\begin{aligned}\frac{{\text{d}}^{2}y}{\text{d}{x}^{2}} & =\frac{\text{d}}{\text{d}x}(15{x}^{4}+12{x}^{2}-20x) \\  & =15\cdot 4{x}^{3}+2\cdot 12x-20 \\  & =60{x}^{3}+24x-20.\end{aligned}
$$

## q-342877 — easy

Source 17592186317334. Function: `(6*x**3 + 2*x**2 - 8)/(2*x)`. Domain: real x.

Field field-1, :answer-field.type/blank, 1 values. Shared pattern: scale this complete source function and its two derivative phases by k.

Source solution:

Computing the first derivative, we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =\frac{\text{d}}{\text{d}x}(\frac{6{x}^{3}+2{x}^{2}-8}{2x}) \\  & =\frac{\text{d}}{\text{d}x}(3{x}^{2}+x-4{x}^{-1}) \\  & =6x+1+(-1)(-4{x}^{-2}) \\  & =6x+1+4{x}^{-2}.\end{aligned}
$$

Computing the second derivative, we get

$$
\begin{aligned}\frac{{\text{d}}^{2}y}{\text{d}{x}^{2}} & =\frac{\text{d}}{\text{d}x}(6x+1+4{x}^{-2}) \\  & =6+0+(-2)(4{x}^{-3}) \\  & =6-\frac{8}{{x}^{3}}.\end{aligned}
$$

## q-342966 — easy

Source 17592186317347. Function: `6*sqrt(x) + 5*cos(x)`. Domain: x>0.

Field field-1, :answer-field.type/blank, 1 values. Shared pattern: scale this complete source function and its two derivative phases by k.

Source solution:

Computing the first derivative, we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =\frac{\text{d}}{\text{d}x}(6\sqrt{x}+5\operatorname{cos}⁡x) \\  & =\frac{\text{d}}{\text{d}x}(6{x}^{1/2}+5\operatorname{cos}⁡x) \\  & =(\frac{1}{2})\cdot 6{x}^{-1/2}+5(-\operatorname{sin}⁡x) \\  & =3{x}^{-1/2}-5\operatorname{sin}⁡x.\end{aligned}
$$

Computing the second derivative, we get

$$
\begin{aligned}\frac{{\text{d}}^{2}y}{\text{d}{x}^{2}} & =\frac{\text{d}}{\text{d}x}(3{x}^{-1/2}-5\operatorname{sin}⁡x) \\  & =(-\frac{1}{2})\cdot 3{x}^{-3/2}-5\operatorname{cos}⁡x \\  & =-\frac{3}{2\sqrt{{x}^{3}}}-5\operatorname{cos}⁡x.\end{aligned}
$$

## q-342970 — easy

Source 17592186317348. Function: `x**5 + 3*sin(x) - 1/x**2`. Domain: x!=0.

Field field-1, :answer-field.type/blank, 1 values. Shared pattern: scale this complete source function and its two derivative phases by k.

Source solution:

Computing the first derivative, we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =\frac{\text{d}}{\text{d}x}({x}^{5}+3\operatorname{sin}⁡x-\frac{1}{{x}^{2}}) \\  & =\frac{\text{d}}{\text{d}x}({x}^{5}+3\operatorname{sin}⁡x-{x}^{-2}) \\  & =5{x}^{4}+3\operatorname{cos}⁡x-(-2){x}^{-3} \\  & =5{x}^{4}+3\operatorname{cos}⁡x+2{x}^{-3}.\end{aligned}
$$

Computing the second derivative, we get

$$
\begin{aligned}\frac{{\text{d}}^{2}y}{\text{d}{x}^{2}} & =\frac{\text{d}}{\text{d}x}(5{x}^{4}+3\operatorname{cos}⁡x+2{x}^{-3}) \\  & =4\cdot 5{x}^{3}+3(-\operatorname{sin}⁡x)+(-3)\cdot 2{x}^{-4} \\  & =20{x}^{3}-3\operatorname{sin}⁡x-\frac{6}{{x}^{4}}.\end{aligned}
$$
