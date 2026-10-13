# Template extraction: four stages

## 1. Specific source descriptions

### q-76186 / ratio

Evaluate the line integral of the function $f(x,y)=\frac{12x}{y-1}$ along the curve parametrized by $r(t)={t}^{2}\,i+(t+1)\,j\,$ for $t\in [\sqrt{2},\sqrt{6}].$

Original worked solution (presence is part of fidelity):

To calculate the line integral, we will use the formula

$$
{\int }_{C}f(x,y)\,\text{d}s={\int }_{a}^{b}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t.
$$

 

Since $r(t)={t}^{2}\,i+(t+1)\,j$, then along the curve we have $x={t}^{2}$ and $y=t+1.$

Computing ${r}^{′}(t)$ and $‖{r}^{′}(t)‖,$ we get the following:

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j \\  & =\frac{\text{d}}{\text{d}t}({t}^{2})\,i+\frac{\text{d}}{\text{d}t}(t+1)\,j \\  & =2t\,i+j \\ ‖{r}^{′}(t)‖ & =\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}} \\  & =\sqrt{(2t)^{2}+{1}^{2}} \\  & =\sqrt{4{t}^{2}+1}\end{aligned}
$$

Now, since $f(x,y)=\frac{12x}{y-1}$, we obtain

$$
\begin{aligned}f(r(t)) & =\frac{12{t}^{2}}{(t+1)-1} \\  & =\frac{12{t}^{2}}{t} \\  & =12t.\end{aligned}
$$

Therefore, we can write the integral as 

$$
\begin{aligned}{\int }_{C}f(x,y)\,\text{d}s & ={\int }_{\sqrt{2}}^{\sqrt{6}}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t \\  & ={\int }_{\sqrt{2}}^{\sqrt{6}}12t\sqrt{4{t}^{2}+1}\,\text{d}t.\end{aligned}
$$

We can solve this using the substitution $u=4{t}^{2}+1,$ $\text{d}u=8t\,\text{d}t$ as follows:

$$
\begin{aligned}{\int }_{\sqrt{2}}^{\sqrt{6}}12t\sqrt{4{t}^{2}+1}\,\text{d}t & ={\int }_{9}^{25}\frac{3}{2}{u}^{1/2}\text{d}u \\  & ={u}^{3/2}{|}_{9}^{25} \\  & ={25}^{3/2}-{9}^{3/2} \\  & =125-27 \\  & =98\end{aligned}
$$

### q-76187 / sin_cos

Evaluate the line integral $\displaystyle \int_(C)4yz\cos xds$, where the curve $C$ is parametrized by $r(t) = ti + \sin tj + k$ for $0 < t < \frac{π}{2}$.

Original worked solution (presence is part of fidelity):

[Absent in source.]

### q-167612 / cubic

Evaluate the line integral of the function $f(x,y)={x}^{3}+y$ along the curve parametrized by $r(t)=3t\,i+{t}^{3}\,j\,$ for $t\in [0,1].$

Original worked solution (presence is part of fidelity):

To calculate the line integral, we will use the formula

$$
{\int }_{C}f(x,y)\,\text{d}s={\int }_{a}^{b}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t.
$$

 

Since $r(t)=3t\,i+{t}^{3}\,j$, then along the curve we have $x=3t$ and $y={t}^{3}.$

Computing ${r}^{′}(t)$ and $‖{r}^{′}(t)‖,$ we get the following:

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j \\  & =\frac{\text{d}}{\text{d}t}(3t)\,i+\frac{\text{d}}{\text{d}t}({t}^{3})\,j \\  & =3\,i+3{t}^{2}\,j \\ ‖{r}^{′}(t)‖ & =\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}} \\  & =\sqrt{{3}^{2}+{(3{t}^{2})}^{2}} \\  & =\sqrt{9+9{t}^{4}} \\  & =3\sqrt{1+{t}^{4}}\end{aligned}
$$

Now, since $f(x,y)={x}^{3}+y$, we obtain

$$
\begin{aligned}f(r(t)) & =(3t)^{3}+{t}^{3} \\  & =27{t}^{3}+{t}^{3} \\  & =28{t}^{3}.\end{aligned}
$$

Therefore, we can write the integral as 

$$
\begin{aligned}{\int }_{C}f(x,y)\,\text{d}s & ={\int }_{0}^{1}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t \\  & ={\int }_{0}^{1}28{t}^{3}\cdot 3\sqrt{1+{t}^{4}}\,\text{d}t \\  & ={\int }_{0}^{1}84{t}^{3}\sqrt{1+{t}^{4}}.\end{aligned}
$$

