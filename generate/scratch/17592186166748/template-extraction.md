# Template extraction

## 1. Describe each original

See classification for the nine original prompts. All use independent x, dependent y=y(x), f(x,y), df/dx radio response, exact symbolic elementary forms and one fixed worked solution. Shared prose is stored verbatim. Sources differ in partial-derivative structure, substitution reductions, expansion, common-denominator, factoring or radical cancellation; they remain distinct masks.

## 2. Generalize the shared pattern

Compute f_x with y held fixed and f_y with x held fixed. Substitute the actual y(x), differentiate that dependency, then substitute into df/dx=f_x+f_y y′ and reduce. Preserve the displayed derivative operator, both partial components, every dependency derivative, substitution rows and full final arithmetic sequence.

## 3. Original components and complete bank maps

Each observed option is a complete expression-pattern recipe scaled by the whole-function coefficient a, not a recovered wrong-operation algorithm. At a=1 this is the exact printed value. Several banks combine altered argument, trigonometric function, coefficient and exponent; their intent is underdetermined. Every observed full bank therefore has an explicit evidence-only public profile observed:q-ID. No opaque wrong operations are admitted as learning defaults. Original choice order and answer IDs stay in source.json; replay changes owned identities and shuffles only option order.


### q-94588 / sine_power

Prompt: If $f(x,y)=\operatorname{sin}⁡({x}^{2}+y)$ and $y={x}^{2},$ compute $\frac{\text{d}f}{\text{d}x}.$

Profile: `observed:q-94588`; parameters `{a: 1}`. Field selection/radio; all math values; correct ID bbe84aab-93e0-5d36-b349-3a91b328cae0.

| Original position | Complete value | Designation | Parameterized recipe |

|---|---|---|---|

| 1 | $({x}^{2}+1)\operatorname{cos}⁡({x}^{2})$ | wrong | multiply entire displayed expression by a; preserve internal pattern |

| 2 | $2x{sin}^{2}⁡(2x)$ | wrong | multiply entire displayed expression by a; preserve internal pattern |

| 3 | $2{x}^{3}\operatorname{cos}⁡(2{x}^{2})$ | wrong | multiply entire displayed expression by a; preserve internal pattern |

| 4 | $4x\operatorname{cos}⁡(2{x}^{2})$ | correct | multiply entire displayed expression by a; preserve internal pattern |

| 5 | $2x(x+1)\operatorname{sin}⁡({x}^{2})$ | wrong | multiply entire displayed expression by a; preserve internal pattern |

Complete original solution sequence (verbatim evidence):

The chain rule for a multivariable function $f(x,y)$ in the case where $y=y(x)$ can be expressed as follows:

$$
\frac{\text{d}f}{\text{d}x}=\frac{∂f}{∂x}+\frac{∂f}{∂y}\cdot \frac{\text{d}y}{\text{d}x}
$$

First, we find the partial derivatives of $f$ with respect to $x$ and $y:$ 

$$
\begin{aligned}\frac{∂f}{∂x}=2x\operatorname{cos}⁡({x}^{2}+y),\,\frac{∂f}{∂y}=\operatorname{cos}⁡({x}^{2}+y)\end{aligned}
$$

Writing the above results in terms of $x,$ we get

$$
\begin{aligned}\frac{∂f}{∂x} & =2x\operatorname{cos}⁡({x}^{2}+{x}^{2})=2x\operatorname{cos}⁡(2{x}^{2}), \\ \frac{∂f}{∂y} & =\operatorname{cos}⁡({x}^{2}+{x}^{2})=\operatorname{cos}⁡(2{x}^{2}).\end{aligned}
$$

Next, we take the derivative $y$ with respect to $x,$ and we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =2x.\end{aligned}
$$

Finally, putting the derivatives into the multivariable chain rule, we get

