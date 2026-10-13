# Improper integrals using substitution

Source snapshot: basis 1980, immutable lineage 01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1. All 17 practice records and the canonical example are retained under reference/initial/. None requires plots.

Each template asks for the convergent integral C*x^(n-1)/(A*x^n+B)^p from L to infinity. Substitution u=A*x^n+B converts it to a power integral; positivity of the substitution base and p>1 establish convergence. Moderate uses affine substitutions; hard uses nonlinear power substitutions. Exact-answer and radio layouts are separate, as are radical/integer denominator forms and different variables/lower bounds. There are four moderate families and three hard families, separated by affine/power substitution, radical/integer denominator notation and blank/radio response layout. Numeric and variable changes do not create new families. Sixteen concrete source rendering profiles retain exact original typography and complete banks. The generator selects those source profiles; its reproducibility `template` key is the concrete rendering profile, mapped to these families in templates.json.

Variants scale C by an integer 1..1000. They preserve the original complete bank, field shape, variables, domain and mathematical steps. Numeric distractors scale by the same multiplier; divergence text stays fixed. These are observed value patterns with unresolved error interpretations, not inferred new mistake recipes. Scaling is justified by linearity; all other parameters remain fixed. Source scale 1 replays the exact original Markdown and bank. Variants use a disclosed notation/layout extension for the same fixed substitution, derivative, bounds table, transformed integral, antiderivative and limit sequence.

## q-118619

Evaluate the integral ${\int }_{0}^{\infty }\frac{x}{{(1+{x}^{2})}^{2}}\,\text{d}x.$

Observed components: {"C": 1, "n": 2, "A": 1, "B": 1, "p": "2", "lower": 0, "variable": "x", "radical": false, "domain": "x >= 0; 1*x^2+1>0", "correct_formula": "C/[A*n*(p-1)] * (A*L^n+B)^(1-p)"}.

Field and complete bank: [{"source_answer_id": "5844549f-b897-5a58-bf08-acfbe8efa2a6", "source_value": "0", "correct": false, "recipe": "scale * (0)", "recipe_at_original_parameters": "0", "interpretation": "Observed complete value pattern; error mechanism unresolved", "full_value_replayed": true}, {"source_answer_id": "7667e2f4-ee83-5482-af7c-d2bdd84fc202", "source_value": "\\frac{1}{2}", "correct": true, "recipe": "scale * (\\frac{1}{2})", "recipe_at_original_parameters": "\\frac{1}{2}", "interpretation": "exact convergent limit", "full_value_replayed": true}, {"source_answer_id": "a218e653-d88f-5440-be12-f0ad6810fe89", "source_value": "The integral diverges", "correct": false, "recipe": "unchanged divergence text", "recipe_at_original_parameters": "The integral diverges", "interpretation": "Observed complete value pattern; error mechanism unresolved", "full_value_replayed": true}, {"source_answer_id": "c7cc8e9f-2139-5926-aacc-b95747012288", "source_value": "2", "correct": false, "recipe": "scale * (2)", "recipe_at_original_parameters": "2", "interpretation": "Observed complete value pattern; error mechanism unresolved", "full_value_replayed": true}, {"source_answer_id": "f79ecc31-c3ea-5c7d-ae4d-ea007b99bc9d", "source_value": "1", "correct": false, "recipe": "scale * (1)", "recipe_at_original_parameters": "1", "interpretation": "Observed complete value pattern; error mechanism unresolved", "full_value_replayed": true}]

Original fixed solution:

First, we substitute $u=1+{x}^{2}.$ Differentiating, we get

$$
\frac{\text{d}u}{\text{d}x}=2x\,⟹\,\frac{1}{2}\text{d}u=x\,\text{d}x.
$$

Since $u\to \infty $ when $x\to \infty ,$ the table for the limits of integration using the rule $u=1+{x}^{2}$ is as follows:

| $x$ | $0$ | $\infty $ |
| --- | --- | --- |
| $u$ | $1$ | $\infty $ |

So, the integral in terms of the new variable $u$ is

$$
\begin{aligned}{\int }_{0}^{\infty }\frac{x}{{(1+{x}^{2})}^{2}}\,\text{d}x & =\frac{1}{2}{\int }_{1}^{\infty }\frac{1}{{u}^{2}}\,\text{d}u.\end{aligned}
$$

Finally, we proceed by setting the upper bound equal to some parameter $a,$ integrating as usual, and then taking the limit as $a\to \infty .$

$$
\begin{aligned}{\int }_{0}^{\infty }\frac{x}{{(1+{x}^{2})}^{2}}\,\text{d}x & =\frac{1}{2}{\int }_{1}^{\infty }\frac{1}{{u}^{2}}\,\text{d}u \\  & =\frac{1}{2}{\int }_{1}^{\infty }{u}^{-2}\,\text{d}u \\  & =\frac{1}{2}{lim}_{a\to \infty }{\int }_{1}^{a}{u}^{-2}\,\text{d}u \\  & =\frac{1}{2}{lim}_{a\to \infty }[-{u}^{-1}]_{1}^{a} \\  & =-\frac{1}{2}{lim}_{a\to \infty }{[\frac{1}{u}]}_{1}^{a} \\  & =-\frac{1}{2}{lim}_{a\to \infty }(\frac{1}{a}-1) \\  & =-\frac{1}{2}(0-1) \\  & =\frac{1}{2}.\end{aligned}
$$

## q-118618

Evaluate the integral ${\int }_{0}^{\infty }\frac{x}{\sqrt{({x}^{2}+1)^{3}}}\,\text{d}x.$

Observed components: {"C": 1, "n": 2, "A": 1, "B": 1, "p": "3/2", "lower": 0, "variable": "x", "radical": true, "domain": "x >= 0; 1*x^2+1>0", "correct_formula": "C/[A*n*(p-1)] * (A*L^n+B)^(1-p)"}.

Field and complete bank: [{"source_answer_id": "2796c11a-4fa6-505d-9e0a-aa25efdb9c37", "source_value": "The integral diverges", "correct": false, "recipe": "unchanged divergence text", "recipe_at_original_parameters": "The integral diverges", "interpretation": "Observed complete value pattern; error mechanism unresolved", "full_value_replayed": true}, {"source_answer_id": "5ec32c39-76e1-531c-a980-52d6069a233f", "source_value": "1", "correct": true, "recipe": "scale * (1)", "recipe_at_original_parameters": "1", "interpretation": "exact convergent limit", "full_value_replayed": true}, {"source_answer_id": "946eb912-f177-51c6-8055-52cb6bf80ad7", "source_value": "\\frac{1}{3}", "correct": false, "recipe": "scale * (\\frac{1}{3})", "recipe_at_original_parameters": "\\frac{1}{3}", "interpretation": "Observed complete value pattern; error mechanism unresolved", "full_value_replayed": true}, {"source_answer_id": "9c077374-79f0-523e-825a-f5521b2be909", "source_value": "2", "correct": false, "recipe": "scale * (2)", "recipe_at_original_parameters": "2", "interpretation": "Observed complete value pattern; error mechanism unresolved", "full_value_replayed": true}, {"source_answer_id": "bd295589-d9fe-5cee-b9fd-e8e6c502b237", "source_value": "\\frac{1}{9}", "correct": false, "recipe": "scale * (\\frac{1}{9})", "recipe_at_original_parameters": "\\frac{1}{9}", "interpretation": "Observed complete value pattern; error mechanism unresolved", "full_value_replayed": true}]

