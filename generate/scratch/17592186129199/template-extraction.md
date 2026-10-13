# Template extraction

## Stage 1 — individual sources

### q-161044

Level: moderate (authored assignment; original is unrated). Template `xy2`; radius $\sqrt{5}$; $\theta\in[0,2 \pi]$. Prompt contains one region raster followed by the Cartesian double integral. Field key `selection`, radio, five complete-integral math options. Function $x y^{2}$; x and y are Cartesian variables, r is nonnegative and θ is angular. Exact answers; no numerical evaluation requested.

![](images/e2/e2fe61de100b4a469e4d79dc67869dd68936a0bf396757c4d08fb4d6cade6bda.png)

The region $D$ is the circle shown above. What is $∬_(D)xy^{2}dA$ expressed in polar coordinates?

### q-38076

Level: moderate (observed). Template `twoxy`; radius $2$; $\theta\in[- \frac{\pi}{2},\frac{\pi}{2}]$. Prompt contains one region raster followed by the Cartesian double integral. Field key `selection`, radio, five complete-integral math options. Function $2 x y$; x and y are Cartesian variables, r is nonnegative and θ is angular. Exact answers; no numerical evaluation requested.

![](images/bc/bccbe3973fa63908f5e264f4566e1207c5019dc1de9c36ef42481428527aef3b.png)

The region $D$ is the semicircle shown above. What is
${∬}_{D}2xy\,\text{d}A$
expressed in polar coordinates?

### q-161038

Level: moderate (observed). Template `exp`; radius $4$; $\theta\in[\pi,\frac{3 \pi}{2}]$. Prompt contains one region raster followed by the Cartesian double integral. Field key `selection`, radio, five complete-integral math options. Function $e^{x^{2} + y^{2}}$; x and y are Cartesian variables, r is nonnegative and θ is angular. Exact answers; no numerical evaluation requested.

![](images/aa/aa5b04b98d3796656fca912d8dc1732ea7e12bab9083f8ca543ad5fd4fdb10ff.png)

The region $D$ is the quarter-circle shown above. What is ${∬}_{D}{e}^{{x}^{2}+{y}^{2}}\,\text{d}A$ expressed in polar coordinates?

### q-161039

Level: easy (observed). Template `diff`; radius $2$; $\theta\in[0,2 \pi]$. Prompt contains one region raster followed by the Cartesian double integral. Field key `selection`, radio, five complete-integral math options. Function $x^{2} - y^{2}$; x and y are Cartesian variables, r is nonnegative and θ is angular. Exact answers; no numerical evaluation requested.

![](images/cd/cdd5f0c58228b47a0bbba77daf2b426ce0247e71259e2b5af1a4a80fa833a036.png)

The region $D$ is the circle shown above. What is ${∬}_{D}({x}^{2}-{y}^{2})\,\text{d}A$ expressed in polar coordinates?

### q-161041

Level: easy (observed). Template `log`; radius $4$; $\theta\in[0,2 \pi]$. Prompt contains one region raster followed by the Cartesian double integral. Field key `selection`, radio, five complete-integral math options. Function $\ln{\left(x^{2} + y^{2} + 1 \right)}$; x and y are Cartesian variables, r is nonnegative and θ is angular. Exact answers; no numerical evaluation requested.

![](images/6b/6b077d20bcb79f293383a7810d1c46ad42ce78d17a8d631b01f66a9fd547f475.png)

The region $D$ is the circle shown above. What is ${∬}_{D}\operatorname{ln}⁡({x}^{2}+{y}^{2}+1)\,\text{d}A$ expressed in polar coordinates?

### q-83499

Level: moderate (observed). Template `sum`; radius $2$; $\theta\in[- \frac{\pi}{2},0]$. Prompt contains one region raster followed by the Cartesian double integral. Field key `selection`, radio, five complete-integral math options. Function $x^{2} + y^{2}$; x and y are Cartesian variables, r is nonnegative and θ is angular. Exact answers; no numerical evaluation requested.

