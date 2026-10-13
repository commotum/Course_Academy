# Template extraction

## Stage 1 — Specific source descriptions

Every following description preserves the captured expressions, variable roles, parameter domain, response fields and solution stages. Original bank values remain visible; none is silently dropped.


### q-15678 → observed_15678

The parameters are real. The captured x expression is `$\frac{1}{t - 2}$`, y expression `$t^{2}$`, and parameter domain `Complement(Reals, {2})`. Its exact x image is `Complement(Reals, {0})`. Isolate t and substitute into y; retain the supplied simplification/factorization row order.

Find the Cartesian equation of the curve defined parametrically by

$$
x=\frac{1}{t-2},\,\,\,y={t}^{2},\,t\ne 2.
$$

Field `selection`, `:answer-field.type/radio`. Complete observed bank:

- `28b55e3d-922e-5fd5-a435-05886bb984e3`: $y=-{(\frac{1+2x}{x})}^{2},\,x\ne 0$. Recipe: substitute `(x-h)/a` for every x operand; the whole equation and its explicit domain are transformed together. Captured incorrect designation.

- `8a657071-1650-5d6c-b5c4-92125994bb16`: $y={(\frac{1-2x}{x})}^{2},\,x\ne 0$. Recipe: substitute `(x-h)/a` for every x operand; the whole equation and its explicit domain are transformed together. Captured incorrect designation.

- `94ae029c-717d-594a-94b3-99e945ac9df3`: $y={(\frac{-1-2x}{x})}^{2},\,x\ne 0$. Recipe: substitute `(x-h)/a` for every x operand; the whole equation and its explicit domain are transformed together. Captured incorrect designation.

- `e5c8491d-ffbc-5e21-af51-3dd2104b993d`: $y={(\frac{1+2x}{x})}^{2},\,x\ne 0$. Recipe: substitute `(x-h)/a` for every x operand; the whole equation and its explicit domain are transformed together. Captured correct designation.

- `f9e82ab8-5078-5eff-8d80-7c402c1a0adc`: $y=-{(\frac{-1+2x}{x})}^{2},\,x\ne 0$. Recipe: substitute `(x-h)/a` for every x operand; the whole equation and its explicit domain are transformed together. Captured incorrect designation.

Solution stage evidence:

To find the Cartesian equation, we eliminate $t.$ First, we use the $x$ equation to solve for $t:$

$$
\begin{aligned}x & =\frac{1}{t-2} \\ x(t-2) & =1 \\ t-2 & =\frac{1}{x} \\ t & =\frac{1}{x}+2 \\ t & =\frac{1+2x}{x}\end{aligned}
$$

Now substituting $t=\frac{1+2x}{x}$ into our expression for $y={t}^{2},$ we get

$$
\begin{aligned}y & ={(\frac{1+2x}{x})}^{2}\end{aligned}
$$

So the Cartesian equation of the given curve is $y={(\frac{1+2x}{x})}^{2}.$

Finally, since $t\ne 2$ and $x=\frac{1}{t-2},$ we must have $x\ne 0.$

So, the complete Cartesian equation is

$$
y={(\frac{1+2x}{x})}^{2},\,x\ne 0.
$$


### q-15755 → observed_15755

The parameters are real. The captured x expression is `$t - 2$`, y expression `$t^{2}$`, and parameter domain `Reals`. Its exact x image is `Reals`. Isolate t and substitute into y; retain the supplied simplification/factorization row order.

Find the Cartesian equation of the curve defined parametrically by
$x = t - 2, y = t^{2}, t ∈ (- ∞, ∞)$.

Field `selection`, `:answer-field.type/radio`. Complete observed bank:

- `85aa4d14-80d1-5752-8fd1-0411a67d3ba3`: $y = (x - 2)^{2}, x ∈ (- ∞, ∞)$. Recipe: substitute `(x-h)/a` for every x operand; the whole equation and its explicit domain are transformed together. No captured correct designation.

- `88ed67e5-8008-5e9a-bf16-7f21332088a2`: $y = x^{2}, x ∈ (- ∞, ∞)$. Recipe: substitute `(x-h)/a` for every x operand; the whole equation and its explicit domain are transformed together. No captured correct designation.

- `cb64b154-ef9a-5411-b1ee-b7338acfc194`: $y = x + 2, x ∈ (- ∞, ∞)$. Recipe: substitute `(x-h)/a` for every x operand; the whole equation and its explicit domain are transformed together. No captured correct designation.

- `ec57c426-a179-55be-92bb-f8bfdbc1e791`: $y = (x + 4)^{2}, x ∈ (- ∞, ∞)$. Recipe: substitute `(x-h)/a` for every x operand; the whole equation and its explicit domain are transformed together. No captured correct designation.

- `ed10e3fb-a8f9-5fb6-a491-53e533208b77`: $y = (x + 2)^{2}, x ∈ (- ∞, ∞)$. Recipe: substitute `(x-h)/a` for every x operand; the whole equation and its explicit domain are transformed together. No captured correct designation.

Solution stage evidence:

No captured solution. The generated t=x+2 and y=(x+2)² solution is explicitly authored.


### q-102664 → observed_102664

The parameters are real. The captured x expression is `$1 - 2 t$`, y expression `$(t - 2)^{2} (t + 1)$`, and parameter domain `Reals`. Its exact x image is `Reals`. Isolate t and substitute into y; retain the supplied simplification/factorization row order.

Find the Cartesian equation of the curve defined parametrically by

$$
x=1-2t,\,\,\,y=(t-2)^{2}(t+1),\,t\in (-\infty ,\infty ).
$$

Field `selection`, `:answer-field.type/radio`. Complete observed bank:

- `166d0a6c-05a8-5786-b48c-f4e93b1f3b0c`: $y=-\frac{1}{2}(x+3)^{2}(x-3)$. Recipe: substitute `(x-h)/a` for every x operand; the whole equation and its explicit domain are transformed together. Captured incorrect designation.

- `1dc3551c-3d67-5cc6-8438-b49e16bdf115`: $y=\frac{1}{4}(x+3)^{2}(x-3)$. Recipe: substitute `(x-h)/a` for every x operand; the whole equation and its explicit domain are transformed together. Captured incorrect designation.

- `45c69b36-6d72-503c-9c36-09fae5919dba`: $y=-\frac{1}{8}(x+3)^{2}(x-3)$. Recipe: substitute `(x-h)/a` for every x operand; the whole equation and its explicit domain are transformed together. Captured correct designation.