Original fixed solution:

First, we substitute $u={x}^{2}+1.$ Differentiating, we get

$$
\frac{\text{d}u}{\text{d}x}=2x\,⟹\,\frac{1}{2}\text{d}u=x\,\text{d}x.
$$

Since $u\to \infty $ when $x\to \infty ,$ the table for the limits of integration using the rule $u={x}^{2}+1$ is as follows:

| $x$ | $0$ | $\infty $ |
| --- | --- | --- |
| $u$ | $1$ | $\infty $ |

So, the integral in terms of the new variable $u$ is

$$
\begin{aligned}{\int }_{0}^{\infty }\frac{x}{\sqrt{({x}^{2}+1)^{3}}}\,\text{d}x & =\frac{1}{2}{\int }_{1}^{\infty }\frac{1}{\sqrt{{u}^{3}}}\,\text{d}u.\end{aligned}
$$

Finally, we proceed by setting the upper bound equal to some parameter $a,$ integrating as usual, and then taking the limit as $a\to \infty .$

$$
\begin{aligned}{\int }_{0}^{\infty }\frac{x}{\sqrt{{x}^{2}+1}}\,\text{d}x & =\frac{1}{2}{\int }_{1}^{\infty }\frac{1}{\sqrt{{u}^{3}}}\,\text{d}u \\  & =\frac{1}{2}{\int }_{1}^{\infty }{u}^{-3/2}\,\text{d}u \\  & =\frac{1}{2}{lim}_{a\to \infty }{\int }_{1}^{a}{u}^{-3/2}\,\text{d}u \\  & =\frac{1}{2}{lim}_{a\to \infty }{[-2{u}^{-1/2}]}_{1}^{a} \\  & =-{lim}_{a\to \infty }{[\frac{1}{\sqrt{u}}]}_{1}^{a} \\  & =-{lim}_{a\to \infty }(\frac{1}{\sqrt{a}}-1) \\  & =-(0-1) \\  & =1.\end{aligned}
$$

## q-152045

Evaluate ${\int }_{0}^{\infty }\frac{3}{\sqrt{(2x+4)^{3}}}\,\text{d}x.$

Observed components: {"C": 3, "n": 1, "A": 2, "B": 4, "p": "3/2", "lower": 0, "variable": "x", "radical": true, "domain": "x >= 0; 2*x^1+4>0", "correct_formula": "C/[A*n*(p-1)] * (A*L^n+B)^(1-p)"}.

Field and complete bank: [{"source_answer_id": "38b40290-f4b5-5a0c-be7c-96b2f991be33", "source_value": "\\frac{3}{4}", "correct": false, "recipe": "scale * (\\frac{3}{4})", "recipe_at_original_parameters": "\\frac{3}{4}", "interpretation": "Observed complete value pattern; error mechanism unresolved", "full_value_replayed": true}, {"source_answer_id": "58e3e781-1f60-5931-b1ab-d40d34456c59", "source_value": "\\frac{3}{2}", "correct": true, "recipe": "scale * (\\frac{3}{2})", "recipe_at_original_parameters": "\\frac{3}{2}", "interpretation": "exact convergent limit", "full_value_replayed": true}, {"source_answer_id": "cdcef9fb-9792-5a33-9834-01011e4cecef", "source_value": "The integral diverges", "correct": false, "recipe": "unchanged divergence text", "recipe_at_original_parameters": "The integral diverges", "interpretation": "Observed complete value pattern; error mechanism unresolved", "full_value_replayed": true}, {"source_answer_id": "d21993ef-a070-5549-8573-0bebbc8c466f", "source_value": "\\frac{1}{6}", "correct": false, "recipe": "scale * (\\frac{1}{6})", "recipe_at_original_parameters": "\\frac{1}{6}", "interpretation": "Observed complete value pattern; error mechanism unresolved", "full_value_replayed": true}, {"source_answer_id": "fa381c2a-d88b-56af-ae05-33eda16e16c3", "source_value": "\\frac{1}{2}", "correct": false, "recipe": "scale * (\\frac{1}{2})", "recipe_at_original_parameters": "\\frac{1}{2}", "interpretation": "Observed complete value pattern; error mechanism unresolved", "full_value_replayed": true}]

Original fixed solution:

First, we substitute $u=2x+4.$ Differentiating, we get

$$
\frac{\text{d}u}{\text{d}x}=2\,⟹\,\frac{1}{2}\,\text{d}u=\text{d}x.
$$

Since $u\to \infty $ when $x\to \infty ,$ the table for the limits of integration using the rule $u=2x+4$ is as follows:

| $x$ | $0$ | $\infty $ |
| --- | --- | --- |
| $u$ | $4$ | $\infty $ |

So, the integral in terms of the new variable $u$ is

$$
\begin{aligned}{\int }_{0}^{\infty }\frac{3}{\sqrt{(2x+4)^{3}}}\,\text{d}x & ={\int }_{4}^{\infty }\frac{3}{\sqrt{{u}^{3}}}(\frac{1}{2}\,\text{d}u) \\  & =\frac{3}{2}{\int }_{4}^{\infty }\frac{1}{\sqrt{{u}^{3}}}\,\text{d}u\end{aligned}
$$

Finally, we proceed by setting the upper bound equal to some parameter $a,$ integrating as usual, and then taking the limit as $a\to \infty .$

$$
\begin{aligned}{\int }_{0}^{\infty }\frac{3}{\sqrt{(2x+4)^{3}}}\,\text{d}x & =\frac{3}{2}{\int }_{4}^{\infty }\frac{1}{\sqrt{{u}^{3}}}\,\text{d}u \\  & =\frac{3}{2}{\int }_{4}^{\infty }{u}^{-3/2}\,\text{d}u \\  & =\frac{3}{2}{lim}_{a\to \infty }{\int }_{4}^{a}{u}^{-3/2}\,\text{d}u \\  & =\frac{3}{2}{lim}_{a\to \infty }{[-2{u}^{-1/2}]}_{4}^{a} \\  & =-3\cdot {lim}_{a\to \infty }{[\frac{1}{\sqrt{u}}]}_{4}^{a} \\  & =-3\cdot {lim}_{a\to \infty }[\frac{1}{\sqrt{a}}-\frac{1}{\sqrt{4}}] \\  & =-3\cdot (0-\frac{1}{2}) \\  & =\frac{3}{2}.\end{aligned}
$$

## q-152056

Evaluate the integral ${\int }_{0}^{\infty }\frac{{x}^{2}}{\sqrt{({x}^{3}+1)^{5}}}\,\text{d}x.$