$$
\begin{aligned}\frac{\text{d}f}{\text{d}x} & =2x\operatorname{cos}⁡(2{x}^{2})+\operatorname{cos}⁡(2{x}^{2})\cdot 2x \\  & =2x\operatorname{cos}⁡(2{x}^{2})+2x\operatorname{cos}⁡(2{x}^{2}) \\  & =4x\operatorname{cos}⁡(2{x}^{2}).\end{aligned}
$$


### q-95121 / x_log_sum

Prompt: If $f(x,y)=x\operatorname{ln}⁡(x+y)$ and $y={x}^{2},$ compute $\frac{\text{d}f}{\text{d}x}.$

Profile: `observed:q-95121`; parameters `{a: 1}`. Field selection/radio; all math values; correct ID 0e272a6d-78d3-5cb9-95c9-c87f0fea3da6.

| Original position | Complete value | Designation | Parameterized recipe |

|---|---|---|---|

| 1 | $\operatorname{ln}⁡(x+{x}^{2})+\frac{1+2x}{1+x}$ | correct | multiply entire displayed expression by a; preserve internal pattern |

| 2 | ${x}^{2}\operatorname{ln}⁡(1+x)$ | wrong | multiply entire displayed expression by a; preserve internal pattern |

| 3 | $\operatorname{ln}⁡(1+{x}^{2})-\frac{1+3{x}^{2}}{1+2x}$ | wrong | multiply entire displayed expression by a; preserve internal pattern |

| 4 | $\operatorname{ln}⁡(1+x)-\frac{1+2{x}^{2}}{1+{x}^{2}}$ | wrong | multiply entire displayed expression by a; preserve internal pattern |

| 5 | $\frac{1+2x}{1+x}$ | wrong | multiply entire displayed expression by a; preserve internal pattern |

Complete original solution sequence (verbatim evidence):

The chain rule for a multivariable function $f(x,y)$ in the case where $y=y(x)$ can be expressed as follows:

$$
\frac{\text{d}f}{\text{d}x}=\frac{∂f}{∂x}+\frac{∂f}{∂y}\cdot \frac{\text{d}y}{\text{d}x}
$$

First, we find the partial derivatives of $f$ with respect to $x$ and $y:$ 

$$
\begin{aligned}\frac{∂f}{∂x}=\operatorname{ln}⁡(x+y)+\frac{x}{x+y},\,\frac{∂f}{∂y}=\frac{x}{x+y}\end{aligned}
$$

Writing the above results in terms of $x,$ we get

$$
\begin{aligned}\frac{∂f}{∂x} & =\operatorname{ln}⁡(x+{x}^{2})+\frac{x}{x+{x}^{2}}, \\ \frac{∂f}{∂y} & =\frac{x}{x+{x}^{2}}.\end{aligned}
$$

Next, we take the derivative $y$ with respect to $x,$ and we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =2x.\end{aligned}
$$

Finally, putting the derivatives into the multivariable chain rule, we get

$$
\begin{aligned}\frac{\text{d}f}{\text{d}x} & =\operatorname{ln}⁡(x+{x}^{2})+\frac{x}{x+{x}^{2}}+\frac{x}{x+{x}^{2}}\cdot 2x \\  & =\operatorname{ln}⁡(x+{x}^{2})+\frac{x+2{x}^{2}}{x+{x}^{2}} \\  & =\operatorname{ln}⁡(x+{x}^{2})+\frac{x(1+2x)}{x(1+x)} \\  & =\operatorname{ln}⁡(x+{x}^{2})+\frac{1+2x}{1+x}.\end{aligned}
$$


### q-170670 / y_log_power

Prompt: If $f(x,y)=y\operatorname{ln}⁡({x}^{2}+1)$ and $y={x}^{2}+1,$ compute $\frac{\text{d}f}{\text{d}x}.$

Profile: `observed:q-170670`; parameters `{a: 1}`. Field selection/radio; all math values; correct ID 49b2d0a3-8640-5928-a7d2-f8a14102a68f.

