# Template extraction

Each bank is field-owned. Original prompt, solution, choices and correct designations remain in source.json. Variable templates use only positive integer coefficients 1..24; negative coefficients, alternate angles, and other changes are outside v1. These are narrower explicit policies, not mathematical impossibility claims. Five other complete templates retain a finite limit of one observed task. No shuffled or seed-only question is new.

## q-1886

Specific source

Find the slope of $y=f(x)$ at $x=\sqrt{3}$ if $f(x)=11\operatorname{cos}⁡x-\operatorname{sec}⁡x+\frac{1}{x}.$

Fixed solution sequence

First, we calculate the derivative using the sum rule:

$$
\begin{aligned}\begin{aligned}{f}^{′}(x) & =\frac{\text{d}}{\text{d}x}(11\operatorname{cos}⁡x-\operatorname{sec}⁡x+\frac{1}{x}) \\  & =\frac{\text{d}}{\text{d}x}(11\operatorname{cos}⁡x-\operatorname{sec}⁡x+{x}^{-1}) \\  & =11(-\operatorname{sin}⁡x)-\operatorname{sec}⁡x\operatorname{tan}⁡x-\frac{1}{{x}^{2}} \\  & =-11\operatorname{sin}⁡x-\operatorname{sec}⁡x\operatorname{tan}⁡x-\frac{1}{{x}^{2}}\end{aligned}\end{aligned}
$$

Then, we substitute $x=\sqrt{3}$ in the derivative and get

$$
\begin{aligned}{f}^{′}(\sqrt{3}) & =-11\operatorname{sin}⁡(\sqrt{3})-\operatorname{sec}⁡(\sqrt{3})\operatorname{tan}⁡(\sqrt{3})-\frac{1}{(\sqrt{3})^{2}} \\  & =-11\operatorname{sin}⁡(\sqrt{3})-\operatorname{sec}⁡(\sqrt{3})\operatorname{tan}⁡(\sqrt{3})-\frac{1}{3}.\end{aligned}
$$

General pattern and response

n cos(x) - sec(x) + 1/x at sqrt(3); sum and power rules, then evaluation. Correct = -n sin(sqrt(3)) - sec(sqrt(3))tan(sqrt(3)) - 1/3. Domain excludes x=0 and cos(x)=0. Field type/key and answer shape remain exact.

Observed parameter: 11. Proposed domain: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24].

Complete observed profile q-1886-observed-bank. Each original choice maps exactly once, ignoring order:

- Answer 2092ed7b-78ba-5b08-8ed9-5a3ae1c22f13; field selection; distractor; value `$-\operatorname{sin}⁡(\sqrt{3})-\operatorname{csc}⁡(\sqrt{3})\operatorname{cot}⁡(\sqrt{3})-\frac{1}{3}$`; recipe: Replace every coefficient 11 by n; coefficient 1 in the first distractor remains fixed. Exact complete expression at n=11.

- Answer 61025999-7cbd-5360-838b-eda24fb2a51c; field selection; correct; value `$-11\operatorname{sin}⁡(\sqrt{3})-\operatorname{sec}⁡(\sqrt{3})\operatorname{tan}⁡(\sqrt{3})-\frac{1}{3}$`; recipe: Replace every coefficient 11 by n; coefficient 1 in the first distractor remains fixed. Exact complete expression at n=11.

- Answer a9b589e9-9125-5e9a-b153-823caacb3c8a; field selection; distractor; value `$-11\operatorname{sin}⁡(\sqrt{3})+\operatorname{sec}⁡(\sqrt{3})\operatorname{tan}⁡(\sqrt{3})+\frac{1}{3}$`; recipe: Replace every coefficient 11 by n; coefficient 1 in the first distractor remains fixed. Exact complete expression at n=11.

- Answer b5151810-8b1c-5b10-a7e3-87a15f4d9958; field selection; distractor; value `$11\operatorname{sin}⁡(\sqrt{3})-\operatorname{sec}⁡(\sqrt{3})\operatorname{tan}⁡(\sqrt{3})-\frac{1}{3}$`; recipe: Replace every coefficient 11 by n; coefficient 1 in the first distractor remains fixed. Exact complete expression at n=11.

- Answer daba25ff-6035-5619-8ac0-07d5eb9bd01a; field selection; distractor; value `$-11\operatorname{sin}⁡(\sqrt{3})-\operatorname{csc}⁡(\sqrt{3})\operatorname{cot}⁡(\sqrt{3})-1$`; recipe: Replace every coefficient 11 by n; coefficient 1 in the first distractor remains fixed. Exact complete expression at n=11.

