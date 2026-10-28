# Ellipse generator review

Raw originals, separate supported completions, six authored variants per level, and explicitly generated changed-parameter variants for every observed bank. Checked boxes mark designated correct choices; original omissions remain visible.

### raw observed evidence — unrated (inferred easy) — observed-q-127362

![](/media/jake/SSD/EDB/math/images/f7/f74e1bfe8c53edb73d22633aa3bbf59f5046ebf793541dac8cbcf35127b72601.png)

Find $\frac{dy}{dx}$ for the ellipse shown above.

- [ ] $\frac{3x}{2y}$

- [ ] $\frac{4x}{9y}$

- [ ] $-\frac{4x}{9y}$

- [ ] $-\frac{9x}{4y}$

- [ ] $-\frac{2x}{3y}$

Captured correct designation absent; independently inferred: $- \frac{4 x}{9 y}$.

Captured worked solution absent.

### supported source completion — easy — completed-q-127362

![](/media/jake/SSD/EDB/math/images/f7/f74e1bfe8c53edb73d22633aa3bbf59f5046ebf793541dac8cbcf35127b72601.png)

Find $\frac{dy}{dx}$ for the ellipse shown above.

- [ ] $\frac{3x}{2y}$

- [ ] $\frac{4x}{9y}$

- [ ] $-\frac{2x}{3y}$

- [x] $-\frac{4x}{9y}$

- [ ] $-\frac{9x}{4y}$

Since our ellipse is centered at the origin and has semiaxes $3$ and $2,$ its equation is given by

$$
\frac{{x}^{2}}{{3}^{2}}+\frac{{y}^{2}}{{2}^{2}}=1\,⟹\,\frac{{x}^{2}}{9}+\frac{{y}^{2}}{4}=1.
$$

Now, to calculate $\frac{\text{d}y}{\text{d}x},$ we use implicit differentiation:

$$
\begin{aligned}\frac{\text{d}}{\text{d}x}(\frac{{x}^{2}}{9}+\frac{{y}^{2}}{4}) & =\frac{\text{d}}{\text{d}x}(1) \\ \frac{\text{d}}{\text{d}x}(\frac{{x}^{2}}{9})+\frac{\text{d}}{\text{d}x}(\frac{{y}^{2}}{4}) & =0 \\ \frac{2x}{9}+\frac{2y}{4}\cdot \frac{\text{d}y}{\text{d}x} & =0 \\ \frac{y}{2}\cdot \frac{\text{d}y}{\text{d}x} & =-\frac{2x}{9} \\ \frac{\text{d}y}{\text{d}x} & =-\frac{4x}{9y}\end{aligned}
$$

### raw observed evidence — unrated (inferred hard) — observed-q-127364

![](/media/jake/SSD/EDB/math/images/b5/b56ff4cb47d9b529762c6364eac2eed4b666c7ca9eab6f6ba7d3bc161387433e.png)

Find $\frac{dy}{dx}$ for the ellipse shown above.

- [ ] $- (4(x - 2))/(3(y + 1))$

- [ ] $- (16(x - 2))/(9(y + 1))$

- [ ] $(3(y + 1))/(4(x - 2))$

- [ ] $(16(x - 2))/(9(y + 1))$

- [ ] $- (9(y + 1))/(16(x - 2))$

Captured correct designation absent; independently inferred: $- \frac{16\left(x - 2\right)}{9\left(y + 1\right)}$.

Captured worked solution absent.

### supported source completion — hard — completed-q-127364

![](/media/jake/SSD/EDB/math/images/b5/b56ff4cb47d9b529762c6364eac2eed4b666c7ca9eab6f6ba7d3bc161387433e.png)

Find $\frac{dy}{dx}$ for the ellipse shown above.

- [ ] $- (4(x - 2))/(3(y + 1))$

- [x] $- (16(x - 2))/(9(y + 1))$

- [ ] $- (9(y + 1))/(16(x - 2))$

- [ ] $(3(y + 1))/(4(x - 2))$

- [ ] $(16(x - 2))/(9(y + 1))$

Since our ellipse is centered at $(2,-1)$ and has semiaxes $3$ and $4,$ its equation is given by

$$
\frac{(x-2)^{2}}{{3}^{2}}+\frac{(y-(-1))^{2}}{{4}^{2}}=1\,⟹\,\frac{(x-2)^{2}}{9}+\frac{(y+1)^{2}}{16}=1.
$$

Now, to calculate $\frac{\text{d}y}{\text{d}x},$ we use implicit differentiation:

$$
\begin{aligned}\frac{\text{d}}{\text{d}x}(\frac{(x-2)^{2}}{9}+\frac{(y+1)^{2}}{16}) & =\frac{\text{d}}{\text{d}x}(1) \\ \frac{\text{d}}{\text{d}x}(\frac{(x-2)^{2}}{9})+\frac{\text{d}}{\text{d}x}(\frac{(y+1)^{2}}{16}) & =0 \\ \frac{2(x-2)}{9}+\frac{2(y+1)}{16}\cdot \frac{\text{d}y}{\text{d}x} & =0 \\ \frac{y+1}{8}\cdot \frac{\text{d}y}{\text{d}x} & =-\frac{2(x-2)}{9} \\ \frac{\text{d}y}{\text{d}x} & =-\frac{16(x-2)}{9(y+1)}\end{aligned}
$$

### raw observed evidence — easy — observed-q-127511

![](/media/jake/SSD/EDB/math/images/c0/c0295c7cdc1abc16273efda842a0aa7a892ece2f5dda5e29f7baab25320b23ec.png)

Find $\frac{\text{d}y}{\text{d}x}$ for the ellipse shown above.

- [x] $-\frac{4x}{y}$

- [ ] $\frac{x}{4y}$

- [ ] $\frac{y}{4x}$

- [ ] $-\frac{2x}{y}$

- [ ] $-\frac{y}{2x}$

Since our ellipse is centered at the origin and has semiaxes $1$ and $2,$ its equation is given by

$$
\frac{{x}^{2}}{{1}^{2}}+\frac{{y}^{2}}{{2}^{2}}=1\,⟹\,{x}^{2}+\frac{{y}^{2}}{4}=1.
$$

Now, to calculate $\frac{\text{d}y}{\text{d}x},$ we use implicit differentiation:

$$
\begin{aligned}\frac{\text{d}}{\text{d}x}({x}^{2}+\frac{{y}^{2}}{4}) & =\frac{\text{d}}{\text{d}x}(1) \\ \frac{\text{d}}{\text{d}x}({x}^{2})+\frac{\text{d}}{\text{d}x}(\frac{{y}^{2}}{4}) & =0 \\ 2x+\frac{2y}{4}\cdot \frac{\text{d}y}{\text{d}x} & =0 \\ \frac{y}{2}\cdot \frac{\text{d}y}{\text{d}x} & =-2x \\ \frac{\text{d}y}{\text{d}x} & =-\frac{4x}{y}\end{aligned}
$$

### supported source completion — easy — completed-q-127511

![](/media/jake/SSD/EDB/math/images/c0/c0295c7cdc1abc16273efda842a0aa7a892ece2f5dda5e29f7baab25320b23ec.png)

Find $\frac{\text{d}y}{\text{d}x}$ for the ellipse shown above.

- [x] $-\frac{4x}{y}$

- [ ] $\frac{x}{4y}$

- [ ] $-\frac{y}{2x}$

- [ ] $\frac{y}{4x}$

- [ ] $-\frac{2x}{y}$

Since our ellipse is centered at the origin and has semiaxes $1$ and $2,$ its equation is given by

$$
\frac{{x}^{2}}{{1}^{2}}+\frac{{y}^{2}}{{2}^{2}}=1\,⟹\,{x}^{2}+\frac{{y}^{2}}{4}=1.
$$

Now, to calculate $\frac{\text{d}y}{\text{d}x},$ we use implicit differentiation:

$$
\begin{aligned}\frac{\text{d}}{\text{d}x}({x}^{2}+\frac{{y}^{2}}{4}) & =\frac{\text{d}}{\text{d}x}(1) \\ \frac{\text{d}}{\text{d}x}({x}^{2})+\frac{\text{d}}{\text{d}x}(\frac{{y}^{2}}{4}) & =0 \\ 2x+\frac{2y}{4}\cdot \frac{\text{d}y}{\text{d}x} & =0 \\ \frac{y}{2}\cdot \frac{\text{d}y}{\text{d}x} & =-2x \\ \frac{\text{d}y}{\text{d}x} & =-\frac{4x}{y}\end{aligned}
$$

### raw observed evidence — easy — observed-q-127512

![](/media/jake/SSD/EDB/math/images/43/43e8ed1ee117ccd10f0e3aa03fc8db8ec1db6c076689e9072e1e22e048dfc279.png)

Find $\frac{\text{d}y}{\text{d}x}$ for the ellipse shown above.

- [ ] $\frac{25y}{9x}$

- [ ] $\frac{5y}{3x}$

- [ ] $-\frac{3x}{5y}$

- [x] $-\frac{9x}{25y}$

- [ ] $-\frac{9y}{25x}$

Since our ellipse is centered at the origin and has semiaxes $5$ and $3,$ its equation is given by

$$
\frac{{x}^{2}}{{5}^{2}}+\frac{{y}^{2}}{{3}^{2}}=1\,⟹\,\frac{{x}^{2}}{25}+\frac{{y}^{2}}{9}=1.
$$

Now, to calculate $\frac{\text{d}y}{\text{d}x},$ we use implicit differentiation:

$$
\begin{aligned}\frac{\text{d}}{\text{d}x}(\frac{{x}^{2}}{25}+\frac{{y}^{2}}{9}) & =\frac{\text{d}}{\text{d}x}(1) \\ \frac{\text{d}}{\text{d}x}(\frac{{x}^{2}}{25})+\frac{\text{d}}{\text{d}x}(\frac{{y}^{2}}{9}) & =0 \\ \frac{2x}{25}+\frac{2y}{9}\cdot \frac{\text{d}y}{\text{d}x} & =0 \\ \frac{2y}{9}\cdot \frac{\text{d}y}{\text{d}x} & =-\frac{2x}{25} \\ \frac{\text{d}y}{\text{d}x} & =-\frac{9x}{25y}\end{aligned}
$$

### supported source completion — easy — completed-q-127512

![](/media/jake/SSD/EDB/math/images/43/43e8ed1ee117ccd10f0e3aa03fc8db8ec1db6c076689e9072e1e22e048dfc279.png)

Find $\frac{\text{d}y}{\text{d}x}$ for the ellipse shown above.

- [ ] $\frac{25y}{9x}$

- [ ] $\frac{5y}{3x}$

- [ ] $-\frac{9y}{25x}$

- [ ] $-\frac{3x}{5y}$

- [x] $-\frac{9x}{25y}$

Since our ellipse is centered at the origin and has semiaxes $5$ and $3,$ its equation is given by

$$
\frac{{x}^{2}}{{5}^{2}}+\frac{{y}^{2}}{{3}^{2}}=1\,⟹\,\frac{{x}^{2}}{25}+\frac{{y}^{2}}{9}=1.
$$

Now, to calculate $\frac{\text{d}y}{\text{d}x},$ we use implicit differentiation:

$$
\begin{aligned}\frac{\text{d}}{\text{d}x}(\frac{{x}^{2}}{25}+\frac{{y}^{2}}{9}) & =\frac{\text{d}}{\text{d}x}(1) \\ \frac{\text{d}}{\text{d}x}(\frac{{x}^{2}}{25})+\frac{\text{d}}{\text{d}x}(\frac{{y}^{2}}{9}) & =0 \\ \frac{2x}{25}+\frac{2y}{9}\cdot \frac{\text{d}y}{\text{d}x} & =0 \\ \frac{2y}{9}\cdot \frac{\text{d}y}{\text{d}x} & =-\frac{2x}{25} \\ \frac{\text{d}y}{\text{d}x} & =-\frac{9x}{25y}\end{aligned}
$$

### raw observed evidence — easy — observed-q-127513

![](/media/jake/SSD/EDB/math/images/f8/f8effaf21270245ed6f8df63d2e430483756f47537b1c7325e88acc5286544db.png)

Find $\frac{\text{d}y}{\text{d}x}$ for the ellipse shown above.

- [ ] $-\frac{5y}{2x}$

- [ ] $\frac{5x}{2y}$

- [ ] $\frac{25y}{4x}$

- [ ] $-\frac{5x}{2y}$

- [x] $-\frac{25x}{4y}$

Since our ellipse is centered at the origin and has semiaxes $2$ and $5,$ its equation is given by

$$
\frac{{x}^{2}}{{2}^{2}}+\frac{{y}^{2}}{{5}^{2}}=1\,⟹\,\frac{{x}^{2}}{4}+\frac{{y}^{2}}{25}=1.
$$

Now, to calculate $\frac{\text{d}y}{\text{d}x},$ we use implicit differentiation:

$$
\begin{aligned}\frac{\text{d}}{\text{d}x}(\frac{{x}^{2}}{4}+\frac{{y}^{2}}{25}) & =\frac{\text{d}}{\text{d}x}(1) \\ \frac{\text{d}}{\text{d}x}(\frac{{x}^{2}}{4})+\frac{\text{d}}{\text{d}x}(\frac{{y}^{2}}{25}) & =0 \\ \frac{2x}{4}+\frac{2y}{25}\cdot \frac{\text{d}y}{\text{d}x} & =0 \\ \frac{2y}{25}\cdot \frac{\text{d}y}{\text{d}x} & =-\frac{x}{2} \\ \frac{\text{d}y}{\text{d}x} & =-\frac{25x}{4y}\end{aligned}
$$

### supported source completion — easy — completed-q-127513

![](/media/jake/SSD/EDB/math/images/f8/f8effaf21270245ed6f8df63d2e430483756f47537b1c7325e88acc5286544db.png)

Find $\frac{\text{d}y}{\text{d}x}$ for the ellipse shown above.

- [ ] $-\frac{5y}{2x}$

- [ ] $\frac{5x}{2y}$

- [x] $-\frac{25x}{4y}$

- [ ] $\frac{25y}{4x}$

- [ ] $-\frac{5x}{2y}$

Since our ellipse is centered at the origin and has semiaxes $2$ and $5,$ its equation is given by

$$
\frac{{x}^{2}}{{2}^{2}}+\frac{{y}^{2}}{{5}^{2}}=1\,⟹\,\frac{{x}^{2}}{4}+\frac{{y}^{2}}{25}=1.
$$

Now, to calculate $\frac{\text{d}y}{\text{d}x},$ we use implicit differentiation:

$$
\begin{aligned}\frac{\text{d}}{\text{d}x}(\frac{{x}^{2}}{4}+\frac{{y}^{2}}{25}) & =\frac{\text{d}}{\text{d}x}(1) \\ \frac{\text{d}}{\text{d}x}(\frac{{x}^{2}}{4})+\frac{\text{d}}{\text{d}x}(\frac{{y}^{2}}{25}) & =0 \\ \frac{2x}{4}+\frac{2y}{25}\cdot \frac{\text{d}y}{\text{d}x} & =0 \\ \frac{2y}{25}\cdot \frac{\text{d}y}{\text{d}x} & =-\frac{x}{2} \\ \frac{\text{d}y}{\text{d}x} & =-\frac{25x}{4y}\end{aligned}
$$

### raw observed evidence — easy — observed-q-127514

![](/media/jake/SSD/EDB/math/images/54/547b79b566d2914db4a63997cd5fc9f02dd1517b8dcd5e53cde8c07ac5ca05a2.png)

Find $\frac{\text{d}y}{\text{d}x}$ for the ellipse shown above.

- [ ] $-\frac{9x}{y}$

- [x] $-\frac{x}{9y}$

- [ ] $-\frac{9y}{x}$

- [ ] $-\frac{3y}{x}$

- [ ] $-\frac{x}{3y}$

Since our ellipse is centered at the origin and has semiaxes $3$ and $1,$ its equation is given by

$$
\frac{{x}^{2}}{{3}^{2}}+\frac{{y}^{2}}{{1}^{2}}=1\,⟹\,\frac{{x}^{2}}{9}+{y}^{2}=1.
$$

Now, to calculate $\frac{\text{d}y}{\text{d}x},$ we use implicit differentiation:

$$
\begin{aligned}\frac{\text{d}}{\text{d}x}(\frac{{x}^{2}}{9}+{y}^{2}) & =\frac{\text{d}}{\text{d}x}(1) \\ \frac{\text{d}}{\text{d}x}(\frac{{x}^{2}}{9})+\frac{\text{d}}{\text{d}x}({y}^{2}) & =0 \\ \frac{2x}{9}+2y\cdot \frac{\text{d}y}{\text{d}x} & =0 \\ 2y\cdot \frac{\text{d}y}{\text{d}x} & =-\frac{2x}{9} \\ \frac{\text{d}y}{\text{d}x} & =-\frac{x}{9y}\end{aligned}
$$

### supported source completion — easy — completed-q-127514

![](/media/jake/SSD/EDB/math/images/54/547b79b566d2914db4a63997cd5fc9f02dd1517b8dcd5e53cde8c07ac5ca05a2.png)

Find $\frac{\text{d}y}{\text{d}x}$ for the ellipse shown above.

- [ ] $-\frac{9x}{y}$

- [x] $-\frac{x}{9y}$

- [ ] $-\frac{x}{3y}$

- [ ] $-\frac{9y}{x}$

- [ ] $-\frac{3y}{x}$

Since our ellipse is centered at the origin and has semiaxes $3$ and $1,$ its equation is given by

$$
\frac{{x}^{2}}{{3}^{2}}+\frac{{y}^{2}}{{1}^{2}}=1\,⟹\,\frac{{x}^{2}}{9}+{y}^{2}=1.
$$

Now, to calculate $\frac{\text{d}y}{\text{d}x},$ we use implicit differentiation:

$$
\begin{aligned}\frac{\text{d}}{\text{d}x}(\frac{{x}^{2}}{9}+{y}^{2}) & =\frac{\text{d}}{\text{d}x}(1) \\ \frac{\text{d}}{\text{d}x}(\frac{{x}^{2}}{9})+\frac{\text{d}}{\text{d}x}({y}^{2}) & =0 \\ \frac{2x}{9}+2y\cdot \frac{\text{d}y}{\text{d}x} & =0 \\ 2y\cdot \frac{\text{d}y}{\text{d}x} & =-\frac{2x}{9} \\ \frac{\text{d}y}{\text{d}x} & =-\frac{x}{9y}\end{aligned}
$$

### raw observed evidence — moderate — observed-q-127523

![](/media/jake/SSD/EDB/math/images/eb/ebef81911a434828ab94e643007d06b677538cdf0995198c7a065e35a8f81996.png)

Find $\frac{\text{d}y}{\text{d}x}$ for the ellipse shown above.

- [ ] $-\frac{4(y+1)}{x+1}$

- [ ] $\frac{y-1}{4(x-1)}$

- [ ] $-\frac{4(x+1)}{y+1}$

- [ ] $\frac{x-1}{4(y-1)}$