Observed components: {"C": 1, "n": 3, "A": 1, "B": 1, "p": "5/2", "lower": 0, "variable": "x", "radical": true, "domain": "x >= 0; 1*x^3+1>0", "correct_formula": "C/[A*n*(p-1)] * (A*L^n+B)^(1-p)"}.

Field and complete bank: [{"source_answer_id": "26a11a46-1ee3-5e97-8f5c-d2abb45897e8", "source_value": "\\frac{1}{9}", "correct": false, "recipe": "scale * (\\frac{1}{9})", "recipe_at_original_parameters": "\\frac{1}{9}", "interpretation": "Observed complete value pattern; error mechanism unresolved", "full_value_replayed": true}, {"source_answer_id": "3ac4135a-ba42-51f2-9589-6f253f1dccac", "source_value": "The integral diverges", "correct": false, "recipe": "unchanged divergence text", "recipe_at_original_parameters": "The integral diverges", "interpretation": "Observed complete value pattern; error mechanism unresolved", "full_value_replayed": true}, {"source_answer_id": "3d241674-25f3-586b-9f92-1ae97b73f2d8", "source_value": "\\frac{2}{9}", "correct": true, "recipe": "scale * (\\frac{2}{9})", "recipe_at_original_parameters": "\\frac{2}{9}", "interpretation": "exact convergent limit", "full_value_replayed": true}, {"source_answer_id": "82c45777-32c0-5bbe-903e-12a9832686d4", "source_value": "\\frac{1}{3}", "correct": false, "recipe": "scale * (\\frac{1}{3})", "recipe_at_original_parameters": "\\frac{1}{3}", "interpretation": "Observed complete value pattern; error mechanism unresolved", "full_value_replayed": true}, {"source_answer_id": "e43e2450-5746-5333-88fb-b2698cd7c90f", "source_value": "\\frac{2}{3}", "correct": false, "recipe": "scale * (\\frac{2}{3})", "recipe_at_original_parameters": "\\frac{2}{3}", "interpretation": "Observed complete value pattern; error mechanism unresolved", "full_value_replayed": true}]

Original fixed solution:

First, we substitute $u={x}^{3}+1.$ Differentiating, we get

$$
\frac{\text{d}u}{\text{d}x}=3{x}^{2}\,⟹\,\frac{1}{3}\text{d}u={x}^{2}\,\text{d}x.
$$

Since $u\to \infty $ when $x\to \infty ,$ the table for the limits of integration using the rule $u={x}^{3}+1$ is as follows:

| $x$ | $0$ | $\infty $ |
| --- | --- | --- |
| $u$ | $1$ | $\infty $ |

So, the integral in terms of the new variable $u$ is

$$
\begin{aligned}{\int }_{0}^{\infty }\frac{{x}^{2}}{\sqrt{({x}^{3}+1)^{5}}}\,\text{d}x & =\frac{1}{3}{\int }_{1}^{\infty }\frac{1}{\sqrt{{u}^{5}}}\,\text{d}u.\end{aligned}
$$

Finally, we proceed by setting the upper bound equal to some parameter $a,$ integrating as usual, and then taking the limit as $a\to \infty .$

$$
\begin{aligned}{\int }_{0}^{\infty }\frac{x}{\sqrt{{x}^{3}+1}}\,\text{d}x & =\frac{1}{3}{\int }_{1}^{\infty }\frac{1}{\sqrt{{u}^{5}}}\,\text{d}u \\  & =\frac{1}{3}{\int }_{1}^{\infty }{u}^{-5/2}\,\text{d}u \\  & =\frac{1}{3}{lim}_{a\to \infty }{\int }_{1}^{a}{u}^{-5/2}\,\text{d}u \\  & =\frac{1}{3}{lim}_{a\to \infty }{[-\frac{2}{3}{u}^{-3/2}]}_{1}^{a} \\  & =-\frac{2}{9}{lim}_{a\to \infty }{[\frac{1}{\sqrt{{u}^{3}}}]}_{1}^{a} \\  & =-\frac{2}{9}{lim}_{a\to \infty }(\frac{1}{\sqrt{{a}^{3}}}-1) \\  & =-\frac{2}{9}(0-1) \\  & =\frac{2}{9}.\end{aligned}
$$

## q-152779

Evaluate ${\int }_{-1}^{\infty }\frac{6}{(z+2)^{4}}\,\text{d}z.$

Observed components: {"C": 6, "n": 1, "A": 1, "B": 2, "p": "4", "lower": -1, "variable": "z", "radical": false, "domain": "z >= -1; 1*z^1+2>0", "correct_formula": "C/[A*n*(p-1)] * (A*L^n+B)^(1-p)"}.

Field and complete bank: [{"source_answer_id": "09c25cd7-e43c-5867-9197-1ea57513487c", "source_value": "The integral diverges", "correct": false, "recipe": "unchanged divergence text", "recipe_at_original_parameters": "The integral diverges", "interpretation": "Observed complete value pattern; error mechanism unresolved", "full_value_replayed": true}, {"source_answer_id": "aa37f140-928a-5f9c-98df-08319686b282", "source_value": "2", "correct": true, "recipe": "scale * (2)", "recipe_at_original_parameters": "2", "interpretation": "exact convergent limit", "full_value_replayed": true}, {"source_answer_id": "bf4f57fe-edf1-5a1a-80e8-43a57330b833", "source_value": "\\frac{1}{2}", "correct": false, "recipe": "scale * (\\frac{1}{2})", "recipe_at_original_parameters": "\\frac{1}{2}", "interpretation": "Observed complete value pattern; error mechanism unresolved", "full_value_replayed": true}, {"source_answer_id": "c27f9c75-c61b-5146-a432-d5051ff1cbbf", "source_value": "\\frac{1}{3}", "correct": false, "recipe": "scale * (\\frac{1}{3})", "recipe_at_original_parameters": "\\frac{1}{3}", "interpretation": "Observed complete value pattern; error mechanism unresolved", "full_value_replayed": true}, {"source_answer_id": "f8fe9d4f-ca4d-59b2-bf98-68697411b047", "source_value": "3", "correct": false, "recipe": "scale * (3)", "recipe_at_original_parameters": "3", "interpretation": "Observed complete value pattern; error mechanism unresolved", "full_value_replayed": true}]

Original fixed solution:

First, we substitute $u=z+2.$ Differentiating, we get

$$
\frac{\text{d}u}{\text{d}z}=1\,⟹\,\text{d}u=\text{d}z.
$$

Since $u\to \infty $ when $z\to \infty ,$ the table for the limits of integration using the rule $u=z+2$ is as follows:

| $z$ | $-1$ | $\infty $ |
| --- | --- | --- |
| $u$ | $1$ | $\infty $ |

So, the integral in terms of the new variable $u$ is

$$
{\int }_{-1}^{\infty }\frac{6}{(z+2)^{4}}\,\text{d}z={\int }_{1}^{\infty }\frac{6}{{u}^{4}}\,\text{d}u
$$