![](images/8c/8c3056de2634d5315aebcbc978bf279eeb95da736ab6796c9d86dc39d9feadc5.png)

The region $D$ is the quarter-circle shown above. What is
${∬}_{D}({x}^{2}+{y}^{2})\,\text{d}A$
expressed in polar coordinates?

### q-83500

Level: moderate (observed). Template `linear`; radius $\sqrt{2}$; $\theta\in[0,\pi]$. Prompt contains one region raster followed by the Cartesian double integral. Field key `selection`, radio, five complete-integral math options. Function $x + y$; x and y are Cartesian variables, r is nonnegative and θ is angular. Exact answers; no numerical evaluation requested.

![](images/55/55bbf6f55ce287321f2cc593ea48d65a78c655ca18d2a34df68b63c2bda92c8f.png)

The region $D$ is the semicircle shown above. What is
${∬}_{D}(x+y)\,\text{d}A$
expressed in polar coordinates?

### q-83954

Level: moderate (observed). Template `x`; radius $\sqrt{3}$; $\theta\in[\frac{\pi}{2},\pi]$. Prompt contains one region raster followed by the Cartesian double integral. Field key `selection`, radio, five complete-integral math options. Function $x$; x and y are Cartesian variables, r is nonnegative and θ is angular. Exact answers; no numerical evaluation requested.

![](images/a6/a60d80425c240deb1ea372d7a21c3774247c4827536ce6f409f7e8736c7c94bc.png)

The region $D$ is the quarter-circle shown above. What is
${∬}_{D}x\,\text{d}A$
expressed in polar coordinates?

### q-161043

Level: easy (observed). Template `y2`; radius $5$; $\theta\in[0,2 \pi]$. Prompt contains one region raster followed by the Cartesian double integral. Field key `selection`, radio, five complete-integral math options. Function $y^{2}$; x and y are Cartesian variables, r is nonnegative and θ is angular. Exact answers; no numerical evaluation requested.

![](images/2d/2db1e29e5f911a45c4c48ab41c4ad6dc63eeb36a8112672ae66844e14342f4c0.png)

The region $D$ is the circle shown above. What is ${∬}_{D}{y}^{2}\,\text{d}A$ expressed in polar coordinates?

## Stage 2 — shared mathematical pattern

Read an origin-centered disk sector from the plot, form Δ=[0,R]×[a,b], substitute x=r cosθ and y=r sinθ into the entire integrand, multiply by r, and simplify Pythagorean/double-angle expressions if present. Retain the complete iterated integral as the response. The family does not require computing its value.

## Stage 3 — complete component and bank maps

Each observed bank is retained intact. The following symbolic recipes parameterize full components: radius R replaces the observed radius R₀; observed R₀² becomes R²; observed R₀/2 becomes R/2; −R₀ becomes −R; zero remains zero. Every angular bound becomes its observed value plus kπ/2, with k=0 for full disks. The integrand component in each observed option remains its displayed expression. This preserves recovered expression patterns without claiming the unknown author intended a particular error. Compounded changes are retained together, never pooled across banks.

### Profile q-161044

Correct source index: 5 (independent inference, no observed designation).