| Original position | Complete value | Designation | Parameterized recipe |

|---|---|---|---|

| 1 | $({x}^{2}+1)\operatorname{ln}⁡({x}^{2}+1)$ | wrong | multiply entire displayed expression by a; preserve internal pattern |

| 2 | $2x(1+\operatorname{ln}⁡({x}^{2}+1))$ | correct | multiply entire displayed expression by a; preserve internal pattern |

| 3 | $\frac{2x({x}^{2}+1)}{\operatorname{ln}⁡({x}^{2}+1)}$ | wrong | multiply entire displayed expression by a; preserve internal pattern |

| 4 | $\frac{2x}{\operatorname{ln}⁡({x}^{2}+1)}$ | wrong | multiply entire displayed expression by a; preserve internal pattern |

| 5 | $2x\operatorname{ln}⁡({x}^{2}+1)$ | wrong | multiply entire displayed expression by a; preserve internal pattern |

Complete original solution sequence (verbatim evidence):

The chain rule for a multivariable function $f(x,y)$ in the case where $y=y(x)$ can be expressed as follows:

$$
\frac{\text{d}f}{\text{d}x}=\frac{∂f}{∂x}+\frac{∂f}{∂y}\cdot \frac{\text{d}y}{\text{d}x}
$$

First, we find the partial derivatives of $f$ with respect to $x$ and $y:$ 

$$
\begin{aligned}\frac{∂f}{∂x}=\frac{2xy}{{x}^{2}+1},\,\frac{∂f}{∂y}=\operatorname{ln}⁡({x}^{2}+1)\end{aligned}
$$

Writing the above results in terms of $x,$ we get

$$
\begin{aligned}\frac{∂f}{∂x} & =\frac{2x({x}^{2}+1)}{{x}^{2}+1}=2x, \\ \frac{∂f}{∂y} & =\operatorname{ln}⁡({x}^{2}+1).\end{aligned}
$$

Next, we take the derivative $y$ with respect to $x,$ and we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =2x.\end{aligned}
$$

Finally, putting the derivatives into the multivariable chain rule, we get

$$
\begin{aligned}\frac{\text{d}f}{\text{d}x} & =2x+\operatorname{ln}⁡({x}^{2}+1)\cdot 2x \\  & =2x(1+\operatorname{ln}⁡({x}^{2}+1)).\end{aligned}
$$


### q-95088 / reciprocal_exp

Prompt: If $f(x,y)=\frac{1}{x+y}$ and $y={e}^{-x},$ compute $\frac{\text{d}f}{\text{d}x}.$

Profile: `observed:q-95088`; parameters `{a: 1}`. Field selection/radio; all math values; correct ID a03e6cf2-e199-53c6-82f6-4585f233d777.

| Original position | Complete value | Designation | Parameterized recipe |

|---|---|---|---|

| 1 | $\frac{2}{(x+{e}^{-x})^{2}}$ | wrong | multiply entire displayed expression by a; preserve internal pattern |

| 2 | $\frac{1-{e}^{-x}}{1+x{e}^{-x}}$ | wrong | multiply entire displayed expression by a; preserve internal pattern |

| 3 | $\frac{1-2{e}^{-x}}{(x+{e}^{-x})^{2}}$ | wrong | multiply entire displayed expression by a; preserve internal pattern |

| 4 | $\frac{-1+{e}^{-x}}{(x+{e}^{-x})^{2}}$ | correct | multiply entire displayed expression by a; preserve internal pattern |

| 5 | $\frac{{e}^{-x}}{1+x{e}^{-x}}$ | wrong | multiply entire displayed expression by a; preserve internal pattern |

Complete original solution sequence (verbatim evidence):

The chain rule for a multivariable function $f(x,y)$ in the case where $y=y(x)$ can be expressed as follows:

$$
\frac{\text{d}f}{\text{d}x}=\frac{∂f}{∂x}+\frac{∂f}{∂y}\cdot \frac{\text{d}y}{\text{d}x}
$$