- [x] $-\frac{x+1}{4(y+1)}$

Since our ellipse is centered at $(-1,-1)$ and has semiaxes $2$ and $1,$ its equation is given by

$$
\frac{(x-(-1))^{2}}{{2}^{2}}+\frac{(y-(-1))^{2}}{{1}^{2}}=1\,⟹\,\frac{(x+1)^{2}}{4}+(y+1)^{2}=1.
$$

Now, to calculate $\frac{\text{d}y}{\text{d}x},$ we use implicit differentiation:

$$
\begin{aligned}\frac{\text{d}}{\text{d}x}(\frac{(x+1)^{2}}{4}+(y+1)^{2}) & =\frac{\text{d}}{\text{d}x}(1) \\ \frac{\text{d}}{\text{d}x}(\frac{(x+1)^{2}}{4})+\frac{\text{d}}{\text{d}x}((y+1)^{2}) & =0 \\ \frac{2(x+1)}{4}+2(y+1)\cdot \frac{\text{d}y}{\text{d}x} & =0 \\ 2(y+1)\cdot \frac{\text{d}y}{\text{d}x} & =-\frac{x+1}{2} \\ \frac{\text{d}y}{\text{d}x} & =-\frac{x+1}{4(y+1)}\end{aligned}
$$

### supported source completion — moderate — completed-q-127523

![](/media/jake/SSD/EDB/math/images/eb/ebef81911a434828ab94e643007d06b677538cdf0995198c7a065e35a8f81996.png)

Find $\frac{\text{d}y}{\text{d}x}$ for the ellipse shown above.

- [ ] $-\frac{4(y+1)}{x+1}$

- [ ] $\frac{y-1}{4(x-1)}$

- [x] $-\frac{x+1}{4(y+1)}$

- [ ] $-\frac{4(x+1)}{y+1}$

- [ ] $\frac{x-1}{4(y-1)}$

Since our ellipse is centered at $(-1,-1)$ and has semiaxes $2$ and $1,$ its equation is given by

$$
\frac{(x-(-1))^{2}}{{2}^{2}}+\frac{(y-(-1))^{2}}{{1}^{2}}=1\,⟹\,\frac{(x+1)^{2}}{4}+(y+1)^{2}=1.
$$

Now, to calculate $\frac{\text{d}y}{\text{d}x},$ we use implicit differentiation:

$$
\begin{aligned}\frac{\text{d}}{\text{d}x}(\frac{(x+1)^{2}}{4}+(y+1)^{2}) & =\frac{\text{d}}{\text{d}x}(1) \\ \frac{\text{d}}{\text{d}x}(\frac{(x+1)^{2}}{4})+\frac{\text{d}}{\text{d}x}((y+1)^{2}) & =0 \\ \frac{2(x+1)}{4}+2(y+1)\cdot \frac{\text{d}y}{\text{d}x} & =0 \\ 2(y+1)\cdot \frac{\text{d}y}{\text{d}x} & =-\frac{x+1}{2} \\ \frac{\text{d}y}{\text{d}x} & =-\frac{x+1}{4(y+1)}\end{aligned}
$$

### raw observed evidence — moderate — observed-q-127525

![](/media/jake/SSD/EDB/math/images/eb/eb0fbc8f57621946a5ec5168e8c607d230269e0c6a64b4c86c835c110f0f6288.png)

Find $\frac{\text{d}y}{\text{d}x}$ for the ellipse shown above.

- [ ] $\frac{3x}{2(y-1)}$

- [ ] $\frac{3(y-1)}{2x}$

- [ ] $\frac{4x}{9(y-1)}$

- [x] $-\frac{9x}{4(y-1)}$

- [ ] $-\frac{4(y-1)}{9x}$

Since our ellipse is centered at $(0,1)$ and has semiaxes $2$ and $3,$ its equation is given by

$$
\frac{(x-0)^{2}}{{2}^{2}}+\frac{(y-1)^{2}}{{3}^{2}}=1\,⟹\,\frac{{x}^{2}}{4}+\frac{(y-1)^{2}}{9}=1.
$$

Now, to calculate $\frac{\text{d}y}{\text{d}x},$ we use implicit differentiation:

$$
\begin{aligned}\frac{\text{d}}{\text{d}x}(\frac{{x}^{2}}{4}+\frac{(y-1)^{2}}{9}) & =\frac{\text{d}}{\text{d}x}(1) \\ \frac{\text{d}}{\text{d}x}(\frac{{x}^{2}}{4})+\frac{\text{d}}{\text{d}x}(\frac{(y-1)^{2}}{9}) & =0 \\ \frac{2x}{4}+\frac{2(y-1)}{9}\cdot \frac{\text{d}y}{\text{d}x} & =0 \\ \frac{2(y-1)}{9}\cdot \frac{\text{d}y}{\text{d}x} & =-\frac{x}{2} \\ \frac{\text{d}y}{\text{d}x} & =-\frac{9x}{4(y-1)}\end{aligned}
$$

### supported source completion — moderate — completed-q-127525

![](/media/jake/SSD/EDB/math/images/eb/eb0fbc8f57621946a5ec5168e8c607d230269e0c6a64b4c86c835c110f0f6288.png)

Find $\frac{\text{d}y}{\text{d}x}$ for the ellipse shown above.

- [ ] $\frac{3x}{2(y-1)}$

- [ ] $\frac{3(y-1)}{2x}$

- [ ] $-\frac{4(y-1)}{9x}$

- [ ] $\frac{4x}{9(y-1)}$

- [x] $-\frac{9x}{4(y-1)}$

Since our ellipse is centered at $(0,1)$ and has semiaxes $2$ and $3,$ its equation is given by

$$
\frac{(x-0)^{2}}{{2}^{2}}+\frac{(y-1)^{2}}{{3}^{2}}=1\,⟹\,\frac{{x}^{2}}{4}+\frac{(y-1)^{2}}{9}=1.
$$

Now, to calculate $\frac{\text{d}y}{\text{d}x},$ we use implicit differentiation:

$$
\begin{aligned}\frac{\text{d}}{\text{d}x}(\frac{{x}^{2}}{4}+\frac{(y-1)^{2}}{9}) & =\frac{\text{d}}{\text{d}x}(1) \\ \frac{\text{d}}{\text{d}x}(\frac{{x}^{2}}{4})+\frac{\text{d}}{\text{d}x}(\frac{(y-1)^{2}}{9}) & =0 \\ \frac{2x}{4}+\frac{2(y-1)}{9}\cdot \frac{\text{d}y}{\text{d}x} & =0 \\ \frac{2(y-1)}{9}\cdot \frac{\text{d}y}{\text{d}x} & =-\frac{x}{2} \\ \frac{\text{d}y}{\text{d}x} & =-\frac{9x}{4(y-1)}\end{aligned}
$$

### raw observed evidence — moderate — observed-q-127526

![](/media/jake/SSD/EDB/math/images/e4/e4c39b409f6049a4fdead506c329d232820876c37ede9540adfeade2d7c1b9dc.png)

Find $\frac{\text{d}y}{\text{d}x}$ for the ellipse shown above.

- [ ] $-\frac{4(y-3)}{9x}$

- [ ] $\frac{2(x-3)}{3y}$

- [x] $-\frac{4(x-3)}{9y}$

- [ ] $\frac{9x}{4(y-3)}$

- [ ] $-\frac{3y}{2(x-3)}$

Since our ellipse is centered at $(3,0)$ and has semiaxes $3$ and $2,$ its equation is given by

$$
\frac{(x-3)^{2}}{{3}^{2}}+\frac{(y-0)^{2}}{{2}^{2}}=1\,⟹\,\frac{(x-3)^{2}}{9}+\frac{{y}^{2}}{4}=1.
$$

Now, to calculate $\frac{\text{d}y}{\text{d}x},$ we use implicit differentiation:

$$
\begin{aligned}\frac{\text{d}}{\text{d}x}(\frac{(x-3)^{2}}{9}+\frac{{y}^{2}}{4}) & =\frac{\text{d}}{\text{d}x}(1) \\ \frac{\text{d}}{\text{d}x}(\frac{(x-3)^{2}}{9})+\frac{\text{d}}{\text{d}x}(\frac{{y}^{2}}{4}) & =0 \\ \frac{2(x-3)}{9}+\frac{2y}{4}\cdot \frac{\text{d}y}{\text{d}x} & =0 \\ \frac{y}{2}\cdot \frac{\text{d}y}{\text{d}x} & =-\frac{2(x-3)}{9} \\ \frac{\text{d}y}{\text{d}x} & =-\frac{4(x-3)}{9y}\end{aligned}
$$

### supported source completion — moderate — completed-q-127526

![](/media/jake/SSD/EDB/math/images/e4/e4c39b409f6049a4fdead506c329d232820876c37ede9540adfeade2d7c1b9dc.png)

Find $\frac{\text{d}y}{\text{d}x}$ for the ellipse shown above.

- [ ] $-\frac{4(y-3)}{9x}$

- [ ] $\frac{2(x-3)}{3y}$

- [ ] $-\frac{3y}{2(x-3)}$

- [x] $-\frac{4(x-3)}{9y}$

- [ ] $\frac{9x}{4(y-3)}$

Since our ellipse is centered at $(3,0)$ and has semiaxes $3$ and $2,$ its equation is given by

$$
\frac{(x-3)^{2}}{{3}^{2}}+\frac{(y-0)^{2}}{{2}^{2}}=1\,⟹\,\frac{(x-3)^{2}}{9}+\frac{{y}^{2}}{4}=1.
$$

