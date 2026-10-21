# Quiz 2: preparation for textbook sections 2.2-2.6

Prepared October 19, 2026 for MTH 256. Textbook: William F. Trench, *Elementary Differential Equations*, free edition 1.01, December 2013. [Open the textbook][textbook]. Page numbers below refer to the printed pages; the PDF viewer's page numbers are ten higher.

## What to prioritize

The professor's announcement identifies sections 2.2-2.6 as the scope, with **most preparation focused on sections 2.2-2.3**. Problems from later sections will be guided in a manner similar to Recitation 3; the main computational difficulty is expected to be separation of variables. The professor also clarified that the integration on the quiz will involve **power and exponential functions**.

Prepare to solve separable equations and initial-value problems independently, including constant solutions, branch selection, and solution intervals. Give existence and uniqueness its own review session: solving equations alone does not prepare you for section 2.3. Then practice following the transformations and intermediate steps used in sections 2.4-2.6.

This report distinguishes the textbook's full coverage from the announced emphasis. The additional exercise topics listed below are part of the book, not a prediction that every one will appear on the quiz. Recitation 3 and the promised review activity/key were not supplied or reviewed; use those materials to refine the remaining priorities when available.

| Priority | Material | What you should be able to do |
| --- | --- | --- |
| Highest | 2.2: separation and IVPs | Separate correctly, integrate, impose initial data, and give a valid solution. |
| Highest | 2.2: exceptional solutions and domains | Recover solutions excluded by division, choose the correct branch, and find the open solution interval containing the initial point. |
| Highest | 2.3: existence and uniqueness | Identify where the theorem applies and state exactly what it guarantees. |
| Next | 2.4: substitutions | Differentiate the supplied substitution, solve the resulting separable equation, and substitute back. |
| Next | 2.5: exact equations | Check exactness and construct an implicit solution from partial derivatives. |
| Next | 2.6: integrating factors | Apply or verify the supplied factor, recognize the one-variable tests, and solve the resulting exact equation. |

## Math Academy lessons and target status

The matches below were checked against lesson examples/questions, not just titles. Foundations lessons were searched first, followed by Differential Equations. The separation lessons occur in both courses under the same MA topic identities; the Foundations codes are shown here.

All seven lessons are now in your `:learner/targets`. The three additions committed on October 19 were **3184, 2521, and 6353**. The target count increased from **138 to 141**, with all previous targets preserved; verification used EDB basis **4731**. Target membership records a study destination, not completion or demonstrated mastery.

| Order | Verified lesson | MA ID | Coverage and status |
| --- | --- | ---: | --- |
| 1 | [MF3 12.1.4: Solving First-Order ODEs Using Separation of Variables][ma-separation] | 466 | Direct match for separating and finding implicit/explicit solution families. Already targeted. |
| 2 | [MF3 12.1.5: Solving First-Order IVPs Using Separation of Variables][ma-ivp] | 1179 | Direct match for solving a separable IVP. Already targeted. |
| 3 | [DEQ 1.4.2: Equilibrium Solutions of First-Order ODEs][ma-equilibria] | 3184 | Component coverage for finding constant solutions; the inspected examples are autonomous. Added. |
| 4 | [DEQ 1.2.2: Homogeneous First-Order ODEs][ma-homogeneous] | 878 | Direct match for using `y = xv` to obtain and solve a separable equation. Already targeted. |
| 5 | [DEQ 1.2.5: Bernoulli Differential Equations][ma-bernoulli] | 2522 | Same equation family; MA uses a different substitution from the textbook. Already targeted. |
| 6 | [DEQ 1.2.3: Exact Differential Equations][ma-exact] | 2521 | Direct match for testing exactness, constructing a potential, and solving exact IVPs. Added. |
| 7 | [DEQ 1.2.4: Solving Exact ODEs Using Integrating Factors][ma-factors] | 6353 | Direct coverage of one-variable factors and verification of given factors; partial coverage of the full textbook section. Added. |

For access from your MacBook while connected to Tailscale, open the corresponding Course Academy topic: [466][app-separation], [1179][app-ivp], [3184][app-equilibria], [878][app-homogeneous], [2522][app-bernoulli], [2521][app-exact], or [6353][app-factors]. These are topic-reference pages; availability of a practice activity is a separate application check.

## Section 2.2: Separable Equations

### Textbook coverage