We can solve this using the substitution $u=1+{t}^{4},$ $\text{d}u=4{t}^{3}\,\text{d}t$ as follows:

$$
\begin{aligned}{\int }_{0}^{1}84{t}^{3}\sqrt{1+{t}^{4}}\,\text{d}t & ={\int }_{1}^{2}21\cdot {u}^{1/2}\,\text{d}u \\  & =21\cdot \frac{2}{3}{u}^{3/2}{|}_{1}^{2} \\  & =14({2}^{3/2}-{1}^{3/2}) \\  & =14(2\sqrt{2}-1)\end{aligned}
$$

### q-76479 / cos_diagonal

Evaluate the line integral of the function $f(x,y)=\operatorname{cos}⁡x$  along the curve $C$ parametrized by $r(t)={t}^{2}\,i-{t}^{2}\,j$ for $0<t<\sqrt{\pi /2}.$

Original worked solution (presence is part of fidelity):

To calculate the line integral, we will use the formula

$$
{\int }_{C}f(x,y)\,\text{d}s={\int }_{a}^{b}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t.
$$

 

Since $r(t)={t}^{2}\,i-{t}^{2}\,j,$ then along the curve we have $x={t}^{2}$ and $y=-{t}^{2}.$

Computing ${r}^{′}(t)$ and $‖{r}^{′}(t)‖,$ we get the following:

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j \\  & =\frac{\text{d}}{\text{d}t}({t}^{2})\,i+\frac{\text{d}}{\text{d}t}(-{t}^{2})\,j \\  & =2t\,j-2t\,k \\ ‖{r}^{′}(t)‖ & =\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}} \\  & =\sqrt{(2t)^{2}+(-2t)^{2}} \\  & =\sqrt{8{t}^{2}} \\  & =2\sqrt{2}|t| \\  & =2\sqrt{2}t\end{aligned}
$$

Notice that $|t|=t$ because $t>0$ along the path of $C.$

Now, since $f(x,y)=\operatorname{cos}⁡x$, we obtain

$$
\begin{aligned}f(r(t)) & =\operatorname{cos}⁡{t}^{2}.\end{aligned}
$$

Therefore, we can write the integral as 

$$
\begin{aligned}{\int }_{C}f(x,y)\,\text{d}s & ={\int }_{0}^{\sqrt{\pi /2}}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t \\  & ={\int }_{0}^{\sqrt{\pi /2}}\operatorname{cos}⁡{t}^{2}\cdot 2\sqrt{2}\,t\,\text{d}t.\end{aligned}
$$

We can solve this using the substitution $u={t}^{2}$, $\text{d}u=2t\,\text{d}t$ as follows: 

$$
\begin{aligned}{\int }_{0}^{\sqrt{\pi /2}}\operatorname{cos}⁡{t}^{2}\cdot 2\sqrt{2}\,t\,\text{d}t & =\sqrt{2}{\int }_{0}^{\pi /2}\operatorname{cos}⁡u\,\,\text{d}u \\  & =\sqrt{2}\,\operatorname{sin}⁡u\,{|}_{0}^{\pi /2} \\  & =\sqrt{2}(1-0) \\  & =\sqrt{2}\end{aligned}
$$

### q-76484 / sine_line

Evaluate the line integral of the function $f(x,y)=\frac{{x}^{2}+{y}^{2}}{5},$ along the curve parametrized by $r(t)=⟨4\operatorname{sin}⁡t,\,-3\operatorname{sin}⁡t⟩$ for $t\in [0,\frac{\pi }{2}].$

Original worked solution (presence is part of fidelity):

To calculate the line integral, we will use the formula

$$
{\int }_{C}f(x,y)\,\text{d}s={\int }_{a}^{b}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t.
$$

 

Since $r(t)=⟨4\operatorname{sin}⁡t,\,-3\operatorname{sin}⁡t⟩,$ then along the curve we have $x=4\operatorname{sin}⁡t$ and $y=-3\operatorname{sin}⁡t.$   

Computing ${r}^{′}(t)$ and $‖{r}^{′}(t)‖,$ we get the following:

$$
\begin{aligned}r(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j \\  & =\frac{\text{d}}{\text{d}t}(4\operatorname{sin}⁡t)i+\frac{\text{d}}{\text{d}t}(-3\operatorname{sin}⁡t)j \\  & =4\operatorname{cos}⁡t\,i-3\operatorname{cos}⁡t\,j \\ ‖{r}^{′}(t)‖ & =\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}} \\  & =\sqrt{(4\operatorname{cos}⁡t)^{2}+(-3\operatorname{cos}⁡t)^{2}} \\  & =\sqrt{16{cos}^{2}+9{cos}^{2}⁡t} \\  & =\sqrt{25{cos}^{2}⁡t} \\  & =5|\operatorname{cos}⁡t| \\  & =5\operatorname{cos}⁡t\end{aligned}
$$

Notice that $|\operatorname{cos}⁡t|=\operatorname{cos}⁡t$ because $\operatorname{cos}⁡t\ge 0$ when $t\in [0,\frac{\pi }{2}].$

Now, since $f(x,y)=\frac{{x}^{2}+{y}^{2}}{5}$, we obtain

$$
\begin{aligned}f(r(t)) & =\frac{16{sin}^{2}⁡t+9{sin}^{2}⁡t}{5} \\  & =\frac{25{sin}^{2}⁡t}{5} \\  & =5{sin}^{2}⁡t.\end{aligned}
$$

Therefore, we can write the integral as

$$
\begin{aligned}{\int }_{C}f(x,y)\,\text{d}s & ={\int }_{0}^{\pi /2}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t \\  & ={\int }_{0}^{\pi /2}5{sin}^{2}⁡t\cdot 5\operatorname{cos}⁡t\,\text{d}t \\  & =25{\int }_{0}^{\pi /2}{sin}^{2}⁡t\cdot \operatorname{cos}⁡t\,\text{d}t.\end{aligned}
$$

   

We can solve this using the substitution $u=\operatorname{sin}⁡t,$ $\text{d}u=\operatorname{cos}⁡t\,\text{d}t$ as follows: 

$$
\begin{aligned}25{\int }_{0}^{\pi /2}{sin}^{2}⁡t\cdot \operatorname{cos}⁡t\,\text{d}t & =25{\int }_{0}^{1}{u}^{2}\,\text{d}u \\  & =25\cdot {\frac{{u}^{3}}{3}|}_{0}^{1} \\  & =25(\frac{1}{3}-0) \\  & =\frac{25}{3}\end{aligned}
$$

### q-76496 / space_ratio

Evaluate the line integral ${\int }_{C}\frac{y+z}{x}\,\text{d}s,$ where the curve $C$ is parametrized by $r(t)=t\,i+\frac{{t}^{2}}{2}\,j+\frac{{t}^{2}}{2}\,k$
for $1<t<\sqrt{2}.$

Original worked solution (presence is part of fidelity):

To calculate the line integral, we will use the formula

$$
{\int }_{C}f(x,y)\,\text{d}s={\int }_{a}^{b}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t.
$$

 

Since $r(t)=t\,i+\frac{{t}^{2}}{2}\,j+\frac{{t}^{2}}{2}\,k,$ then along the curve we have $x=t,$ $y=\frac{{t}^{2}}{2},$ and $z=\frac{{t}^{2}}{2}.$

Computing ${r}^{′}(t)$ and $‖{r}^{′}(t)‖,$ we get the following:

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j+\frac{\text{d}z}{\text{d}t}\,k \\  & =\frac{\text{d}}{\text{d}t}(t)\,i+\frac{\text{d}}{\text{d}t}(\frac{{t}^{2}}{2})\,j+\frac{\text{d}}{\text{d}t}(\frac{{t}^{2}}{2})\,k \\  & =i+t\,j+t\,k \\ ‖{r}^{′}(t)‖ & =\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}+{(\frac{\text{d}z}{\text{d}t})}^{2}} \\  & =\sqrt{{1}^{2}+{t}^{2}+{t}^{2}} \\  & =\sqrt{1+2{t}^{2}}\end{aligned}
$$

Now, if $f(x,y)=\frac{y+z}{x}$, then we obtain

$$
\begin{aligned}f(r(t)) & =\frac{\frac{{t}^{2}}{2}+\frac{{t}^{2}}{2}}{t}=t.\end{aligned}
$$

Therefore, we can write the integral as 

$$
\begin{aligned}{\int }_{C}\frac{y+z}{x}\,\text{d}s & ={\int }_{1}^{\sqrt{2}}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t \\  & ={\int }_{1}^{\sqrt{2}}t\sqrt{1+2{t}^{2}}\,\text{d}t.\end{aligned}
$$