Now, to calculate $\frac{\text{d}y}{\text{d}x},$ we use implicit differentiation:

$$
\begin{aligned}\frac{\text{d}}{\text{d}x}(\frac{(x-3)^{2}}{9}+\frac{{y}^{2}}{4}) & =\frac{\text{d}}{\text{d}x}(1) \\ \frac{\text{d}}{\text{d}x}(\frac{(x-3)^{2}}{9})+\frac{\text{d}}{\text{d}x}(\frac{{y}^{2}}{4}) & =0 \\ \frac{2(x-3)}{9}+\frac{2y}{4}\cdot \frac{\text{d}y}{\text{d}x} & =0 \\ \frac{y}{2}\cdot \frac{\text{d}y}{\text{d}x} & =-\frac{2(x-3)}{9} \\ \frac{\text{d}y}{\text{d}x} & =-\frac{4(x-3)}{9y}\end{aligned}
$$

### authored parameter variant — easy — authored-method

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186166866/assets/6beb929f9ee4969de76288de340fc3dd8ae83c2849ae39d97c52ea1a5e3121b7.png)

Find $\frac{\text{d}y}{\text{d}x}$ for the ellipse shown above.

- [ ] $-\frac{16y}{x}$

- [ ] $-\frac{16x}{y}$

- [ ] $\frac{x}{16y}$

- [x] $-\frac{x}{16y}$

- [ ] $-\frac{x}{4y}$

Since our ellipse is centered at the origin and has semiaxes $4$ and $1,$ its equation is given by

$$
\frac{{x}^{2}}{{4}^{2}}+\frac{{y}^{2}}{{1}^{2}}=1\,⟹\,\frac{{x}^{2}}{16}+{y}^{2}=1.
$$

Now, to calculate $\frac{\text{d}y}{\text{d}x},$ we use implicit differentiation:

$$
\begin{aligned}\frac{\text{d}}{\text{d}x}(\frac{{x}^{2}}{16}+{y}^{2}) & =\frac{\text{d}}{\text{d}x}(1) \\ \frac{\text{d}}{\text{d}x}(\frac{{x}^{2}}{16})+\frac{\text{d}}{\text{d}x}({y}^{2}) & =0 \\ \frac{2x}{16}+2y\cdot \frac{\text{d}y}{\text{d}x} & =0 \\ 2y\cdot \frac{\text{d}y}{\text{d}x} & =-\frac{x}{8} \\ \frac{\text{d}y}{\text{d}x} & =-\frac{x}{16y}\end{aligned}
$$

### authored parameter variant — easy — authored-method

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186166866/assets/09a38ad9289f8b114042f686664ff02ac84b58ccb037d6e5ba12711608028143.png)

Find $\frac{\text{d}y}{\text{d}x}$ for the ellipse shown above.

- [ ] $-\frac{4x}{y}$

- [ ] $-\frac{x}{2y}$

- [ ] $\frac{x}{4y}$

- [x] $-\frac{x}{4y}$

- [ ] $-\frac{4y}{x}$

Since our ellipse is centered at the origin and has semiaxes $2$ and $1,$ its equation is given by

$$
\frac{{x}^{2}}{{2}^{2}}+\frac{{y}^{2}}{{1}^{2}}=1\,⟹\,\frac{{x}^{2}}{4}+{y}^{2}=1.
$$

Now, to calculate $\frac{\text{d}y}{\text{d}x},$ we use implicit differentiation:

$$
\begin{aligned}\frac{\text{d}}{\text{d}x}(\frac{{x}^{2}}{4}+{y}^{2}) & =\frac{\text{d}}{\text{d}x}(1) \\ \frac{\text{d}}{\text{d}x}(\frac{{x}^{2}}{4})+\frac{\text{d}}{\text{d}x}({y}^{2}) & =0 \\ \frac{2x}{4}+2y\cdot \frac{\text{d}y}{\text{d}x} & =0 \\ 2y\cdot \frac{\text{d}y}{\text{d}x} & =-\frac{x}{2} \\ \frac{\text{d}y}{\text{d}x} & =-\frac{x}{4y}\end{aligned}
$$

### authored parameter variant — easy — authored-method

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186166866/assets/2b40b30ba3b54e51df4a2692bb8bea607b6b0e35c74d4c00bf66b0e5c8da774f.png)

Find $\frac{\text{d}y}{\text{d}x}$ for the ellipse shown above.

- [ ] $-\frac{x}{9y}$

- [ ] $-\frac{3x}{y}$

- [ ] $\frac{9x}{y}$

- [ ] $-\frac{y}{9x}$

- [x] $-\frac{9x}{y}$

Since our ellipse is centered at the origin and has semiaxes $1$ and $3,$ its equation is given by

$$
\frac{{x}^{2}}{{1}^{2}}+\frac{{y}^{2}}{{3}^{2}}=1\,⟹\,{x}^{2}+\frac{{y}^{2}}{9}=1.
$$

Now, to calculate $\frac{\text{d}y}{\text{d}x},$ we use implicit differentiation:

$$
\begin{aligned}\frac{\text{d}}{\text{d}x}({x}^{2}+\frac{{y}^{2}}{9}) & =\frac{\text{d}}{\text{d}x}(1) \\ \frac{\text{d}}{\text{d}x}({x}^{2})+\frac{\text{d}}{\text{d}x}(\frac{{y}^{2}}{9}) & =0 \\ 2x+\frac{2y}{9}\cdot \frac{\text{d}y}{\text{d}x} & =0 \\ \frac{2y}{9}\cdot \frac{\text{d}y}{\text{d}x} & =-2x \\ \frac{\text{d}y}{\text{d}x} & =-\frac{9x}{y}\end{aligned}
$$

### authored parameter variant — easy — authored-method

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186166866/assets/4cd2321958019c6baaa6ee0fe712ae99bb6387ba67fa91ae4cb2cb09e50c3ee4.png)

Find $\frac{\text{d}y}{\text{d}x}$ for the ellipse shown above.

- [x] $-\frac{25x}{4y}$

- [ ] $-\frac{4x}{25y}$

- [ ] $-\frac{5x}{2y}$

- [ ] $\frac{25x}{4y}$

- [ ] $-\frac{4y}{25x}$

Since our ellipse is centered at the origin and has semiaxes $2$ and $5,$ its equation is given by

$$
\frac{{x}^{2}}{{2}^{2}}+\frac{{y}^{2}}{{5}^{2}}=1\,⟹\,\frac{{x}^{2}}{4}+\frac{{y}^{2}}{25}=1.
$$

Now, to calculate $\frac{\text{d}y}{\text{d}x},$ we use implicit differentiation:

$$
\begin{aligned}\frac{\text{d}}{\text{d}x}(\frac{{x}^{2}}{4}+\frac{{y}^{2}}{25}) & =\frac{\text{d}}{\text{d}x}(1) \\ \frac{\text{d}}{\text{d}x}(\frac{{x}^{2}}{4})+\frac{\text{d}}{\text{d}x}(\frac{{y}^{2}}{25}) & =0 \\ \frac{2x}{4}+\frac{2y}{25}\cdot \frac{\text{d}y}{\text{d}x} & =0 \\ \frac{2y}{25}\cdot \frac{\text{d}y}{\text{d}x} & =-\frac{x}{2} \\ \frac{\text{d}y}{\text{d}x} & =-\frac{25x}{4y}\end{aligned}
$$

### authored parameter variant — easy — authored-method

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186166866/assets/4cd2321958019c6baaa6ee0fe712ae99bb6387ba67fa91ae4cb2cb09e50c3ee4.png)

Find $\frac{\text{d}y}{\text{d}x}$ for the ellipse shown above.

- [ ] $-\frac{5x}{2y}$

- [ ] $\frac{25x}{4y}$

- [ ] $-\frac{4y}{25x}$

- [x] $-\frac{25x}{4y}$

- [ ] $-\frac{4x}{25y}$

Since our ellipse is centered at the origin and has semiaxes $2$ and $5,$ its equation is given by

$$
\frac{{x}^{2}}{{2}^{2}}+\frac{{y}^{2}}{{5}^{2}}=1\,⟹\,\frac{{x}^{2}}{4}+\frac{{y}^{2}}{25}=1.
$$

Now, to calculate $\frac{\text{d}y}{\text{d}x},$ we use implicit differentiation:

$$
\begin{aligned}\frac{\text{d}}{\text{d}x}(\frac{{x}^{2}}{4}+\frac{{y}^{2}}{25}) & =\frac{\text{d}}{\text{d}x}(1) \\ \frac{\text{d}}{\text{d}x}(\frac{{x}^{2}}{4})+\frac{\text{d}}{\text{d}x}(\frac{{y}^{2}}{25}) & =0 \\ \frac{2x}{4}+\frac{2y}{25}\cdot \frac{\text{d}y}{\text{d}x} & =0 \\ \frac{2y}{25}\cdot \frac{\text{d}y}{\text{d}x} & =-\frac{x}{2} \\ \frac{\text{d}y}{\text{d}x} & =-\frac{25x}{4y}\end{aligned}
$$

### authored parameter variant — easy — authored-method

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186166866/assets/d06b0bddee9bcc3bf6ec8ae3ee0c8737d5fe5e29bf7d45ba86b9379cca8ae543.png)

Find $\frac{\text{d}y}{\text{d}x}$ for the ellipse shown above.

- [ ] $\frac{16x}{25y}$

- [x] $-\frac{16x}{25y}$

- [ ] $-\frac{4x}{5y}$

- [ ] $-\frac{25y}{16x}$

- [ ] $-\frac{25x}{16y}$

Since our ellipse is centered at the origin and has semiaxes $5$ and $4,$ its equation is given by