The section begins on printed page 45. Its instructional examples are 2.2.1-2.2.6.

1. **Recognizing and separating an equation.** Rewrite it as

   $$h(y)y'=g(x).$$

   If $H'=h$ and $G'=g$, integration gives

   $$H(y)=G(x)+C.$$

2. **Implicit versus explicit solutions.** Solve for $y$ when practical, but recognize that an implicit relation can describe valid solution branches even when an explicit formula is unavailable. An implicit curve is not automatically one differentiable function on its entire domain.
3. **Initial conditions and branch selection.** Use $(x_0,y_0)$ to determine the constant and select the sign or branch that passes through the initial point. Example 2.2.2 illustrates semicircle branches of the same implicit family.
4. **Local solvability of the implicit relation.** Theorem 2.2.1 gives conditions under which $H(y)=G(x)+C$ defines a local solution, including $h(y_0)\ne0$ and the relevant continuity assumptions.
5. **Constant solutions lost during division.** For $y'=g(x)p(y)$, division by $p(y)$ excludes its zeros. Test each excluded constant in the original equation. A constant solution may or may not appear as a special value of the integration constant in the nonconstant family.
6. **Intervals of validity.** Find the connected open interval containing $x_0$ on which the selected solution is real, differentiable, and satisfies the original equation. Check the original equation's denominators as well as the solution formula's denominators and radicals.
7. **Linear versus nonlinear behavior.** Nonlinear equations can have exceptional solutions outside a displayed one-parameter family, and their solution intervals can depend on the initial value. Example 2.2.6 makes this dependence explicit.

The exercise set also includes direction fields and integral curves; logistic population and epidemic models; cure or harvesting terms; long-term behavior; bifurcation parameters; and some transformations using variation of parameters. Some exercises use inverse trigonometric integration, logarithms, or partial fractions. These extend beyond the narrow integration practice now worth prioritizing.

### Focus and MA gaps

Use the two separation lessons for the main computational method. They contain actual separation, implicit/explicit solution, and IVP tasks. Add the equilibrium lesson for the component skill of finding constants, then transfer that idea to nonautonomous products $g(x)p(y)$ by checking the original equation.

**MA does not fully cover the textbook's combination of exceptional solutions, branch selection, and maximal solution intervals in these lessons.** Review Examples **2.2.2, 2.2.4, and 2.2.6** directly. The [Continuity of Functions][ma-continuity] lesson supplies supporting practice with intervals and domain restrictions, but is not an ODE solution-interval lesson.

## Section 2.3: Existence and Uniqueness of Solutions of Nonlinear Equations

### Textbook coverage

The section begins on printed page 55. The central result is **Theorem 2.3.1**, on printed page 56, for

$$y'=f(x,y),\qquad y(x_0)=y_0.$$

| Hypotheses on an open rectangle containing $(x_0,y_0)$ | Conclusion |
| --- | --- |
| $f$ is continuous throughout the rectangle. | At least one solution exists on some open interval containing $x_0$. |
| Both $f$ and $f_y$ are continuous throughout the rectangle. | A unique solution exists on some open interval containing $x_0$. |

The section teaches you to:

- Compute $f_y$ while treating $x$ as constant.
- Identify excluded points, curves, or boundaries caused by denominators, logarithms, radicals, and fractional powers, and determine whether a suitable open rectangle can surround the initial point.
- Distinguish an existence guarantee from a uniqueness guarantee.
- Recognize that these are **sufficient conditions**. If a hypothesis fails, the theorem is inconclusive; failure is not proof that there is no solution or that there are multiple solutions.
- Distinguish local conclusions from global ones. Continuity of $f$ and $f_y$ on the entire plane does not, by itself, prevent finite-time blow-up of a solution.
- Use uniqueness to explain why a different solution cannot meet a constant solution at a point where the theorem's uniqueness hypotheses hold locally.
- Exhibit nonuniqueness when uniqueness hypotheses fail, including the zero solution and nonzero solutions through the same point.
- Understand solutions that agree on an interval and branch apart later, including piecewise constructions. An interval on which a solution formula is valid can be larger than an interval on which that IVP's solution is unique.

Examples **2.3.1-2.3.3** illustrate continuity regions. Example **2.3.4** applies uniqueness to constant solutions. Examples **2.3.5-2.3.8** distinguish existence, local uniqueness, multiple solutions, and the largest interval of uniqueness. Exercises add classification tasks, verification of piecewise solutions, and proofs of the constant-solution/noncrossing conclusions.