- Choice 1: `$\displaystyle \int_{0}^{π}\displaystyle \int_{0}^{5}r^{3}\cos θ\sin θdrdθ$`. Bounds recipe (θ lower, θ upper, r lower, r upper): `0 + k*pi/2, pi + k*pi/2, 0, R**2`; pointwise integrand `r**3*sin(theta)*cos(theta)`. Fails actual domain and/or pointwise integrand criterion; error intent unresolved.
- Choice 2: `$\displaystyle \int_{0}^{2π}\displaystyle \int_{0}^{\sqrt{5}}r^{3}\cos θ\sin θdrdθ$`. Bounds recipe (θ lower, θ upper, r lower, r upper): `0 + k*pi/2, 2*pi + k*pi/2, 0, R`; pointwise integrand `r**3*sin(theta)*cos(theta)`. Fails actual domain and/or pointwise integrand criterion; error intent unresolved.
- Choice 3: `$\displaystyle \int_{0}^{2π}\displaystyle \int_{0}^{5}r^{4}\cos θ\sin^{2} θdrdθ$`. Bounds recipe (θ lower, θ upper, r lower, r upper): `0 + k*pi/2, 2*pi + k*pi/2, 0, R**2`; pointwise integrand `r**4*sin(theta)**2*cos(theta)`. Fails actual domain and/or pointwise integrand criterion; error intent unresolved.
- Choice 4: `$\displaystyle \int_{0}^{π}\displaystyle \int_{0}^{\sqrt{5}}r^{4}\cos θ\sin^{2} θdrdθ$`. Bounds recipe (θ lower, θ upper, r lower, r upper): `0 + k*pi/2, pi + k*pi/2, 0, R`; pointwise integrand `r**4*sin(theta)**2*cos(theta)`. Fails actual domain and/or pointwise integrand criterion; error intent unresolved.
- Choice 5: `$\displaystyle \int_{0}^{2π}\displaystyle \int_{0}^{\sqrt{5}}r^{4}\cos θ\sin^{2} θdrdθ$`. Bounds recipe (θ lower, θ upper, r lower, r upper): `0 + k*pi/2, 2*pi + k*pi/2, 0, R`; pointwise integrand `r**4*sin(theta)**2*cos(theta)`. Valid setup.

Worked solution sequence: absent in capture; full formal formula/domain/substitution/reduction solution is authored.

### Profile q-38076

Correct source index: 1 (observed designation).

- Choice 1: `${\int }_{-\pi /2}^{\pi /2}{\int }_{0}^{2}{r}^{3}\operatorname{sin}⁡(2\theta )\,\text{d}r\,\text{d}\theta $`. Bounds recipe (θ lower, θ upper, r lower, r upper): `-pi/2 + k*pi/2, pi/2 + k*pi/2, 0, R`; pointwise integrand `r**3*sin(2*theta)`. Valid setup.
- Choice 2: `${\int }_{-\pi /2}^{\pi /2}{\int }_{0}^{1}{r}^{2}\operatorname{sin}⁡(2\theta )\,\text{d}r\,\text{d}\theta $`. Bounds recipe (θ lower, θ upper, r lower, r upper): `-pi/2 + k*pi/2, pi/2 + k*pi/2, 0, R/2`; pointwise integrand `r**2*sin(2*theta)`. Fails actual domain and/or pointwise integrand criterion; error intent unresolved.
- Choice 3: `${\int }_{0}^{\pi /2}{\int }_{0}^{2}{r}^{3}\operatorname{sin}⁡(2\theta )\,\text{d}r\,\text{d}\theta $`. Bounds recipe (θ lower, θ upper, r lower, r upper): `0 + k*pi/2, pi/2 + k*pi/2, 0, R`; pointwise integrand `r**3*sin(2*theta)`. Fails actual domain and/or pointwise integrand criterion; error intent unresolved.
- Choice 4: `${\int }_{0}^{\pi /2}{\int }_{0}^{2}{r}^{2}\operatorname{sin}⁡(2\theta )\,\text{d}r\,\text{d}\theta $`. Bounds recipe (θ lower, θ upper, r lower, r upper): `0 + k*pi/2, pi/2 + k*pi/2, 0, R`; pointwise integrand `r**2*sin(2*theta)`. Fails actual domain and/or pointwise integrand criterion; error intent unresolved.
- Choice 5: `${\int }_{-\pi /2}^{\pi /2}{\int }_{0}^{2}{r}^{2}\operatorname{sin}⁡(2\theta )\,\text{d}r\,\text{d}\theta $`. Bounds recipe (θ lower, θ upper, r lower, r upper): `-pi/2 + k*pi/2, pi/2 + k*pi/2, 0, R`; pointwise integrand `r**2*sin(2*theta)`. Fails actual domain and/or pointwise integrand criterion; error intent unresolved.

