# Template extraction — four stages

## 1. Source-specific descriptions

All 13 sources below are retained at basis 1356. Table entries describe complete supplied functions and point inputs, not only final answers.

| Source | Original prompt | Field | Derivative/evaluation stages |

|---|---|---|---|

| q-17373 | Given that $y =-\frac{3}{5}\ln x$, find the slope of the tangent at $x = 1$. | radio | absent (normal authored 3/2) |

| q-17395 | Given that $y = \log_{3} x + 5\ln x$, find the slope of the tangent at $x = 1$. | radio | absent (normal authored 3/2) |

| q-101723 | Given that $y=4{e}^{x}-3{log}_{7}x$, find the slope of the tangent at $x=3.$ | absent (normal authored blank) | 1/3 |

| q-340014 | Given the function $y=5{x}^{2}+6\operatorname{ln}x,$ the slope of the tangent line at $x=3$ is{{field-1}}. | blank | 4/3 |

| q-340022 | Given the function $y=5\operatorname{ln}x-2\cdot {3}^{x},$ the slope of the tangent line at $x=2$ is{{field-1}}. | blank | 4/3 |

| q-340109 | Given the function $y=-3{e}^{x}+2{log}_{4}x,$ the slope of the tangent line at $x=2$ is{{field-1}}. | blank | 4/3 |

| q-70897 | Given that $y=2{log}_{2}x+{2}^{x}$, find the slope of the tangent at $x=2.$ | absent (normal authored blank) | 1/3 |

| q-101726 | Given that $y=3x-5+8{log}_{2}⁡x$, find the slope of the tangent at $x=\frac{1}{ln⁡2}.$ | radio | 5/4 |

| q-17371 | Given that $y=3ln⁡x+2{x}^{2}-5x$, find the slope of the tangent at $x=1.$ | radio | 5/4 |

| q-340024 | Given the function $y=2{x}^{3}-5{log}_{3}⁡x,$ the slope of the tangent line at $x=2$ is{{field-1}}. | blank | 4/3 |

| q-340026 | Given the function $y=6{log}_{2}⁡x+4{x}^{2}-3x,$ the slope of the tangent line at $x=1$ is{{field-1}}. | blank | 4/3 |

| q-340110 | Given the function $y=4{e}^{x}-3{log}_{2}⁡x+7,$ the slope of the tangent line at $x=3$ is{{field-1}}. | blank | 4/3 |

| q-70903 | Given that $y=3\operatorname{log}⁡x+{x}^{3}-4$, find the slope of the tangent at $x=3.$ | radio | 1/3 |

## 2. Shared pattern

Find the slope as dy/dx evaluated at the supplied positive x. Functions are signed constant multiples of ln x, log_b x, simple integer powers of x, exponential functions already covered by the predecessor topic, and constants. Every source has at least one logarithm. Different source families retain their own derivative splitting/coefficient extraction, zero contribution, reduction and substitution rows; families do not share a generic CAS chain.

## 3. Complete component and bank map

Each choice below belongs to its sole source-owned field. A raw mask is an ordered arithmetic expression in prompt parameters; exact bank reproduction does not establish the intent of a scalar wrong answer. All raw profiles are marked evidence-only/ineligible. Literal exponent/widget digits stay fixed. The extraction script gives ordered semantic roles for every numeric atom inside complete source components.

### q-17373

Parameters: `{"n": 3, "d": 5, "t": 1}`; public profile `raw:q-17373`.

Prompt component mask:

```text
Given that $y =-\frac{@@n@@}{@@d@@}\ln x$, find the slope of the tangent at $x = @@t@@$.
```

Field `selection`:

| Original complete value | Parameterized expression mask | Status |

|---|---|---|

| `-\frac{5}{3}` | `-\frac{@@d@@}{@@n@@}` | historical wrong value; intent unresolved |

| `0` | `0` | historical wrong value; intent unresolved |

| `\frac{3}{5}` | `\frac{@@n@@}{@@d@@}` | historical wrong value; intent unresolved |

| `-\frac{3}{5}` | `-\frac{@@n@@}{@@d@@}` | correct inferred from differentiation, designation missing |

| `\frac{5}{3}` | `\frac{@@d@@}{@@n@@}` | historical wrong value; intent unresolved |

Worked solution mask (absence remains absence in raw API):

```text
None
```

### q-17395