Finally, we proceed by setting the upper bound equal to some parameter $a,$ integrating as usual, and then taking the limit as $a\to \infty .$

$$
\begin{aligned}{\int }_{-1}^{\infty }\frac{6}{(z+2)^{4}}\,\text{d}z & ={\int }_{1}^{\infty }\frac{6}{{u}^{4}}\,\text{d}u \\  & =6{\int }_{1}^{\infty }{u}^{-4}\,\text{d}u \\  & =6{lim}_{a\to \infty }{\int }_{1}^{a}{u}^{-4}\,\text{d}u \\  & =6{lim}_{a\to \infty }{[-\frac{1}{3}{u}^{-3}]}_{1}^{a} \\  & =-2\cdot {lim}_{a\to \infty }{[\frac{1}{{u}^{3}}]}_{1}^{a} \\  & =-2\cdot {lim}_{a\to \infty }[\frac{1}{{a}^{3}}-\frac{1}{{1}^{3}}] \\  & =-2\cdot (0-1) \\  & =2.\end{aligned}
$$

## q-152785

Evaluate the integral ${\int }_{1}^{\infty }\frac{8{z}^{3}}{{({z}^{4}+1)}^{4}}\,\text{d}z.$

Observed components: {"C": 8, "n": 4, "A": 1, "B": 1, "p": "4", "lower": 1, "variable": "z", "radical": false, "domain": "z >= 1; 1*z^4+1>0", "correct_formula": "C/[A*n*(p-1)] * (A*L^n+B)^(1-p)"}.

Field and complete bank: [{"source_answer_id": "32496a0b-0230-56b7-a08f-0eacec67f0e5", "source_value": "\\frac{5}{6}", "correct": false, "recipe": "scale * (\\frac{5}{6})", "recipe_at_original_parameters": "\\frac{5}{6}", "interpretation": "Observed complete value pattern; error mechanism unresolved", "full_value_replayed": true}, {"source_answer_id": "54d16173-4764-586a-9e7d-eae609ca54b7", "source_value": "The Integral diverges", "correct": false, "recipe": "unchanged divergence text", "recipe_at_original_parameters": "The Integral diverges", "interpretation": "Observed complete value pattern; error mechanism unresolved", "full_value_replayed": true}, {"source_answer_id": "6e3a8ce3-a04f-549b-961f-7f4308c92010", "source_value": "\\frac{1}{12}", "correct": true, "recipe": "scale * (\\frac{1}{12})", "recipe_at_original_parameters": "\\frac{1}{12}", "interpretation": "exact convergent limit", "full_value_replayed": true}, {"source_answer_id": "cff5572a-a2b4-5582-bb9e-a320f544f89d", "source_value": "\\frac{1}{6}", "correct": false, "recipe": "scale * (\\frac{1}{6})", "recipe_at_original_parameters": "\\frac{1}{6}", "interpretation": "Observed complete value pattern; error mechanism unresolved", "full_value_replayed": true}, {"source_answer_id": "fe4ae8a0-1bfb-5e1e-a786-8e51d30074fe", "source_value": "\\frac{3}{4}", "correct": false, "recipe": "scale * (\\frac{3}{4})", "recipe_at_original_parameters": "\\frac{3}{4}", "interpretation": "Observed complete value pattern; error mechanism unresolved", "full_value_replayed": true}]

Original fixed solution:

First, we substitute $u={z}^{4}+1.$ Differentiating, we get

$$
\frac{\text{d}u}{\text{d}z}=4{z}^{3}\,⟹\,\frac{1}{4}\text{d}u={z}^{3}\,\text{d}z.
$$

Since $u\to \infty $ when $z\to \infty ,$ the table for the limits of integration using the rule $u={z}^{4}+1$ is as follows:

| $z$ | $1$ | $\infty $ |
| --- | --- | --- |
| $u$ | $2$ | $\infty $ |

So, the integral in terms of the new variable $u$ is

$$
\begin{aligned}{\int }_{1}^{\infty }\frac{8{z}^{3}}{{({z}^{4}+1)}^{4}}\,\text{d}z & ={\int }_{2}^{\infty }\frac{8}{{u}^{4}}(\frac{1}{4}\,\text{d}u) \\  & =2{\int }_{2}^{\infty }\frac{1}{{u}^{4}}\,\text{d}u.\end{aligned}
$$

Finally, we proceed by setting the upper bound equal to some parameter $a,$ integrating as usual, and then taking the limit as $a\to \infty .$

$$
\begin{aligned}{\int }_{1}^{\infty }\frac{8{z}^{3}}{{({z}^{4}+1)}^{4}}\,\text{d}z & =2{\int }_{2}^{\infty }\frac{1}{{u}^{4}}\,\text{d}u \\  & =2{\int }_{2}^{\infty }{u}^{-4}\,\text{d}u \\  & =2{lim}_{a\to \infty }{\int }_{2}^{a}{u}^{-4}\,\text{d}u \\  & =2{lim}_{a\to \infty }{[-\frac{1}{3}{u}^{-3}]}_{2}^{a} \\  & =-\frac{2}{3}{lim}_{a\to \infty }{[\frac{1}{{u}^{3}}]}_{2}^{a} \\  & =-\frac{2}{3}{lim}_{a\to \infty }(\frac{1}{{a}^{3}}-\frac{1}{8}) \\  & =-\frac{2}{3}(0-\frac{1}{8}) \\  & =\frac{1}{12}.\end{aligned}
$$

## q-350527

Evaluate the following integral. Do not round the answer.

${\int }_{0}^{\infty }\frac{3}{(x+1)^{5}}\,\text{d}x=$
{{field-1}}

Observed components: {"C": 3, "n": 1, "A": 1, "B": 1, "p": "5", "lower": 0, "variable": "x", "radical": false, "domain": "x >= 0; 1*x^1+1>0", "correct_formula": "C/[A*n*(p-1)] * (A*L^n+B)^(1-p)"}.

Field and complete bank: [{"source_answer_id": "f2b84759-63fa-5697-9589-8a03b63ecdef", "source_value": "\\frac{3}{4}", "correct": true, "recipe": "scale * (\\frac{3}{4})", "recipe_at_original_parameters": "\\frac{3}{4}", "interpretation": "exact convergent limit", "full_value_replayed": true}]

Original fixed solution:

First, we substitute $u=x+1.$ Differentiating, we get

$$
\frac{\text{d}u}{\text{d}x}=1\,⟹\,\text{d}u=\text{d}x.
$$

Since $u\to \infty $ when $x\to \infty ,$ the table for the limits of integration using the rule $u=x+1$ is as follows:

| $x$ | $0$ | $\infty $ |
| --- | --- | --- |
| $u$ | $1$ | $\infty $ |

So, the integral in terms of the new variable $u$ is

$$
{\int }_{0}^{\infty }\frac{3}{(x+1)^{5}}\,\text{d}x={\int }_{1}^{\infty }\frac{3}{{u}^{5}}\,\text{d}u
$$

Finally, we proceed by setting the upper bound equal to some parameter $a,$ integrating as usual, and then taking the limit as $a\to \infty .$