Worked solution sequence: formal change-of-variables formula → radius/domain paragraph → Δ bounds → Therefore sentence → exact source aligned substitution and simplification rows. All original rows and shared prose are preserved under complete-bound slots.

### Profile q-161038

Correct source index: 4 (observed designation).

- Choice 1: `${\int }_{\pi }^{3\pi /2}{\int }_{0}^{2}{e}^{{r}^{2}}\,\text{d}r\,\text{d}\theta $`. Bounds recipe (θ lower, θ upper, r lower, r upper): `pi + k*pi/2, 3*pi/2 + k*pi/2, 0, R/2`; pointwise integrand `exp(r**2)`. Fails actual domain and/or pointwise integrand criterion; error intent unresolved.
- Choice 2: `${\int }_{\pi /2}^{3\pi /2}{\int }_{0}^{4}r{e}^{{r}^{2}}\,\text{d}r\,\text{d}\theta $`. Bounds recipe (θ lower, θ upper, r lower, r upper): `pi/2 + k*pi/2, 3*pi/2 + k*pi/2, 0, R`; pointwise integrand `r*exp(r**2)`. Fails actual domain and/or pointwise integrand criterion; error intent unresolved.
- Choice 3: `${\int }_{\pi }^{3\pi /2}{\int }_{0}^{4}r{e}^{r}\,\text{d}r\,\text{d}\theta $`. Bounds recipe (θ lower, θ upper, r lower, r upper): `pi + k*pi/2, 3*pi/2 + k*pi/2, 0, R`; pointwise integrand `r*exp(r)`. Fails actual domain and/or pointwise integrand criterion; error intent unresolved.
- Choice 4: `${\int }_{\pi }^{3\pi /2}{\int }_{0}^{4}r{e}^{{r}^{2}}\,\text{d}r\,\text{d}\theta $`. Bounds recipe (θ lower, θ upper, r lower, r upper): `pi + k*pi/2, 3*pi/2 + k*pi/2, 0, R`; pointwise integrand `r*exp(r**2)`. Valid setup.
- Choice 5: `${\int }_{\pi /2}^{3\pi /2}{\int }_{0}^{2}{r}^{2}{e}^{r}\,\text{d}r\,\text{d}\theta $`. Bounds recipe (θ lower, θ upper, r lower, r upper): `pi/2 + k*pi/2, 3*pi/2 + k*pi/2, 0, R/2`; pointwise integrand `r**2*exp(r)`. Fails actual domain and/or pointwise integrand criterion; error intent unresolved.

Worked solution sequence: formal change-of-variables formula → radius/domain paragraph → Δ bounds → Therefore sentence → exact source aligned substitution and simplification rows. All original rows and shared prose are preserved under complete-bound slots.

### Profile q-161039

Correct source index: 4 (observed designation).

- Choice 1: `${\int }_{0}^{2\pi }{\int }_{0}^{2}{r}^{3}\,\text{d}r\,\text{d}\theta $`. Bounds recipe (θ lower, θ upper, r lower, r upper): `0 + k*pi/2, 2*pi + k*pi/2, 0, R`; pointwise integrand `r**3`. Fails actual domain and/or pointwise integrand criterion; error intent unresolved.
- Choice 2: `${\int }_{0}^{\pi }{\int }_{0}^{4}{r}^{2}\operatorname{cos}⁡2\theta \,\text{d}r\,\text{d}\theta $`. Bounds recipe (θ lower, θ upper, r lower, r upper): `0 + k*pi/2, pi + k*pi/2, 0, R**2`; pointwise integrand `r**2*cos(2*theta)`. Fails actual domain and/or pointwise integrand criterion; error intent unresolved.
- Choice 3: `${\int }_{0}^{2\pi }{\int }_{0}^{4}{r}^{3}\operatorname{cos}⁡2\theta \,\text{d}r\,\text{d}\theta $`. Bounds recipe (θ lower, θ upper, r lower, r upper): `0 + k*pi/2, 2*pi + k*pi/2, 0, R**2`; pointwise integrand `r**3*cos(2*theta)`. Fails actual domain and/or pointwise integrand criterion; error intent unresolved.
- Choice 4: `${\int }_{0}^{2\pi }{\int }_{0}^{2}{r}^{3}\operatorname{cos}⁡2\theta \,\text{d}r\,\text{d}\theta $`. Bounds recipe (θ lower, θ upper, r lower, r upper): `0 + k*pi/2, 2*pi + k*pi/2, 0, R`; pointwise integrand `r**3*cos(2*theta)`. Valid setup.
- Choice 5: `${\int }_{0}^{2\pi }{\int }_{0}^{2}{r}^{2}\,\text{d}r\,\text{d}\theta $`. Bounds recipe (θ lower, θ upper, r lower, r upper): `0 + k*pi/2, 2*pi + k*pi/2, 0, R`; pointwise integrand `r**2`. Fails actual domain and/or pointwise integrand criterion; error intent unresolved.