Parameters: `{"b": 3, "c": 5, "t": 1}`; public profile `raw:q-17395`.

Prompt component mask:

```text
Given that $y = \log_{@@b@@} x + @@c@@\ln x$, find the slope of the tangent at $x = @@t@@$.
```

Field `selection`:

| Original complete value | Parameterized expression mask | Status |

|---|---|---|

| `\frac{1}{\ln 3}` | `\frac{1}{\ln @@b@@}` | historical wrong value; intent unresolved |

| `\ln 3 + 5` | `\ln @@b@@ + @@c@@` | historical wrong value; intent unresolved |

| `0` | `0` | historical wrong value; intent unresolved |

| `\frac{5}{\ln 3}` | `\frac{@@c@@}{\ln @@b@@}` | historical wrong value; intent unresolved |

| `\frac{1}{\ln 3} + 5` | `\frac{1}{\ln @@b@@} + @@c@@` | correct inferred from differentiation, designation missing |

Worked solution mask (absence remains absence in raw API):

```text
None
```

### q-101723

Parameters: `{"a": 4, "c": 3, "b": 7, "t": 3}`; public profile `raw:q-101723`.

Prompt component mask:

```text
Given that $y=@@a@@{e}^{x}-@@c@@{log}_{@@b@@}x$, find the slope of the tangent at $x=@@t@@.$
```

Worked solution mask (absence remains absence in raw API):

```text
To find the slope of the tangent at a given point, we have to find $\frac{\text{d}y}{\text{d}x}$ at that point.

Taking the derivative, we have

$$
\frac{\text{d}y}{\text{d}x}=@@a@@{e}^{x}-\frac{@@c@@}{x\operatorname{ln}@@b@@}\,.
$$

Therefore, the slope  of the tangent at $x=@@t@@$ is 

$$
\begin{aligned}{\frac{\text{d}y}{\text{d}x}|}_{x=@@t@@} & ={(@@a@@{e}^{x}-\frac{@@c@@}{x\operatorname{ln}@@b@@})|}_{x=@@t@@} \\  & =@@a@@{e}^{@@t@@}-\frac{@@c@@}{@@t@@\operatorname{ln}@@b@@} \\  & =@@a@@{e}^{@@t@@}-\frac{@@c/t@@}{\operatorname{ln}@@b@@}\,.\end{aligned}
$$
```

### q-340014

Parameters: `{"a": 5, "c": 6, "t": 3}`; public profile `raw:q-340014`.

Prompt component mask:

```text
Given the function $y=@@a@@{x}^{2}+@@c@@\operatorname{ln}x,$ the slope of the tangent line at $x=@@t@@$ is{{field-1}}.
```

Field `field-1`:

| Original complete value | Parameterized expression mask | Status |

|---|---|---|

| `32` | `@@answer@@` | observed correct |

Worked solution mask (absence remains absence in raw API):

```text
To find the slope of the tangent at a given point, we have to find $\frac{\text{d}y}{\text{d}x}$ at that point.

Taking the derivative, we have

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =\frac{\text{d}}{\text{d}x}(@@a@@{x}^{2}+@@c@@\operatorname{ln}x) \\  & =@@a@@\frac{\text{d}}{\text{d}x}({x}^{2})+@@c@@\frac{\text{d}}{\text{d}x}(\operatorname{ln}x) \\  & =@@a@@\cdot 2x+@@c@@\cdot \frac{1}{x} \\  & =@@2*a@@x+\frac{@@c@@}{x}\,.\end{aligned}
$$

Therefore, the slope of the tangent at $x=@@t@@$ is 

$$
\begin{aligned}{\frac{\text{d}y}{\text{d}x}|}_{x=@@t@@} & ={(@@2*a@@x+\frac{@@c@@}{x})|}_{x=@@t@@} \\  & =@@2*a@@\cdot @@t@@+\frac{@@c@@}{@@t@@} \\  & =@@answer@@\,.\end{aligned}
$$
```

### q-340022

Parameters: `{"a": 5, "c": 2, "b": 3, "t": 2}`; public profile `raw:q-340022`.

Prompt component mask:

```text
Given the function $y=@@a@@\operatorname{ln}x-@@c@@\cdot {@@b@@}^{x},$ the slope of the tangent line at $x=@@t@@$ is{{field-1}}.
```

Field `field-1`:

| Original complete value | Parameterized expression mask | Status |

|---|---|---|

| `\frac{5}{2}-18\operatorname{ln}3` | `\frac{@@a@@}{@@t@@}-@@c*b**t@@\operatorname{ln}@@b@@` | observed correct |

Worked solution mask (absence remains absence in raw API):

```text
To find the slope of the tangent at a given point, we have to find $\frac{\text{d}y}{\text{d}x}$ at that point.

Taking the derivative, we have

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =\frac{\text{d}}{\text{d}x}(@@a@@\operatorname{ln}x-@@c@@\cdot {@@b@@}^{x}) \\  & =@@a@@\frac{\text{d}}{\text{d}x}(\operatorname{ln}x)-@@c@@\frac{\text{d}}{\text{d}x}({@@b@@}^{x}) \\  & =@@a@@\cdot \frac{1}{x}-@@c@@\cdot {@@b@@}^{x}\operatorname{ln}@@b@@ \\  & =\frac{@@a@@}{x}-@@c@@\operatorname{ln}@@b@@\cdot {@@b@@}^{x}\,.\end{aligned}
$$

Therefore, the slope of the tangent at $x=@@t@@$ is 

$$
\begin{aligned}{\frac{\text{d}y}{\text{d}x}|}_{x=@@t@@} & ={(\frac{@@a@@}{x}-@@c@@\operatorname{ln}@@b@@\cdot {@@b@@}^{x})|}_{x=@@t@@} \\  & =\frac{@@a@@}{@@t@@}-@@c@@\operatorname{ln}@@b@@\cdot {@@b@@}^{@@t@@} \\  & =\frac{@@a@@}{@@t@@}-@@c*b**t@@\operatorname{ln}@@b@@\,.\end{aligned}
$$
```

### q-340109

Parameters: `{"a": 3, "c": 2, "b": 4, "t": 2}`; public profile `raw:q-340109`.

Prompt component mask:

```text
Given the function $y=-@@a@@{e}^{x}+@@c@@{log}_{@@b@@}x,$ the slope of the tangent line at $x=@@t@@$ is{{field-1}}.
```

Field `field-1`:

| Original complete value | Parameterized expression mask | Status |

|---|---|---|

| `-3{e}^{2}+\frac{1}{\operatorname{ln}4}` | `-@@a@@{e}^{@@t@@}+\frac{@@c/t@@}{\operatorname{ln}@@b@@}` | observed correct |

| `-3e^2+\frac{1}{\ln4}` | `-@@a@@e^@@t@@+\frac{@@c/t@@}{\ln@@b@@}` | equivalent stored answer |

Worked solution mask (absence remains absence in raw API):

```text
To find the slope of the tangent at a given point, we have to find $\frac{\text{d}y}{\text{d}x}$ at that point.

Taking the derivative, we have

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =\frac{\text{d}}{\text{d}x}(-@@a@@{e}^{x}+@@c@@{log}_{@@b@@}x) \\  & =-@@a@@\frac{\text{d}}{\text{d}x}({e}^{x})+@@c@@\frac{\text{d}}{\text{d}x}({log}_{@@b@@}x) \\  & =-@@a@@{e}^{x}+@@c@@\cdot \frac{1}{x\operatorname{ln}@@b@@} \\  & =-@@a@@{e}^{x}+\frac{@@c@@}{x\operatorname{ln}@@b@@}\,.\end{aligned}
$$

Therefore, the slope of the tangent at $x=@@t@@$ is 

$$
\begin{aligned}{\frac{\text{d}y}{\text{d}x}|}_{x=@@t@@} & ={(-@@a@@{e}^{x}+\frac{@@c@@}{x\operatorname{ln}@@b@@})|}_{x=@@t@@} \\  & =-@@a@@{e}^{@@t@@}+\frac{@@c@@}{@@t@@\cdot \operatorname{ln}@@b@@} \\  & =-@@a@@{e}^{@@t@@}+\frac{@@c/t@@}{\operatorname{ln}@@b@@}\,.\end{aligned}
$$
```

### q-70897

Parameters: `{"a": 2, "b": 2, "t": 2}`; public profile `raw:q-70897`.

Prompt component mask:

```text
Given that $y=@@a@@{log}_{@@b@@}x+{@@b@@}^{x}$, find the slope of the tangent at $x=@@t@@.$
```