$$
\begin{aligned}{\int }_{0}^{\infty }\frac{3}{(x+1)^{5}}\,\text{d}x & ={\int }_{1}^{\infty }\frac{3}{{u}^{5}}\,\text{d}u \\  & ={\int }_{1}^{\infty }3{u}^{-5}\,\text{d}u \\  & ={lim}_{a\to \infty }{\int }_{1}^{a}3{u}^{-5}\,\text{d}u \\  & ={lim}_{a\to \infty }{[-\frac{3}{4}{u}^{-4}]}_{1}^{a} \\  & =-\frac{3}{4}\cdot {lim}_{a\to \infty }{[{u}^{-4}]}_{1}^{a} \\  & =-\frac{3}{4}\cdot {lim}_{a\to \infty }[\frac{1}{{a}^{4}}-\frac{1}{{1}^{4}}] \\  & =-\frac{3}{4}\cdot (0-1) \\  & =\frac{3}{4}.\end{aligned}
$$

## q-350528

Evaluate the following integral. Do not round the answer.

${\int }_{0}^{\infty }\frac{2}{\sqrt{(x+3)^{8}}}\,\text{d}x=$
{{field-1}}

Observed components: {"C": 2, "n": 1, "A": 1, "B": 3, "p": "4", "lower": 0, "variable": "x", "radical": true, "domain": "x >= 0; 1*x^1+3>0", "correct_formula": "C/[A*n*(p-1)] * (A*L^n+B)^(1-p)"}.

Field and complete bank: [{"source_answer_id": "30bb13ff-8e84-50d3-8caf-75c51cb5c866", "source_value": "\\frac{2}{81}", "correct": true, "recipe": "scale * (\\frac{2}{81})", "recipe_at_original_parameters": "\\frac{2}{81}", "interpretation": "exact convergent limit", "full_value_replayed": true}]

Original fixed solution:

First, we substitute $u=x+3.$ Differentiating, we get

$$
\frac{\text{d}u}{\text{d}x}=1\,⟹\,\text{d}u=\text{d}x.
$$

Since $u\to \infty $ when $x\to \infty ,$ the table for the limits of integration using the rule $u=x+3$ is as follows:

| $x$ | $0$ | $\infty $ |
| --- | --- | --- |
| $u$ | $3$ | $\infty $ |

So, the integral in terms of the new variable $u$ is

$$
{\int }_{0}^{\infty }\frac{2}{\sqrt{(x+3)^{8}}}\,\text{d}x={\int }_{3}^{\infty }\frac{2}{\sqrt{{u}^{8}}}\,\text{d}u
$$

Finally, we proceed by setting the upper bound equal to some parameter $a,$ integrating as usual, and then taking the limit as $a\to \infty .$

$$
\begin{aligned}{\int }_{0}^{\infty }\frac{2}{\sqrt{(x+3)^{8}}}\,\text{d}x & ={\int }_{3}^{\infty }\frac{2}{\sqrt{{u}^{8}}}\,\text{d}u \\  & ={\int }_{3}^{\infty }2{u}^{-4}\,\text{d}u \\  & ={lim}_{a\to \infty }{\int }_{3}^{a}2{u}^{-4}\,\text{d}u \\  & ={lim}_{a\to \infty }{[-\frac{2}{3}{u}^{-3}]}_{3}^{a} \\  & =-\frac{2}{3}\cdot {lim}_{a\to \infty }{[{u}^{-3}]}_{3}^{a} \\  & =-\frac{2}{3}\cdot {lim}_{a\to \infty }[\frac{1}{{a}^{3}}-\frac{1}{{3}^{3}}] \\  & =-\frac{2}{3}\cdot (0-\frac{1}{27}) \\  & =\frac{2}{81}.\end{aligned}
$$

## q-350530

Evaluate the following integral. Do not round the answer.

${\int }_{0}^{\infty }\frac{5}{(3y+2)^{4}}\,\text{d}y=$
{{field-1}}

Observed components: {"C": 5, "n": 1, "A": 3, "B": 2, "p": "4", "lower": 0, "variable": "y", "radical": false, "domain": "y >= 0; 3*y^1+2>0", "correct_formula": "C/[A*n*(p-1)] * (A*L^n+B)^(1-p)"}.

Field and complete bank: [{"source_answer_id": "dc93f73c-03ee-59bf-93ed-905ccaef63cd", "source_value": "\\frac{5}{72}", "correct": true, "recipe": "scale * (\\frac{5}{72})", "recipe_at_original_parameters": "\\frac{5}{72}", "interpretation": "exact convergent limit", "full_value_replayed": true}]

Original fixed solution:

First, we substitute $u=3y+2.$ Differentiating, we get

$$
\frac{\text{d}u}{\text{d}y}=3\,⟹\,\text{d}u=3\text{d}y.
$$

Since $u\to \infty $ when $y\to \infty ,$ the table for the limits of integration using the rule $u=3y+2$ is as follows:

| $y$ | $0$ | $\infty $ |
| --- | --- | --- |
| $u$ | $2$ | $\infty $ |

So, the integral in terms of the new variable $u$ is

$$
{\int }_{0}^{\infty }\frac{5}{(3y+2)^{4}}\,\text{d}y={\int }_{2}^{\infty }\frac{5}{3{u}^{4}}\,\text{d}u
$$

Finally, we proceed by setting the upper bound equal to some parameter $a,$ integrating as usual, and then taking the limit as $a\to \infty .$

$$
\begin{aligned}{\int }_{0}^{\infty }\frac{5}{(3y+2)^{4}}\,\text{d}y & ={\int }_{2}^{\infty }\frac{5}{3{u}^{4}}\,\text{d}u \\  & ={\int }_{2}^{\infty }\frac{5}{3}{u}^{-4}\,\text{d}u \\  & ={lim}_{a\to \infty }{\int }_{2}^{a}\frac{5}{3}{u}^{-4}\,\text{d}u \\  & ={lim}_{a\to \infty }{[-\frac{5}{9}{u}^{-3}]}_{2}^{a} \\  & =-\frac{5}{9}\cdot {lim}_{a\to \infty }{[{u}^{-3}]}_{2}^{a} \\  & =-\frac{5}{9}\cdot {lim}_{a\to \infty }[\frac{1}{{a}^{3}}-\frac{1}{{2}^{3}}] \\  & =-\frac{5}{9}\cdot (0-\frac{1}{8}) \\  & =\frac{5}{72}.\end{aligned}
$$

## q-350531

Evaluate the following integral. Do not round the answer.

${\int }_{0}^{\infty }\frac{6}{\sqrt{(4t+3)^{3}}}\,\text{d}t=$
{{field-1}}

Observed components: {"C": 6, "n": 1, "A": 4, "B": 3, "p": "3/2", "lower": 0, "variable": "t", "radical": true, "domain": "t >= 0; 4*t^1+3>0", "correct_formula": "C/[A*n*(p-1)] * (A*L^n+B)^(1-p)"}.