Worked solution sequence: formal change-of-variables formula → radius/domain paragraph → Δ bounds → Therefore sentence → exact source aligned substitution and simplification rows. All original rows and shared prose are preserved under complete-bound slots.

### Profile q-161041

Correct source index: 1 (observed designation).

- Choice 1: `${\int }_{0}^{2\pi }{\int }_{0}^{4}r\operatorname{ln}⁡({r}^{2}+1)\,\text{d}r\,\text{d}\theta $`. Bounds recipe (θ lower, θ upper, r lower, r upper): `0 + k*pi/2, 2*pi + k*pi/2, 0, R`; pointwise integrand `r*log(r**2 + 1)`. Valid setup.
- Choice 2: `${\int }_{0}^{\pi }{\int }_{0}^{16}\operatorname{ln}⁡({r}^{2}+1)\,\text{d}r\,\text{d}\theta $`. Bounds recipe (θ lower, θ upper, r lower, r upper): `0 + k*pi/2, pi + k*pi/2, 0, R**2`; pointwise integrand `log(r**2 + 1)`. Fails actual domain and/or pointwise integrand criterion; error intent unresolved.
- Choice 3: `${\int }_{0}^{2\pi }{\int }_{0}^{16}{r}^{2}\operatorname{ln}⁡(r+1)\,\text{d}r\,\text{d}\theta $`. Bounds recipe (θ lower, θ upper, r lower, r upper): `0 + k*pi/2, 2*pi + k*pi/2, 0, R**2`; pointwise integrand `r**2*log(r + 1)`. Fails actual domain and/or pointwise integrand criterion; error intent unresolved.
- Choice 4: `${\int }_{0}^{\pi }{\int }_{0}^{4}r\operatorname{ln}⁡({r}^{2}+1)\,\text{d}r\,\text{d}\theta $`. Bounds recipe (θ lower, θ upper, r lower, r upper): `0 + k*pi/2, pi + k*pi/2, 0, R`; pointwise integrand `r*log(r**2 + 1)`. Fails actual domain and/or pointwise integrand criterion; error intent unresolved.
- Choice 5: `${\int }_{0}^{2\pi }{\int }_{0}^{4}\operatorname{ln}⁡(r+1)\,\text{d}r\,\text{d}\theta $`. Bounds recipe (θ lower, θ upper, r lower, r upper): `0 + k*pi/2, 2*pi + k*pi/2, 0, R`; pointwise integrand `log(r + 1)`. Fails actual domain and/or pointwise integrand criterion; error intent unresolved.

Worked solution sequence: formal change-of-variables formula → radius/domain paragraph → Δ bounds → Therefore sentence → exact source aligned substitution and simplification rows. All original rows and shared prose are preserved under complete-bound slots.

### Profile q-83499

Correct source index: 5 (observed designation).