Worked solution mask (absence remains absence in raw API):

```text
To find the slope of the tangent at a given point, we have to find $\frac{\text{d}y}{\text{d}x}$ at that point.

Taking the derivative, we have

$$
\frac{\text{d}y}{\text{d}x}=\frac{@@a@@}{x\operatorname{ln}@@b@@}+{@@b@@}^{x}\operatorname{ln}@@b@@\,.
$$

Therefore, the slope of the tangent at $x=@@t@@$ is 

$$
\begin{aligned}{\frac{\text{d}y}{\text{d}x}|}_{x=@@t@@} & ={(\frac{@@a@@}{x\operatorname{ln}@@b@@}+{@@b@@}^{x}\operatorname{ln}@@b@@)|}_{x=@@t@@} \\  & =\frac{@@a@@}{@@t@@\cdot \operatorname{ln}@@b@@}+{@@b@@}^{@@t@@}\operatorname{ln}@@b@@ \\  & =\frac{@@a/t@@}{\operatorname{ln}@@b@@}+@@b**t@@\operatorname{ln}@@b@@\,.\end{aligned}
$$
```

### q-101726

Parameters: `{"a": 3, "k": 5, "c": 8, "b": 2}`; public profile `raw:q-101726`.

Prompt component mask:

```text
Given that $y=@@a@@x-@@k@@+@@c@@{log}_{@@b@@}⁡x$, find the slope of the tangent at $x=\frac{1}{ln⁡@@b@@}.$
```

Field `selection`:

| Original complete value | Parameterized expression mask | Status |

|---|---|---|

| `4` | `@@a+1@@` | historical wrong value; intent unresolved |

| `3+8ln⁡2` | `@@a@@+@@c@@ln⁡@@b@@` | historical wrong value; intent unresolved |

| `11` | `@@answer@@` | observed correct |

| `8ln⁡2-2` | `@@c@@ln⁡@@b@@-@@k-a@@` | historical wrong value; intent unresolved |

| `6` | `@@a+c-k@@` | historical wrong value; intent unresolved |

Worked solution mask (absence remains absence in raw API):

```text
To find the slope of the tangent at a given point, we have to find $\frac{\text{d}y}{\text{d}x}$ at that point.

Taking the derivative, we have

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =\frac{\text{d}}{\text{d}x}(@@a@@x-@@k@@+@@c@@{log}_{@@b@@}⁡x) \\  & =\frac{\text{d}}{\text{d}x}(@@a@@x)+\frac{\text{d}}{\text{d}x}(-@@k@@)+\frac{\text{d}}{\text{d}x}(@@c@@{log}_{@@b@@}⁡x) \\  & =@@a@@\frac{\text{d}}{\text{d}x}(x)-\frac{\text{d}}{\text{d}x}(@@k@@)+@@c@@\frac{\text{d}}{\text{d}x}({log}_{@@b@@}⁡x) \\  & =@@a@@-0+@@c@@\cdot \frac{1}{xln⁡@@b@@} \\  & =@@a@@+\frac{@@c@@}{xln⁡@@b@@}\,.\end{aligned}
$$

Therefore, the slope of the tangent at $x=\frac{1}{ln⁡@@b@@}$ is 

$$
\begin{aligned}{\frac{\text{d}y}{\text{d}x}|}_{x=1/ln⁡@@b@@} & ={(@@a@@+\frac{@@c@@}{xln⁡@@b@@})|}_{x=1/ln⁡@@b@@} \\  & =@@a@@+\frac{@@c@@}{(\frac{1}{ln⁡@@b@@}\cdot ln⁡@@b@@)} \\  & =@@a@@+@@c@@ \\  & =@@answer@@\,.\end{aligned}
$$
```

### q-17371

Parameters: `{"a": 3, "c": 2, "k": 5, "t": 1}`; public profile `raw:q-17371`.

Prompt component mask:

```text
Given that $y=@@a@@ln⁡x+@@c@@{x}^{2}-@@k@@x$, find the slope of the tangent at $x=@@t@@.$
```

Field `selection`:

| Original complete value | Parameterized expression mask | Status |

|---|---|---|

| `2` | `@@answer@@` | observed correct |

| `-3` | `-@@a@@` | historical wrong value; intent unresolved |

| `-2` | `-@@answer@@` | historical wrong value; intent unresolved |