### Focus and MA gaps

**No whole-task MA equivalent was verified for this section's existence-and-uniqueness analysis.** The scoped Foundations and DEQ searches, followed by the global catalog fallback, did not establish an equivalent lesson. The title *Qualitative Analysis of First-Order ODEs* is not a substitute: its inspected tasks concern stationary points and second derivatives, rather than this theorem.

Useful component lessons are [Computing Partial Derivatives Using the Rules of Differentiation][ma-partials] and [The Domain of a Multivariable Function][ma-domain]. These come from **Multivariable Calculus**, outside the normal Foundations/DEQ route. Their verified contributions are differentiating $f$ and identifying domain restrictions; neither supplies the ODE theorem or its local/global interpretation.

Give this section direct textbook practice even if all seven MA target lessons have been studied. Learn to answer separately: **Does the theorem guarantee existence? Does it guarantee uniqueness? What remains undecided?**

## Section 2.4: Transformation of Nonlinear Equations into Separable Equations

### Textbook coverage

The section starts at the bottom of printed page 62; the main development begins on page 63.

**Bernoulli equations.** For

$$y'+p(x)y=f(x)y^r,\qquad r\ne0,1,$$

the textbook first finds a nonzero solution $y_1$ of $y_1'+p(x)y_1=0$, then substitutes

$$y=u(x)y_1(x),\qquad y'=u'y_1+uy_1'.$$

The linear terms cancel, leaving the separable equation

$$u'=f(x)y_1(x)^{r-1}u^r.$$

Solve for $u$, substitute back for $y$, apply initial data when present, and check any solutions excluded by division. Example 2.4.1 demonstrates this method.

**More general multiplicative substitutions.** The section explains when a suitably chosen $y=u y_1(x)$ converts another nonlinear equation into a separable one. A guided problem can supply $y_1$ and ask you to carry out the transformation and finish the separation.

**Homogeneous nonlinear equations.** When

$$y'=q(y/x),$$

use $y=xu$, so $y'=u+xu'$ and

$$xu'=q(u)-u.$$

Check constant $u$ satisfying $q(u)=u$ before dividing by $q(u)-u$. Such constants produce straight-line solutions $y=ux$, which are not generally constant solutions for $y$. Solve the remaining separable equation and substitute back. Examples 2.4.2-2.4.3 cover this process, IVPs, and complications at $x=0$.

The word **homogeneous** here means dependence on $y/x$; it has a different meaning from “homogeneous linear equation.” The substitution requires care at $x=0$, even when the original equation has solutions extending through it.

Exercises extend this material to shifted coordinates for ratios of affine expressions, other choices of $y_1$, direction fields and scaling, implicit solutions and solution intervals, time-dependent logistic/Bernoulli models, and generalized Riccati equations with a known solution.

### Focus and MA gaps

The homogeneous ODE lesson matches the textbook's $y=xu$ method directly. Be especially comfortable using the product rule, canceling terms, and converting the initial condition into a condition on $u$.

The Bernoulli lesson covers the **same equation family**, but MA uses $z=y^{1-r}$ to obtain a linear equation. That is a valid alternative solution method; it does **not** rehearse the textbook's $y=u y_1$ transformation into a separable equation. Practice the textbook method so that you can follow a supplied substitution during a guided quiz problem.

No full equivalent was verified for the entire collection of more general $y=u y_1$ transformations or the section's exceptional continuation/uniqueness analysis. The ordinary separation and homogeneous lessons cover useful components without closing those gaps.

## Section 2.5: Exact Equations

### Textbook coverage

The section begins on printed page 73. Write the equation as

$$M(x,y)\,dx+N(x,y)\,dy=0.$$

The book discusses both interpretations, with $y$ depending on $x$ or $x$ depending on $y$, and uses an implicit relation $F(x,y)=C$ to describe solutions.

An equation is exact when a potential function satisfies

$$F_x=M,\qquad F_y=N.$$

Under the stated continuity assumptions on an open rectangle, the exactness test is

$$M_y=N_x.$$

Equality only on a line or at one point is insufficient. To solve an exact equation:

1. Check exactness.
2. Integrate $M$ with respect to $x$, treating $y$ as constant: $F=G(x,y)+\phi(y)$.
3. Differentiate with respect to $y$ and impose $F_y=N$, giving $\phi'=N-G_y$.
4. Integrate for $\phi$ and write **$F(x,y)=C$**. The potential $F$ alone is not the implicit solution.
5. Apply initial conditions, then solve explicitly if practical.

You can instead integrate $N$ with respect to $y$ and add an unknown function of $x$; choose whichever direction makes integration easier. If the equation is inexact, the construction fails because the proposed derivative of the unknown one-variable function still depends on the other variable.

Examples cover verification of an implicit solution, the exactness condition, both reconstruction directions, choosing the easier integral, and failure on an inexact equation. Exercises add exact IVPs; missing coefficients or parameter conditions for exactness; direction fields and intervals; definite-integral formulas for the potential; links between separability and exactness; and harmonic functions and harmonic conjugates.

### Focus and MA gaps

The exact-equations lesson is a direct match for the main method, including rearranging a $y'$ equation into differential form and imposing initial conditions. Keep polynomial and exponential examples first under the professor's integration restriction.

The match does not establish coverage of every extension or proof in the exercise set, especially harmonic conjugates and the integral reconstruction proofs. Those are lower-priority extensions unless the recitation/review materials emphasize them. Existence, uniqueness, and maximal-domain arguments attached to an exact IVP still require the separate textbook review above.

## Section 2.6: Integrating Factors

### Textbook coverage

The section begins on printed page 83 and ends on page 93. An integrating factor $\mu(x,y)$ makes

$$\mu M\,dx+\mu N\,dy=0$$

exact. Verify a proposed factor by checking $(\mu M)_y=(\mu N)_x$, then solve the resulting exact equation.

**Factors depending only on $x$.** If

$$\frac{M_y-N_x}{N}=p(x)$$

depends only on $x$ on the working region, a factor is

$$\mu(x)=e^{\int p(x)\,dx}.$$

**Factors depending only on $y$.** If

$$\frac{N_x-M_y}{M}=q(y)$$

depends only on $y$, a factor is

$$\mu(y)=e^{\int q(y)\,dy}.$$

The opposite numerator signs in these two formulas matter. Use each ratio only where its denominator is nonzero and the required continuity conditions hold. Failure of these tests does not prove that no integrating factor exists.

**Product factors.** The section also searches for $\mu=P(x)Q(y)$. With $p=P'/P$ and $q=Q'/Q$, the condition becomes

$$M_y-N_x=p(x)N-q(y)M.$$

Some examples reduce this to matching coefficients for factors of the form $x^a y^b$ on suitable domains. These are not covered by merely memorizing the one-variable formulas.

**Exceptional solutions.** Multiplication preserves equivalence where the factor is defined and nonzero. Zeros or singularities of the factor can introduce apparent solutions or exclude original ones. Check affected curves in the original equation.

Examples 2.6.1-2.6.2 find one-variable factors. Examples 2.6.3-2.6.4 find product factors, including a way to avoid an unpleasant integral. Exercises include verification of proposed factors, lost or added solutions, product-factor families and proofs, and deriving the usual integrating-factor formula for linear first-order equations.

### Focus and MA gaps

The MA integrating-factor lesson covers the one-variable tests, verification of supplied factors, and solving the resulting exact equation. It includes verification of a given two-variable factor, but **no equivalent instruction was verified for discovering general $P(x)Q(y)$ or $x^a y^b$ factors**.

Review textbook Examples **2.6.3-2.6.4** at the level of following a guided derivation. The book's checks for solutions gained or lost through singular factors also need direct review. The separate MA lesson *Solving First-Order Linear ODEs Using Integrating Factors* is already targeted, but does not replace this section's exact-equation material.

## Integration preparation under the professor's clarification

Be fluent with

$$\int u^n\,du=\frac{u^{n+1}}{n+1}+C\quad(n\ne-1),$$

$$\int e^{au}\,du=\frac{e^{au}}a+C\quad(a\ne0),$$

and constants, sums, negative powers, and fractional powers. In a separated equation, integrate the $y$ side with respect to $y$ and the $x$ side with respect to $x$. The same rule applies to a substituted variable $u$.

Keep the power-rule exception available:

$$\int u^{-1}\,du=\ln|u|+C.$$