Field and complete bank: [{"source_answer_id": "b355d9a6-e99e-5ef7-91c3-31ee7ef8c4e5", "source_value": "\\sqrt{3}", "correct": true, "recipe": "scale * (\\sqrt{3})", "recipe_at_original_parameters": "\\sqrt{3}", "interpretation": "exact convergent limit", "full_value_replayed": true}]

Original fixed solution:

First, we substitute $u=4t+3.$ Differentiating, we get

$$
\frac{\text{d}u}{\text{d}t}=4\,⟹\,\text{d}u=4\text{d}t.
$$

Since $u\to \infty $ when $t\to \infty ,$ the table for the limits of integration using the rule $u=4t+3$ is as follows:

| $t$ | $0$ | $\infty $ |
| --- | --- | --- |
| $u$ | $3$ | $\infty $ |

So, the integral in terms of the new variable $u$ is

$$
{\int }_{0}^{\infty }\frac{6}{\sqrt{(4t+3)^{3}}}\,\text{d}t={\int }_{3}^{\infty }\frac{3}{2\sqrt{{u}^{3}}}\,\text{d}u
$$

Finally, we proceed by setting the upper bound equal to some parameter $a,$ integrating as usual, and then taking the limit as $a\to \infty .$

$$
\begin{aligned}{\int }_{0}^{\infty }\frac{6}{\sqrt{(4t+3)^{3}}}\,\text{d}t & ={\int }_{3}^{\infty }\frac{3}{2\sqrt{{u}^{3}}}\,\text{d}u \\  & ={\int }_{3}^{\infty }\frac{3}{2}{u}^{-3/2}\,\text{d}u \\  & ={lim}_{a\to \infty }{\int }_{3}^{a}\frac{3}{2}{u}^{-3/2}\,\text{d}u \\  & ={lim}_{a\to \infty }{[-3{u}^{-1/2}]}_{3}^{a} \\  & =-3\cdot {lim}_{a\to \infty }{[{u}^{-1/2}]}_{3}^{a} \\  & =-3\cdot {lim}_{a\to \infty }[\frac{1}{\sqrt{a}}-\frac{1}{\sqrt{3}}] \\  & =-3\cdot (0-\frac{1}{\sqrt{3}}) \\  & =\sqrt{3}.\end{aligned}
$$

## q-350532

Evaluate the following integral. Do not round the answer.

${\int }_{0}^{\infty }\frac{2}{(5\theta +1)^{3}}\,\text{d}\theta =$
{{field-1}}

Observed components: {"C": 2, "n": 1, "A": 5, "B": 1, "p": "3", "lower": 0, "variable": "\\theta", "radical": false, "domain": "\\theta >= 0; 5*\\theta^1+1>0", "correct_formula": "C/[A*n*(p-1)] * (A*L^n+B)^(1-p)"}.

Field and complete bank: [{"source_answer_id": "4b108f43-8cc9-5ed2-849e-bf0b3ad9c65c", "source_value": "\\frac{1}{5}", "correct": true, "recipe": "scale * (\\frac{1}{5})", "recipe_at_original_parameters": "\\frac{1}{5}", "interpretation": "exact convergent limit", "full_value_replayed": true}]

Original fixed solution:

First, we substitute $u=5\theta +1.$ Differentiating, we get

$$
\frac{\text{d}u}{\text{d}\theta }=5\,⟹\,\text{d}u=5\text{d}\theta .
$$

Since $u\to \infty $ when $\theta \to \infty ,$ the table for the limits of integration using the rule $u=5\theta +1$ is as follows:

| $\theta $ | $0$ | $\infty $ |
| --- | --- | --- |
| $u$ | $1$ | $\infty $ |

So, the integral in terms of the new variable $u$ is

$$
{\int }_{0}^{\infty }\frac{2}{(5\theta +1)^{3}}\,\text{d}\theta ={\int }_{1}^{\infty }\frac{2}{5{u}^{3}}\,\text{d}u
$$

Finally, we proceed by setting the upper bound equal to some parameter $a,$ integrating as usual, and then taking the limit as $a\to \infty .$

$$
\begin{aligned}{\int }_{0}^{\infty }\frac{2}{(5\theta +1)^{3}}\,\text{d}\theta  & ={\int }_{1}^{\infty }\frac{2}{5{u}^{3}}\,\text{d}u \\  & ={\int }_{1}^{\infty }\frac{2}{5}{u}^{-3}\,\text{d}u \\  & ={lim}_{a\to \infty }{\int }_{1}^{a}\frac{2}{5}{u}^{-3}\,\text{d}u \\  & ={lim}_{a\to \infty }{[-\frac{1}{5}{u}^{-2}]}_{1}^{a} \\  & =-\frac{1}{5}\cdot {lim}_{a\to \infty }{[{u}^{-2}]}_{1}^{a} \\  & =-\frac{1}{5}\cdot {lim}_{a\to \infty }[\frac{1}{{a}^{2}}-\frac{1}{{1}^{2}}] \\  & =-\frac{1}{5}\cdot (0-1) \\  & =\frac{1}{5}.\end{aligned}
$$

## q-350534

Evaluate the following integral. Do not round the answer.

${\int }_{0}^{\infty }\frac{4{x}^{3}}{\sqrt{({x}^{4}+2)^{3}}}\,\text{d}x=$
{{field-1}}

Observed components: {"C": 4, "n": 4, "A": 1, "B": 2, "p": "3/2", "lower": 0, "variable": "x", "radical": true, "domain": "x >= 0; 1*x^4+2>0", "correct_formula": "C/[A*n*(p-1)] * (A*L^n+B)^(1-p)"}.

Field and complete bank: [{"source_answer_id": "325cede2-6960-5085-95d8-87d16b121023", "source_value": "\\sqrt{2}", "correct": true, "recipe": "scale * (\\sqrt{2})", "recipe_at_original_parameters": "\\sqrt{2}", "interpretation": "exact convergent limit", "full_value_replayed": true}]

Original fixed solution:

First, we substitute $u={x}^{4}+2.$ Differentiating, we get

$$
\frac{\text{d}u}{\text{d}x}=4{x}^{3}\,⟹\,\text{d}u=4{x}^{3}\text{d}x.
$$

Since $u\to \infty $ when $x\to \infty ,$ the table for the limits of integration using the rule $u={x}^{4}+2$ is as follows:

| $x$ | $0$ | $\infty $ |
| --- | --- | --- |
| $u$ | $2$ | $\infty $ |

So, the integral in terms of the new variable $u$ is

$$
{\int }_{0}^{\infty }\frac{4{x}^{3}}{\sqrt{({x}^{4}+2)^{3}}}\,\text{d}x={\int }_{2}^{\infty }\frac{1}{\sqrt{{u}^{3}}}\,\text{d}u
$$

Finally, we proceed by setting the upper bound equal to some parameter $a,$ integrating as usual, and then taking the limit as $a\to \infty .$