- `d00d1ba1-3166-54b8-b47f-c8a1f0daadff`: $y=-\frac{1}{4}(x+3)(x-3)^{2}$. Recipe: substitute `(x-h)/a` for every x operand; the whole equation and its explicit domain are transformed together. Captured incorrect designation.

- `f55f988f-ed06-5427-b54b-471e782de7ff`: $y=\frac{1}{8}(x+3)(x-3)^{2}$. Recipe: substitute `(x-h)/a` for every x operand; the whole equation and its explicit domain are transformed together. Captured incorrect designation.

Solution stage evidence:

To find the Cartesian equation, we eliminate $t.$ First, we use the $x$ equation to solve for $t:$

$$
\begin{aligned}x=1-2t\,⇒\,t=\frac{1-x}{2}\end{aligned}
$$

Now, substituting $t=\frac{1-x}{2}$ into our expression for $y,$ we get

$$
\begin{aligned}y & ={(\frac{1-x}{2}-2)}^{2}(\frac{1-x}{2}+1) \\  & ={(\frac{1-x-4}{2})}^{2}(\frac{1-x+2}{2}) \\  & ={(\frac{-x-3}{2})}^{2}(\frac{3-x}{2}) \\  & =-\frac{1}{8}(x+3)^{2}(x-3).\end{aligned}
$$

So the Cartesian equation of the given curve is $y=-\frac{1}{8}(x+3)^{2}(x-3).$


### q-102668 → observed_102668

The parameters are real. The captured x expression is `$\frac{t}{2} - \frac{5}{2}$`, y expression `$(t - 4) (t^{2} - 25)$`, and parameter domain `Reals`. Its exact x image is `Reals`. Isolate t and substitute into y; retain the supplied simplification/factorization row order.

Find the Cartesian equation of the curve defined parametrically by

$$
x=\frac{t-5}{2},\,\,\,y=({t}^{2}-25)(t-4),\,t\in (-\infty ,\infty ).
$$

Field `selection`, `:answer-field.type/radio`. Complete observed bank:

- `77633f7b-a4f6-5605-b197-300dedbccde8`: $y=4x(x+5)(2x+1)$. Recipe: substitute `(x-h)/a` for every x operand; the whole equation and its explicit domain are transformed together. Captured correct designation.

- `7b957847-885e-58d3-87c4-376c6913a3f1`: $y=2(2x+1)^{3}$. Recipe: substitute `(x-h)/a` for every x operand; the whole equation and its explicit domain are transformed together. Captured incorrect designation.

- `878bf002-299b-523a-93bd-80e7642d9000`: $y=4x(2x+1)(2x-5)$. Recipe: substitute `(x-h)/a` for every x operand; the whole equation and its explicit domain are transformed together. Captured incorrect designation.

- `8b44f564-28f4-5786-9cf7-4b0382705e60`: $y=(2x+1)^{3}$. Recipe: substitute `(x-h)/a` for every x operand; the whole equation and its explicit domain are transformed together. Captured incorrect designation.

- `abe07822-f677-59f4-b923-e8aa2238417d`: $y=2x(x-5)(2x+1)$. Recipe: substitute `(x-h)/a` for every x operand; the whole equation and its explicit domain are transformed together. Captured incorrect designation.

Solution stage evidence:

To find the Cartesian equation, we eliminate $t.$ First, we use the $x$ equation to solve for $t:$

$$
\begin{aligned}x=\frac{t-5}{2}\,⇒\,t=2x+5\end{aligned}
$$

Now, substituting $t=2x+5$ into our expression for $y,$ we get

$$
\begin{aligned}y & =((2x+5)^{2}-25)(2x+5-4) \\  & =(4{x}^{2}+20x+25-25)(2x+1) \\  & =(4{x}^{2}+20x)(2x+1) \\  & =4x(x+5)(2x+1).\end{aligned}
$$

So the Cartesian equation of the given curve is $y=4x(x+5)(2x+1).$


### q-15653 → observed_15653

The parameters are real. The captured x expression is `$5 - t$`, y expression `$t^{2} - 1$`, and parameter domain `Reals`. Its exact x image is `Reals`. Isolate t and substitute into y; retain the supplied simplification/factorization row order.

Find the Cartesian equation of the curve defined parametrically by

$$
x=5-t,\,\,\,y={t}^{2}-1,\,t\in (-\infty ,\infty ).
$$

Field `selection`, `:answer-field.type/radio`. Complete observed bank:

- `20505f6c-76c3-5503-9aa4-58967d3492b7`: $y=5{x}^{2}+x+2,\,x\in (-\infty ,\infty )$. Recipe: substitute `(x-h)/a` for every x operand; the whole equation and its explicit domain are transformed together. Captured incorrect designation.

- `80f54d66-49b1-5053-b817-7ebbba893a52`: $y=-{x}^{2}+10x-24,\,x\in (-\infty ,\infty )$. Recipe: substitute `(x-h)/a` for every x operand; the whole equation and its explicit domain are transformed together. Captured incorrect designation.

- `be1b076f-fa12-524f-9aeb-e359af08e3c6`: $y=2{x}^{2}-5x-12,\,x\in (-\infty ,\infty )$. Recipe: substitute `(x-h)/a` for every x operand; the whole equation and its explicit domain are transformed together. Captured incorrect designation.

- `db025224-4e97-5e03-8743-b73b379a2eea`: $y=-4{x}^{2}-2x+5,\,x\in (-\infty ,\infty )$. Recipe: substitute `(x-h)/a` for every x operand; the whole equation and its explicit domain are transformed together. Captured incorrect designation.

- `e21deb99-1b3a-5d03-bd8b-47900ebde6d2`: $y={x}^{2}-10x+24,\,x\in (-\infty ,\infty )$. Recipe: substitute `(x-h)/a` for every x operand; the whole equation and its explicit domain are transformed together. Captured correct designation.

Solution stage evidence:

To find the Cartesian equation, we eliminate $t.$ First, we use the $x$ equation to solve for $t:$

$$
\begin{aligned}x=5-t\,⇒\,t=5-x\end{aligned}
$$

Now, substituting $t=5-x$ into our expression for $y,$ we get

$$
\begin{aligned}y & =(5-x)^{2}-1 \\  & =25-10x+{x}^{2}-1 \\  & ={x}^{2}-10x+24\end{aligned}
$$

So the Cartesian equation of the given curve is $y={x}^{2}-10x+24.$

Finally, since $t\in (-\infty ,\infty )$ and $x=5-t,$ we must have $x\in (-\infty ,\infty ).$