$$
\frac{{x}^{2}}{{5}^{2}}+\frac{{y}^{2}}{{4}^{2}}=1\,⟹\,\frac{{x}^{2}}{25}+\frac{{y}^{2}}{16}=1.
$$

Now, to calculate $\frac{\text{d}y}{\text{d}x},$ we use implicit differentiation:

$$
\begin{aligned}\frac{\text{d}}{\text{d}x}(\frac{{x}^{2}}{25}+\frac{{y}^{2}}{16}) & =\frac{\text{d}}{\text{d}x}(1) \\ \frac{\text{d}}{\text{d}x}(\frac{{x}^{2}}{25})+\frac{\text{d}}{\text{d}x}(\frac{{y}^{2}}{16}) & =0 \\ \frac{2x}{25}+\frac{2y}{16}\cdot \frac{\text{d}y}{\text{d}x} & =0 \\ \frac{y}{8}\cdot \frac{\text{d}y}{\text{d}x} & =-\frac{2x}{25} \\ \frac{\text{d}y}{\text{d}x} & =-\frac{16x}{25y}\end{aligned}
$$

### authored parameter variant — moderate — authored-method

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186166866/assets/39cc57968434246b4cd1716567c2cadae2c6cbd1dc21ce4f6728fd0ddd0e63f0.png)

Find $\frac{\text{d}y}{\text{d}x}$ for the ellipse shown above.

- [ ] $-\frac{x-3}{16(y+1)}$

- [ ] $\frac{16(x-3)}{y+1}$

- [x] $-\frac{16(x-3)}{y+1}$

- [ ] $-\frac{y+1}{16(x-3)}$

- [ ] $-\frac{4(x-3)}{y+1}$

Since our ellipse is centered at $(3,-1)$ and has semiaxes $1$ and $4,$ its equation is given by

$$
\frac{(x-3)^{2}}{{1}^{2}}+\frac{(y-(-1))^{2}}{{4}^{2}}=1\,⟹\,(x-3)^{2}+\frac{(y+1)^{2}}{16}=1.
$$

Now, to calculate $\frac{\text{d}y}{\text{d}x},$ we use implicit differentiation:

$$
\begin{aligned}\frac{\text{d}}{\text{d}x}((x-3)^{2}+\frac{(y+1)^{2}}{16}) & =\frac{\text{d}}{\text{d}x}(1) \\ \frac{\text{d}}{\text{d}x}((x-3)^{2})+\frac{\text{d}}{\text{d}x}(\frac{(y+1)^{2}}{16}) & =0 \\ 2(x-3)+\frac{2(y+1)}{16}\cdot \frac{\text{d}y}{\text{d}x} & =0 \\ \frac{y+1}{8}\cdot \frac{\text{d}y}{\text{d}x} & =-2(x-3) \\ \frac{\text{d}y}{\text{d}x} & =-\frac{16(x-3)}{y+1}\end{aligned}
$$

### authored parameter variant — moderate — authored-method

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186166866/assets/157beadfbd70b0b3f97c354de6251d48ce16d535197e8f3631b744f9163e4c7a.png)

Find $\frac{\text{d}y}{\text{d}x}$ for the ellipse shown above.

- [ ] $-\frac{4(x+3)}{y-3}$

- [ ] $-\frac{x+3}{2(y-3)}$

- [ ] $\frac{x+3}{4(y-3)}$

- [x] $-\frac{x+3}{4(y-3)}$

- [ ] $-\frac{4(y-3)}{x+3}$

Since our ellipse is centered at $(-3,3)$ and has semiaxes $4$ and $2,$ its equation is given by

$$
\frac{(x-(-3))^{2}}{{4}^{2}}+\frac{(y-3)^{2}}{{2}^{2}}=1\,⟹\,\frac{(x+3)^{2}}{16}+\frac{(y-3)^{2}}{4}=1.
$$

Now, to calculate $\frac{\text{d}y}{\text{d}x},$ we use implicit differentiation:

$$
\begin{aligned}\frac{\text{d}}{\text{d}x}(\frac{(x+3)^{2}}{16}+\frac{(y-3)^{2}}{4}) & =\frac{\text{d}}{\text{d}x}(1) \\ \frac{\text{d}}{\text{d}x}(\frac{(x+3)^{2}}{16})+\frac{\text{d}}{\text{d}x}(\frac{(y-3)^{2}}{4}) & =0 \\ \frac{2(x+3)}{16}+\frac{2(y-3)}{4}\cdot \frac{\text{d}y}{\text{d}x} & =0 \\ \frac{y-3}{2}\cdot \frac{\text{d}y}{\text{d}x} & =-\frac{x+3}{8} \\ \frac{\text{d}y}{\text{d}x} & =-\frac{x+3}{4(y-3)}\end{aligned}
$$

### authored parameter variant — moderate — authored-method

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186166866/assets/07cca628e4ceb0de66c35990c4c7529f2383b76aa9664b7d7120e67f8d6c6e76.png)

Find $\frac{\text{d}y}{\text{d}x}$ for the ellipse shown above.

- [ ] $-\frac{4(x-3)}{25y}$

- [ ] $\frac{25(x-3)}{4y}$

- [ ] $-\frac{5(x-3)}{2y}$

- [ ] $-\frac{4y}{25(x-3)}$

- [x] $-\frac{25(x-3)}{4y}$

Since our ellipse is centered at $(3,0)$ and has semiaxes $2$ and $5,$ its equation is given by

$$
\frac{(x-3)^{2}}{{2}^{2}}+\frac{(y-0)^{2}}{{5}^{2}}=1\,⟹\,\frac{(x-3)^{2}}{4}+\frac{{y}^{2}}{25}=1.
$$

Now, to calculate $\frac{\text{d}y}{\text{d}x},$ we use implicit differentiation:

$$
\begin{aligned}\frac{\text{d}}{\text{d}x}(\frac{(x-3)^{2}}{4}+\frac{{y}^{2}}{25}) & =\frac{\text{d}}{\text{d}x}(1) \\ \frac{\text{d}}{\text{d}x}(\frac{(x-3)^{2}}{4})+\frac{\text{d}}{\text{d}x}(\frac{{y}^{2}}{25}) & =0 \\ \frac{2(x-3)}{4}+\frac{2y}{25}\cdot \frac{\text{d}y}{\text{d}x} & =0 \\ \frac{2y}{25}\cdot \frac{\text{d}y}{\text{d}x} & =-\frac{x-3}{2} \\ \frac{\text{d}y}{\text{d}x} & =-\frac{25(x-3)}{4y}\end{aligned}
$$

### authored parameter variant — moderate — authored-method

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186166866/assets/7c4305aa894d517053edba61ee9769e6de7313c11e1220fe6799f8965f965a57.png)

Find $\frac{\text{d}y}{\text{d}x}$ for the ellipse shown above.

- [x] $-\frac{9(x+2)}{y-2}$

- [ ] $-\frac{x+2}{9(y-2)}$

- [ ] $-\frac{3(x+2)}{y-2}$

- [ ] $\frac{9(x+2)}{y-2}$

- [ ] $-\frac{y-2}{9(x+2)}$

Since our ellipse is centered at $(-2,2)$ and has semiaxes $1$ and $3,$ its equation is given by

$$
\frac{(x-(-2))^{2}}{{1}^{2}}+\frac{(y-2)^{2}}{{3}^{2}}=1\,⟹\,(x+2)^{2}+\frac{(y-2)^{2}}{9}=1.
$$

Now, to calculate $\frac{\text{d}y}{\text{d}x},$ we use implicit differentiation:

$$
\begin{aligned}\frac{\text{d}}{\text{d}x}((x+2)^{2}+\frac{(y-2)^{2}}{9}) & =\frac{\text{d}}{\text{d}x}(1) \\ \frac{\text{d}}{\text{d}x}((x+2)^{2})+\frac{\text{d}}{\text{d}x}(\frac{(y-2)^{2}}{9}) & =0 \\ 2(x+2)+\frac{2(y-2)}{9}\cdot \frac{\text{d}y}{\text{d}x} & =0 \\ \frac{2(y-2)}{9}\cdot \frac{\text{d}y}{\text{d}x} & =-2(x+2) \\ \frac{\text{d}y}{\text{d}x} & =-\frac{9(x+2)}{y-2}\end{aligned}
$$

### authored parameter variant — moderate — authored-method

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186166866/assets/23a3b5e3d32500172d3480b1f6bbb44743d991e33c8e95f40999964366ffd4b9.png)

Find $\frac{\text{d}y}{\text{d}x}$ for the ellipse shown above.

- [ ] $-\frac{2(x+2)}{y-2}$

- [ ] $\frac{4(x+2)}{y-2}$

- [ ] $-\frac{y-2}{4(x+2)}$

- [x] $-\frac{4(x+2)}{y-2}$

- [ ] $-\frac{x+2}{4(y-2)}$

Since our ellipse is centered at $(-2,2)$ and has semiaxes $1$ and $2,$ its equation is given by

$$
\frac{(x-(-2))^{2}}{{1}^{2}}+\frac{(y-2)^{2}}{{2}^{2}}=1\,⟹\,(x+2)^{2}+\frac{(y-2)^{2}}{4}=1.
$$

Now, to calculate $\frac{\text{d}y}{\text{d}x},$ we use implicit differentiation:

$$
\begin{aligned}\frac{\text{d}}{\text{d}x}((x+2)^{2}+\frac{(y-2)^{2}}{4}) & =\frac{\text{d}}{\text{d}x}(1) \\ \frac{\text{d}}{\text{d}x}((x+2)^{2})+\frac{\text{d}}{\text{d}x}(\frac{(y-2)^{2}}{4}) & =0 \\ 2(x+2)+\frac{2(y-2)}{4}\cdot \frac{\text{d}y}{\text{d}x} & =0 \\ \frac{y-2}{2}\cdot \frac{\text{d}y}{\text{d}x} & =-2(x+2) \\ \frac{\text{d}y}{\text{d}x} & =-\frac{4(x+2)}{y-2}\end{aligned}
$$

### authored parameter variant — moderate — authored-method

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186166866/assets/e818b778f03a522d1167a95a46abcb15e7e9f764b9270ab411679d54971d4ca9.png)

Find $\frac{\text{d}y}{\text{d}x}$ for the ellipse shown above.

- [ ] $\frac{x-1}{4(y-1)}$

- [x] $-\frac{x-1}{4(y-1)}$

- [ ] $-\frac{x-1}{2(y-1)}$

- [ ] $-\frac{4(y-1)}{x-1}$

- [ ] $-\frac{4(x-1)}{y-1}$

Since our ellipse is centered at $(1,1)$ and has semiaxes $4$ and $2,$ its equation is given by

$$
\frac{(x-1)^{2}}{{4}^{2}}+\frac{(y-1)^{2}}{{2}^{2}}=1\,⟹\,\frac{(x-1)^{2}}{16}+\frac{(y-1)^{2}}{4}=1.
$$

Now, to calculate $\frac{\text{d}y}{\text{d}x},$ we use implicit differentiation:

$$
\begin{aligned}\frac{\text{d}}{\text{d}x}(\frac{(x-1)^{2}}{16}+\frac{(y-1)^{2}}{4}) & =\frac{\text{d}}{\text{d}x}(1) \\ \frac{\text{d}}{\text{d}x}(\frac{(x-1)^{2}}{16})+\frac{\text{d}}{\text{d}x}(\frac{(y-1)^{2}}{4}) & =0 \\ \frac{2(x-1)}{16}+\frac{2(y-1)}{4}\cdot \frac{\text{d}y}{\text{d}x} & =0 \\ \frac{y-1}{2}\cdot \frac{\text{d}y}{\text{d}x} & =-\frac{x-1}{8} \\ \frac{\text{d}y}{\text{d}x} & =-\frac{x-1}{4(y-1)}\end{aligned}
$$

### authored hard extension — hard — authored-method

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186166866/assets/41ecbb38cfeba2a615e744f6cdb5cf9789cfc9d5f459130c201f29830b768244.png)

Find $\frac{\text{d}y}{\text{d}x}$ for the ellipse shown above.

- [ ] $-\frac{49(y+1)}{64(x-1)}$

- [ ] $-\frac{49(x-1)}{64(y+1)}$

- [ ] $\frac{64(x-1)}{49(y+1)}$

- [x] $-\frac{64(x-1)}{49(y+1)}$

- [ ] $-\frac{8(x-1)}{7(y+1)}$

Since our ellipse is centered at $(1,-1)$ and has semiaxes $7$ and $8,$ its equation is given by

$$
\frac{(x-1)^{2}}{{7}^{2}}+\frac{(y-(-1))^{2}}{{8}^{2}}=1\,⟹\,\frac{(x-1)^{2}}{49}+\frac{(y+1)^{2}}{64}=1.
$$

Now, to calculate $\frac{\text{d}y}{\text{d}x},$ we use implicit differentiation:

$$
\begin{aligned}\frac{\text{d}}{\text{d}x}(\frac{(x-1)^{2}}{49}+\frac{(y+1)^{2}}{64}) & =\frac{\text{d}}{\text{d}x}(1) \\ \frac{\text{d}}{\text{d}x}(\frac{(x-1)^{2}}{49})+\frac{\text{d}}{\text{d}x}(\frac{(y+1)^{2}}{64}) & =0 \\ \frac{2(x-1)}{49}+\frac{2(y+1)}{64}\cdot \frac{\text{d}y}{\text{d}x} & =0 \\ \frac{y+1}{32}\cdot \frac{\text{d}y}{\text{d}x} & =-\frac{2(x-1)}{49} \\ \frac{\text{d}y}{\text{d}x} & =-\frac{64(x-1)}{49(y+1)}\end{aligned}
$$

### authored hard extension — hard — authored-method

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186166866/assets/e8e910b9d67f580c6c631e9803eb2442c1a22bb3c5adcc1114b0caa09dc65b30.png)

Find $\frac{\text{d}y}{\text{d}x}$ for the ellipse shown above.

- [ ] $-\frac{25(x+3)}{64(y-1)}$

- [ ] $-\frac{8(x+3)}{5(y-1)}$

- [ ] $\frac{64(x+3)}{25(y-1)}$

- [x] $-\frac{64(x+3)}{25(y-1)}$

- [ ] $-\frac{25(y-1)}{64(x+3)}$

Since our ellipse is centered at $(-3,1)$ and has semiaxes $5$ and $8,$ its equation is given by

$$
\frac{(x-(-3))^{2}}{{5}^{2}}+\frac{(y-1)^{2}}{{8}^{2}}=1\,⟹\,\frac{(x+3)^{2}}{25}+\frac{(y-1)^{2}}{64}=1.
$$

Now, to calculate $\frac{\text{d}y}{\text{d}x},$ we use implicit differentiation:

$$
\begin{aligned}\frac{\text{d}}{\text{d}x}(\frac{(x+3)^{2}}{25}+\frac{(y-1)^{2}}{64}) & =\frac{\text{d}}{\text{d}x}(1) \\ \frac{\text{d}}{\text{d}x}(\frac{(x+3)^{2}}{25})+\frac{\text{d}}{\text{d}x}(\frac{(y-1)^{2}}{64}) & =0 \\ \frac{2(x+3)}{25}+\frac{2(y-1)}{64}\cdot \frac{\text{d}y}{\text{d}x} & =0 \\ \frac{y-1}{32}\cdot \frac{\text{d}y}{\text{d}x} & =-\frac{2(x+3)}{25} \\ \frac{\text{d}y}{\text{d}x} & =-\frac{64(x+3)}{25(y-1)}\end{aligned}
$$

### authored hard extension — hard — authored-method

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186166866/assets/ff05d69e4b5d8489614a139965a500389ac2c09bdb52ed39feddaa753af428e4.png)

Find $\frac{\text{d}y}{\text{d}x}$ for the ellipse shown above.

- [ ] $-\frac{16(x+4)}{25(y-2)}$

- [ ] $-\frac{5(x+4)}{4(y-2)}$

- [ ] $\frac{25(x+4)}{16(y-2)}$

- [ ] $-\frac{16(y-2)}{25(x+4)}$

- [x] $-\frac{25(x+4)}{16(y-2)}$

Since our ellipse is centered at $(-4,2)$ and has semiaxes $4$ and $5,$ its equation is given by

$$
\frac{(x-(-4))^{2}}{{4}^{2}}+\frac{(y-2)^{2}}{{5}^{2}}=1\,⟹\,\frac{(x+4)^{2}}{16}+\frac{(y-2)^{2}}{25}=1.
$$

Now, to calculate $\frac{\text{d}y}{\text{d}x},$ we use implicit differentiation:

$$
\begin{aligned}\frac{\text{d}}{\text{d}x}(\frac{(x+4)^{2}}{16}+\frac{(y-2)^{2}}{25}) & =\frac{\text{d}}{\text{d}x}(1) \\ \frac{\text{d}}{\text{d}x}(\frac{(x+4)^{2}}{16})+\frac{\text{d}}{\text{d}x}(\frac{(y-2)^{2}}{25}) & =0 \\ \frac{2(x+4)}{16}+\frac{2(y-2)}{25}\cdot \frac{\text{d}y}{\text{d}x} & =0 \\ \frac{2(y-2)}{25}\cdot \frac{\text{d}y}{\text{d}x} & =-\frac{x+4}{8} \\ \frac{\text{d}y}{\text{d}x} & =-\frac{25(x+4)}{16(y-2)}\end{aligned}
$$

### authored hard extension — hard — authored-method

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186166866/assets/81925b90795594c1d221a2c374b6fb5474b947c38197be88c662e29fe3d2b0ef.png)

Find $\frac{\text{d}y}{\text{d}x}$ for the ellipse shown above.

- [x] $-\frac{64(x+2)}{9(y-3)}$

- [ ] $-\frac{9(x+2)}{64(y-3)}$

- [ ] $-\frac{8(x+2)}{3(y-3)}$

- [ ] $\frac{64(x+2)}{9(y-3)}$

- [ ] $-\frac{9(y-3)}{64(x+2)}$

Since our ellipse is centered at $(-2,3)$ and has semiaxes $3$ and $8,$ its equation is given by

$$
\frac{(x-(-2))^{2}}{{3}^{2}}+\frac{(y-3)^{2}}{{8}^{2}}=1\,⟹\,\frac{(x+2)^{2}}{9}+\frac{(y-3)^{2}}{64}=1.
$$

Now, to calculate $\frac{\text{d}y}{\text{d}x},$ we use implicit differentiation:

$$
\begin{aligned}\frac{\text{d}}{\text{d}x}(\frac{(x+2)^{2}}{9}+\frac{(y-3)^{2}}{64}) & =\frac{\text{d}}{\text{d}x}(1) \\ \frac{\text{d}}{\text{d}x}(\frac{(x+2)^{2}}{9})+\frac{\text{d}}{\text{d}x}(\frac{(y-3)^{2}}{64}) & =0 \\ \frac{2(x+2)}{9}+\frac{2(y-3)}{64}\cdot \frac{\text{d}y}{\text{d}x} & =0 \\ \frac{y-3}{32}\cdot \frac{\text{d}y}{\text{d}x} & =-\frac{2(x+2)}{9} \\ \frac{\text{d}y}{\text{d}x} & =-\frac{64(x+2)}{9(y-3)}\end{aligned}
$$