First, we find the partial derivatives of $f$ with respect to $x$ and $y:$ 

$$
\begin{aligned}\frac{∂f}{∂x}=-\frac{1}{(x+y)^{2}},\,\frac{∂f}{∂y}=-\frac{1}{(x+y)^{2}}\end{aligned}
$$

Writing the above results in terms of $x,$ we get

$$
\begin{aligned}\frac{∂f}{∂x} & =\frac{∂f}{∂y}=-\frac{1}{(x+{e}^{-x})^{2}}.\end{aligned}
$$

Next, we take the derivative $y$ with respect to $x,$ and we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =-{e}^{-x}.\end{aligned}
$$

Finally, putting the derivatives into the multivariable chain rule, we get

$$
\begin{aligned}\frac{\text{d}f}{\text{d}x} & =-\frac{1}{(x+{e}^{-x})^{2}}-\frac{1}{(x+{e}^{-x})^{2}}\cdot (-{e}^{-x}) \\  & =-\frac{1}{(x+{e}^{-x})^{2}}+\frac{{e}^{-x}}{(x+{e}^{-x})^{2}} \\  & =\frac{-1+{e}^{-x}}{(x+{e}^{-x})^{2}}.\end{aligned}
$$


### q-95114 / radial_power

Prompt: If $f(x,y)=\sqrt{{x}^{2}+{y}^{2}}$ and $y={x}^{3},$ compute $\frac{\text{d}f}{\text{d}x}.$

Profile: `observed:q-95114`; parameters `{a: 1}`. Field selection/radio; all math values; correct ID 96f6c6ee-cd4d-5972-a765-20abbc025c7d.

| Original position | Complete value | Designation | Parameterized recipe |

|---|---|---|---|

| 1 | $\frac{3{x}^{2}}{\sqrt{1+{x}^{4}}}$ | wrong | multiply entire displayed expression by a; preserve internal pattern |

| 2 | $\frac{1+{x}^{2}}{\sqrt{1+{x}^{4}}}$ | wrong | multiply entire displayed expression by a; preserve internal pattern |

| 3 | $\frac{3{x}^{4}}{\sqrt{1+{x}^{4}}}$ | wrong | multiply entire displayed expression by a; preserve internal pattern |

| 4 | $\frac{1+3{x}^{3}}{x\sqrt{1+{x}^{4}}}$ | wrong | multiply entire displayed expression by a; preserve internal pattern |

| 5 | $\frac{1+3{x}^{4}}{\sqrt{1+{x}^{4}}}$ | correct | multiply entire displayed expression by a; preserve internal pattern |

Complete original solution sequence (verbatim evidence):

The chain rule for a multivariable function $f(x,y)$ in the case where $y=y(x)$ can be expressed as follows:

$$
\frac{\text{d}f}{\text{d}x}=\frac{∂f}{∂x}+\frac{∂f}{∂y}\cdot \frac{\text{d}y}{\text{d}x}
$$

First, we find the partial derivatives of $f$ with respect to $x$ and $y:$ 

$$
\begin{aligned}\frac{∂f}{∂x}=\frac{x}{\sqrt{{x}^{2}+{y}^{2}}},\,\frac{∂f}{∂y}=\frac{y}{\sqrt{{x}^{2}+{y}^{2}}}\end{aligned}
$$

Writing the above results in terms of $x,$ we get

$$
\begin{aligned}\frac{∂f}{∂x} & =\frac{x}{\sqrt{{x}^{2}+{x}^{6}}} \\  & =\frac{x}{\sqrt{{x}^{2}(1+{x}^{4})}} \\  & =\frac{x}{x\sqrt{1+{x}^{4}}} \\  & =\frac{1}{\sqrt{1+{x}^{4}}}, \\ \frac{∂f}{∂y} & =\frac{{x}^{3}}{\sqrt{{x}^{2}+{x}^{6}}} \\  & =\frac{{x}^{3}}{\sqrt{{x}^{2}(1+{x}^{4})}} \\  & =\frac{{x}^{3}}{x\sqrt{1+{x}^{4}}} \\  & =\frac{{x}^{2}}{\sqrt{1+{x}^{4}}}.\end{aligned}
$$