The wording “power functions” does not explicitly exclude exponent $-1$. Likewise, a logarithm can appear in a solution even when the original right-hand side contains powers or exponentials. Do not use the ordinary power-rule formula when $n=-1$.

For targeted refreshers, use [The Sum Rule for Indefinite Integrals][ma-power], [Integrating Exponential Functions][ma-exponentials], and, if needed, [Integrating the Reciprocal Function][ma-reciprocal]. These are supporting lessons, not additional targets added by this request.

Dedicated partial-fractions, trigonometric/inverse-trigonometric integration, and advanced integration-by-parts review should not take priority over the announced core. The phrase “power and exponential functions” alone does not formally rule out a product such as $xe^x$, so use the professor's review/key to settle any technique ambiguity. Textbook Example 2.4.1 contains such a product; the simpler Bernoulli practice below avoids making that integral the first task.

The restriction concerns **integration**. Trigonometric functions, logarithms, or radicals can still appear in a question asking about continuity, domains, or the existence/uniqueness theorem without requiring their integration.

## Remaining gaps to cover directly

| Gap | Useful MA coverage | Direct preparation |
| --- | --- | --- |
| Applying the nonlinear existence/uniqueness theorem | Partial derivatives and multivariable domain restrictions only | Theorem 2.3.1; Examples 2.3.1-2.3.8; classification exercises |
| Complete separable solutions with exceptional cases and maximal intervals | Separation, IVPs, and autonomous equilibrium components | Examples 2.2.2, 2.2.4, 2.2.6 |
| Distinguishing validity from uniqueness, including piecewise continuation | No whole-task equivalent verified | Examples 2.3.6-2.3.8; revisit the discussion in Example 2.4.3 if needed |
| Bernoulli/general transformations using $y=u y_1(x)$ | Same Bernoulli equation family via a different substitution; separation as a component | Section 2.4's derivation and textbook-method practice |
| Discovering product integrating factors | Given-factor verification, one-variable tests, and exact solving | Examples 2.6.3-2.6.4 |
| Solutions gained/lost through a singular integrating factor | Basic factor verification does not establish this full analysis | Section 2.6's opening discussion and Exercises 1-2 |

“No equivalent verified” describes the inspected local lesson library; it is not a claim that no such instruction could exist elsewhere. Adding targets addresses the three missing target memberships, not these instructional gaps.

## A focused practice sequence

Work the first two rows before investing heavily in the later methods. This selection emphasizes power/exponential integration and conceptual theorem work, rather than reproducing the book's harder integration exercises.

| Stage | Textbook practice | Check before moving on |
| --- | --- | --- |
| Separation and IVPs | 2.2 Exercises **1, 11, 19, 21**; Examples **2.2.4, 2.2.6** | Correct separation, constants, branches, exceptional solutions, and solution intervals |
| Existence/uniqueness | 2.3 Exercises **1, 5, 8, 12**; Examples **2.3.5-2.3.8** | Separate existence and uniqueness answers, justified by regions of continuity; no unsupported global claim |
| Guided substitutions | 2.4 Exercise **1** using the textbook's $y=u y_1$ method; Example **2.4.2** | Differentiate the substitution correctly, separate, solve, substitute back, and check excluded cases |
| Exact equations | 2.5 Exercises **1, 4** | Correct cross-partials, the missing function of the other variable, and final $F=C$ |
| Integrating factors | 2.6 Exercise **6**; guided reading of Example **2.6.3** | Correct one-variable test or supplied factor, exact reconstruction, and original-equation checks |

The earlier suggested 2.2 Exercises 3 and 12 lead to partial fractions when separated. They are not the best first choices after the integration clarification; the selection above replaces them.

Before the quiz, check that you can do the following without notes:

- [ ] Solve a separable IVP involving powers or exponentials.
- [ ] List any valid constant solutions excluded by division.
- [ ] Select the branch through the initial point and give its valid open interval.
- [ ] Compute $f_y$ and state the existence/uniqueness theorem's two conclusions separately.
- [ ] Explain why failure of a sufficient hypothesis is inconclusive.
- [ ] Explain why local uniqueness does not guarantee a global solution or global uniqueness.
- [ ] Follow a supplied substitution through differentiation, separation, and back-substitution.
- [ ] Check exactness and finish an exact equation with an implicit relation $F=C$.
- [ ] Apply or verify an integrating factor and check exceptional cases in the original equation.