We can solve this using the substitution $u=1+2{t}^{2}$, $\text{d}u=4t\,\text{d}t$ as follows: 

$$
\begin{aligned}{\int }_{1}^{\sqrt{2}}t\sqrt{1+2{t}^{2}}\,\text{d}t & ={\int }_{3}^{5}\sqrt{u}\cdot \frac{1}{4}\,\text{d}u \\  & =\frac{1}{4}{\int }_{3}^{5}{u}^{1/2}\,\text{d}u \\  & =\frac{1}{4}\cdot \frac{2}{3}{u}^{3/2}\,{|}_{3}^{5} \\  & =\frac{1}{6}({5}^{3/2}-{3}^{3/2}) \\  & =\frac{5\sqrt{5}-3\sqrt{3}}{6}\end{aligned}
$$

## 2. Shared pattern

Evaluate ∫C f ds by substituting actual coordinates, formally differentiating the supplied parametrization, taking speed (not speed squared), multiplying f(r(t)) by speed, choosing an elementary u substitution, changing both bounds, integrating, evaluating BOTH primitive endpoints, and collecting arithmetic. Six distinct source masks preserve the source operation sequences. Normal masks retain the opening, coordinate prose, formal operators, magnitude, f-substitution, formal integral, concrete integral, u/differential, primitive and endpoint stages. Additional substitution and individual endpoint rows are explicit teaching additions rather than claimed source-exact rows.

## 3. Complete component / bank maps

Every historical scalar bank is opaque: source numbers alone do not identify its generating mistake. Public homogeneous scale recipes multiply the complete original component by scale k; the function and all scalar solution stages scale together, while curve/derivative/speed/bounds stay fixed. These mathematical covariance extensions reproduce every original value and are evidence-only; no arbitrary fitted polynomial or final-answer perturbation is claimed as recovered error intent. Historical banks are never selected as normal defaults.

### raw:q-76186

Field: selection; type :answer-field.type/radio

| Complete source value | Designation | Recipe |

|---|---|---|

| $56$ | incorrect | k·(complete displayed expression); opaque historical intent |

| $-64$ | incorrect | k·(complete displayed expression); opaque historical intent |

| $75$ | incorrect | k·(complete displayed expression); opaque historical intent |

| $-16$ | incorrect | k·(complete displayed expression); opaque historical intent |

| $98$ | correct | k·(complete displayed expression); opaque historical intent |

### raw:q-76187

Field: selection; type :answer-field.type/radio

| Complete source value | Designation | Recipe |

|---|---|---|

| $\frac{3}{2}(\sqrt{2} - 1)$ | undesignated | k·(complete displayed expression); opaque historical intent |

| $\frac{3\sqrt{2}}{4}$ | undesignated | k·(complete displayed expression); opaque historical intent |

| $\frac{1}{2}(2\sqrt{2} + 1)$ | undesignated | k·(complete displayed expression); opaque historical intent |

| $\frac{3\sqrt{2}}{2}$ | undesignated | k·(complete displayed expression); opaque historical intent |

| $\frac{4}{3}(2\sqrt{2} - 1)$ | undesignated | k·(complete displayed expression); opaque historical intent |

### raw:q-167612

Field: selection; type :answer-field.type/radio

| Complete source value | Designation | Recipe |

|---|---|---|

| $28\sqrt{2}$ | incorrect | k·(complete displayed expression); opaque historical intent |

| $14(2\sqrt{2}-1)$ | correct | k·(complete displayed expression); opaque historical intent |

| $7(2\sqrt{2}+1)$ | incorrect | k·(complete displayed expression); opaque historical intent |

| $7(\sqrt{2}-1)$ | incorrect | k·(complete displayed expression); opaque historical intent |

| $12\sqrt{2}-5$ | incorrect | k·(complete displayed expression); opaque historical intent |

### raw:q-76479

Field: selection; type :answer-field.type/radio

| Complete source value | Designation | Recipe |

|---|---|---|

| $2$ | incorrect | k·(complete displayed expression); opaque historical intent |

| $\sqrt{2}-1$ | incorrect | k·(complete displayed expression); opaque historical intent |

| $2-\sqrt{2}$ | incorrect | k·(complete displayed expression); opaque historical intent |

| $2\sqrt{2}$ | incorrect | k·(complete displayed expression); opaque historical intent |

| $\sqrt{2}$ | correct | k·(complete displayed expression); opaque historical intent |

