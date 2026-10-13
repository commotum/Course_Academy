# Template extraction

## Stage 1 — specific source inventory

All originals are preserved verbatim in source.json and replayed in review.md/source-cases.json. Each family below lists its precise ODE, original normalized answer, every complete option and its designation. The component recipe is translation of the whole mathematical expression in that option, including every exponent, function input, denominator and branch bound. No scalar fit or numerical answer lookup is used.

### exp_linear — q-154359

Find the general solution to the differential equation $\frac{\text{d}y}{\text{d}x}=\frac{2x}{{e}^{y}}.$

Source features: h=k=0; all real x,y; right side plus C>0. Field: radio/selection; answer shape: complete equation; options: five.

Bank profile: `observed` for this template. Primitive sequence: To find the general solution, we first separate the variables: 

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =\frac{2x}{{e}^{y}} \\ {e}^{y}\,\frac{\text{d}y}{\text{d}x} & =2x\end{aligned}
$$

Then, we integrate both sides with respect to $x:$

$$
\begin{aligned}\int {e}^{y}\,\frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int 2x\,\text{d}x \\ \int {e}^{y}\,\frac{\text{d}y}{\cancel{\text{d}x}}\,\cancel{\text{d}x} & =\int 2x\,\text{d}x \\ \int {e}^{y}\,\text{d}y & =\int 2x\,\text{d}x \\ {e}^{y} & ={x}^{2}+C\end{aligned}
$$

Therefore, the general solution to the differential equation (in implicit form) is

$$
{e}^{y}={x}^{2}+C.
$$

- Correct `{e}^{y}={x}^{2}+C`; parameterized recipe: replace mathematical x and y components by x+h and y+k throughout this complete relation. Incorrect-operation intent is unresolved; numerical reproduction is not evidence of the source author’s intended mistake.

- Wrong `2{e}^{y}={x}^{2}+C`; parameterized recipe: replace mathematical x and y components by x+h and y+k throughout this complete relation. Incorrect-operation intent is unresolved; numerical reproduction is not evidence of the source author’s intended mistake.

- Wrong `\frac{1}{2}{e}^{2y}=2x+C`; parameterized recipe: replace mathematical x and y components by x+h and y+k throughout this complete relation. Incorrect-operation intent is unresolved; numerical reproduction is not evidence of the source author’s intended mistake.

- Wrong `\frac{3}{2}{e}^{2y}=x+C`; parameterized recipe: replace mathematical x and y components by x+h and y+k throughout this complete relation. Incorrect-operation intent is unresolved; numerical reproduction is not evidence of the source author’s intended mistake.

- Wrong `4{e}^{y}={x}^{3}+C`; parameterized recipe: replace mathematical x and y components by x+h and y+k throughout this complete relation. Incorrect-operation intent is unresolved; numerical reproduction is not evidence of the source author’s intended mistake.

### arcsin_autonomous — q-154367

Find the general solution to the differential equation $\frac{\text{d}y}{\text{d}x}=\sqrt{1-{y}^{2}}\,$ for $\,|y|<1.$

Source features: h=k=0; |y|<1; arcsin(y) principal branch. Field: radio/selection; answer shape: complete equation; options: five.

Bank profile: `observed` for this template. Primitive sequence: To find the general solution, we first separate the variables: 

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =\sqrt{1-{y}^{2}} \\ \frac{1}{\sqrt{1-{y}^{2}}}\cdot \frac{\text{d}y}{\text{d}x} & =1\end{aligned}
$$

Then, we integrate both sides with respect to $x:$

$$
\begin{aligned}\int \frac{1}{\sqrt{1-{y}^{2}}}\cdot \frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int \,\text{d}x \\ \int \frac{1}{\sqrt{1-{y}^{2}}}\cdot \frac{\text{d}y}{\cancel{\text{d}x}}\,\cancel{\text{d}x} & =\int \,\text{d}x \\ \int \frac{1}{\sqrt{1-{y}^{2}}}\,\text{d}y & =\int \text{d}x \\ \operatorname{arcsin}⁡y & =x+C.\end{aligned}
$$