So, the complete Cartesian equation is

$$
y={x}^{2}-10x+24,\,x\in (-\infty ,\infty ).
$$


### q-15654 → observed_15654

The parameters are real. The captured x expression is `$\sqrt{t}$`, y expression `$t (9 - t)$`, and parameter domain `Interval(0, oo)`. Its exact x image is `Interval(0, oo)`. Isolate t and substitute into y; retain the supplied simplification/factorization row order.

Find the Cartesian equation of the curve defined parametrically by

$$
x=\sqrt{t},\,\,\,y=t(9-t),\,t\ge 0.
$$

Field `selection`, `:answer-field.type/radio`. Complete observed bank:

- `20261641-fd84-5f77-86f9-34f0fa33a731`: $y=-x(3+{x}^{2}),\,x\ge 0$. Recipe: substitute `(x-h)/a` for every x operand; the whole equation and its explicit domain are transformed together. Captured incorrect designation.

- `24a93e7a-6bb2-5462-9150-db02feafe760`: $y=2{x}^{2}(9-{x}^{2}),\,x\ge 0$. Recipe: substitute `(x-h)/a` for every x operand; the whole equation and its explicit domain are transformed together. Captured incorrect designation.

- `43312442-bb1a-5f99-b317-fe4c73170b3c`: $y=-2x(9-{x}^{2}),\,x\ge 0$. Recipe: substitute `(x-h)/a` for every x operand; the whole equation and its explicit domain are transformed together. Captured incorrect designation.

- `65eba75f-db0c-5c62-b886-977dc76e3ace`: $y={x}^{2}(9-{x}^{2}),\,x\ge 0$. Recipe: substitute `(x-h)/a` for every x operand; the whole equation and its explicit domain are transformed together. Captured correct designation.

- `8180fde6-b73a-51b5-92cf-81508b0e34d4`: $y={x}^{2}(3+{x}^{2}),\,x\ge 0$. Recipe: substitute `(x-h)/a` for every x operand; the whole equation and its explicit domain are transformed together. Captured incorrect designation.

Solution stage evidence:

To find the Cartesian equation, we eliminate $t.$ First, we use the $x$ equation to solve for $t:$

$$
\begin{aligned}x=\sqrt{t}\,⇒\,t={x}^{2}\end{aligned}
$$

Now, substituting $t={x}^{2}$ into our expression for $y,$ we get

$$
\begin{aligned}y & ={x}^{2}(9-{x}^{2})\end{aligned}
$$

So the Cartesian equation of the given curve is $y={x}^{2}(9-{x}^{2}).$

Finally, since $t\ge 0$ and $x=\sqrt{t},$ we must have $x\ge 0.$

So, the complete Cartesian equation is

$$
y={x}^{2}(9-{x}^{2}),\,x\ge 0.
$$


### q-15677 → observed_15677

The parameters are real. The captured x expression is `$\frac{1}{t + 1}$`, y expression `$\frac{1}{t - 2}$`, and parameter domain `Complement(Reals, {-1, 2})`. Its exact x image is `Complement(Reals, {0, 1/3})`. Isolate t and substitute into y; retain the supplied simplification/factorization row order.

Find the Cartesian equation of the curve defined parametrically by

$$
x=\frac{1}{t+1},\,\,\,y=\frac{1}{t-2},\,t\ne -1,\,2.
$$

Field `selection`, `:answer-field.type/radio`. Complete observed bank:

- `1d045052-a873-54a4-84e5-7bf4e6574118`: $y=\frac{3x}{1+2x},\,x\ne -\frac{1}{2},\,0$. Recipe: substitute `(x-h)/a` for every x operand; the whole equation and its explicit domain are transformed together. Captured incorrect designation.

- `22c4e507-f7c6-5de7-b268-663b56128436`: $y=\frac{x}{1-x},\,\,x\ne 0,\,1$. Recipe: substitute `(x-h)/a` for every x operand; the whole equation and its explicit domain are transformed together. Captured incorrect designation.

- `81222995-5d78-5bef-9adf-4e395c20b564`: $y=\frac{x}{1+x},\,\,x\ne -1,\,0$. Recipe: substitute `(x-h)/a` for every x operand; the whole equation and its explicit domain are transformed together. Captured incorrect designation.

- `af021638-e540-5191-98d4-73961ba655c5`: $y=\frac{x}{1-3x},\,x\ne 0,\,\frac{1}{3}$. Recipe: substitute `(x-h)/a` for every x operand; the whole equation and its explicit domain are transformed together. Captured correct designation.

- `db25591c-9dfe-5ed2-9b3e-5d90e2274d32`: $y=\frac{3x}{1-2x},\,x\ne 0,\,\frac{1}{2}$. Recipe: substitute `(x-h)/a` for every x operand; the whole equation and its explicit domain are transformed together. Captured incorrect designation.

Solution stage evidence:

To find the Cartesian equation, we eliminate $t.$ First, we use the $x$ equation to solve for $t:$

$$
\begin{aligned}x=\frac{1}{t+1}\,⇒\,t=\frac{1}{x}-1\end{aligned}
$$

Now substituting $t=\frac{1}{x}-1$ into our expression for $y$, we get

$$
\begin{aligned}y & =\frac{1}{((\frac{1}{x}-1)-2)} \\ y & =\frac{1}{(\frac{1}{x}-3)} \\ y & =\frac{1}{(\frac{1-3x}{x})} \\ y & =\frac{x}{1-3x}\end{aligned}
$$

So the Cartesian equation of the given curve is $y=\frac{x}{1-3x}.$

Finally, since $t\ne -1,\,2$ and $x=\frac{1}{t+1},$ we must have $x\ne 0,\,\frac{1}{3}.$

So, the complete Cartesian equation is

$$
y=\frac{x}{1-3x},\,x\ne 0,\,\frac{1}{3}.
$$


### q-276277 → observed_276277

The parameters are real. The captured x expression is `$t + 1$`, y expression `$t^{2} + 4$`, and parameter domain `Reals`. Its exact x image is `Reals`. Isolate t and substitute into y; retain the supplied simplification/factorization row order.

Consider the curve defined parametrically as

$$
x=t+1,\,\,\,y={t}^{2}+4,\,t\in (-\infty ,\infty ).
$$

The Cartesian equation of this curve is

$y=$
{{field-1}}.

Field `field-1`, `:answer-field.type/blank`. Complete observed bank:

- `f98dd494-7f2f-57dc-af90-42867eb57511`: ${x}^{2}-2x+5$. Recipe: substitute `(x-h)/a` for every x operand; the whole equation and its explicit domain are transformed together. Captured correct designation.

Solution stage evidence:

To find the Cartesian equation, we eliminate $t.$ First, we use the $x$ equation to solve for $t:$

$$
\begin{aligned}x=t+1\,⇒\,t=x-1\end{aligned}
$$

Now, substituting $t=x-1$ into our expression for $y,$ we get

$$
\begin{aligned}y & =(x-1)^{2}+4 \\ y & ={x}^{2}-2x+5\end{aligned}
$$

So, the Cartesian equation of the given curve is 
$y={x}^{2}-2x+5.$


### q-276284 → observed_276284

The parameters are real. The captured x expression is `$\frac{1}{t - 4}$`, y expression `$\frac{t}{2 t + 1}$`, and parameter domain `Complement(Reals, {-1/2, 4})`. Its exact x image is `Complement(Reals, {-2/9, 0})`. Isolate t and substitute into y; retain the supplied simplification/factorization row order.

Consider the curve defined parametrically as

$$
x=\frac{1}{t-4},\,\,\,y=\frac{t}{2t+1},\,t\ne 4,\,\,\,t\ne -\frac{1}{2}.
$$

The Cartesian equation of this curve is

$y=$
{{field-1}}$,\,x\ne $
{{field-2}}$,\,\,\,x\ne 0.$

Field `field-2`, `:answer-field.type/blank`. Complete observed bank:

- `efebc768-607d-542f-b7b0-0c55ce311093`: $-\frac{2}{9}$. Recipe: substitute `(x-h)/a` for every x operand; the whole equation and its explicit domain are transformed together. Captured correct designation.

Field `field-1`, `:answer-field.type/blank`. Complete observed bank:

- `27cbd4cc-c040-570c-8981-361a2c723b70`: $\frac{4x+1}{9x+2}$. Recipe: substitute `(x-h)/a` for every x operand; the whole equation and its explicit domain are transformed together. Captured correct designation.

Solution stage evidence:

To find the Cartesian equation, we eliminate $t.$ First, we use the $x$ equation to solve for $t:$

$$
x=\frac{1}{t-4}\,⇒\,t=\frac{4x+1}{x}
$$

Now, substituting $t=\frac{4x+1}{x}$ into our expression for $y,$ we get

$$
\begin{aligned}y & =\frac{(\frac{4x+1}{x})}{(2\cdot \frac{4x+1}{x}+1)} \\ y & =\frac{(\frac{4x+1}{x})}{(\frac{8x+2}{x}+1)} \\ y & =\frac{(\frac{4x+1}{x})}{(\frac{9x+2}{x})} \\ y & =\frac{4x+1}{\cancel{x}}\cdot \frac{\cancel{x}}{9x+2} \\ y & =\frac{4x+1}{9x+2}\end{aligned}
$$

So, the Cartesian equation of the given curve is $y=\frac{4x+1}{9x+2}.$

Finally, since $t\ne -\frac{1}{2}$ and $x=\frac{1}{t-4}$ has range $x\ne 0,$ we must have 
$x\ne -\frac{2}{9},\text{ }0.$ 

Therefore, the complete Cartesian equation is

$$
y=\frac{4x+1}{9x+2},\,x\ne -\frac{2}{9},\,\,\,x\ne 0.
$$


### q-320871 → observed_276277

The parameters are real. The captured x expression is `$t - 2$`, y expression `$t^{2} - 4$`, and parameter domain `Reals`. Its exact x image is `Reals`. Isolate t and substitute into y; retain the supplied simplification/factorization row order.

Consider the curve defined parametrically as

$$
x=t-2,\,\,\,y={t}^{2}-4,\,t\in (-\infty ,\infty ).
$$

The Cartesian equation of this curve is

$y=$
{{field-1}}.

Field `field-1`, `:answer-field.type/blank`. Complete observed bank:

- `1a1c86cb-411d-534e-810a-79bce25d9b55`: ${x}^{2}+4x$. Recipe: substitute `(x-h)/a` for every x operand; the whole equation and its explicit domain are transformed together. Captured correct designation.

Solution stage evidence:

To find the Cartesian equation, we eliminate $t.$ First, we use the $x$ equation to solve for $t:$

$$
\begin{aligned}x=t-2\,⇒\,t=x+2\end{aligned}
$$

Now, substituting $t=x+2$ into our expression for $y,$ we get

$$
\begin{aligned}y & =(x+2)^{2}-4 \\ y & ={x}^{2}+4x\end{aligned}
$$

So, the Cartesian equation of the given curve is 
$y={x}^{2}+4x.$


### q-320926 → observed_320926

The parameters are real. The captured x expression is `$\frac{1}{t + 3}$`, y expression `$\frac{t}{1 - 2 t}$`, and parameter domain `Complement(Reals, {-3, 1/2})`. Its exact x image is `Complement(Reals, {0, 2/7})`. Isolate t and substitute into y; retain the supplied simplification/factorization row order.

Consider the curve defined parametrically as

$$
x=\frac{1}{t+3},\,\,\,y=\frac{t}{-2t+1},\,t\ne -3,\,\,\,t\ne \frac{1}{2}.
$$

The Cartesian equation of this curve is

$y=$
{{field-1}}$,\,x\ne $
{{field-2}}$,\,\,\,x\ne 0.$

Field `field-1`, `:answer-field.type/blank`. Complete observed bank:

- `cd8f4c87-04b9-5012-91a0-2fa1e73539ce`: $\frac{1-3x}{7x-2}$. Recipe: substitute `(x-h)/a` for every x operand; the whole equation and its explicit domain are transformed together. Captured correct designation.

Field `field-2`, `:answer-field.type/blank`. Complete observed bank:

- `5584afb0-f812-5610-86a2-9366973652b3`: $\frac{2}{7}$. Recipe: substitute `(x-h)/a` for every x operand; the whole equation and its explicit domain are transformed together. Captured correct designation.

Solution stage evidence:

To find the Cartesian equation, we eliminate $t.$ First, we use the $x$ equation to solve for $t:$

$$
x=\frac{1}{t+3}\,⇒\,t=-3+\frac{1}{x}
$$

Now, substituting $t=-3+\frac{1}{x}$ into our expression for $y,$ we get