| `12` | `@@a+2*c+k@@` | historical wrong value; intent unresolved |

| `-5` | `-@@k@@` | historical wrong value; intent unresolved |

Worked solution mask (absence remains absence in raw API):

```text
To find the slope of the tangent at a given point, we have to find $\frac{\text{d}y}{\text{d}x}$ at that point.

Taking the derivative, we have

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =\frac{\text{d}}{\text{d}x}(@@a@@ln⁡x+@@c@@{x}^{2}-@@k@@x) \\  & =\frac{\text{d}}{\text{d}x}(@@a@@ln⁡x)+\frac{\text{d}}{\text{d}x}(@@c@@{x}^{2})-\frac{\text{d}}{\text{d}x}(@@k@@x) \\  & =@@a@@\frac{\text{d}}{\text{d}x}(ln⁡x)+\frac{\text{d}}{\text{d}x}(@@c@@{x}^{2})-\frac{\text{d}}{\text{d}x}(@@k@@x) \\  & =@@a@@\cdot \frac{1}{x}+@@2*c@@x-@@k@@ \\  & =\frac{@@a@@}{x}+@@2*c@@x-@@k@@\,.\end{aligned}
$$

Therefore, the slope of the tangent at $x=@@t@@$ is 

$$
\begin{aligned}{\frac{\text{d}y}{\text{d}x}|}_{x=@@t@@} & ={(\frac{@@a@@}{x}+@@2*c@@x-@@k@@)|}_{x=@@t@@} \\  & =\frac{@@a@@}{@@t@@}+@@2*c@@\cdot @@t@@-@@k@@ \\  & =@@a/t@@+@@2*c*t@@-@@k@@ \\  & =@@answer@@\,.\end{aligned}
$$
```

### q-340024

Parameters: `{"a": 2, "c": 5, "b": 3, "t": 2}`; public profile `raw:q-340024`.

Prompt component mask:

```text
Given the function $y=@@a@@{x}^{3}-@@c@@{log}_{@@b@@}⁡x,$ the slope of the tangent line at $x=@@t@@$ is{{field-1}}.
```

Field `field-1`:

| Original complete value | Parameterized expression mask | Status |

|---|---|---|

| `24-\frac{5}{2\operatorname{ln}3}` | `@@3*a*t**2@@-\frac{@@c@@}{@@t@@\operatorname{ln}@@b@@}` | observed correct |

Worked solution mask (absence remains absence in raw API):

```text
To find the slope of the tangent at a given point, we have to find $\frac{\text{d}y}{\text{d}x}$ at that point.

Taking the derivative, we have

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =\frac{\text{d}}{\text{d}x}(@@a@@{x}^{3}-@@c@@{log}_{@@b@@}⁡x) \\  & =@@a@@\frac{\text{d}}{\text{d}x}({x}^{3})-@@c@@\frac{\text{d}}{\text{d}x}({log}_{@@b@@}⁡x) \\  & =@@a@@\cdot 3{x}^{2}-@@c@@\cdot \frac{1}{xln⁡@@b@@} \\  & =@@3*a@@{x}^{2}-\frac{@@c@@}{xln⁡@@b@@}\,.\end{aligned}
$$

Therefore, the slope of the tangent at $x=@@t@@$ is 

$$
\begin{aligned}{\frac{\text{d}y}{\text{d}x}|}_{x=@@t@@} & ={(@@3*a@@{x}^{2}-\frac{@@c@@}{xln⁡@@b@@})|}_{x=@@t@@} \\  & =@@3*a@@(@@t@@)^{2}-\frac{@@c@@}{@@t@@ln⁡@@b@@} \\  & =@@3*a*t**2@@-\frac{@@c@@}{@@t@@ln⁡@@b@@}\,.\end{aligned}
$$
```

### q-340026

Parameters: `{"a": 6, "c": 4, "k": 3, "b": 2, "t": 1}`; public profile `raw:q-340026`.

Prompt component mask:

```text
Given the function $y=@@a@@{log}_{@@b@@}⁡x+@@c@@{x}^{2}-@@k@@x,$ the slope of the tangent line at $x=@@t@@$ is{{field-1}}.
```

Field `field-1`:

| Original complete value | Parameterized expression mask | Status |

|---|---|---|

| `\frac{6}{\operatorname{ln}2}+5` | `\frac{@@a/t@@}{\operatorname{ln}@@b@@}+@@2*c*t-k@@` | observed correct |