Therefore, the general solution to the differential equation (in implicit form) is

$$
\operatorname{arcsin}⁡y=x+C.
$$

- Wrong `\operatorname{sin}⁡y=x+C`; parameterized recipe: replace mathematical x and y components by x+h and y+k throughout this complete relation. Incorrect-operation intent is unresolved; numerical reproduction is not evidence of the source author’s intended mistake.

- Correct `\operatorname{arcsin}⁡y=x+C`; parameterized recipe: replace mathematical x and y components by x+h and y+k throughout this complete relation. Incorrect-operation intent is unresolved; numerical reproduction is not evidence of the source author’s intended mistake.

- Wrong `\operatorname{arctan}⁡y=x+C`; parameterized recipe: replace mathematical x and y components by x+h and y+k throughout this complete relation. Incorrect-operation intent is unresolved; numerical reproduction is not evidence of the source author’s intended mistake.

- Wrong `\operatorname{arccos}⁡y=x+C`; parameterized recipe: replace mathematical x and y components by x+h and y+k throughout this complete relation. Incorrect-operation intent is unresolved; numerical reproduction is not evidence of the source author’s intended mistake.

- Wrong `\operatorname{tan}⁡y=x+C`; parameterized recipe: replace mathematical x and y components by x+h and y+k throughout this complete relation. Incorrect-operation intent is unresolved; numerical reproduction is not evidence of the source author’s intended mistake.

### tan_exp — q-118885

Find the general solution to the differential equation $\frac{\text{d}y}{\text{d}x}={e}^{x}{cos}^{2}⁡y$ for $0<y<\frac{\pi }{2}.$

Source features: h=k=0; 0<y<pi/2. Field: radio/selection; answer shape: complete equation; options: five.

Bank profile: `observed` for this template. Primitive sequence: To find the general solution, we first separate the variables: 

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & ={e}^{x}{cos}^{2}⁡y \\ \frac{1}{{cos}^{2}⁡y}\,\frac{\text{d}y}{\text{d}x} & ={e}^{x} \\ {sec}^{2}⁡y\,\frac{\text{d}y}{\text{d}x} & ={e}^{x}\end{aligned}
$$

Then, we integrate both sides with respect to $x:$

$$
\begin{aligned}\int {sec}^{2}⁡y\,\frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int {e}^{x}\,\text{d}x \\ \int {sec}^{2}⁡y\,\frac{\text{d}y}{\cancel{\text{d}x}}\,\cancel{\text{d}x} & =\int {e}^{x}\,\text{d}x \\ \int {sec}^{2}⁡y\,\text{d}y & =\int {e}^{x}\,\text{d}x \\ \operatorname{tan}⁡y & ={e}^{x}+C\end{aligned}
$$

Therefore, the general solution to the differential equation (in implicit form) is

$$
\operatorname{tan}⁡y={e}^{x}+C.
$$

- Wrong `2\operatorname{tan}⁡y={e}^{x}+C`; parameterized recipe: replace mathematical x and y components by x+h and y+k throughout this complete relation. Incorrect-operation intent is unresolved; numerical reproduction is not evidence of the source author’s intended mistake.

- Wrong `\operatorname{tan}⁡y={e}^{2x}+C`; parameterized recipe: replace mathematical x and y components by x+h and y+k throughout this complete relation. Incorrect-operation intent is unresolved; numerical reproduction is not evidence of the source author’s intended mistake.

- Wrong `2\operatorname{tan}⁡y={e}^{2x}+C`; parameterized recipe: replace mathematical x and y components by x+h and y+k throughout this complete relation. Incorrect-operation intent is unresolved; numerical reproduction is not evidence of the source author’s intended mistake.

- Wrong `\operatorname{tan}⁡y=2{e}^{x}+C`; parameterized recipe: replace mathematical x and y components by x+h and y+k throughout this complete relation. Incorrect-operation intent is unresolved; numerical reproduction is not evidence of the source author’s intended mistake.