$$
\begin{aligned}y & =\frac{(-3+\frac{1}{x})}{(-2\,(-3+\frac{1}{x})+1)} \\  & =\frac{(-3+\frac{1}{x})}{(6-\frac{2}{x}+1)} \\  & =\frac{(-3+\frac{1}{x})}{(7-\frac{2}{x})} \\  & =\frac{-3x+1}{\cancel{x}}\cdot \frac{\cancel{x}}{7x-2} \\  & =\frac{1-3x}{7x-2}.\end{aligned}
$$

So, the Cartesian equation of the given curve is $y=\frac{1-3x}{7x-2}.$

Finally, since $t\ne \frac{1}{2}$ and $x=\frac{1}{t+3}$ has range $x\ne 0,$ we must have 
$x\ne \frac{2}{7},\text{ }0.$ 

Therefore, the complete Cartesian equation is

$$
y=\frac{1-3x}{7x-2},\,x\ne \frac{2}{7},\,\,\,x\ne 0.
$$


### q-321074 → observed_321074

The parameters are real. The captured x expression is `$\frac{t}{3} + \frac{1}{3}$`, y expression `$(1 - t)^{2} (t^{2} - 4)$`, and parameter domain `Reals`. Its exact x image is `Reals`. Isolate t and substitute into y; retain the supplied simplification/factorization row order.

Find the Cartesian equation of the curve defined parametrically by

$$
x=\frac{t+1}{3},\,\,\,y=({t}^{2}-4)(1-t)^{2},\,t\in (-\infty ,\infty ).
$$

$y=$
{{field-1}}.

Field `field-1`, `:answer-field.type/blank`. Complete observed bank:

- `52d81c8c-e7c3-5d18-9722-ffa9b4fbde0b`: $3(3x+1)(x-1)(2-3x)^{2}$. Recipe: substitute `(x-h)/a` for every x operand; the whole equation and its explicit domain are transformed together. Captured correct designation.

Solution stage evidence:

To find the Cartesian equation, we eliminate $t.$ First, we use the $x$ equation to solve for $t:$

$$
\begin{aligned}x=\frac{t+1}{3}\,⇒\,t=3x-1\end{aligned}
$$

Now, substituting $t=3x-1$ into our expression for $y,$ we get

$$
\begin{aligned}y & =((3x-1)^{2}-4){(1-(3x-1))}^{2} \\  & =(9{x}^{2}-6x+1-4)(2-3x)^{2} \\  & =(9{x}^{2}-6x-3)(2-3x)^{2} \\  & =3(3{x}^{2}-2x-1)(2-3x)^{2} \\  & =3(3x+1)(x-1)(2-3x)^{2}.\end{aligned}
$$

So, the Cartesian equation of the given curve is $y=3(3x+1)(x-1)(2-3x)^{2}.$


### q-321075 → observed_321075

The parameters are real. The captured x expression is `$\frac{1}{4} - \frac{t}{4}$`, y expression `$(t + 1)^{2} (t^{2} - 1)$`, and parameter domain `Reals`. Its exact x image is `Reals`. Isolate t and substitute into y; retain the supplied simplification/factorization row order.

Find the Cartesian equation of the curve defined parametrically by

$$
x=\frac{1-t}{4},\,\,\,y=({t}^{2}-1)(1+t)^{2},\,t\in (-\infty ,\infty ).
$$

$y=$
{{field-1}}.

Field `field-1`, `:answer-field.type/blank`. Complete observed bank:

- `1e6c8835-3261-554a-afbb-957028b9b565`: $32x(2x-1)^{3}$. Recipe: substitute `(x-h)/a` for every x operand; the whole equation and its explicit domain are transformed together. Captured correct designation.

Solution stage evidence:

To find the Cartesian equation, we eliminate $t.$ First, we use the $x$ equation to solve for $t:$

$$
\begin{aligned}x=\frac{1-t}{4}\,⇒\,t=1-4x\end{aligned}
$$

Now, substituting $t=1-4x$ into our expression for $y,$ we get

$$
\begin{aligned}y & =((1-4x)^{2}-1)((1+(1-4x))^{2}) \\  & =(1-8x+16{x}^{2}-1)((2-4x)^{2}) \\  & =(-8x+16{x}^{2})(4)(1-2x)^{2} \\  & =8x(2x-1)(2-4x)^{2} \\  & =8x(2x-1)\cdot 4(1-2x)^{2} \\  & =32x(2x-1)^{3}.\end{aligned}
$$

So, the Cartesian equation of the given curve is $y=32x(2x-1)^{3}.$


### q-321084 → observed_321084

The parameters are real. The captured x expression is `$\sqrt{t + 1}$`, y expression `$t (4 - t)$`, and parameter domain `Interval(0, oo)`. Its exact x image is `Interval(1, oo)`. Isolate t and substitute into y; retain the supplied simplification/factorization row order.

Consider the curve defined parametrically as

$$
x=\sqrt{\,t+1\,},\,\,\,y=t(4-t),\,t\ge 0.
$$

The Cartesian equation of this curve is

$y=$
{{field-1}}$,\,x\ge 1.$

Field `field-1`, `:answer-field.type/blank`. Complete observed bank:

- `f5593662-8d5b-547d-8bc2-6520dd120c28`: $({x}^{2}-1)(5-{x}^{2})$. Recipe: substitute `(x-h)/a` for every x operand; the whole equation and its explicit domain are transformed together. Captured correct designation.

Solution stage evidence:

To find the Cartesian equation, we eliminate $t.$ First, we use the $x$ equation to solve for $t:$

$$
\begin{aligned}x=\sqrt{\,t+1\,}\,⇒\,t={x}^{2}-1\end{aligned}
$$

Now, substituting $t={x}^{2}-1$ into our expression for $y,$ we get

$$
\begin{aligned}y & =({x}^{2}-1)(4-({x}^{2}-1)) \\  & =({x}^{2}-1)(5-{x}^{2})\end{aligned}
$$

So, the Cartesian equation of the given curve is $y=({x}^{2}-1)(5-{x}^{2}).$

Finally, since $t\ge 0$ and $t={x}^{2}-1,$ we must have ${x}^{2}-1\ge 0,$ i.e., $x\ge 1.$

Therefore, the complete Cartesian equation is $y=({x}^{2}-1)(5-{x}^{2}),\,x\ge 1.$


### q-321090 → observed_321090

The parameters are real. The captured x expression is `$\sqrt{t^{2} - 9}$`, y expression `$3 t^{2}$`, and parameter domain `Interval(3, oo)`. Its exact x image is `Interval(0, oo)`. Isolate t² and substitute into y; retain the supplied simplification/factorization row order.

Consider the curve defined parametrically as