## Sources and verification

- [Trench textbook][textbook], sections 2.2-2.6, printed pages 45-93. The report covers the main development and catalogs the exercise extensions separately.
- Professor Pat's announcement and the integration clarification supplied in this conversation. The allocation of study time is a recommendation based on those statements, not an additional promise about the quiz.
- The linked local Math Academy lesson Markdown, inspected for worked examples/questions. MA IDs identify shared topics even when course codes differ.
- Live `math` EDB: the three requested additions were committed and all seven listed lessons verified as targets at basis 4731. This report does not assess your mastery or completion history.

[textbook]: </home/jake/Downloads/ElementaryDifferentialEquations.pdf>
[ma-separation]: <../study/MA/Mathematical-Foundations/MF3/12. Differential Equations/12.1. Introduction to Differential Equations/Lessons/12.1.4. Solving First-Order ODEs Using Separation of Variables.md>
[ma-ivp]: <../study/MA/Mathematical-Foundations/MF3/12. Differential Equations/12.1. Introduction to Differential Equations/Lessons/12.1.5. Solving First-Order IVPs Using Separation of Variables.md>
[ma-equilibria]: <../study/MA/Mathematical-Analysis-&-Modeling/DEQ/1. First-Order Differential Equations/1.4. Qualitative Techniques for Differential Equations/Lessons/1.4.2. Equilibrium Solutions of First-Order ODEs.md>
[ma-homogeneous]: <../study/MA/Mathematical-Analysis-&-Modeling/DEQ/1. First-Order Differential Equations/1.2. Special First-Order Equations/Lessons/1.2.2. Homogeneous First-Order ODEs.md>
[ma-bernoulli]: <../study/MA/Mathematical-Analysis-&-Modeling/DEQ/1. First-Order Differential Equations/1.2. Special First-Order Equations/Lessons/1.2.5. Bernoulli Differential Equations.md>
[ma-exact]: <../study/MA/Mathematical-Analysis-&-Modeling/DEQ/1. First-Order Differential Equations/1.2. Special First-Order Equations/Lessons/1.2.3. Exact Differential Equations.md>
[ma-factors]: <../study/MA/Mathematical-Analysis-&-Modeling/DEQ/1. First-Order Differential Equations/1.2. Special First-Order Equations/Lessons/1.2.4. Solving Exact ODEs Using Integrating Factors.md>
[ma-continuity]: <../study/MA/Mathematical-Foundations/MF3/7. Limits & Continuity/7.2. Continuity/Lessons/7.2.1. Continuity of Functions.md>
[ma-partials]: <../study/MA/Mathematical-Analysis-&-Modeling/MVC/2. Multivariable Functions/2.3. Partial Derivatives/Lessons/2.3.2. Computing Partial Derivatives Using the Rules of Differentiation.md>
[ma-domain]: <../study/MA/Mathematical-Analysis-&-Modeling/MVC/2. Multivariable Functions/2.1. Introduction to Multivariable Functions/Lessons/2.1.4. The Domain of a Multivariable Function.md>
[ma-power]: <../study/MA/Mathematical-Foundations/MF2/12. Introduction to Calculus/12.4. Indefinite Integrals/Lessons/12.4.3. The Sum Rule for Indefinite Integrals.md>
[ma-exponentials]: <../study/MA/Mathematical-Foundations/MF2/12. Introduction to Calculus/12.4. Indefinite Integrals/Lessons/12.4.5. Integrating Exponential Functions.md>
[ma-reciprocal]: <../study/MA/Mathematical-Foundations/MF2/12. Introduction to Calculus/12.4. Indefinite Integrals/Lessons/12.4.4. Integrating the Reciprocal Function.md>
[app-separation]: https://eve.taild9e59b.ts.net:8443/topic?topic=466
[app-ivp]: https://eve.taild9e59b.ts.net:8443/topic?topic=1179
[app-equilibria]: https://eve.taild9e59b.ts.net:8443/topic?topic=3184
[app-homogeneous]: https://eve.taild9e59b.ts.net:8443/topic?topic=878
[app-bernoulli]: https://eve.taild9e59b.ts.net:8443/topic?topic=2522
[app-exact]: https://eve.taild9e59b.ts.net:8443/topic?topic=2521
[app-factors]: https://eve.taild9e59b.ts.net:8443/topic?topic=6353