### raw:q-76484

Field: selection; type :answer-field.type/radio

| Complete source value | Designation | Recipe |

|---|---|---|

| $\frac{5}{3}$ | incorrect | k·(complete displayed expression); opaque historical intent |

| $\frac{2}{5}$ | incorrect | k·(complete displayed expression); opaque historical intent |

| $\frac{25}{3}$ | correct | k·(complete displayed expression); opaque historical intent |

| $\frac{5}{2}$ | incorrect | k·(complete displayed expression); opaque historical intent |

| $\frac{20}{3}$ | incorrect | k·(complete displayed expression); opaque historical intent |

### raw:q-76496

Field: selection; type :answer-field.type/radio

| Complete source value | Designation | Recipe |

|---|---|---|

| $\frac{\sqrt{5}+\sqrt{3}}{3}$ | incorrect | k·(complete displayed expression); opaque historical intent |

| $\frac{\sqrt{5}+3}{2}$ | incorrect | k·(complete displayed expression); opaque historical intent |

| $5\sqrt{5}-3\sqrt{3}$ | incorrect | k·(complete displayed expression); opaque historical intent |

| $\sqrt{5}+\sqrt{3}$ | incorrect | k·(complete displayed expression); opaque historical intent |

| $\frac{5\sqrt{5}-3\sqrt{3}}{6}$ | correct | k·(complete displayed expression); opaque historical intent |

## 4. Reusable masks and guarded variation

Raw prompt masks replace exactly one complete integrand component. Raw worked solutions are tokenized at display blocks: derivative and speed remain intact; every concrete f(r) component and scalar integral/primitive/evaluated component is multiplied by k, including the first integral LHS. Symbolic f(r) references incorporate k already and are not multiplied again. Scale 1 is ordinary parameter rendering of these same masks, not a literal-payload or answer-table return branch. Exact raw source prose, field layout, enum spelling, rating omission, solution omission and correct-ref omission are retained. UUID ownership is generated locally and source database identities are not transplanted.

Normal families vary the actual curve/integrand/bounds under finite workload guards (see script domain function). Algebraic radicands remain exact; planar ratio bounds give odd integer square roots of u. Cubic coefficients and fourth powers retain their substitution workload. Trig evaluation angles are π/2, π/3, or π/6 as applicable; cosine sign domains stay fixed. Hard always retains all three nonzero velocity components and nonzero radical endpoint subtraction. Easy always remains direct y substitution and zero lower parameter bound.

Authored COMPLETE banks (one eligible operation bank per family): algebraic families use omitted substitution differential, square-root rather than three-halves primitive, addition of endpoint values, and omitted speed. Diagonal cosine uses missing 2a differential, cosine instead of sine primitive, unchanged old parameter bounds, and signed velocity sum instead of Euclidean speed. Sine-line uses omitted speed, actual speed squared (integral of sin²cos²), missing cubic reciprocal, and a square primitive. Sin/cos uses omitted speed, actual speed squared, omitted negative differential factor, and square-root primitive. All members are derived from method inputs; all are computed before whole-instance equivalence rejection.

## Source defects, inference and denominators

q-76187 independently gives 4/3(2√2−1): r′=(1,cos t,0), speed=√(1+cos²t), f(r)=4 sin t cos t. Let u=1+cos²t and du=−2 sin t cos t dt, so −2∫₂¹√u du=4/3(2√2−1). This matches the fifth EDB option. Original key, difficulty and worked solution are absent. Raw replay retains their absence; normal `sin_cos` uses an inferred correct ref, authored moderate assignment and complete worked solution. It cannot count as matched original designation.

q-76479 source derivative uses j and k for a planar i,j curve; its component magnitudes and final answer are right. q-76484 source derivative LHS says r(t), not r′(t), and one cosine-squared summand lacks t. Normal solutions correct these teaching defects. q-167612 has a concrete integrand row lacking dt; normal display includes it. Three-variable source solutions retain f(x,y) in their generic formula; normal output uses f without misdeclaring its arity. Raw-exact solutions: five of five present. Normal corrected solutions are separately audited and are not claimed verbatim exact.

The canonical ratio at t=0 is undefined before cancellation; only the limiting integrand is finite. It is context, not a practice fidelity denominator. Easy uses a nonsingular linear f in y.

No new algebraic branches, integration by parts, direct elementary-only integration, or vector-field line integral methods are added. Scalars are exact and no numerical rounding is introduced.