$$
\begin{aligned}{\int }_{0}^{\infty }\frac{4{x}^{3}}{\sqrt{({x}^{4}+2)^{3}}}\,\text{d}x & ={\int }_{2}^{\infty }\frac{1}{\sqrt{{u}^{3}}}\,\text{d}u \\  & ={\int }_{2}^{\infty }{u}^{-3/2}\,\text{d}u \\  & ={lim}_{a\to \infty }{\int }_{2}^{a}{u}^{-3/2}\,\text{d}u \\  & ={lim}_{a\to \infty }{[-2{u}^{-1/2}]}_{2}^{a} \\  & =-2\cdot {lim}_{a\to \infty }{[{u}^{-1/2}]}_{2}^{a} \\  & =-2\cdot {lim}_{a\to \infty }[\frac{1}{{a}^{1/2}}-\frac{1}{{2}^{1/2}}] \\  & =-2\cdot (0-\frac{1}{\sqrt{2}}) \\  & =\sqrt{2}.\end{aligned}
$$

## q-152053

Evaluate the integral ${\int }_{0}^{\infty }\frac{{x}^{2}}{{(1+{x}^{3})}^{4}}\,\text{d}x.$

Observed components: {"C": 1, "n": 3, "A": 1, "B": 1, "p": "4", "lower": 0, "variable": "x", "radical": false, "domain": "x >= 0; 1*x^3+1>0", "correct_formula": "C/[A*n*(p-1)] * (A*L^n+B)^(1-p)"}.

Field and complete bank: [{"source_answer_id": "03e197f9-926d-5a38-b07b-3b834b50535f", "source_value": "The integral diverges", "correct": false, "recipe": "unchanged divergence text", "recipe_at_original_parameters": "The integral diverges", "interpretation": "Observed complete value pattern; error mechanism unresolved", "full_value_replayed": true}, {"source_answer_id": "dafbddd2-29ab-58ca-9736-d248a9876ed7", "source_value": "\\frac{2}{3}", "correct": false, "recipe": "scale * (\\frac{2}{3})", "recipe_at_original_parameters": "\\frac{2}{3}", "interpretation": "Observed complete value pattern; error mechanism unresolved", "full_value_replayed": true}, {"source_answer_id": "2f7cd5c5-dc32-5789-8e7c-5560c7a38366", "source_value": "\\frac{4}{9}", "correct": false, "recipe": "scale * (\\frac{4}{9})", "recipe_at_original_parameters": "\\frac{4}{9}", "interpretation": "Observed complete value pattern; error mechanism unresolved", "full_value_replayed": true}, {"source_answer_id": "6db6a9c1-e6da-5b48-a604-1d3d52519aeb", "source_value": "\\frac{1}{6}", "correct": false, "recipe": "scale * (\\frac{1}{6})", "recipe_at_original_parameters": "\\frac{1}{6}", "interpretation": "Observed complete value pattern; error mechanism unresolved", "full_value_replayed": true}, {"source_answer_id": "990bf603-9c44-51da-bab2-c8dd72364300", "source_value": "\\frac{1}{9}", "correct": true, "recipe": "scale * (\\frac{1}{9})", "recipe_at_original_parameters": "\\frac{1}{9}", "interpretation": "exact convergent limit", "full_value_replayed": true}]

Original fixed solution:

First, we substitute $u=1+{x}^{3}.$ Differentiating, we get

$$
\frac{\text{d}u}{\text{d}x}=3{x}^{2}\,⟹\,\frac{1}{3}\text{d}u={x}^{2}\,\text{d}x.
$$

Since $u\to \infty $ when $x\to \infty ,$ the table for the limits of integration using the rule $u=1+{x}^{3}$ is as follows:

| $x$ | $0$ | $\infty $ |
| --- | --- | --- |
| $u$ | $1$ | $\infty $ |

So, the integral in terms of the new variable $u$ is

$$
\begin{aligned}{\int }_{0}^{\infty }\frac{{x}^{2}}{{(1+{x}^{3})}^{4}}\,\text{d}x & =\frac{1}{3}{\int }_{1}^{\infty }\frac{1}{{u}^{4}}\,\text{d}u.\end{aligned}
$$

Finally, we proceed by setting the upper bound equal to some parameter $a,$ integrating as usual, and then taking the limit as $a\to \infty .$

$$
\begin{aligned}{\int }_{0}^{\infty }\frac{{x}^{2}}{{(1+{x}^{3})}^{4}}\,\text{d}x & =\frac{1}{3}{\int }_{1}^{\infty }\frac{1}{{u}^{4}}\,\text{d}u \\  & =\frac{1}{3}{\int }_{1}^{\infty }{u}^{-4}\,\text{d}u \\  & =\frac{1}{3}{lim}_{a\to \infty }{\int }_{1}^{a}{u}^{-4}\,\text{d}u \\  & =\frac{1}{3}{lim}_{a\to \infty }{[-\frac{1}{3}{u}^{-3}]}_{1}^{a} \\  & =-\frac{1}{9}{lim}_{a\to \infty }{[\frac{1}{{u}^{3}}]}_{1}^{a} \\  & =-\frac{1}{9}{lim}_{a\to \infty }(\frac{1}{{a}^{3}}-1) \\  & =-\frac{1}{9}(0-1) \\  & =\frac{1}{9}.\end{aligned}
$$

## q-346591

Evaluate the following integral. Do not round the answer.

${\int }_{0}^{\infty }\frac{1}{\sqrt{(x+1)^{9}}}\,\text{d}x=$
{{field-1}}

Observed components: {"C": 1, "n": 1, "A": 1, "B": 1, "p": "9/2", "lower": 0, "variable": "x", "radical": true, "domain": "x >= 0; 1*x^1+1>0", "correct_formula": "C/[A*n*(p-1)] * (A*L^n+B)^(1-p)"}.

Field and complete bank: [{"source_answer_id": "703e41a4-7d89-5c9f-bced-f0d638d7838b", "source_value": "\\frac{2}{7}", "correct": true, "recipe": "scale * (\\frac{2}{7})", "recipe_at_original_parameters": "\\frac{2}{7}", "interpretation": "exact convergent limit", "full_value_replayed": true}]

Original fixed solution:

First, we substitute $u=x+1.$ Differentiating, we get

$$
\frac{\text{d}u}{\text{d}x}=1\,⟹\,\text{d}u=\text{d}x.
$$

Since $u\to \infty $ when $x\to \infty ,$ the table for the limits of integration using the rule $u=x+1$ is as follows:

| $x$ | $0$ | $\infty $ |
| --- | --- | --- |
| $u$ | $1$ | $\infty $ |

So, the integral in terms of the new variable $u$ is

$$
{\int }_{0}^{\infty }\frac{1}{\sqrt{(x+1)^{9}}}\,\text{d}x={\int }_{1}^{\infty }\frac{1}{\sqrt{{u}^{9}}}\,\text{d}u
$$

Finally, we proceed by setting the upper bound equal to some parameter $a,$ integrating as usual, and then taking the limit as $a\to \infty .$