- Correct `\operatorname{tan}⁡y={e}^{x}+C`; parameterized recipe: replace mathematical x and y components by x+h and y+k throughout this complete relation. Incorrect-operation intent is unresolved; numerical reproduction is not evidence of the source author’s intended mistake.

### log_exp — q-14246

Find the general solution to the differential equation $\frac{\text{d}y}{\text{d}x}=y{e}^{x}$ for $y\ne 0.$

Source features: h=k=0; y≠0; each sign branch separately. Field: radio/selection; answer shape: complete equation; options: five.

Bank profile: `observed` for this template. Primitive sequence: To find the general solution, we first separate the variables: 

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =y{e}^{x} \\ \frac{1}{y}\cdot \frac{\text{d}y}{\text{d}x} & ={e}^{x}\end{aligned}
$$

Then, we integrate both sides with respect to $x:$

$$
\begin{aligned}\int \frac{1}{y}\cdot \frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int {e}^{x}\,\text{d}x \\ \int \frac{1}{y}\cdot \frac{\text{d}y}{\cancel{\text{d}x}}\,\cancel{\text{d}x} & =\int {e}^{x}\,\text{d}x \\ \int \frac{1}{y}\,\text{d}y & =\int {e}^{x}\,\text{d}x \\ \operatorname{ln}⁡|y| & ={e}^{x}+C\end{aligned}
$$

Therefore, the general solution to the differential equation (in implicit form) is

$$
\operatorname{ln}⁡|y|={e}^{x}+C
$$

- Wrong `{e}^{y}=\operatorname{ln}⁡|x|+C`; parameterized recipe: replace mathematical x and y components by x+h and y+k throughout this complete relation. Incorrect-operation intent is unresolved; numerical reproduction is not evidence of the source author’s intended mistake.

- Correct `\operatorname{ln}⁡|y|={e}^{x}+C`; parameterized recipe: replace mathematical x and y components by x+h and y+k throughout this complete relation. Incorrect-operation intent is unresolved; numerical reproduction is not evidence of the source author’s intended mistake.

- Wrong `\operatorname{ln}⁡|y|={e}^{\sqrt{x}}+C`; parameterized recipe: replace mathematical x and y components by x+h and y+k throughout this complete relation. Incorrect-operation intent is unresolved; numerical reproduction is not evidence of the source author’s intended mistake.

- Wrong `y={e}^{\sqrt{x}}+C`; parameterized recipe: replace mathematical x and y components by x+h and y+k throughout this complete relation. Incorrect-operation intent is unresolved; numerical reproduction is not evidence of the source author’s intended mistake.

- Wrong `y={e}^{x}+C`; parameterized recipe: replace mathematical x and y components by x+h and y+k throughout this complete relation. Incorrect-operation intent is unresolved; numerical reproduction is not evidence of the source author’s intended mistake.

### tan_autonomous — q-154357

Find the general solution to the differential equation $\frac{\text{d}y}{\text{d}x}=\frac{1}{{sec}^{2}⁡y}$ for $-\frac{\pi }{2}<y<\frac{\pi }{2}.$

Source features: h=k=0; -pi/2<y<pi/2. Field: radio/selection; answer shape: complete equation; options: five.

Bank profile: `observed` for this template. Primitive sequence: To find the general solution, we first separate the variables: 

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =\frac{1}{{sec}^{2}⁡y} \\ {sec}^{2}⁡y\,\frac{\text{d}y}{\text{d}x} & =1\end{aligned}
$$

Then, we integrate both sides with respect to $x:$

$$
\begin{aligned}\int {sec}^{2}⁡y\,\frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int 1\,\text{d}x \\ \int {sec}^{2}⁡y\,\frac{\text{d}y}{\cancel{\text{d}x}}\,\cancel{\text{d}x} & =\int 1\,\text{d}x \\ \int {sec}^{2}⁡y\,\text{d}y & =\int 1\,\text{d}x \\ \operatorname{tan}⁡y & =x+C\end{aligned}
$$

Therefore, the general solution to the differential equation (in implicit form) is

$$
\operatorname{tan}⁡y=x+C.
$$