$$
x=\sqrt{{t}^{2}-9},\,\,\,y=3{t}^{2},\,t\ge 3.
$$

The Cartesian equation of this curve is

$y=$
{{field-1}}$,\,x\ge 0.$

Field `field-1`, `:answer-field.type/blank`. Complete observed bank:

- `d744dcd4-0a3e-511e-b60c-7b2673712e59`: $3{x}^{2}+27$. Recipe: substitute `(x-h)/a` for every x operand; the whole equation and its explicit domain are transformed together. Captured correct designation.

Solution stage evidence:

To find the Cartesian equation, we eliminate $t.$ First, we use the $x$ equation to solve for ${t}^{2}:$

$$
x=\sqrt{{t}^{2}-9}\,⇒\,{t}^{2}={x}^{2}+9
$$

Now, substituting ${t}^{2}={x}^{2}+9$ into our expression for $y,$ we get

$$
y=3({x}^{2}+9)=3{x}^{2}+27.
$$

So, the Cartesian equation of the given curve is $y=3{x}^{2}+27.$

Finally, since $t\ge 3$ and $x=\sqrt{{t}^{2}-9},$ we must have $x\ge 0.$

Therefore, the complete Cartesian equation is $y=3{x}^{2}+27,\,x\ge 0.$


### q-321141 → observed_321141

The parameters are real. The captured x expression is `$\frac{1}{2 t + 1}$`, y expression `$(t + 1)^{2}$`, and parameter domain `Complement(Reals, {-1/2})`. Its exact x image is `Complement(Reals, {0})`. Isolate t and substitute into y; retain the supplied simplification/factorization row order.

Consider the curve defined parametrically as

$$
x=\frac{1}{2t+1},\,\,\,y=(t+1)^{2},\,t\ne -\frac{1}{2}.
$$

The Cartesian equation of this curve is

$y=$
{{field-1}}$,\,x\ne $
{{field-2}}.

Field `field-2`, `:answer-field.type/blank`. Complete observed bank:

- `d45792f3-0a28-56c8-a67d-3d50eaf93eb2`: $0$. Recipe: substitute `(x-h)/a` for every x operand; the whole equation and its explicit domain are transformed together. Captured correct designation.

Field `field-1`, `:answer-field.type/blank`. Complete observed bank:

- `fba2eb2c-542e-5741-9da4-b68fe7825059`: $\frac{(1+x)^{2}}{4{x}^{2}}$. Recipe: substitute `(x-h)/a` for every x operand; the whole equation and its explicit domain are transformed together. Captured correct designation.

Solution stage evidence:

To find the Cartesian equation, we eliminate $t.$ First, we use the $x$ equation to solve for $t:$

$$
x=\frac{1}{2t+1}\,⇒\,2t+1=\frac{1}{x}\,⇒\,t=\frac{1}{2x}-\frac{1}{2}.
$$

Now, substituting $t=\frac{1}{2x}-\frac{1}{2}$ into our expression for $y,$ we get

$$
\begin{aligned}y & ={(\frac{1}{2x}-\frac{1}{2}+1)}^{2} \\  & ={(\frac{1}{2x}+\frac{1}{2})}^{2} \\  & ={(\frac{1+x}{2x})}^{2} \\  & =\frac{(1+x)^{2}}{4{x}^{2}}.\end{aligned}
$$

So, the Cartesian equation of the given curve is $y=\frac{(1+x)^{2}}{4{x}^{2}}.$

Finally, since $t\ne -\frac{1}{2}$ and $x=\frac{1}{2t+1}$ we must have $x\ne 0.$

Therefore, the complete Cartesian equation is

$$
y=\frac{(1+x)^{2}}{4{x}^{2}},\,x\ne 0.
$$


### q-321410 → observed_321410

The parameters are real. The captured x expression is `$2 - 3 t$`, y expression `$- \frac{1}{t}$`, and parameter domain `Complement(Reals, {0})`. Its exact x image is `Complement(Reals, {2})`. Isolate t and substitute into y; retain the supplied simplification/factorization row order.

Consider the curve defined parametrically as

$$
x=-3t+2,\,\,\,y=-\frac{1}{t},\,t\ne 0.
$$

The Cartesian equation of this curve is

$y=$
{{field-1}}$,\,x\ne $
{{field-2}}.

Field `field-2`, `:answer-field.type/blank`. Complete observed bank:

- `b3625268-1369-5f41-a534-a0649eceb53b`: $2$. Recipe: substitute `(x-h)/a` for every x operand; the whole equation and its explicit domain are transformed together. Captured correct designation.

Field `field-1`, `:answer-field.type/blank`. Complete observed bank:

- `e2d9df89-b63c-55a8-bd14-62b985a73272`: $\frac{3}{x-2}$. Recipe: substitute `(x-h)/a` for every x operand; the whole equation and its explicit domain are transformed together. Captured correct designation.

Solution stage evidence:

To find the Cartesian equation, we eliminate $t.$ First, we use the $x$ equation to solve for $t:$

$$
\begin{aligned}x=-3t+2\,⇒\,t=\frac{2-x}{3}\end{aligned}
$$

Now, substituting $t=\frac{2-x}{3}$ into our expression for $y,$ we get

$$
\begin{aligned}y & =-\frac{1}{(\frac{2-x}{3})} \\ y & =\frac{3}{x-2}\end{aligned}
$$

So, the Cartesian equation of the given curve is $y=\frac{3}{x-2}.$

Finally, since $t\ne 0$ and $x=-3t+2$ , we must have $x\ne 2.$ 

Therefore, the complete Cartesian equation is

$$
y=\frac{3}{x-2},\,x\ne 2.
$$


### q-6828 → observed_6828

The parameters are real. The captured x expression is `$t^{2} + 5$`, y expression `$\frac{1}{t^{2}}$`, and parameter domain `Complement(Reals, {0})`. Its exact x image is `Interval.open(5, oo)`. Isolate t² and substitute into y; retain the supplied simplification/factorization row order.

Find the Cartesian equation of the curve defined parametrically by

$$
x={t}^{2}+5,\,\,\,y=\frac{1}{{t}^{2}},\,t\ne 0.
$$

Field `selection`, `:answer-field.type/radio`. Complete observed bank:

- `085c2edd-3369-5dc5-a8be-7a04e4833c75`: $y=\frac{1}{x-5},\,x\ne 5$. Recipe: substitute `(x-h)/a` for every x operand; the whole equation and its explicit domain are transformed together. Captured correct designation.