Next, we take the derivative $y$ with respect to $x,$ and we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =3{x}^{2}.\end{aligned}
$$

Finally, putting the derivatives into the multivariable chain rule, we get

$$
\begin{aligned}\frac{\text{d}f}{\text{d}x} & =\frac{1}{\sqrt{1+{x}^{4}}}+\frac{{x}^{2}}{\sqrt{1+{x}^{4}}}\cdot 3{x}^{2} \\  & =\frac{1}{\sqrt{1+{x}^{4}}}+\frac{3{x}^{4}}{\sqrt{1+{x}^{4}}} \\  & =\frac{1+3{x}^{4}}{\sqrt{1+{x}^{4}}}.\end{aligned}
$$


### q-95117 / x_exp_sine

Prompt: If $f(x,y)=x{e}^{y}$ and $y=\operatorname{sin}⁡x,$ compute $\frac{\text{d}f}{\text{d}x}.$

Profile: `observed:q-95117`; parameters `{a: 1}`. Field selection/radio; all math values; correct ID 682e2303-0eea-58c6-9296-93c2403f441a.

| Original position | Complete value | Designation | Parameterized recipe |

|---|---|---|---|

| 1 | ${e}^{\operatorname{sin}⁡x}(1-\operatorname{cos}⁡x)$ | wrong | multiply entire displayed expression by a; preserve internal pattern |

| 2 | ${e}^{\operatorname{cos}⁡x}(1+\operatorname{sin}⁡x)$ | wrong | multiply entire displayed expression by a; preserve internal pattern |

| 3 | ${e}^{\operatorname{sin}⁡x}(1+x\operatorname{cos}⁡x)$ | correct | multiply entire displayed expression by a; preserve internal pattern |

| 4 | ${e}^{\operatorname{sin}⁡x}(1+x\operatorname{sin}⁡x)$ | wrong | multiply entire displayed expression by a; preserve internal pattern |

| 5 | ${e}^{\operatorname{cos}⁡x}(1-x\operatorname{sin}⁡x)$ | wrong | multiply entire displayed expression by a; preserve internal pattern |

Complete original solution sequence (verbatim evidence):

The chain rule for a multivariable function $f(x,y)$ in the case where $y=y(x)$ can be expressed as follows:

$$
\frac{\text{d}f}{\text{d}x}=\frac{∂f}{∂x}+\frac{∂f}{∂y}\cdot \frac{\text{d}y}{\text{d}x}
$$

First, we find the partial derivatives of $f$ with respect to $x$ and $y:$ 

$$
\begin{aligned}\frac{∂f}{∂x}={e}^{y},\,\frac{∂f}{∂y}=x{e}^{y}\end{aligned}
$$

Writing the above results in terms of $x,$ we get

$$
\begin{aligned}\frac{∂f}{∂x} & ={e}^{\operatorname{sin}⁡x}, \\ \frac{∂f}{∂y} & =x{e}^{\operatorname{sin}⁡x}.\end{aligned}
$$

Next, we take the derivative $y$ with respect to $x,$ and we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =\operatorname{cos}⁡x.\end{aligned}
$$

Finally, putting the derivatives into the multivariable chain rule, we get

$$
\begin{aligned}\frac{\text{d}f}{\text{d}x} & ={e}^{\operatorname{sin}⁡x}+x{e}^{\operatorname{sin}⁡x}\cdot \operatorname{cos}⁡x \\  & ={e}^{\operatorname{sin}⁡x}(1+x\operatorname{cos}⁡x).\end{aligned}
$$