$$
\begin{aligned}{\int }_{0}^{\infty }\frac{1}{\sqrt{(x+1)^{9}}}\,\text{d}x & ={\int }_{1}^{\infty }\frac{1}{\sqrt{{u}^{9}}}\,\text{d}u \\  & ={\int }_{1}^{\infty }{u}^{-9/2}\,\text{d}u \\  & ={lim}_{a\to \infty }{\int }_{1}^{a}{u}^{-9/2}\,\text{d}u \\  & ={lim}_{a\to \infty }{[-\frac{2}{7}{u}^{-7/2}]}_{1}^{a} \\  & =-\frac{2}{7}\cdot {lim}_{a\to \infty }{[{u}^{-7/2}]}_{1}^{a} \\  & =-\frac{2}{7}\cdot {lim}_{a\to \infty }[\frac{1}{{a}^{7/2}}-\frac{1}{{1}^{7/2}}] \\  & =-\frac{2}{7}\cdot (0-1) \\  & =\frac{2}{7}.\end{aligned}
$$

## q-350533

Evaluate the following integral. Do not round the answer.

${\int }_{0}^{\infty }\frac{3{x}^{2}}{\sqrt{({x}^{3}+1)^{3}}}\,\text{d}x=$
{{field-1}}

Observed components: {"C": 3, "n": 3, "A": 1, "B": 1, "p": "3/2", "lower": 0, "variable": "x", "radical": true, "domain": "x >= 0; 1*x^3+1>0", "correct_formula": "C/[A*n*(p-1)] * (A*L^n+B)^(1-p)"}.

Field and complete bank: [{"source_answer_id": "a0acdd02-a3ba-5daf-84fc-f0e64c6786e5", "source_value": "2", "correct": true, "recipe": "scale * (2)", "recipe_at_original_parameters": "2", "interpretation": "exact convergent limit", "full_value_replayed": true}]

Original fixed solution:

First, we substitute $u={x}^{3}+1.$ Differentiating, we get

$$
\frac{\text{d}u}{\text{d}x}=3{x}^{2}\,⟹\,\text{d}u=3{x}^{2}\text{d}x.
$$

Since $u\to \infty $ when $x\to \infty ,$ the table for the limits of integration using the rule $u={x}^{3}+1$ is as follows:

| $x$ | $0$ | $\infty $ |
| --- | --- | --- |
| $u$ | $1$ | $\infty $ |

So, the integral in terms of the new variable $u$ is

$$
{\int }_{0}^{\infty }\frac{3{x}^{2}}{\sqrt{({x}^{3}+1)^{3}}}\,\text{d}x={\int }_{1}^{\infty }\frac{1}{\sqrt{{u}^{3}}}\,\text{d}u
$$

Finally, we proceed by setting the upper bound equal to some parameter $a,$ integrating as usual, and then taking the limit as $a\to \infty .$

$$
\begin{aligned}{\int }_{0}^{\infty }\frac{3{x}^{2}}{\sqrt{({x}^{3}+1)^{3}}}\,\text{d}x & ={\int }_{1}^{\infty }\frac{1}{\sqrt{{u}^{3}}}\,\text{d}u \\  & ={\int }_{1}^{\infty }{u}^{-3/2}\,\text{d}u \\  & ={lim}_{a\to \infty }{\int }_{1}^{a}{u}^{-3/2}\,\text{d}u \\  & ={lim}_{a\to \infty }{[-2{u}^{-1/2}]}_{1}^{a} \\  & =-2\cdot {lim}_{a\to \infty }{[{u}^{-1/2}]}_{1}^{a} \\  & =-2\cdot {lim}_{a\to \infty }[\frac{1}{{a}^{1/2}}-\frac{1}{{1}^{1/2}}] \\  & =-2\cdot (0-1) \\  & =2.\end{aligned}
$$

## q-350536

Evaluate the following integral. Do not round the answer.

${\int }_{0}^{\infty }\frac{10{x}^{4}}{\sqrt{({x}^{5}+1)^{9}}}\,\text{d}x=$
{{field-1}}

Observed components: {"C": 10, "n": 5, "A": 1, "B": 1, "p": "9/2", "lower": 0, "variable": "x", "radical": true, "domain": "x >= 0; 1*x^5+1>0", "correct_formula": "C/[A*n*(p-1)] * (A*L^n+B)^(1-p)"}.

Field and complete bank: [{"source_answer_id": "2f416306-21bf-539b-9b9c-b3c0c7c1874f", "source_value": "\\frac{4}{7}", "correct": true, "recipe": "scale * (\\frac{4}{7})", "recipe_at_original_parameters": "\\frac{4}{7}", "interpretation": "exact convergent limit", "full_value_replayed": true}]

Original fixed solution:

First, we substitute $u={x}^{5}+1.$ Differentiating, we get

$$
\frac{\text{d}u}{\text{d}x}=5{x}^{4}\,⟹\,\text{d}u=5{x}^{4}\text{d}x.
$$

Since $u\to \infty $ when $x\to \infty ,$ the table for the limits of integration using the rule $u={x}^{5}+1$ is as follows:

| $x$ | $0$ | $\infty $ |
| --- | --- | --- |
| $u$ | $1$ | $\infty $ |

So, the integral in terms of the new variable $u$ is

$$
{\int }_{0}^{\infty }\frac{10{x}^{4}}{\sqrt{({x}^{5}+1)^{9}}}\,\text{d}x={\int }_{1}^{\infty }\frac{2}{\sqrt{{u}^{9}}}\,\text{d}u
$$

Finally, we proceed by setting the upper bound equal to some parameter $a,$ integrating as usual, and then taking the limit as $a\to \infty .$

$$
\begin{aligned}{\int }_{0}^{\infty }\frac{10{x}^{4}}{\sqrt{({x}^{5}+1)^{9}}}\,\text{d}x & ={\int }_{1}^{\infty }\frac{2}{\sqrt{{u}^{9}}}\,\text{d}u \\  & ={\int }_{1}^{\infty }2{u}^{-9/2}\,\text{d}u \\  & ={lim}_{a\to \infty }{\int }_{1}^{a}2{u}^{-9/2}\,\text{d}u \\  & ={lim}_{a\to \infty }{[-\frac{4}{7}{u}^{-7/2}]}_{1}^{a} \\  & =-\frac{4}{7}\cdot {lim}_{a\to \infty }{[{u}^{-7/2}]}_{1}^{a} \\  & =-\frac{4}{7}\cdot {lim}_{a\to \infty }[\frac{1}{{a}^{7/2}}-\frac{1}{{1}^{7/2}}] \\  & =-\frac{4}{7}\cdot (0-1) \\  & =\frac{4}{7}.\end{aligned}
$$

## Capability exceptions

Easy remains unclassified/unsupported by this package; no easy questions are claimed filled. q-6297 lacks rating, correct answer and worked solution. It remains unchanged and excluded. Its new source evidence would reopen classification. Canonical e-10717 supports the method but is never counted as available practice.

`templates.json` retains each source field, choice UUID/value and parameterized complete-value recipe. `review.md` places original replay and scaled variant side by side. `validation.json` separates source fidelity, independent mathematics, and actual engine grading.