- `23ef77a2-3fdc-5a4c-8d16-fa9808fc0f18`: $y=-\frac{2}{x},\,x\ne 0$. Recipe: substitute `(x-h)/a` for every x operand; the whole equation and its explicit domain are transformed together. Captured incorrect designation.

- `392acd54-3425-5339-9d3d-6a019cf5800e`: $y=\frac{1}{{x}^{2}},\,x\ne 0$. Recipe: substitute `(x-h)/a` for every x operand; the whole equation and its explicit domain are transformed together. Captured incorrect designation.

- `99b89343-add4-5f68-b419-80457c1c4731`: $y=\frac{5}{x},\,x\ne 0$. Recipe: substitute `(x-h)/a` for every x operand; the whole equation and its explicit domain are transformed together. Captured incorrect designation.

- `f75b4892-5861-5baf-acfb-fc468d5720ec`: $y=\frac{1}{x+5},\,x\ne -5$. Recipe: substitute `(x-h)/a` for every x operand; the whole equation and its explicit domain are transformed together. Captured incorrect designation.

Solution stage evidence:

To find the Cartesian equation, we eliminate $t.$ First, we use the $x$ equation to solve for ${t}^{2}:$

$$
\begin{aligned}x={t}^{2}+5\,⇒\,{t}^{2}=x-5\end{aligned}
$$

Now, substituting ${t}^{2}=x-5$ into our expression for $y,$ we get

$$
\begin{aligned}y & =\frac{1}{x-5}\end{aligned}
$$

So the Cartesian equation of the given curve is $y=\frac{1}{x-5}.$

Finally, since $t\ne 0$ and $x={t}^{2}+5,$ we must have $x\ne 5.$ 

So, the complete Cartesian equation is

$$
y=\frac{1}{x-5},\,x\ne 5.
$$


### q-6830 → observed_6830

The parameters are real. The captured x expression is `$\sqrt{t^{2} - 4}$`, y expression `$2 t^{2}$`, and parameter domain `Interval(2, oo)`. Its exact x image is `Interval(0, oo)`. Isolate t² and substitute into y; retain the supplied simplification/factorization row order.

Find the Cartesian equation of the curve defined parametrically by

$$
x=\sqrt{{t}^{2}-4},\,\,\,y=2{t}^{2},\,t\ge 2.
$$

Field `selection`, `:answer-field.type/radio`. Complete observed bank:

- `63c62779-8b0d-585a-b920-9d1b9d20ae31`: $y=2{x}^{2}+8,\,x\ge 0$. Recipe: substitute `(x-h)/a` for every x operand; the whole equation and its explicit domain are transformed together. Captured correct designation.

- `9e017776-ba43-519f-8ae0-9da1f2fddf1f`: $y=4{x}^{2}+8,\,x\ge 0$. Recipe: substitute `(x-h)/a` for every x operand; the whole equation and its explicit domain are transformed together. Captured incorrect designation.

- `bf39d551-3f09-580c-8c58-bb70cec2a129`: $y=4{x}^{2}-16,\,x\ge 0$. Recipe: substitute `(x-h)/a` for every x operand; the whole equation and its explicit domain are transformed together. Captured incorrect designation.

- `e494c19c-979d-5647-9d5a-9c8e8a25d8e0`: $y=2{x}^{2}+4,\,x\ge 0$. Recipe: substitute `(x-h)/a` for every x operand; the whole equation and its explicit domain are transformed together. Captured incorrect designation.

- `f3188548-f10a-5f7e-b17b-d07a087d2bfb`: $y=2{x}^{2}-8,\,x\ge 0$. Recipe: substitute `(x-h)/a` for every x operand; the whole equation and its explicit domain are transformed together. Captured incorrect designation.

Solution stage evidence:

To find the Cartesian equation, we eliminate $t.$ First, we use the $x$ equation to solve for ${t}^{2}:$

$$
\begin{aligned}x=\sqrt{{t}^{2}-4}\,⇒\,{t}^{2}={x}^{2}+4\end{aligned}
$$

Now, substituting ${t}^{2}={x}^{2}+4$ into our expression for $y,$ we get

$$
y=2({x}^{2}+4)=2{x}^{2}+8
$$

So the Cartesian equation of the given curve is $y=2{x}^{2}+8.$

Finally, since $t\ge 2.$ and $x=\sqrt{{t}^{2}-4},$ we must have $x\ge 0.$

So, the complete Cartesian equation is

$$
y=2{x}^{2}+8,\,x\ge 0.
$$


### q-276278 → observed_276278

The parameters are real. The captured x expression is `$2 t + 5$`, y expression `$(t - 2) (t + 1)$`, and parameter domain `Reals`. Its exact x image is `Reals`. Isolate t and substitute into y; retain the supplied simplification/factorization row order.

Consider the curve defined parametrically as

$$
x=2t+5,\,\,\,y=(t-2)(t+1),\,t\in (-\infty ,\infty ).
$$

The Cartesian equation of this curve is

$y=$
{{field-1}}.

Field `field-1`, `:answer-field.type/blank`. Complete observed bank:

- `33526b37-cab0-5457-9e07-446f0c05aa08`: $\frac{1}{4}(x-9)(x-3)$. Recipe: substitute `(x-h)/a` for every x operand; the whole equation and its explicit domain are transformed together. Captured correct designation.

Solution stage evidence:

To find the Cartesian equation, we eliminate $t.$ First, we use the $x$ equation to solve for $t:$

$$
\begin{aligned}x=2t+5\,⇒\,t=\frac{x-5}{2}\end{aligned}
$$

Now, substituting $t=\frac{x-5}{2}$ into our expression for $y,$ we get

$$
\begin{aligned}y & =(\frac{x-5}{2}-2)(\frac{x-5}{2}+1) \\  & =(\frac{x-5-4}{2})(\frac{x-5+2}{2}) \\  & =(\frac{x-9}{2})(\frac{x-3}{2}) \\  & =\frac{1}{4}(x-9)(x-3).\end{aligned}
$$


### q-320878 → observed_276278

The parameters are real. The captured x expression is `$3 t - 1$`, y expression `$(t - 2) (t + 5)$`, and parameter domain `Reals`. Its exact x image is `Reals`. Isolate t and substitute into y; retain the supplied simplification/factorization row order.

Consider the curve defined parametrically as

$$
x=3t-1,\,\,\,y=(t+5)(t-2),\,t\in (-\infty ,\infty ).
$$

The Cartesian equation of this curve is

$y=$
{{field-1}}.

Field `field-1`, `:answer-field.type/blank`. Complete observed bank:

- `e76ec15d-4235-56b9-b033-fb60f2aa5631`: $\frac{1}{9}(x+16)(x-5)$. Recipe: substitute `(x-h)/a` for every x operand; the whole equation and its explicit domain are transformed together. Captured correct designation.

Solution stage evidence:

To find the Cartesian equation, we eliminate $t.$ First, we use the $x$ equation to solve for $t:$

$$
\begin{aligned}x=3t-1\,⇒\,t=\frac{x+1}{3}\end{aligned}
$$

Now, substituting $t=\frac{x+1}{3}$ into our expression for $y,$ we get

$$
\begin{aligned}y & =(\frac{x+1}{3}+5)(\frac{x+1}{3}-2) \\  & =(\frac{x+1+15}{3})(\frac{x+1-6}{3}) \\  & =(\frac{x+16}{3})(\frac{x-5}{3}) \\  & =\frac{1}{9}(x+16)(x-5).\end{aligned}
$$

## Stage 2 — Shared instructional pattern

These questions eliminate a nontrigonometric real parameter by isolating t or t² from the x equation, substituting into y, then simplifying the resulting polynomial or rational expression. Radical outputs require the nonnegative branch, and parameter exclusions may remove additional Cartesian values. Moderate sources put more structure into the polynomial factors; hard sources combine a reciprocal inverse with a rational y expression. Neither derivatives nor trigonometric identities are assessed.

The lesson route follows first-step 17592186101708 → KP step 17592186101709 → trig tutorial step 17592186101711 → adjacent trig KP step 17592186101710. Pull collection order is not used. The owning KP's canonical x=2t²,y=t²+1,t≥0 establishes that range restrictions belong to the assessed method. The adjacent trig KP is excluded from this generator. Substitution and radical-equation prerequisites support the polynomial/rational isolation performed here.

## Stage 3 — Components and choice-bank recipes

The preceding per-question table and extraction.json account for every prompt, field, answer UUID, complete equation/fragment, captured designation and solution. The reusable coordinate recipe C_(a,h) is a bijection x_old=(x-h)/a with a>0. It acts on each complete observed expression and constraint, so bank counts and algebraic equivalences are preserved. This is an authored, exact expression-level extension; it does not claim to recover an original author's error-generating algorithm. It is not an arbitrary polynomial fit to source values.

q15653's unrelated polynomial coefficient bank and q6828's unexplained rational constants are treated as empirical replay evidence only at their original parameters. Their normal defaults are separately authored **complete** method banks. q15653 uses correct substitution, negation, reversed shift, omitted linear term and unchanged squared-shift constant. q6828 uses correct substitution, reversed denominator shift, negation, extra denominator square and omitted shift. Every member is derived from the assessed substitution, defined on the actual x>5 domain, and distinct from all others. There is no first-valid distractor pool.

## Stage 4 — Reusable templates, constraints and calculations

Fixed: all source prose, display layout, number of fields, field keys/types, complete profile count, parameter elimination route and solution row order. Variable: source mathematical x operands under C_(a,h); a ranges 1…7 and h ranges −9…9 by default. Original a=1,h=0 is normal recipe evaluation. Explicit a is constrained to 1…12, h to −20…20; invalid values fail, without resampling. The prompt displays the transformed coordinate on the x equation's left-hand side, retaining each original right-hand expression and all domain requirements. Powers receive a grouped substitution. The same mapping transforms every solution equality, choice equation and domain expression.

Correctness is derived from the stored parameter equations, solving for t or t², substituting into y, and computing the exact transformed x image. Source answer IDs designate only raw evidence; ordinary correct refs are selected by full derived mathematics. Independent validation re-parses the displayed parameter equations and every displayed equality and checks the equation under the parameterization; it separately verifies exact real domains and branch ranges. Whole-equation comparisons admit a nonzero scalar factor; identical correct relations cannot be treated as separate distractors.

The coordinate family has 133 default parameter pairs per source profile. Native coefficient extensions provide further distinct tasks: easy x=t+b,y=t²+c with nonzero integer b in −8…8 and c in −12…12 (400 combinations); moderate x=at+b,y=(t-u)(t-v), a in ±2,±3,±4, b in −8…8 and distinct roots in −5…5 (5610 unordered-root combinations); hard x=1/(t-h),y=t/(ct+d), h in ±2…±5 and c,d in ±1…±3 excluding ch+d=0 (280 combinations). These are peer variations at their assigned workloads, not a within-level progression. The native moderate template is anchored to q276278/q320878, and native hard to q276284/q320926. Negative coefficients retain source sign work. Extra factors, arbitrary powers, differentiation and trigonometric identities are absent.

Content identity includes version, entire rendered prompt, fixed solution, fields and the whole displayed bank. Canonical mathematical identity separately includes normalized displayed x(t) and y(t), their exact real parameter domain, the normalized Cartesian y relation, exact x image and normalized response fragments/field types, independent of template name, seed and option order. Equivalent factored/expanded templates collapse under the task fingerprint.

## Recorded source anomalies and repairs

- **q15678:** the captured options y=((-1−2x)/x)² and y=((1+2x)/x)² are identical. The raw profile preserves both and the captured correct ID; its unique-correct safety explicitly fails. The normal repaired profile removes the square only from the duplicate numerator option, representing an omitted square in substitution, preserving five choices and all other options. The entire repaired bank is validated together.
- **q6828:** t≠0 implies t²>0 and x=t²+5>5. The source's x≠5 omits the range restriction. Raw evidence retains it; the normal solution/range uses x>5. Its empirical whole bank is replay-only; normal questions use the authored complete operation bank above.
- **q15755:** the EDB capture has no difficulty, correct ref or worked solution. The original MA widget JSON and rendered screenshot at /home/jake/Developer/MA/DATA/Lessons/1255/Source were inspected: five choices, correct mathematical expression y=(x+2)² on all real x is option a. The snapshot does not expose a correct flag, so this is **independently derived**, not a matched missing designation. t=x+2 gives y=(x+2)² and all real x. The source bank and prompt are exactly retained; the easy level and solution are authored.
- **q321075 audit correction:** the displayed factor 4 in (−8x+16x²)(4)(1−2x)² is valid, since (2−4x)²=4(1−2x)². Its original rows are retained unchanged and independently checked. An initial suspicion of a false row was withdrawn.

Raw exact bank and solution fidelity, source mathematical safety, repaired normal correctness and actual engine grading are separate validation denominators. A raw q15678 bank does not pass unique correctness merely because native radio IDs grade.