### q-95118 / polynomial_sine

Prompt: If $f(x,y)={x}^{2}+yx$ and $y=\operatorname{sin}⁡x,$ compute $\frac{\text{d}f}{\text{d}x}.$

Profile: `observed:q-95118`; parameters `{a: 1}`. Field selection/radio; all math values; correct ID 4be18679-efe0-59e6-80ac-db92f8d96a8e.

| Original position | Complete value | Designation | Parameterized recipe |

|---|---|---|---|

| 1 | $2x+\operatorname{sin}⁡x+x\operatorname{cos}⁡x$ | correct | multiply entire displayed expression by a; preserve internal pattern |

| 2 | $2x+\operatorname{sin}⁡x-2\operatorname{sin}⁡x$ | wrong | multiply entire displayed expression by a; preserve internal pattern |

| 3 | $2x+\operatorname{sin}⁡x+\operatorname{cos}⁡x$ | wrong | multiply entire displayed expression by a; preserve internal pattern |

| 4 | $2x+\operatorname{sin}⁡x+\operatorname{cos}⁡x\operatorname{sin}⁡x$ | wrong | multiply entire displayed expression by a; preserve internal pattern |

| 5 | $2x+x\operatorname{sin}⁡x$ | wrong | multiply entire displayed expression by a; preserve internal pattern |

Complete original solution sequence (verbatim evidence):

The chain rule for a multivariable function $f(x,y)$ in the case where $y=y(x)$ can be expressed as follows:

$$
\frac{\text{d}f}{\text{d}x}=\frac{∂f}{∂x}+\frac{∂f}{∂y}\cdot \frac{\text{d}y}{\text{d}x}
$$

First, we find the partial derivatives of $f$ with respect to $x$ and $y:$ 

$$
\begin{aligned}\frac{∂f}{∂x}=2x+y,\,\frac{∂f}{∂y}=x\end{aligned}
$$

Writing the above results in terms of $x,$ we get

$$
\begin{aligned}\frac{∂f}{∂x} & =2x+\operatorname{sin}⁡x \\ \frac{∂f}{∂y} & =x.\end{aligned}
$$

Next, we take the derivative $y$ with respect to $x,$ and we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =\operatorname{cos}⁡x.\end{aligned}
$$

Finally, putting the derivatives into the multivariable chain rule, we get

$$
\begin{aligned}\frac{\text{d}f}{\text{d}x} & =2x+\operatorname{sin}⁡x+x\operatorname{cos}⁡x.\end{aligned}
$$


### q-95119 / cosine_reciprocal

Prompt: If $f(x,y)=\operatorname{cos}⁡({x}^{2}+y)$ and $y=\frac{1}{x},$ compute $\frac{\text{d}f}{\text{d}x}.$

Profile: `observed:q-95119`; parameters `{a: 1}`. Field selection/radio; all math values; correct ID 70539894-ff4f-5b7d-809c-ae8c476c88fc.

| Original position | Complete value | Designation | Parameterized recipe |

|---|---|---|---|

| 1 | $(1+4{x}^{2})\operatorname{cos}⁡(\frac{{x}^{2}-1}{x})$ | wrong | multiply entire displayed expression by a; preserve internal pattern |

| 2 | $(\frac{1-4{x}^{3}}{x})\operatorname{cos}⁡(\frac{{x}^{3}+1}{{x}^{2}})$ | wrong | multiply entire displayed expression by a; preserve internal pattern |

| 3 | $(1-3{x}^{3})\operatorname{sin}⁡(\frac{{x}^{2}+1}{{x}^{2}})$ | wrong | multiply entire displayed expression by a; preserve internal pattern |

| 4 | $(\frac{1-2{x}^{3}}{{x}^{2}})\operatorname{sin}⁡(\frac{{x}^{3}+1}{x})$ | correct | multiply entire displayed expression by a; preserve internal pattern |