- Choice 1: `${\int }_{3\pi /2}^{0}{\int }_{0}^{1}{r}^{2}\,\text{d}r\,\text{d}\theta $`. Bounds recipe (θ lower, θ upper, r lower, r upper): `3*pi/2 + k*pi/2, 0 + k*pi/2, 0, R/2`; pointwise integrand `r**2`. Fails actual domain and/or pointwise integrand criterion; error intent unresolved.
- Choice 2: `${\int }_{-\pi /2}^{0}{\int }_{0}^{2}r\,\text{d}r\,\text{d}\theta $`. Bounds recipe (θ lower, θ upper, r lower, r upper): `-pi/2 + k*pi/2, 0 + k*pi/2, 0, R`; pointwise integrand `r`. Fails actual domain and/or pointwise integrand criterion; error intent unresolved.
- Choice 3: `${\int }_{-\pi /2}^{0}{\int }_{0}^{1}{r}^{3}\,\text{d}r\,\text{d}\theta $`. Bounds recipe (θ lower, θ upper, r lower, r upper): `-pi/2 + k*pi/2, 0 + k*pi/2, 0, R/2`; pointwise integrand `r**3`. Fails actual domain and/or pointwise integrand criterion; error intent unresolved.
- Choice 4: `${\int }_{0}^{\pi /2}{\int }_{0}^{2}{r}^{2}\,\text{d}r\,\text{d}\theta $`. Bounds recipe (θ lower, θ upper, r lower, r upper): `0 + k*pi/2, pi/2 + k*pi/2, 0, R`; pointwise integrand `r**2`. Fails actual domain and/or pointwise integrand criterion; error intent unresolved.
- Choice 5: `${\int }_{-\pi /2}^{0}{\int }_{0}^{2}{r}^{3}\,\text{d}r\,\text{d}\theta $`. Bounds recipe (θ lower, θ upper, r lower, r upper): `-pi/2 + k*pi/2, 0 + k*pi/2, 0, R`; pointwise integrand `r**3`. Valid setup.

Worked solution sequence: formal change-of-variables formula → radius/domain paragraph → Δ bounds → Therefore sentence → exact source aligned substitution and simplification rows. All original rows and shared prose are preserved under complete-bound slots.

### Profile q-83500

Correct source index: 4 (observed designation).

- Choice 1: `${\int }_{0}^{2\pi }{\int }_{0}^{\sqrt{2}}r(\operatorname{cos}⁡\theta +\operatorname{sin}⁡\theta )\,\text{d}r\,\text{d}\theta $`. Bounds recipe (θ lower, θ upper, r lower, r upper): `0 + k*pi/2, 2*pi + k*pi/2, 0, R`; pointwise integrand `r*(sin(theta) + cos(theta))`. Fails actual domain and/or pointwise integrand criterion; error intent unresolved.
- Choice 2: `${\int }_{0}^{\pi }{\int }_{-\sqrt{2}}^{\sqrt{2}}{r}^{2}(\operatorname{cos}⁡\theta +\operatorname{sin}⁡\theta )\,\text{d}r\,\text{d}\theta $`. Bounds recipe (θ lower, θ upper, r lower, r upper): `0 + k*pi/2, pi + k*pi/2, -R, R`; pointwise integrand `r**2*(sin(theta) + cos(theta))`. Fails actual domain and/or pointwise integrand criterion; error intent unresolved.
- Choice 3: `${\int }_{0}^{\pi }{\int }_{-\sqrt{2}}^{\sqrt{2}}r\,\text{d}r\,\text{d}\theta $`. Bounds recipe (θ lower, θ upper, r lower, r upper): `0 + k*pi/2, pi + k*pi/2, -R, R`; pointwise integrand `r`. Fails actual domain and/or pointwise integrand criterion; error intent unresolved.
- Choice 4: `${\int }_{0}^{\pi }{\int }_{0}^{\sqrt{2}}{r}^{2}(\operatorname{cos}⁡\theta +\operatorname{sin}⁡\theta )\,\text{d}r\,\text{d}\theta $`. Bounds recipe (θ lower, θ upper, r lower, r upper): `0 + k*pi/2, pi + k*pi/2, 0, R`; pointwise integrand `r**2*(sin(theta) + cos(theta))`. Valid setup.
- Choice 5: `${\int }_{0}^{\pi }{\int }_{0}^{\sqrt{2}}{r}^{2}\,\text{d}r\,\text{d}\theta $`. Bounds recipe (θ lower, θ upper, r lower, r upper): `0 + k*pi/2, pi + k*pi/2, 0, R`; pointwise integrand `r**2`. Fails actual domain and/or pointwise integrand criterion; error intent unresolved.