- Wrong `\operatorname{sin}⁡y=x+C`; parameterized recipe: replace mathematical x and y components by x+h and y+k throughout this complete relation. Incorrect-operation intent is unresolved; numerical reproduction is not evidence of the source author’s intended mistake.

- Wrong `y=\operatorname{tan}⁡x+C`; parameterized recipe: replace mathematical x and y components by x+h and y+k throughout this complete relation. Incorrect-operation intent is unresolved; numerical reproduction is not evidence of the source author’s intended mistake.

- Wrong `\operatorname{tan}⁡y=\sqrt{x}+C`; parameterized recipe: replace mathematical x and y components by x+h and y+k throughout this complete relation. Incorrect-operation intent is unresolved; numerical reproduction is not evidence of the source author’s intended mistake.

- Wrong `\operatorname{sin}⁡y=\sqrt{x}+C`; parameterized recipe: replace mathematical x and y components by x+h and y+k throughout this complete relation. Incorrect-operation intent is unresolved; numerical reproduction is not evidence of the source author’s intended mistake.

- Correct `\operatorname{tan}⁡y=x+C`; parameterized recipe: replace mathematical x and y components by x+h and y+k throughout this complete relation. Incorrect-operation intent is unresolved; numerical reproduction is not evidence of the source author’s intended mistake.

### power_cube — q-154361

Find the general solution to the differential equation $\frac{\text{d}y}{\text{d}x}=\frac{{x}^{2}}{{y}^{2}}.$

Source features: h=k=0; y≠0. Field: radio/selection; answer shape: complete equation; options: five.

Bank profile: `observed` for this template. Primitive sequence: To find the general solution, we first separate the variables: 

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =\frac{{x}^{2}}{{y}^{2}} \\ {y}^{2}\frac{\text{d}y}{\text{d}x} & ={x}^{2}\end{aligned}
$$

Then, we integrate both sides with respect to $x:$

$$
\begin{aligned}\int {y}^{2}\,\frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int {x}^{2}\,\text{d}x \\ \int {y}^{2}\,\frac{\text{d}y}{\cancel{\text{d}x}}\,\cancel{\text{d}x} & =\int {x}^{2}\,\text{d}x \\ \int {y}^{2}\,\text{d}y & =\int {x}^{2}\,\text{d}x \\ \frac{{y}^{3}}{3} & =\frac{{x}^{3}}{3}+K \\ {y}^{3} & ={x}^{3}+C,\end{aligned}
$$

where $C=3K.$

Therefore, the general solution to the differential equation (in implicit form) is

$$
{y}^{3}={x}^{3}+C.
$$

- Wrong `{y}^{2}={x}^{3}+C`; parameterized recipe: replace mathematical x and y components by x+h and y+k throughout this complete relation. Incorrect-operation intent is unresolved; numerical reproduction is not evidence of the source author’s intended mistake.

- Wrong `{y}^{3}=x+C`; parameterized recipe: replace mathematical x and y components by x+h and y+k throughout this complete relation. Incorrect-operation intent is unresolved; numerical reproduction is not evidence of the source author’s intended mistake.

- Correct `{y}^{3}={x}^{3}+C`; parameterized recipe: replace mathematical x and y components by x+h and y+k throughout this complete relation. Incorrect-operation intent is unresolved; numerical reproduction is not evidence of the source author’s intended mistake.

- Wrong `{y}^{2}={x}^{2}+C`; parameterized recipe: replace mathematical x and y components by x+h and y+k throughout this complete relation. Incorrect-operation intent is unresolved; numerical reproduction is not evidence of the source author’s intended mistake.

- Wrong `y={x}^{3}+C`; parameterized recipe: replace mathematical x and y components by x+h and y+k throughout this complete relation. Incorrect-operation intent is unresolved; numerical reproduction is not evidence of the source author’s intended mistake.

### exp_affine — q-154369

Find the general solution to the differential equation $\frac{\text{d}y}{\text{d}x}=2{e}^{-y}(x-1).$

Source features: h=k=0; all real x,y; right side plus C>0. Field: radio/selection; answer shape: complete equation; options: five.