| 5 | $(\frac{2{x}^{2}+1}{x})\operatorname{sin}⁡(\frac{{x}^{3}+1}{x})$ | wrong | multiply entire displayed expression by a; preserve internal pattern |

Complete original solution sequence (verbatim evidence):

The chain rule for a multivariable function $f(x,y)$ in the case where $y=y(x)$ can be expressed as follows:

$$
\frac{\text{d}f}{\text{d}x}=\frac{∂f}{∂x}+\frac{∂f}{∂y}\cdot \frac{\text{d}y}{\text{d}x}
$$

First, we find the partial derivatives of $f$ with respect to $x$ and $y:$ 

$$
\begin{aligned}\frac{∂f}{∂x}=-2x\operatorname{sin}⁡({x}^{2}+y),\,\frac{∂f}{∂y}=-\operatorname{sin}⁡({x}^{2}+y)\end{aligned}
$$

Writing the above results in terms of $x,$ we get

$$
\begin{aligned}\frac{∂f}{∂x} & =-2x\operatorname{sin}⁡({x}^{2}+\frac{1}{x}), \\ \frac{∂f}{∂y} & =-\operatorname{sin}⁡({x}^{2}+\frac{1}{x}).\end{aligned}
$$

Next, we take the derivative $y$ with respect to $x,$ and we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =-\frac{1}{{x}^{2}}.\end{aligned}
$$

Finally, putting the derivatives into the multivariable chain rule, we get

$$
\begin{aligned}\frac{\text{d}f}{\text{d}x} & =-2x\operatorname{sin}⁡({x}^{2}+\frac{1}{x})+(-\operatorname{sin}⁡({x}^{2}+\frac{1}{x}))\cdot (-\frac{1}{{x}^{2}}) \\  & =(\frac{1}{{x}^{2}}-2x)\operatorname{sin}⁡({x}^{2}+\frac{1}{x}) \\  & =(\frac{1-2{x}^{3}}{{x}^{2}})\operatorname{sin}⁡(\frac{{x}^{3}+1}{x}).\end{aligned}
$$


### q-95122 / quotient_power

Prompt: If $f(x,y)=\frac{y}{x+1}$ and $y={x}^{3},$ compute $\frac{\text{d}f}{\text{d}x}.$

Profile: `observed:q-95122`; parameters `{a: 1}`. Field selection/radio; all math values; correct ID d1925cff-23b1-5f65-a480-35f2ce80acbc.

| Original position | Complete value | Designation | Parameterized recipe |

|---|---|---|---|

| 1 | $\frac{4{x}^{2}(x-6)}{x+1}$ | wrong | multiply entire displayed expression by a; preserve internal pattern |

| 2 | $\frac{{x}^{2}(3{x}^{2}-1)}{(x+1)^{2}}$ | wrong | multiply entire displayed expression by a; preserve internal pattern |

| 3 | $\frac{x(3x+4)}{(x+1)^{2}}$ | wrong | multiply entire displayed expression by a; preserve internal pattern |

| 4 | $\frac{x(4x-3)}{x+1}$ | wrong | multiply entire displayed expression by a; preserve internal pattern |

| 5 | $\frac{{x}^{2}(2x+3)}{(x+1)^{2}}$ | correct | multiply entire displayed expression by a; preserve internal pattern |

Complete original solution sequence (verbatim evidence):

The chain rule for a multivariable function $f(x,y)$ in the case where $y=y(x)$ can be expressed as follows:

$$
\frac{\text{d}f}{\text{d}x}=\frac{∂f}{∂x}+\frac{∂f}{∂y}\cdot \frac{\text{d}y}{\text{d}x}
$$

First, we find the partial derivatives of $f$ with respect to $x$ and $y:$ 

$$
\begin{aligned}\frac{∂f}{∂x}=-\frac{y}{(x+1)^{2}},\,\frac{∂f}{∂y}=\frac{1}{x+1}\end{aligned}
$$