Prompt and solution recipe: Apply the same coefficient replacement to original Markdown, including every intermediate and final calculated coefficient. All shared instructional sentences remain exact. New UUIDs derive from task content and field-owned answer values, never seed or order. No plot generation is needed.

## q-1905

Specific source

Find the slope of $y=f(x)$ at $x=\frac{\pi }{4}$ if $f(x)=2x-\sqrt{2}sec⁡x.$

Fixed solution sequence

First, we calculate the derivative using the sum rule:

$$
\begin{aligned}\begin{aligned}{f}^{′}(x) & =\frac{\text{d}}{\text{d}x}(2x-\sqrt{2}sec⁡x) \\  & =2-\sqrt{2}sec⁡xtan⁡x\end{aligned}\end{aligned}
$$

Then, we substitute $x=\frac{\pi }{4}$ in the derivative and get

$$
\begin{aligned}{f}^{′}(\frac{\pi }{4}) & =2-\sqrt{2}sec⁡(\frac{\pi }{4})tan⁡(\frac{\pi }{4}) \\  & =2-\sqrt{2}(\sqrt{2})(1) \\  & =2-2 \\  & =0.\end{aligned}
$$

General pattern and response

2x - sqrt(2) sec(x) at pi/4; sum rule, evaluate to 0. Domain cos(x) != 0. Field type/key and answer shape remain exact.

Observed parameter: 1. Proposed domain: [1].

Complete observed profile q-1905-observed-bank. Each original choice maps exactly once, ignoring order:

- Answer 83d05e6b-994a-5931-90fb-0244e740694f; field selection; distractor; value `$4$`; recipe: Fixed observed expression (source-only template; mistake interpretation unresolved)

- Answer b9702af1-9a01-5ff4-990f-2b8e8b2bf574; field selection; distractor; value `$-6\sqrt{2}+2$`; recipe: Fixed observed expression (source-only template; mistake interpretation unresolved)

- Answer c916f7e2-e71d-5044-a1e6-83799fa5fc80; field selection; distractor; value `$3\sqrt{2}+2$`; recipe: Fixed observed expression (source-only template; mistake interpretation unresolved)

- Answer e5017828-3ef7-5857-8b3a-d98ae9e0243d; field selection; correct; value `$0$`; recipe: Fixed observed expression (source-only template; mistake interpretation unresolved)

- Answer e79e42be-aa4f-50c1-a571-518a34f7f2ac; field selection; distractor; value `$-3\sqrt{2}+2$`; recipe: Fixed observed expression (source-only template; mistake interpretation unresolved)

Prompt and solution recipe: Retain original prompt and entire fixed worked solution exactly. No inferred distractor recipes. New UUIDs derive from task content and field-owned answer values, never seed or order. No plot generation is needed.

## q-104437

Specific source

Find the slope of $y=f(x)$ at $x=\frac{\pi }{4}$ if $f(x)=x\operatorname{cot}x.$

Fixed solution sequence

First, we take the derivative using the product rule:

 

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =\frac{\text{d}}{\text{d}x}(x\operatorname{cot}x) \\  & =\operatorname{cot}x+x(-{csc}^{2}x) \\  & =\operatorname{cot}x-x{csc}^{2}x\end{aligned}
$$

Then, we substitute $x=\frac{\pi }{4}$ in the derivative and get

 

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x}{|}_{\pi /4} & =\operatorname{cot}(\frac{\pi }{4})-\frac{\pi }{4}{csc}^{2}(\frac{\pi }{4}) \\  & =1-\frac{\pi }{4}\cdot (\sqrt{2})^{2} \\  & =1-\frac{\pi }{2}.\end{aligned}
$$

Product rule followed by evaluation at pi/4; source answer fields absent. No response structure is guessed or generated.

## q-340642

Specific source

Find the slope $m$ of $y=g(x)$ at $x=\frac{\pi }{2}$ if $g(x)=\operatorname{csc}x\operatorname{cot}x.$

$m=$
{{field-1}}

Fixed solution sequence

First, we calculate the derivative using the product rule and sum rule:

$$
\begin{aligned}{g}^{'}(x) & =\frac{\text{d}}{\text{d}x}(\operatorname{csc}x\operatorname{cot}x) \\  & =(-\operatorname{csc}x\operatorname{cot}x)(\operatorname{cot}x)+(\operatorname{csc}x)(-{csc}^{2}x) \\  & =-\operatorname{csc}x({cot}^{2}x+{csc}^{2}x)\end{aligned}
$$

Now, we substitute $x=\frac{\pi }{2}$ and evaluate the slope $m:$

$$
\begin{aligned}m={g}^{'}(\frac{\pi }{2}) & =-\operatorname{csc}(\frac{\pi }{2})[{cot}^{2}(\frac{\pi }{2})+{csc}^{2}(\frac{\pi }{2})] \\  & =-1\cdot ({0}^{2}+{1}^{2}) \\  & =-1\end{aligned}
$$

General pattern and response

csc(x)cot(x) at pi/2; product rule then evaluation to -1. Domain sin(x) != 0. Field type/key and answer shape remain exact.

Observed parameter: 1. Proposed domain: [1].

Complete observed profile q-340642-observed-bank. Each original choice maps exactly once, ignoring order:

- Answer 03e9d963-612a-5223-a2bb-a0380a286d94; field field-1; correct; value `$-1$`; recipe: Fixed observed expression (source-only template; mistake interpretation unresolved)

Prompt and solution recipe: Retain original prompt and entire fixed worked solution exactly. No inferred distractor recipes. New UUIDs derive from task content and field-owned answer values, never seed or order. No plot generation is needed.

## q-104442

Specific source

Find the slope of $y=f(x)$ at $x=\frac{\pi }{3}$ if $f(x)=\frac{sec⁡x}{\sqrt{3}}+\frac{3{x}^{2}}{\pi }.$

Fixed solution sequence

First, we take the derivative of each term and then add them, as follows:

 

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =\frac{\text{d}}{\text{d}x}(\frac{sec⁡x}{\sqrt{3}}+\frac{3{x}^{2}}{\pi }) \\  & =\frac{sec⁡xtan⁡x}{\sqrt{3}}+\frac{6x}{\pi }\end{aligned}
$$

Then, we substitute $x=\frac{\pi }{3}$ in the derivative and get

 

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x}{|}_{\pi /3} & =\frac{1}{\sqrt{3}}\cdot sec⁡(\frac{\pi }{3})\cdot tan⁡(\frac{\pi }{3})+\frac{6}{\pi }\cdot \frac{\pi }{3} \\  & =\frac{1}{\sqrt{3}}\cdot 2\cdot \sqrt{3}+2 \\  & =2+2 \\  & =4.\end{aligned}
$$

General pattern and response

sec(x)/sqrt(3) + 3x^2/pi at pi/3; termwise differentiation then evaluation to 4. Domain cos(x) != 0. Field type/key and answer shape remain exact.

Observed parameter: 1. Proposed domain: [1].

Complete observed profile q-104442-observed-bank. Each original choice maps exactly once, ignoring order:

- Answer 18f7e706-6667-560b-bd84-79164bd2ed56; field selection; distractor; value `$0$`; recipe: Fixed observed expression (source-only template; mistake interpretation unresolved)

- Answer 485520fe-f7db-5462-90b3-8b9dc00969d6; field selection; distractor; value `$-4$`; recipe: Fixed observed expression (source-only template; mistake interpretation unresolved)

- Answer 4ebd5941-c9bf-5355-a88c-6736db31de31; field selection; distractor; value `$2$`; recipe: Fixed observed expression (source-only template; mistake interpretation unresolved)

- Answer 746fc071-c68b-5025-87be-eb8a9b327237; field selection; correct; value `$4$`; recipe: Fixed observed expression (source-only template; mistake interpretation unresolved)

- Answer fe35b390-cf3c-53c9-b56a-b8e3bb467faa; field selection; distractor; value `$-2$`; recipe: Fixed observed expression (source-only template; mistake interpretation unresolved)

Prompt and solution recipe: Retain original prompt and entire fixed worked solution exactly. No inferred distractor recipes. New UUIDs derive from task content and field-owned answer values, never seed or order. No plot generation is needed.

## q-1904

Specific source

Find the slope of $y=f(x)$ at $x=\frac{\pi }{6}$ if $f(x)=-{x}^{2}+5csc⁡x.$

Fixed solution sequence

First, we calculate the derivative using the sum rule:

$$
\begin{aligned}{f}^{′}(x) & =\frac{d}{dx}(-{x}^{2}+5csc⁡x) \\  & =2\cdot (-x)+5(-csc⁡xcot⁡x) \\  & =-2x-5csc⁡xcot⁡x\end{aligned}
$$

Then, we substitute $x=\frac{\pi }{6}$ into the derivative and get:

$$
\begin{aligned}{f}^{′}(\frac{\pi }{6}) & =-2(\frac{\pi }{6})-5csc⁡(\frac{\pi }{6})cot⁡(\frac{\pi }{6}) \\  & =-\frac{\pi }{3}-5\cdot 2\cdot \sqrt{3} \\  & =-\frac{\pi }{3}-10\sqrt{3}\end{aligned}
$$

General pattern and response

-x^2 + n csc(x) at pi/6; sum rule then evaluation. Correct = -pi/3 - 2n sqrt(3). Domain sin(x) != 0. Field type/key and answer shape remain exact.

Observed parameter: 5. Proposed domain: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24].