Bank profile: `observed` for this template. Primitive sequence: To find the general solution, we first separate the variables: 

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =2{e}^{-y}(x-1) \\ {e}^{y}\,\frac{\text{d}y}{\text{d}x} & =2(x-1)\end{aligned}
$$

Then, we integrate both sides with respect to $x:$

$$
\begin{aligned}\int {e}^{y}\,\frac{\text{d}y}{\text{d}x}\text{d}x & =\int 2(x-1)\,\text{d}x \\ \int {e}^{y}\,\frac{\text{d}y}{\cancel{\text{d}x}}\,\cancel{\text{d}x} & =\int 2x\,\text{d}x-\int 2\,\text{d}x \\ {e}^{y} & ={x}^{2}-2x+C\end{aligned}
$$

Therefore, the general solution to the differential equation (in implicit form) is

$$
{e}^{y}={x}^{2}-2x+C.
$$

- Wrong `y={x}^{2}-2x+C`; parameterized recipe: replace mathematical x and y components by x+h and y+k throughout this complete relation. Incorrect-operation intent is unresolved; numerical reproduction is not evidence of the source author’s intended mistake.

- Correct `{e}^{y}={x}^{2}-2x+C`; parameterized recipe: replace mathematical x and y components by x+h and y+k throughout this complete relation. Incorrect-operation intent is unresolved; numerical reproduction is not evidence of the source author’s intended mistake.

- Wrong `{e}^{2y}=\frac{1}{2}\,{x}^{2}-x+C`; parameterized recipe: replace mathematical x and y components by x+h and y+k throughout this complete relation. Incorrect-operation intent is unresolved; numerical reproduction is not evidence of the source author’s intended mistake.

- Wrong `{e}^{2y}={x}^{2}-2x+C`; parameterized recipe: replace mathematical x and y components by x+h and y+k throughout this complete relation. Incorrect-operation intent is unresolved; numerical reproduction is not evidence of the source author’s intended mistake.

- Wrong `2y=\frac{1}{2}\,{x}^{2}-x+C`; parameterized recipe: replace mathematical x and y components by x+h and y+k throughout this complete relation. Incorrect-operation intent is unresolved; numerical reproduction is not evidence of the source author’s intended mistake.

### root_power — q-154373

Find the general solution to the differential equation $\frac{\text{d}y}{\text{d}x}=\frac{\sqrt{x}}{\sqrt{y}}.$

Source features: h=k=0; x≥0, y>0. Field: radio/selection; answer shape: complete equation; options: five.

Bank profile: `observed` for this template. Primitive sequence: To find the general solution, we first separate the variables: 

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =\frac{\sqrt{x}}{\sqrt{y}} \\ \sqrt{y}\,\frac{\text{d}y}{\text{d}x} & =\sqrt{x}\end{aligned}
$$

Then, we integrate both sides with respect to $x:$

$$
\begin{aligned}\int \sqrt{y}\,\frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int \sqrt{x}\,\text{d}x \\ \int \sqrt{y}\,\frac{\text{d}y}{\cancel{\text{d}x}}\,\cancel{\text{d}x} & =\int \sqrt{x}\,\text{d}x \\ \int {y}^{1/2}\,\text{d}y & =\int {x}^{1/2}\,\text{d}x \\ \frac{2{y}^{3/2}}{3} & =\frac{2{x}^{3/2}}{3}+K \\ {y}^{3/2} & ={x}^{3/2}+C \\ \sqrt{{y}^{3}} & =\sqrt{{x}^{3}}+C,\end{aligned}
$$

where $C=\frac{3K}{2}.$

Therefore, the general solution to the differential equation (in implicit form) is

$$
\sqrt{{y}^{3}}=\sqrt{{x}^{3}}+C.
$$

- Wrong `y={x}^{2}+C`; parameterized recipe: replace mathematical x and y components by x+h and y+k throughout this complete relation. Incorrect-operation intent is unresolved; numerical reproduction is not evidence of the source author’s intended mistake.