Worked solution sequence: formal change-of-variables formula → radius/domain paragraph → Δ bounds → Therefore sentence → exact source aligned substitution and simplification rows. All original rows and shared prose are preserved under complete-bound slots.

### Profile q-83954

Correct source index: 5 (observed designation).

- Choice 1: `${\int }_{-\pi }^{\pi }{\int }_{0}^{\sqrt{3}}{r}^{2}\operatorname{cos}⁡\theta \,\text{d}r\,\text{d}\theta $`. Bounds recipe (θ lower, θ upper, r lower, r upper): `-pi + k*pi/2, pi + k*pi/2, 0, R`; pointwise integrand `r**2*cos(theta)`. Fails actual domain and/or pointwise integrand criterion; error intent unresolved.
- Choice 2: `${\int }_{\pi /2}^{\pi /2}{\int }_{0}^{\sqrt{3}}{r}^{2}\operatorname{cos}⁡\theta \,\text{d}r\,\text{d}\theta $`. Bounds recipe (θ lower, θ upper, r lower, r upper): `pi/2 + k*pi/2, pi/2 + k*pi/2, 0, R`; pointwise integrand `r**2*cos(theta)`. Fails actual domain and/or pointwise integrand criterion; error intent unresolved.
- Choice 3: `${\int }_{\pi /2}^{\pi }{\int }_{-\sqrt{3}}^{\sqrt{3}}{r}^{2}\operatorname{cos}⁡\theta \,\text{d}r\,\text{d}\theta $`. Bounds recipe (θ lower, θ upper, r lower, r upper): `pi/2 + k*pi/2, pi + k*pi/2, -R, R`; pointwise integrand `r**2*cos(theta)`. Fails actual domain and/or pointwise integrand criterion; error intent unresolved.
- Choice 4: `${\int }_{0}^{\pi }{\int }_{-\sqrt{3}}^{\sqrt{3}}{r}^{2}\operatorname{cos}⁡\theta \,\text{d}r\,\text{d}\theta $`. Bounds recipe (θ lower, θ upper, r lower, r upper): `0 + k*pi/2, pi + k*pi/2, -R, R`; pointwise integrand `r**2*cos(theta)`. Fails actual domain and/or pointwise integrand criterion; error intent unresolved.
- Choice 5: `${\int }_{\pi /2}^{\pi }{\int }_{0}^{\sqrt{3}}{r}^{2}\operatorname{cos}⁡\theta \,\text{d}r\,\text{d}\theta $`. Bounds recipe (θ lower, θ upper, r lower, r upper): `pi/2 + k*pi/2, pi + k*pi/2, 0, R`; pointwise integrand `r**2*cos(theta)`. Valid setup.

Worked solution sequence: formal change-of-variables formula → radius/domain paragraph → Δ bounds → Therefore sentence → exact source aligned substitution and simplification rows. All original rows and shared prose are preserved under complete-bound slots.

### Profile q-161043

Correct source index: 3 (observed designation).