Worked solution mask (absence remains absence in raw API):

```text
To find the slope of the tangent at a given point, we have to find $\frac{\text{d}y}{\text{d}x}$ at that point.

Taking the derivative, we have

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =\frac{\text{d}}{\text{d}x}(@@a@@{log}_{@@b@@}⁡x+@@c@@{x}^{2}-@@k@@x) \\  & =@@a@@\frac{\text{d}}{\text{d}x}({log}_{@@b@@}⁡x)+@@c@@\frac{\text{d}}{\text{d}x}({x}^{2})-@@k@@\frac{\text{d}}{\text{d}x}(x) \\  & =@@a@@\cdot \frac{1}{xln⁡@@b@@}+@@c@@\cdot 2x-@@k@@ \\  & =\frac{@@a@@}{xln⁡@@b@@}+@@2*c@@x-@@k@@\,.\end{aligned}
$$

Therefore, the slope of the tangent at $x=@@t@@$ is 

$$
\begin{aligned}{\frac{\text{d}y}{\text{d}x}|}_{x=@@t@@} & ={(\frac{@@a@@}{xln⁡@@b@@}+@@2*c@@x-@@k@@)|}_{x=@@t@@} \\  & =\frac{@@a@@}{@@t@@\cdot ln⁡@@b@@}+@@2*c@@(@@t@@)-@@k@@ \\  & =\frac{@@a/t@@}{ln⁡@@b@@}+@@2*c*t-k@@\,.\end{aligned}
$$
```

### q-340110

Parameters: `{"a": 4, "c": 3, "b": 2, "k": 7, "t": 3}`; public profile `raw:q-340110`.

Prompt component mask:

```text
Given the function $y=@@a@@{e}^{x}-@@c@@{log}_{@@b@@}⁡x+@@k@@,$ the slope of the tangent line at $x=@@t@@$ is{{field-1}}.
```

Field `field-1`:

| Original complete value | Parameterized expression mask | Status |

|---|---|---|

| `4{e}^{3}-\frac{1}{\operatorname{ln}2}` | `@@a@@{e}^{@@t@@}-\frac{@@c/t@@}{\operatorname{ln}@@b@@}` | observed correct |

Worked solution mask (absence remains absence in raw API):

```text
To find the slope of the tangent at a given point, we have to find $\frac{\text{d}y}{\text{d}x}$ at that point.

Taking the derivative, we have

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =\frac{\text{d}}{\text{d}x}(@@a@@{e}^{x}-@@c@@{log}_{@@b@@}⁡x+@@k@@) \\  & =@@a@@\frac{\text{d}}{\text{d}x}({e}^{x})-@@c@@\frac{\text{d}}{\text{d}x}({log}_{@@b@@}⁡x)+\frac{\text{d}}{\text{d}x}(@@k@@) \\  & =@@a@@{e}^{x}-@@c@@\cdot \frac{1}{xln⁡@@b@@}+0 \\  & =@@a@@{e}^{x}-\frac{@@c@@}{xln⁡@@b@@}\,.\end{aligned}
$$

Therefore, the slope of the tangent at $x=@@t@@$ is 

$$
\begin{aligned}{\frac{\text{d}y}{\text{d}x}|}_{x=@@t@@} & ={(@@a@@{e}^{x}-\frac{@@c@@}{xln⁡@@b@@})|}_{x=@@t@@} \\  & =@@a@@{e}^{@@t@@}-\frac{@@c@@}{@@t@@\cdot ln⁡@@b@@} \\  & =@@a@@{e}^{@@t@@}-\frac{@@c/t@@}{ln⁡@@b@@}\,.\end{aligned}
$$
```

### q-70903

Parameters: `{"a": 3, "b": 10, "k": 4, "t": 3}`; public profile `raw:q-70903`.

Prompt component mask:

```text
Given that $y=@@a@@\operatorname{log}⁡x+{x}^{3}-@@k@@$, find the slope of the tangent at $x=@@t@@.$
```

Field `selection`:

| Original complete value | Parameterized expression mask | Status |

|---|---|---|

| `\frac{9}{\operatorname{ln}⁡10}-3` | `\frac{@@a*t@@}{\operatorname{ln}⁡10}-@@t@@` | historical wrong value; intent unresolved |