- Wrong `\sqrt{{y}^{3}}=x+C`; parameterized recipe: replace mathematical x and y components by x+h and y+k throughout this complete relation. Incorrect-operation intent is unresolved; numerical reproduction is not evidence of the source author’s intended mistake.

- Correct `\sqrt{{y}^{3}}=\sqrt{{x}^{3}}+C`; parameterized recipe: replace mathematical x and y components by x+h and y+k throughout this complete relation. Incorrect-operation intent is unresolved; numerical reproduction is not evidence of the source author’s intended mistake.

- Wrong `y=\sqrt{{x}^{3}}+C`; parameterized recipe: replace mathematical x and y components by x+h and y+k throughout this complete relation. Incorrect-operation intent is unresolved; numerical reproduction is not evidence of the source author’s intended mistake.

- Wrong `{y}^{3}=\sqrt{x}+C`; parameterized recipe: replace mathematical x and y components by x+h and y+k throughout this complete relation. Incorrect-operation intent is unresolved; numerical reproduction is not evidence of the source author’s intended mistake.

### sin_poly — q-158035

Find the general solution to the differential equation $\frac{\text{d}y}{\text{d}x}=\frac{3{x}^{2}}{\operatorname{cos}⁡y}.$

Source features: h=k=0; cos(y)≠0; each connected branch separately. Field: radio/selection; answer shape: complete equation; options: five.

Bank profile: `observed` for this template. Primitive sequence: To find the general solution, we first separate the variables: 

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =\frac{3{x}^{2}}{\operatorname{cos}⁡y} \\ \operatorname{cos}⁡y\,\frac{\text{d}y}{\text{d}x} & =3{x}^{2}\end{aligned}
$$

Then, we integrate both sides with respect to $x:$

$$
\begin{aligned}\int \operatorname{cos}⁡y\,\frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int 3{x}^{2}\,\text{d}x \\ \int \operatorname{cos}⁡y\,\frac{\text{d}y}{\cancel{\text{d}x}}\,\cancel{\text{d}x} & =\int 3{x}^{2}\,\text{d}x \\ \int \operatorname{cos}⁡y\,\text{d}y & =\int 3{x}^{2}\,\text{d}x \\ \operatorname{sin}⁡y & ={x}^{3}+C\end{aligned}
$$

Therefore, the general solution to the differential equation (in implicit form) is

$$
\operatorname{sin}⁡y={x}^{3}+C.
$$

- Correct `\operatorname{sin}⁡y={x}^{3}+C`; parameterized recipe: replace mathematical x and y components by x+h and y+k throughout this complete relation. Incorrect-operation intent is unresolved; numerical reproduction is not evidence of the source author’s intended mistake.

- Wrong `\text{ }y={x}^{3}+C`; parameterized recipe: replace mathematical x and y components by x+h and y+k throughout this complete relation. Incorrect-operation intent is unresolved; numerical reproduction is not evidence of the source author’s intended mistake.

- Wrong `\operatorname{tan}⁡y={x}^{3}+C`; parameterized recipe: replace mathematical x and y components by x+h and y+k throughout this complete relation. Incorrect-operation intent is unresolved; numerical reproduction is not evidence of the source author’s intended mistake.

- Wrong `\operatorname{sin}⁡y=\frac{1}{{x}^{3}}+C`; parameterized recipe: replace mathematical x and y components by x+h and y+k throughout this complete relation. Incorrect-operation intent is unresolved; numerical reproduction is not evidence of the source author’s intended mistake.

- Wrong `\operatorname{tan}⁡y=\frac{1}{{x}^{3}}+C`; parameterized recipe: replace mathematical x and y components by x+h and y+k throughout this complete relation. Incorrect-operation intent is unresolved; numerical reproduction is not evidence of the source author’s intended mistake.

### sec_log — q-158116

Find the general solution to the differential equation $\frac{\text{d}y}{\text{d}x}=\frac{1}{x\operatorname{sec}⁡y\operatorname{tan}⁡y}$ for $x\ne 0$ and $-\frac{\pi }{2}<y<\frac{\pi }{2}.$

Source features: h=k=0; x≠0; -pi/2<y<pi/2; y≠0. Field: radio/selection; answer shape: complete equation; options: five.