### authored hard extension — hard — authored-method

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186166866/assets/8a111dc75136d8619c9ebc25b4b19f18d0c51a7c33583354aa6591c40f6e22e1.png)

Find $\frac{\text{d}y}{\text{d}x}$ for the ellipse shown above.

- [ ] $-\frac{7(x+2)}{8(y-2)}$

- [ ] $\frac{49(x+2)}{64(y-2)}$

- [ ] $-\frac{64(y-2)}{49(x+2)}$

- [x] $-\frac{49(x+2)}{64(y-2)}$

- [ ] $-\frac{64(x+2)}{49(y-2)}$

Since our ellipse is centered at $(-2,2)$ and has semiaxes $8$ and $7,$ its equation is given by

$$
\frac{(x-(-2))^{2}}{{8}^{2}}+\frac{(y-2)^{2}}{{7}^{2}}=1\,⟹\,\frac{(x+2)^{2}}{64}+\frac{(y-2)^{2}}{49}=1.
$$

Now, to calculate $\frac{\text{d}y}{\text{d}x},$ we use implicit differentiation:

$$
\begin{aligned}\frac{\text{d}}{\text{d}x}(\frac{(x+2)^{2}}{64}+\frac{(y-2)^{2}}{49}) & =\frac{\text{d}}{\text{d}x}(1) \\ \frac{\text{d}}{\text{d}x}(\frac{(x+2)^{2}}{64})+\frac{\text{d}}{\text{d}x}(\frac{(y-2)^{2}}{49}) & =0 \\ \frac{2(x+2)}{64}+\frac{2(y-2)}{49}\cdot \frac{\text{d}y}{\text{d}x} & =0 \\ \frac{2(y-2)}{49}\cdot \frac{\text{d}y}{\text{d}x} & =-\frac{x+2}{32} \\ \frac{\text{d}y}{\text{d}x} & =-\frac{49(x+2)}{64(y-2)}\end{aligned}
$$

### authored hard extension — hard — authored-method

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186166866/assets/15888a108147ab62a890e352b6418df74182d2aff7c319ac9c1ceaa8ef779f9f.png)

Find $\frac{\text{d}y}{\text{d}x}$ for the ellipse shown above.

- [ ] $\frac{49(x-4)}{64(y+3)}$

- [x] $-\frac{49(x-4)}{64(y+3)}$

- [ ] $-\frac{7(x-4)}{8(y+3)}$

- [ ] $-\frac{64(y+3)}{49(x-4)}$

- [ ] $-\frac{64(x-4)}{49(y+3)}$

Since our ellipse is centered at $(4,-3)$ and has semiaxes $8$ and $7,$ its equation is given by

$$
\frac{(x-4)^{2}}{{8}^{2}}+\frac{(y-(-3))^{2}}{{7}^{2}}=1\,⟹\,\frac{(x-4)^{2}}{64}+\frac{(y+3)^{2}}{49}=1.
$$

Now, to calculate $\frac{\text{d}y}{\text{d}x},$ we use implicit differentiation:

$$
\begin{aligned}\frac{\text{d}}{\text{d}x}(\frac{(x-4)^{2}}{64}+\frac{(y+3)^{2}}{49}) & =\frac{\text{d}}{\text{d}x}(1) \\ \frac{\text{d}}{\text{d}x}(\frac{(x-4)^{2}}{64})+\frac{\text{d}}{\text{d}x}(\frac{(y+3)^{2}}{49}) & =0 \\ \frac{2(x-4)}{64}+\frac{2(y+3)}{49}\cdot \frac{\text{d}y}{\text{d}x} & =0 \\ \frac{2(y+3)}{49}\cdot \frac{\text{d}y}{\text{d}x} & =-\frac{x-4}{32} \\ \frac{\text{d}y}{\text{d}x} & =-\frac{49(x-4)}{64(y+3)}\end{aligned}
$$

### generated historical bank variant — easy — completed-q-127362

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186166866/assets/242a77da30ecd95f96e3ff04aacaf8e9984d62999605574df14dd05458480e70.png)

Find $\frac{dy}{dx}$ for the ellipse shown above.

- [ ] $-\frac{x}{4y}$

- [x] $-\frac{4x}{y}$

- [ ] $\frac{x}{2y}$

- [ ] $\frac{4x}{y}$

- [ ] $-\frac{2x}{y}$

Since our ellipse is centered at the origin and has semiaxes $1$ and $2,$ its equation is given by

$$
\frac{{x}^{2}}{{1}^{2}}+\frac{{y}^{2}}{{2}^{2}}=1\,⟹\,{x}^{2}+\frac{{y}^{2}}{4}=1.
$$

Now, to calculate $\frac{\text{d}y}{\text{d}x},$ we use implicit differentiation:

$$
\begin{aligned}\frac{\text{d}}{\text{d}x}({x}^{2}+\frac{{y}^{2}}{4}) & =\frac{\text{d}}{\text{d}x}(1) \\ \frac{\text{d}}{\text{d}x}({x}^{2})+\frac{\text{d}}{\text{d}x}(\frac{{y}^{2}}{4}) & =0 \\ 2x+\frac{2y}{4}\cdot \frac{\text{d}y}{\text{d}x} & =0 \\ \frac{y}{2}\cdot \frac{\text{d}y}{\text{d}x} & =-2x \\ \frac{\text{d}y}{\text{d}x} & =-\frac{4x}{y}\end{aligned}
$$

### generated historical bank variant — hard — completed-q-127364

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186166866/assets/18606f808b4a19e997018a6bfb324762dd6f937734fff63cda4fe6bf58aa0061.png)

Find $\frac{dy}{dx}$ for the ellipse shown above.

- [ ] $(49(x + 3))/(9(y + 3))$

- [ ] $(3(y + 3))/(7(x + 3))$

- [ ] $- (7(x + 3))/(3(y + 3))$

- [x] $- (49(x + 3))/(9(y + 3))$

- [ ] $- (9(y + 3))/(49(x + 3))$

Since our ellipse is centered at $(-3,-3)$ and has semiaxes $3$ and $7,$ its equation is given by

$$
\frac{(x-(-3))^{2}}{{3}^{2}}+\frac{(y-(-3))^{2}}{{7}^{2}}=1\,⟹\,\frac{(x+3)^{2}}{9}+\frac{(y+3)^{2}}{49}=1.
$$

Now, to calculate $\frac{\text{d}y}{\text{d}x},$ we use implicit differentiation:

$$
\begin{aligned}\frac{\text{d}}{\text{d}x}(\frac{(x+3)^{2}}{9}+\frac{(y+3)^{2}}{49}) & =\frac{\text{d}}{\text{d}x}(1) \\ \frac{\text{d}}{\text{d}x}(\frac{(x+3)^{2}}{9})+\frac{\text{d}}{\text{d}x}(\frac{(y+3)^{2}}{49}) & =0 \\ \frac{2(x+3)}{9}+\frac{2(y+3)}{49}\cdot \frac{\text{d}y}{\text{d}x} & =0 \\ \frac{2(y+3)}{49}\cdot \frac{\text{d}y}{\text{d}x} & =-\frac{2(x+3)}{9} \\ \frac{\text{d}y}{\text{d}x} & =-\frac{49(x+3)}{9(y+3)}\end{aligned}
$$

### generated historical bank variant — easy — completed-q-127511

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186166866/assets/2b40b30ba3b54e51df4a2692bb8bea607b6b0e35c74d4c00bf66b0e5c8da774f.png)

Find $\frac{\text{d}y}{\text{d}x}$ for the ellipse shown above.

- [ ] $-\frac{3x}{y}$

- [ ] $\frac{y}{9x}$

- [ ] $\frac{x}{9y}$

- [x] $-\frac{9x}{y}$

- [ ] $-\frac{y}{3x}$

Since our ellipse is centered at the origin and has semiaxes $1$ and $3,$ its equation is given by

$$
\frac{{x}^{2}}{{1}^{2}}+\frac{{y}^{2}}{{3}^{2}}=1\,⟹\,{x}^{2}+\frac{{y}^{2}}{9}=1.
$$

Now, to calculate $\frac{\text{d}y}{\text{d}x},$ we use implicit differentiation:

$$
\begin{aligned}\frac{\text{d}}{\text{d}x}({x}^{2}+\frac{{y}^{2}}{9}) & =\frac{\text{d}}{\text{d}x}(1) \\ \frac{\text{d}}{\text{d}x}({x}^{2})+\frac{\text{d}}{\text{d}x}(\frac{{y}^{2}}{9}) & =0 \\ 2x+\frac{2y}{9}\cdot \frac{\text{d}y}{\text{d}x} & =0 \\ \frac{2y}{9}\cdot \frac{\text{d}y}{\text{d}x} & =-2x \\ \frac{\text{d}y}{\text{d}x} & =-\frac{9x}{y}\end{aligned}
$$

### generated historical bank variant — easy — completed-q-127512

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186166866/assets/242a77da30ecd95f96e3ff04aacaf8e9984d62999605574df14dd05458480e70.png)

Find $\frac{\text{d}y}{\text{d}x}$ for the ellipse shown above.

- [x] $-\frac{4x}{y}$

- [ ] $-\frac{2x}{y}$

- [ ] $\frac{y}{4x}$

- [ ] $\frac{y}{2x}$