| `\frac{1}{\operatorname{ln}⁡10}+27` | `\frac{@@a/t@@}{\operatorname{ln}⁡10}+@@3*t**2@@` | observed correct |

| `\frac{1}{3\operatorname{ln}⁡10}+3` | `\frac{@@a/t@@}{@@t@@\operatorname{ln}⁡10}+@@t@@` | historical wrong value; intent unresolved |

| `\frac{1}{\operatorname{ln}⁡10}-9` | `\frac{@@a/t@@}{\operatorname{ln}⁡10}-@@t**2@@` | historical wrong value; intent unresolved |

| `\frac{3}{\operatorname{ln}⁡10}+9` | `\frac{@@a@@}{\operatorname{ln}⁡10}+@@t**2@@` | historical wrong value; intent unresolved |

Worked solution mask (absence remains absence in raw API):

```text
To find the slope of the tangent at a given point, we have to find $\frac{\text{d}y}{\text{d}x}$ at that point.

Taking the derivative, we have

$$
\frac{\text{d}y}{\text{d}x}=\frac{@@a@@}{x\operatorname{ln}⁡10}+3{x}^{2}\,.
$$

Therefore, the slope of the tangent at $x=1$ is 

$$
\begin{aligned}{\frac{\text{d}y}{\text{d}x}|}_{x=@@t@@} & ={(\frac{@@a@@}{x\operatorname{ln}⁡10}+3{x}^{2})|}_{x=@@t@@} \\  & =\frac{@@a@@}{@@t@@\cdot \operatorname{ln}⁡10}+3\cdot {@@t@@}^{2} \\  & =\frac{@@a/t@@}{\operatorname{ln}⁡10}+@@3*t**2@@\,.\end{aligned}
$$
```

## 4. Reusable backbone, slots and constraints

Slots a,c,k are positive integer coefficient magnitudes, n/d is a reduced positive nonunit rational whose function coefficient is negative, b is a logarithm/exponential base, t is the evaluation input. Integer easy t is 1..4; rational-ln, two-log, and easy three-term quadratic forms retain t=1. The reciprocal-log family has t=1/ln b. Common log remains base ten. Coefficients 1..12 and bases 2..9 match small familiar source number forms. All relevant substitutions, derivative coefficients (2a,2c,3a), reduced evaluated powers, final scalars and point prose are dependent slots. Exact bounds are enforced on explicit parameters. Raw negative historical masks additionally require k>a or positive scalar answer where their sign is structurally fixed. Whole bank collisions reject the entire instance.

Normal easy retains all source-shaped families and operative stage masks. Source defects are repaired only in normal output. Historical scalar banks are not treated as recovered misconception recipes. The normal complete five-choice method banks are selected before parameters, with no first-valid pool:

- Negative rational ln: correct derivative scalar, positive/negative reciprocal of magnitude, positive original magnitude, zero.

- Two logarithms: correct sum, omit natural-log contribution, omit general-log contribution, put ln(base) in numerator, misapply natural-log coefficient to general-log contribution.

- Linear/constant/general-log at reciprocal-log point: correct sum, retain only linear derivative, retain only log contribution, omit reciprocal-log cancellation, retain the constant term.

- Natural-log/quadratic/linear: correct, reverse linear-derivative sign, reverse ln contribution sign, omit quadratic exponent factor, omit ln contribution.

- Common-log/cubic: correct, omit ln(base) factor, omit cubic exponent factor, omit log input substitution, omit log contribution.

Blank families retain scalar answers; q-340109 normal keeps its two equivalent stored spellings. An answer bank is a profile-specific component and affects content identity, not mathematical task counts.

Authored moderate varies t=2..4 for the three natural-log terms, coefficient 1..9. Authored hard substitutes t=s/ln b with s=2..4 into the observed three-term general-log sum; the source-supported cancellation and same derivative/substitution stages remain. Its final collected expression is a complete symbolic component. Hard requires a,c,k nonzero, coefficient <=9 and base 2..9. No chain rule, product rule, tangent equations or higher derivatives. These workloads are distinct from each other; all questions within a level have the same operations.

No plots are required. `masks.json` is a reusable frozen extraction, not a source-answer lookup: explicit changed parameters flow through all prompt, solution and bank slots. Fingerprints exclude additive constants that vanish under differentiation and source/profile aliases; content identity includes actual displayed prompt/solution/bank and difficulty.