Bank profile: `observed` for this template. Primitive sequence: To find the general solution, we first separate the variables: 

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =\frac{1}{x\operatorname{sec}⁡y\operatorname{tan}⁡y} \\ \operatorname{sec}⁡y\operatorname{tan}⁡y\,\frac{\text{d}y}{\text{d}x} & =\frac{1}{x}\end{aligned}
$$

Then, we integrate both sides with respect to $x:$

$$
\begin{aligned}\int \operatorname{sec}⁡y\operatorname{tan}⁡y\,\frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int \frac{1}{x}\,\text{d}x \\ \int \operatorname{sec}⁡y\operatorname{tan}⁡y\,\frac{\text{d}y}{\cancel{\text{d}x}}\,\cancel{\text{d}x} & =\int \frac{1}{x}\,\text{d}x \\ \int \operatorname{sec}⁡y\operatorname{tan}⁡y\,\text{d}y & =\int \frac{1}{x}\,\text{d}x \\ \operatorname{sec}⁡y & =\operatorname{ln}⁡|x|+C\end{aligned}
$$

Therefore, the general solution to the differential equation (in implicit form) is

$$
\operatorname{sec}⁡y=\operatorname{ln}⁡|x|+C.
$$

- Wrong `\operatorname{tan}⁡y=\frac{1}{{x}^{2}}+C`; parameterized recipe: replace mathematical x and y components by x+h and y+k throughout this complete relation. Incorrect-operation intent is unresolved; numerical reproduction is not evidence of the source author’s intended mistake.

- Correct `\operatorname{sec}⁡y=\operatorname{ln}⁡|x|+C`; parameterized recipe: replace mathematical x and y components by x+h and y+k throughout this complete relation. Incorrect-operation intent is unresolved; numerical reproduction is not evidence of the source author’s intended mistake.

- Wrong `\operatorname{sec}⁡y=-\frac{1}{{x}^{2}}+C`; parameterized recipe: replace mathematical x and y components by x+h and y+k throughout this complete relation. Incorrect-operation intent is unresolved; numerical reproduction is not evidence of the source author’s intended mistake.

- Wrong `\operatorname{tan}⁡y=\operatorname{ln}⁡|x|+C`; parameterized recipe: replace mathematical x and y components by x+h and y+k throughout this complete relation. Incorrect-operation intent is unresolved; numerical reproduction is not evidence of the source author’s intended mistake.

- Wrong `{sec}^{2}⁡y=\frac{1}{x}+C`; parameterized recipe: replace mathematical x and y components by x+h and y+k throughout this complete relation. Incorrect-operation intent is unresolved; numerical reproduction is not evidence of the source author’s intended mistake.

### log_sin — q-158117

Find the general solution to the differential equation $\frac{\text{d}y}{\text{d}x}=y\operatorname{sin}⁡x$ for $y\ne 0.$

Source features: h=k=0; y≠0; each sign branch separately. Field: radio/selection; answer shape: complete equation; options: five.

Bank profile: `observed` for this template. Primitive sequence: To find the general solution, we first separate the variables: 

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =y\operatorname{sin}⁡x \\ \frac{1}{y}\cdot \frac{\text{d}y}{\text{d}x} & =\operatorname{sin}⁡x\end{aligned}
$$

Then, we integrate both sides with respect to $x:$

$$
\begin{aligned}\int \frac{1}{y}\cdot \frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int \operatorname{sin}⁡x\,\text{d}x \\ \int \frac{1}{y}\cdot \frac{\text{d}y}{\cancel{\text{d}x}}\,\cancel{\text{d}x} & =\int \operatorname{sin}⁡x\,\text{d}x \\ \int \frac{1}{y}\,\text{d}y & =\int \operatorname{sin}⁡x\,\text{d}x \\ \operatorname{ln}⁡|y| & =-\operatorname{cos}⁡x+C\end{aligned}
$$

Therefore, the general solution to the differential equation (in implicit form) is

$$
\operatorname{ln}⁡|y|=-\operatorname{cos}⁡x+C
$$