- [ ] $-\frac{4y}{x}$

Since our ellipse is centered at the origin and has semiaxes $1$ and $2,$ its equation is given by

$$
\frac{{x}^{2}}{{1}^{2}}+\frac{{y}^{2}}{{2}^{2}}=1\,⟹\,{x}^{2}+\frac{{y}^{2}}{4}=1.
$$

Now, to calculate $\frac{\text{d}y}{\text{d}x},$ we use implicit differentiation:

$$
\begin{aligned}\frac{\text{d}}{\text{d}x}({x}^{2}+\frac{{y}^{2}}{4}) & =\frac{\text{d}}{\text{d}x}(1) \\ \frac{\text{d}}{\text{d}x}({x}^{2})+\frac{\text{d}}{\text{d}x}(\frac{{y}^{2}}{4}) & =0 \\ 2x+\frac{2y}{4}\cdot \frac{\text{d}y}{\text{d}x} & =0 \\ \frac{y}{2}\cdot \frac{\text{d}y}{\text{d}x} & =-2x \\ \frac{\text{d}y}{\text{d}x} & =-\frac{4x}{y}\end{aligned}
$$

### generated historical bank variant — easy — completed-q-127513

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186166866/assets/242a77da30ecd95f96e3ff04aacaf8e9984d62999605574df14dd05458480e70.png)

Find $\frac{\text{d}y}{\text{d}x}$ for the ellipse shown above.

- [ ] $-\frac{2x}{y}$

- [ ] $\frac{4y}{x}$

- [ ] $-\frac{2y}{x}$

- [ ] $\frac{2x}{y}$

- [x] $-\frac{4x}{y}$

Since our ellipse is centered at the origin and has semiaxes $1$ and $2,$ its equation is given by

$$
\frac{{x}^{2}}{{1}^{2}}+\frac{{y}^{2}}{{2}^{2}}=1\,⟹\,{x}^{2}+\frac{{y}^{2}}{4}=1.
$$

Now, to calculate $\frac{\text{d}y}{\text{d}x},$ we use implicit differentiation:

$$
\begin{aligned}\frac{\text{d}}{\text{d}x}({x}^{2}+\frac{{y}^{2}}{4}) & =\frac{\text{d}}{\text{d}x}(1) \\ \frac{\text{d}}{\text{d}x}({x}^{2})+\frac{\text{d}}{\text{d}x}(\frac{{y}^{2}}{4}) & =0 \\ 2x+\frac{2y}{4}\cdot \frac{\text{d}y}{\text{d}x} & =0 \\ \frac{y}{2}\cdot \frac{\text{d}y}{\text{d}x} & =-2x \\ \frac{\text{d}y}{\text{d}x} & =-\frac{4x}{y}\end{aligned}
$$

### generated historical bank variant — easy — completed-q-127514

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186166866/assets/242a77da30ecd95f96e3ff04aacaf8e9984d62999605574df14dd05458480e70.png)

Find $\frac{\text{d}y}{\text{d}x}$ for the ellipse shown above.

- [ ] $-\frac{y}{2x}$

- [ ] $-\frac{y}{4x}$

- [ ] $-\frac{x}{4y}$

- [x] $-\frac{4x}{y}$

- [ ] $-\frac{2x}{y}$

Since our ellipse is centered at the origin and has semiaxes $1$ and $2,$ its equation is given by

$$
\frac{{x}^{2}}{{1}^{2}}+\frac{{y}^{2}}{{2}^{2}}=1\,⟹\,{x}^{2}+\frac{{y}^{2}}{4}=1.
$$

Now, to calculate $\frac{\text{d}y}{\text{d}x},$ we use implicit differentiation:

$$
\begin{aligned}\frac{\text{d}}{\text{d}x}({x}^{2}+\frac{{y}^{2}}{4}) & =\frac{\text{d}}{\text{d}x}(1) \\ \frac{\text{d}}{\text{d}x}({x}^{2})+\frac{\text{d}}{\text{d}x}(\frac{{y}^{2}}{4}) & =0 \\ 2x+\frac{2y}{4}\cdot \frac{\text{d}y}{\text{d}x} & =0 \\ \frac{y}{2}\cdot \frac{\text{d}y}{\text{d}x} & =-2x \\ \frac{\text{d}y}{\text{d}x} & =-\frac{4x}{y}\end{aligned}
$$

### generated historical bank variant — moderate — completed-q-127523

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186166866/assets/8a708ba1fe3d18039ccdd5f7e3e87112345c7f9ff79ecc503aff3a18ef898e52.png)

Find $\frac{\text{d}y}{\text{d}x}$ for the ellipse shown above.

- [ ] $\frac{4(x-1)}{y+3}$

- [ ] $-\frac{x+1}{4(y-3)}$

- [ ] $-\frac{y-3}{4(x+1)}$

- [ ] $\frac{4(y+3)}{x-1}$

- [x] $-\frac{4(x+1)}{y-3}$

Since our ellipse is centered at $(-1,3)$ and has semiaxes $1$ and $2,$ its equation is given by

$$
\frac{(x-(-1))^{2}}{{1}^{2}}+\frac{(y-3)^{2}}{{2}^{2}}=1\,⟹\,(x+1)^{2}+\frac{(y-3)^{2}}{4}=1.
$$

Now, to calculate $\frac{\text{d}y}{\text{d}x},$ we use implicit differentiation:

$$
\begin{aligned}\frac{\text{d}}{\text{d}x}((x+1)^{2}+\frac{(y-3)^{2}}{4}) & =\frac{\text{d}}{\text{d}x}(1) \\ \frac{\text{d}}{\text{d}x}((x+1)^{2})+\frac{\text{d}}{\text{d}x}(\frac{(y-3)^{2}}{4}) & =0 \\ 2(x+1)+\frac{2(y-3)}{4}\cdot \frac{\text{d}y}{\text{d}x} & =0 \\ \frac{y-3}{2}\cdot \frac{\text{d}y}{\text{d}x} & =-2(x+1) \\ \frac{\text{d}y}{\text{d}x} & =-\frac{4(x+1)}{y-3}\end{aligned}
$$

### generated historical bank variant — moderate — completed-q-127525

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186166866/assets/8a708ba1fe3d18039ccdd5f7e3e87112345c7f9ff79ecc503aff3a18ef898e52.png)

Find $\frac{\text{d}y}{\text{d}x}$ for the ellipse shown above.

- [x] $-\frac{4(x+1)}{y-3}$

- [ ] $\frac{x+1}{4(y-3)}$

- [ ] $\frac{2(x+1)}{y-3}$

- [ ] $\frac{2(y-3)}{x+1}$

- [ ] $-\frac{y-3}{4(x+1)}$

Since our ellipse is centered at $(-1,3)$ and has semiaxes $1$ and $2,$ its equation is given by

$$
\frac{(x-(-1))^{2}}{{1}^{2}}+\frac{(y-3)^{2}}{{2}^{2}}=1\,⟹\,(x+1)^{2}+\frac{(y-3)^{2}}{4}=1.
$$

Now, to calculate $\frac{\text{d}y}{\text{d}x},$ we use implicit differentiation:

$$
\begin{aligned}\frac{\text{d}}{\text{d}x}((x+1)^{2}+\frac{(y-3)^{2}}{4}) & =\frac{\text{d}}{\text{d}x}(1) \\ \frac{\text{d}}{\text{d}x}((x+1)^{2})+\frac{\text{d}}{\text{d}x}(\frac{(y-3)^{2}}{4}) & =0 \\ 2(x+1)+\frac{2(y-3)}{4}\cdot \frac{\text{d}y}{\text{d}x} & =0 \\ \frac{y-3}{2}\cdot \frac{\text{d}y}{\text{d}x} & =-2(x+1) \\ \frac{\text{d}y}{\text{d}x} & =-\frac{4(x+1)}{y-3}\end{aligned}
$$

### generated historical bank variant — moderate — completed-q-127526

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186166866/assets/8a708ba1fe3d18039ccdd5f7e3e87112345c7f9ff79ecc503aff3a18ef898e52.png)

Find $\frac{\text{d}y}{\text{d}x}$ for the ellipse shown above.

- [ ] $\frac{x}{4(y+1)}$

- [x] $-\frac{4(x+1)}{y-3}$

- [ ] $-\frac{4(y+1)}{x}$

- [ ] $\frac{2(x+1)}{y-3}$

- [ ] $-\frac{y-3}{2(x+1)}$

Since our ellipse is centered at $(-1,3)$ and has semiaxes $1$ and $2,$ its equation is given by

$$
\frac{(x-(-1))^{2}}{{1}^{2}}+\frac{(y-3)^{2}}{{2}^{2}}=1\,⟹\,(x+1)^{2}+\frac{(y-3)^{2}}{4}=1.
$$

Now, to calculate $\frac{\text{d}y}{\text{d}x},$ we use implicit differentiation:

$$
\begin{aligned}\frac{\text{d}}{\text{d}x}((x+1)^{2}+\frac{(y-3)^{2}}{4}) & =\frac{\text{d}}{\text{d}x}(1) \\ \frac{\text{d}}{\text{d}x}((x+1)^{2})+\frac{\text{d}}{\text{d}x}(\frac{(y-3)^{2}}{4}) & =0 \\ 2(x+1)+\frac{2(y-3)}{4}\cdot \frac{\text{d}y}{\text{d}x} & =0 \\ \frac{y-3}{2}\cdot \frac{\text{d}y}{\text{d}x} & =-2(x+1) \\ \frac{\text{d}y}{\text{d}x} & =-\frac{4(x+1)}{y-3}\end{aligned}
$$