- Choice 1: `${\int }_{0}^{2\pi }{\int }_{0}^{25}{r}^{3}{sin}^{2}⁡\theta \,\text{d}r\,\text{d}\theta $`. Bounds recipe (θ lower, θ upper, r lower, r upper): `0 + k*pi/2, 2*pi + k*pi/2, 0, R**2`; pointwise integrand `r**3*sin(theta)**2`. Fails actual domain and/or pointwise integrand criterion; error intent unresolved.
- Choice 2: `${\int }_{0}^{2\pi }{\int }_{0}^{5}{r}^{2}{sin}^{2}⁡\theta \,\text{d}r\,\text{d}\theta $`. Bounds recipe (θ lower, θ upper, r lower, r upper): `0 + k*pi/2, 2*pi + k*pi/2, 0, R`; pointwise integrand `r**2*sin(theta)**2`. Fails actual domain and/or pointwise integrand criterion; error intent unresolved.
- Choice 3: `${\int }_{0}^{2\pi }{\int }_{0}^{5}{r}^{3}{sin}^{2}⁡\theta \,\text{d}r\,\text{d}\theta $`. Bounds recipe (θ lower, θ upper, r lower, r upper): `0 + k*pi/2, 2*pi + k*pi/2, 0, R`; pointwise integrand `r**3*sin(theta)**2`. Valid setup.
- Choice 4: `${\int }_{0}^{\pi }{\int }_{0}^{5}{r}^{2}{sin}^{2}⁡\theta \,\text{d}r\,\text{d}\theta $`. Bounds recipe (θ lower, θ upper, r lower, r upper): `0 + k*pi/2, pi + k*pi/2, 0, R`; pointwise integrand `r**2*sin(theta)**2`. Fails actual domain and/or pointwise integrand criterion; error intent unresolved.
- Choice 5: `${\int }_{0}^{\pi }{\int }_{0}^{25}{r}^{3}{sin}^{2}⁡\theta \,\text{d}r\,\text{d}\theta $`. Bounds recipe (θ lower, θ upper, r lower, r upper): `0 + k*pi/2, pi + k*pi/2, 0, R**2`; pointwise integrand `r**3*sin(theta)**2`. Fails actual domain and/or pointwise integrand criterion; error intent unresolved.

Worked solution sequence: formal change-of-variables formula → radius/domain paragraph → Δ bounds → Therefore sentence → exact source aligned substitution and simplification rows. All original rows and shared prose are preserved under complete-bound slots.

## Stage 4 — reusable masks and constraints

`templates.json` holds immutable raw family text and complete observed banks. The generator parses full definite-integral bound components into slots, computes changed bounds, and reinserts them without globally replacing numerals. Radius prose and the entire Δ bounds block are separate slots. All other source worked-solution rows and sentences remain unchanged. Source image references normalize to local copied assets. At changed geometry, the entire plot is recreated from the same radius and sector parameters.

Allowed radius_squared is an integer 2..36 (35 exact radii); quarter-turn rotation is 0..3 for partial disks and exactly zero for full disks. Explicit inputs obey the same limits. R=1 is excluded because R and R² distractor bounds would collide. No integrand or domain sampling occurs inside the renderer. Each of easy/moderate/hard has a separate entry point.

Authored hard bank: correct, omitted Jacobian, extra Jacobian, half of the actual angular interval, doubled radius; the entire fixed bank is chosen before validation. A collision or missing member rejects the complete instance. Solutions explicitly show formal formula, Δ, the unreduced substituted expression, factored radial-root expression, root/Pythagorean reduction, and double-angle reduction.

Finite task counts: easy 3×35=105; moderate (one full-disk xy² family ×35)+(five partial-disk families ×35×4)=735; hard 2×35×4=280. These counts include actual geometry, integrand and response criterion and exclude bank profile, choice order, aliases and display-only changes.

Repairs and limits: q-161044 lacks key/difficulty/solution and uses legacy ∫_(D) notation. Raw bank and raw prompt remain in source.json/templates.json and its public profile; normal presentation corrects only integral notation and adds the criterion sentence. q-161039 and q-83499 have unescaped literal set braces in Δ; generated replay escapes those two braces, preserving all mathematics and stage order. Canonical e-7347 has an erroneous missing plus in a root intermediate and is evidence only, not copied into generated teaching. No unknown choice interpretation is promoted to a claimed recovered mistake recipe.