- Wrong `\frac{1}{{y}^{2}}=\operatorname{sec}⁡x+C`; parameterized recipe: replace mathematical x and y components by x+h and y+k throughout this complete relation. Incorrect-operation intent is unresolved; numerical reproduction is not evidence of the source author’s intended mistake.

- Wrong `\operatorname{ln}⁡|y|=\operatorname{sec}⁡x+C`; parameterized recipe: replace mathematical x and y components by x+h and y+k throughout this complete relation. Incorrect-operation intent is unresolved; numerical reproduction is not evidence of the source author’s intended mistake.

- Wrong `y=\operatorname{cos}⁡x+C`; parameterized recipe: replace mathematical x and y components by x+h and y+k throughout this complete relation. Incorrect-operation intent is unresolved; numerical reproduction is not evidence of the source author’s intended mistake.

- Wrong `\frac{1}{{y}^{2}}=-\operatorname{cos}⁡x+C`; parameterized recipe: replace mathematical x and y components by x+h and y+k throughout this complete relation. Incorrect-operation intent is unresolved; numerical reproduction is not evidence of the source author’s intended mistake.

- Correct `\operatorname{ln}⁡|y|=-\operatorname{cos}⁡x+C`; parameterized recipe: replace mathematical x and y components by x+h and y+k throughout this complete relation. Incorrect-operation intent is unresolved; numerical reproduction is not evidence of the source author’s intended mistake.

## Stage 2 — generalized pattern

Find a general implicit family of a first-order separable ODE. Multiply by the reciprocal y factor, formally integrate with respect to x, cancel the differential using substitution, evaluate known power/exponential/trigonometric/inverse-trigonometric/logarithmic primitives, and absorb fixed nonzero integration-constant scales when the source does. Domains must keep the original ODE defined.

## Stage 3 — components and banks

Shared sentences are the exact source opening, integration instruction and implicit-solution conclusion. Complete TeX components are masked only inside math spans; commands, prose, differentials and function names are protected. x+h and y+k appear at every mathematical coordinate occurrence. Original h=k=0 recovers every original option, prompt, solution sentence and ordered mathematical row. Source-specific omissions (such as exp_affine having no extra dy-only row) are retained. There is one fixed solution independent of selected error.

The `standard` bank is an explicitly authored complete bank. It always contains the correct relation L=R+C, right sign reversal L=-R+C, and a spurious right factor L=2R+C. Two additional operations are chosen as a whole per family: exp families use e^(2(y+k))/2 instead of the exponential primitive and fail to integrate B(x); tan families use y+k or sec²(y+k) instead of tan; arcsin uses sin or arctan; log_exp uses y+k or exp(y+k); sec_log uses tan or sec²; sin_poly uses y+k or tan; power_cube, root_power and log_sin use the left integrand or right integrand instead of its primitive. `two_x_terms` omits the left power increment or the linear x primitive. `two_sided_terms` omits the linear y primitive or linear x primitive. These operations are documented exactly by the formulas in standard_bank; they are never mixed from a pooled recipe list.

## Stage 4 — reusable templates and constraints

Observed template: captured fixed math/prose mask → unit-slope translated component render → public observed bank or authored standard whole bank. Parameter domains are those in classification. The observed profile has source-specific correct designation; standard uses a freshly derived correct relation. All choices are checked as complete general-solution relations modulo nonzero constant scale and shifts. The domain/branch restrictions and implicit response criterion are checked separately. Option order is seeded and shuffled after assigning owned IDs; fixed content retains identity regardless of seed.

Authored moderate/hard template: formal ODE row → separated row → integral with dy/dx → cancelled dx row → dy substitution → individually displayed component integrals → component primitives → fixed final implicit relation. All formal rows are parsed back from the displayed TeX and independently checked. Exact symbolic mathematics is used; no rounding or plotted choices.

Mathematical-task fingerprint hashes the ODE and required domains, excluding bank/profile and shuffle. Content identity hashes version, actual prompt, actual fixed solution and sorted displayed bank. Full finite parameter spaces are enumerated in validation.