Complete observed profile q-1904-observed-bank. Each original choice maps exactly once, ignoring order:

- Answer 04d15acc-1672-5ec4-bb78-f3474884b897; field selection; distractor; value `$-\frac{\pi }{3}-5\sqrt{3}$`; recipe: Replace coefficient 5 by n and coefficient 10 by 2n; polynomial pi terms stay fixed. Exact complete expression at n=5.

- Answer 48fabaf5-be8a-589c-8cf0-074c455a9240; field selection; distractor; value `$\frac{\pi }{3}-10\sqrt{3}$`; recipe: Replace coefficient 5 by n and coefficient 10 by 2n; polynomial pi terms stay fixed. Exact complete expression at n=5.

- Answer 63f73e2e-4004-5fc8-9825-f8337f6c2b07; field selection; distractor; value `$-\frac{\pi }{6}-10\sqrt{3}$`; recipe: Replace coefficient 5 by n and coefficient 10 by 2n; polynomial pi terms stay fixed. Exact complete expression at n=5.

- Answer 766bb2aa-4af5-5e09-aed3-a777505c1a5c; field selection; distractor; value `$\frac{\pi }{3}+10\sqrt{3}$`; recipe: Replace coefficient 5 by n and coefficient 10 by 2n; polynomial pi terms stay fixed. Exact complete expression at n=5.

- Answer e40e7c86-1ed2-5d5e-9940-61e65ceaec5c; field selection; correct; value `$-\frac{\pi }{3}-10\sqrt{3}$`; recipe: Replace coefficient 5 by n and coefficient 10 by 2n; polynomial pi terms stay fixed. Exact complete expression at n=5.

Prompt and solution recipe: Apply the same coefficient replacement to original Markdown, including every intermediate and final calculated coefficient. All shared instructional sentences remain exact. New UUIDs derive from task content and field-owned answer values, never seed or order. No plot generation is needed.

## q-340630

Specific source

Find the slope $m$ of $y=h(x)$ at $x=\pi $ if $h(x)={e}^{x}+3\operatorname{sec}⁡x.$

$m=$
{{field-1}}

Fixed solution sequence

First, we calculate the derivative:

$$
\begin{aligned}{h}^{′}(x) & =\frac{\text{d}}{\text{d}x}({e}^{x}+3\operatorname{sec}⁡x) \\  & ={e}^{x}+3\operatorname{sec}⁡x\operatorname{tan}⁡x\end{aligned}
$$

Now, we substitute $x=\pi $ and evaluate the slope $m:$

$$
\begin{aligned}m={h}^{′}(\pi ) & ={e}^{\pi }+3\operatorname{sec}⁡(\pi )\operatorname{tan}⁡(\pi ) \\  & ={e}^{\pi }+3\cdot (-1)\cdot 0 \\  & ={e}^{\pi }\end{aligned}
$$

General pattern and response

exp(x) + 3sec(x) at pi; differentiate then evaluate; sec derivative term vanishes, correct exp(pi). Domain cos(x) != 0. Field type/key and answer shape remain exact.

Observed parameter: 1. Proposed domain: [1].

Complete observed profile q-340630-observed-bank. Each original choice maps exactly once, ignoring order:

- Answer 4212e2b2-4307-5ba7-9307-27d580b7ec58; field field-1; correct; value `${e}^{\pi }$`; recipe: Fixed observed expression (source-only template; mistake interpretation unresolved)

Prompt and solution recipe: Retain original prompt and entire fixed worked solution exactly. No inferred distractor recipes. New UUIDs derive from task content and field-owned answer values, never seed or order. No plot generation is needed.

## q-340660

Specific source

Find the slope of $y=f(x)$ at $x=0$ if $f(x)=\frac{4x}{sec⁡x}.$

$m=$
{{field-1}}

Fixed solution sequence

First, we calculate the derivative using the quotient rule:

$$
\begin{aligned}\begin{aligned}{f}^{′}(x) & =\frac{\text{d}}{\text{d}x}(\frac{4x}{sec⁡x}) \\  & =\frac{\frac{\text{d}}{\text{d}x}(4x)\cdot sec⁡x-4x\cdot \frac{\text{d}}{\text{d}x}(sec⁡x)}{{sec}^{2}⁡x} \\  & =\frac{4sec⁡x-4x\cdot sec⁡xtan⁡x}{{sec}^{2}⁡x} \\  & =\frac{4sec⁡x(1-xtan⁡x)}{{sec}^{2}⁡x} \\  & =\frac{4(1-xtan⁡x)}{sec⁡x}\end{aligned}\end{aligned}
$$

Then, we substitute $x=0$ in the derivative and get

$$
\begin{aligned}\begin{aligned}{f}^{′}(0) & =\frac{4(1-0\cdot tan⁡0)}{sec⁡0} \\  & =\frac{4(1-0)}{1} \\  & =4\end{aligned}\end{aligned}
$$

General pattern and response

n x/sec(x) at 0; quotient rule, cancel common sec factor, evaluate. Correct = n. Source domain cos(x) != 0; cancellation does not extend the domain. Field type/key and answer shape remain exact.

Observed parameter: 4. Proposed domain: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24].

Complete observed profile q-340660-observed-bank. Each original choice maps exactly once, ignoring order:

- Answer faba1883-af56-500b-a141-28392efb394f; field field-1; correct; value `$4$`; recipe: Replace numerator coefficient 4 by n; final blank value n. Exact at n=4.

Prompt and solution recipe: Apply the same coefficient replacement to original Markdown, including every intermediate and final calculated coefficient. All shared instructional sentences remain exact. New UUIDs derive from task content and field-owned answer values, never seed or order. No plot generation is needed.

## q-70874

Specific source

Find the slope of $y=f(x)$ at $x=\frac{\pi }{3}$ if $f(x)=ln⁡x+3csc⁡x.$

Fixed solution sequence

First, we calculate the derivative using the sum rule:

$$
\begin{aligned}\begin{aligned}{f}^{′}(x) & =\frac{\text{d}}{\text{d}x}(ln⁡x+3csc⁡x) \\  & =\frac{1}{x}+3(-csc⁡xcot⁡x) \\  & =\frac{1}{x}-3csc⁡xcot⁡x\end{aligned}\end{aligned}
$$

Then, we substitute $x=\frac{\pi }{3}$ in the derivative and get

$$
\begin{aligned}\begin{aligned}{f}^{′}(\frac{\pi }{3}) & =\frac{1}{(\frac{\pi }{3})}-3csc⁡(\frac{\pi }{3})cot⁡(\frac{\pi }{3}) \\  & =\frac{3}{\pi }-3(\frac{2}{\sqrt{3}})(\frac{1}{\sqrt{3}}) \\  & =\frac{3}{\pi }-3(\frac{2}{3}) \\  & =\frac{3}{\pi }-2.\end{aligned}\end{aligned}
$$

General pattern and response

ln(x) + 3csc(x) at pi/3; sum rule then evaluation to 3/pi - 2. Domain x > 0 and sin(x) != 0. Field type/key and answer shape remain exact.

Observed parameter: 1. Proposed domain: [1].

Complete observed profile q-70874-observed-bank. Each original choice maps exactly once, ignoring order:

- Answer 20324c7d-2431-5dbf-89ba-4a62fbbbbdeb; field selection; distractor; value `$2-\frac{3}{\pi }$`; recipe: Fixed observed expression (source-only template; mistake interpretation unresolved)

- Answer 2d601842-f51f-5a34-901c-3c87ed74673e; field selection; correct; value `$\frac{3}{\pi }-2$`; recipe: Fixed observed expression (source-only template; mistake interpretation unresolved)

- Answer c6ecc1e0-b453-5588-a3e8-923b6e7ebcab; field selection; distractor; value `$\pi -2$`; recipe: Fixed observed expression (source-only template; mistake interpretation unresolved)

- Answer ec9d4934-d293-54d1-9eb4-aaf1a8bf5781; field selection; distractor; value `$\frac{3}{\pi }$`; recipe: Fixed observed expression (source-only template; mistake interpretation unresolved)

- Answer ef4a666c-1131-5d8c-a6c2-62062090c6e3; field selection; distractor; value `$\frac{3}{\pi }+2$`; recipe: Fixed observed expression (source-only template; mistake interpretation unresolved)

Prompt and solution recipe: Retain original prompt and entire fixed worked solution exactly. No inferred distractor recipes. New UUIDs derive from task content and field-owned answer values, never seed or order. No plot generation is needed.