Writing the above results in terms of $x,$ we get

$$
\begin{aligned}\frac{∂f}{∂x} & =-\frac{{x}^{3}}{(x+1)^{2}}, \\ \frac{∂f}{∂y} & =\frac{1}{x+1}.\end{aligned}
$$

Next, we take the derivative $y$ with respect to $x,$ and we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =3{x}^{2}.\end{aligned}
$$

Finally, putting the derivatives into the multivariable chain rule, we get

$$
\begin{aligned}\frac{\text{d}f}{\text{d}x} & =-\frac{{x}^{3}}{(x+1)^{2}}+\frac{1}{x+1}\cdot 3{x}^{2} \\  & =\frac{3{x}^{2}}{x+1}-\frac{{x}^{3}}{(x+1)^{2}} \\  & =\frac{3{x}^{2}(x+1)-{x}^{3}}{(x+1)^{2}} \\  & =\frac{3{x}^{3}+3{x}^{2}-{x}^{3}}{(x+1)^{2}} \\  & =\frac{{x}^{2}(2x+3)}{(x+1)^{2}}.\end{aligned}
$$

## 4. Reusable masks and guards

Source-shaped easy templates fill complete expression slots only. For nonunit a, render f=a·(original function), wrap each complete partial/RHS arithmetic node by a, retain the dependency derivative unscaled, and keep the formal special rule unchanged. At a=1 no strings are changed. All complete source arithmetic masks survive in normal generation, including the radial factor/cancel rows and quotient rearrangement/expansion chain. Signed multiplication is grouped explicitly. No short global variable replacement occurs.

Normal whole operation profile: correct f_x+f_y y′; omit y-chain f_x; reverse chain sign f_x−f_y y′; omit dependency derivative f_x+f_y; substitute y for y′ f_x+f_y y. Reciprocal-exponential has y′=−y, so the last operation would duplicate the reverse-sign option: its eligible complete profile uses omit x-partial f_y y′ instead. This profile is fixed before parameters and no first-valid pool repairs are performed. Reject the entire instance on any equivalent pair. Explicit parameters and samplers share the exact level guards, and unknown/unused parameters fail.

The authored polynomial/exponential solutions reuse source prose and formal/partial/substitution/dependency/final blocks. Hard displays d/dx(cx), d/dx(trig(kx)), then the product rule for y′ before final distribution and factoring. Duplicate mathematically identical final CAS rows are omitted rather than presented as a distinct teaching step.

Identities: seed/choice order excluded; actual prompt, fixed solution, complete bank, domain and level included. Mathematical task fingerprint uses the canonical composed function f(x,y(x)), domain and workload level, excluding bank, profile, seed, coefficients that only rescale the dependent variable, and their product aliases. For authored families b*c aliases are deduplicated. Signed products from |b,c|≤4 give 18 distinct products, eight a values and three frequencies: 432 tasks per family, 864 per missing level. Easy has 9×10=90 tasks. These are finite catalogs, not claims of unlimited diversity.

## Source error and interpretation limits

q-95114 cancels sqrt(x²)=x and designates a positive answer without stating x>0. At x=−1 the true derivative and designated answer have opposite signs. Raw public replay retains every value and solution sentence unchanged and is ineligible. Normal generation makes the minimal supported presentation/domain repair: append Assume x>0. It does not silently alter the answer bank or cancellation chain. Exact replay denominators are 9/9 prompts, 9/9 complete chains and 45/45 values; source correctness without the supported domain repair is 8/9.

Decoded source-byte audit found no adjacent slashes and no literal \u2061 sequences in option values: JSON tool serialization was not a TeX defect. No escaping repairs were applied. All raw original profiles remain evidence-only because wrong-operation intent is not claimed as recovered. Native grading is owned radio selection; algebraically equivalent typed entries are not an available response shape. Independent symbolic QA checks all displayed choices and every equality, and native grading is reported separately.
