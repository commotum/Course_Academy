# Source and generated review

Worker review; parent independent QA remains pending. raw-source/raw-variant profiles are ineligible evidence records preserving the source attribute omissions; source/empirical-variant labels below denote normalized completed reconstructions, not raw parity. All original prompt plots and five solution plots were inspected directly. Each normal completed instance has one fixed source-shaped solution; raw q122484 retains its absent solution attribute. Zero source calculator flags were present; requirement remains unknown.


## Original q-122481

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186162082/q-122481-source-0.png)

Calculate ${\int }_{C}\,\text{d}s,$ where $C$ is a path that traverses a semicircle of radius $2$ once in the counterclockwise direction, as shown above.

The path $C$ is made up of two parts, as shown below:

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186162082/q-122481-source-1.png)

Now, we make use of the following facts:

- If $C={C}_{1}\cup {C}_{2}$ is a piecewise-smooth curve, we have

$$
{\int }_{C}f(x,y)\,\text{d}s={\int }_{{C}_{1}}f(x,y)\,\text{d}s+{\int }_{{C}_{2}}f(x,y)\,\text{d}s.
$$

- The line integral of unity with respect to arc length over $C$ is equal to the arc length $L$ of $C,$ i.e.,

$$
{\int }_{C}\,\text{d}s=L.
$$

The path ${C}_{1}$ is a semi-circle of radius $r=2.$ Therefore, we have

$$
{\int }_{{C}_{1}}\,\text{d}s=\pi r=2\pi .
$$

The path ${C}_{2}$ is a line segment of length $4.$ Therefore, we have

$$
{\int }_{{C}_{2}}\,\text{d}s=4.
$$

Therefore,

$$
{\int }_{C}\,\text{d}s=2\pi +4=2(\pi +2).
$$

Original five options:

- $2(\pi +1)$
- $4(\pi +2)$
- $2(\pi +2)$
- $2(2\pi +1)$
- $4(\pi +1)$

Observed key: $2(\pi +2)$.


### Generated raw-source/q-122481

Parameters/profile: `{"r": "2"}`, `raw-q-122481`.

![](images/55/558dbbc424725ca0d9bad628968489cc2e32d67136102290666ff055a634bc16.png)

Calculate ${\int }_{C}\,\text{d}s,$ where $C$ is a path that traverses a semicircle of radius $2$ once in the counterclockwise direction, as shown above.

- $2(\pi +1)$
- $4(\pi +2)$
- $2(\pi +2)$
- $2(2\pi +1)$
- $4(\pi +1)$

The path $C$ is made up of two parts, as shown below:

![](images/82/82fedadbb33b1747832bac25d9cda8e0b6b18b0fab411a870e90bc09ce47226e.png)

Now, we make use of the following facts:

- If $C={C}_{1}\cup {C}_{2}$ is a piecewise-smooth curve, we have

$$
{\int }_{C}f(x,y)\,\text{d}s={\int }_{{C}_{1}}f(x,y)\,\text{d}s+{\int }_{{C}_{2}}f(x,y)\,\text{d}s.
$$

- The line integral of unity with respect to arc length over $C$ is equal to the arc length $L$ of $C,$ i.e.,

$$
{\int }_{C}\,\text{d}s=L.
$$

The path ${C}_{1}$ is a semi-circle of radius $r=2.$ Therefore, we have

$$
{\int }_{{C}_{1}}\,\text{d}s=\pi r=2\pi .
$$

The path ${C}_{2}$ is a line segment of length $4.$ Therefore, we have

$$
{\int }_{{C}_{2}}\,\text{d}s=4.
$$

Therefore,

$$
{\int }_{C}\,\text{d}s=2\pi +4=2(\pi +2).
$$


### Generated raw-variant/q-122481

Parameters/profile: `{"r": "4"}`, `raw-q-122481`.

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186162082/assets/4e208c0c7217db568ee18d972de9fc09e91726f304709b7c7a324c08c9d0ff51-prompt.png)

Calculate ${\int }_{C}\,\text{d}s,$ where $C$ is a path that traverses a semicircle of radius $4$ once in the counterclockwise direction, as shown above.

- $4(\pi +1)$
- $8(\pi +2)$
- $4(\pi +2)$
- $4(2\pi +1)$
- $8(\pi +1)$

The path $C$ is made up of two parts, as shown below:

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186162082/assets/4e208c0c7217db568ee18d972de9fc09e91726f304709b7c7a324c08c9d0ff51-solution.png)

Now, we make use of the following facts:

- If $C={C}_{1}\cup {C}_{2}$ is a piecewise-smooth curve, we have

$$
{\int }_{C}f(x,y)\,\text{d}s={\int }_{{C}_{1}}f(x,y)\,\text{d}s+{\int }_{{C}_{2}}f(x,y)\,\text{d}s.
$$

- The line integral of unity with respect to arc length over $C$ is equal to the arc length $L$ of $C,$ i.e.,

$$
{\int }_{C}\,\text{d}s=L.
$$

The path ${C}_{1}$ is a semi-circle of radius $r=4.$ Therefore, we have

$$
{\int }_{{C}_{1}}\,\text{d}s=\pi r=4\pi .
$$

The path ${C}_{2}$ is a line segment of length $8.$ Therefore, we have

$$
{\int }_{{C}_{2}}\,\text{d}s=8.
$$

Therefore,

$$
{\int }_{C}\,\text{d}s=4\pi +8=4(\pi +2).
$$


### Generated source/q-122481

Parameters/profile: `{"r": "2"}`, `q-122481`.

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186162082/assets/4586cc752be18a32ce1f01c6ac1e96feb1ee1910087af76624de44ff335f7c6c-prompt.png)

Calculate ${\int }_{C}\,\text{d}s,$ where $C$ is a path that traverses a semicircle of radius $2$ once in the counterclockwise direction, as shown above.

- $4 + 2 \pi$
- $8 + 4 \pi$
- $2 + 2 \pi$
- $4 + 4 \pi$
- $2 + 4 \pi$

The path $C$ is made up of two parts, as shown below:

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186162082/assets/4586cc752be18a32ce1f01c6ac1e96feb1ee1910087af76624de44ff335f7c6c-solution.png)

Now, we make use of the following facts:

- If $C={C}_{1}\cup {C}_{2}$ is a piecewise-smooth curve, we have

$$
{\int }_{C}f(x,y)\,\text{d}s={\int }_{{C}_{1}}f(x,y)\,\text{d}s+{\int }_{{C}_{2}}f(x,y)\,\text{d}s.
$$

- The line integral of unity with respect to arc length over $C$ is equal to the arc length $L$ of $C,$ i.e.,

$$
{\int }_{C}\,\text{d}s=L.
$$

The path ${C}_{1}$ is a semi-circle of radius $r=2.$ Therefore, we have

$$
{\int }_{{C}_{1}}\,\text{d}s=\pi r=2 \pi .
$$

The path ${C}_{2}$ is a line segment of length $4.$ Therefore, we have

$$
{\int }_{{C}_{2}}\,\text{d}s=4.
$$

Therefore,

$$
{\int }_{C}\,\text{d}s=2 \pi+4=2(\pi+2).
$$


### Generated empirical-variant/q-122481

Parameters/profile: `{"r": "4"}`, `q-122481`.

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186162082/assets/4e208c0c7217db568ee18d972de9fc09e91726f304709b7c7a324c08c9d0ff51-prompt.png)

Calculate ${\int }_{C}\,\text{d}s,$ where $C$ is a path that traverses a semicircle of radius $4$ once in the counterclockwise direction, as shown above.

- $8 + 4 \pi$
- $16 + 8 \pi$
- $8 + 8 \pi$
- $4 + 4 \pi$
- $4 + 8 \pi$

The path $C$ is made up of two parts, as shown below:

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186162082/assets/4e208c0c7217db568ee18d972de9fc09e91726f304709b7c7a324c08c9d0ff51-solution.png)

Now, we make use of the following facts:

- If $C={C}_{1}\cup {C}_{2}$ is a piecewise-smooth curve, we have

$$
{\int }_{C}f(x,y)\,\text{d}s={\int }_{{C}_{1}}f(x,y)\,\text{d}s+{\int }_{{C}_{2}}f(x,y)\,\text{d}s.
$$

- The line integral of unity with respect to arc length over $C$ is equal to the arc length $L$ of $C,$ i.e.,

$$
{\int }_{C}\,\text{d}s=L.
$$

The path ${C}_{1}$ is a semi-circle of radius $r=4.$ Therefore, we have

$$
{\int }_{{C}_{1}}\,\text{d}s=\pi r=4 \pi .
$$

The path ${C}_{2}$ is a line segment of length $8.$ Therefore, we have

$$
{\int }_{{C}_{2}}\,\text{d}s=8.
$$

Therefore,

$$
{\int }_{C}\,\text{d}s=4 \pi+8=4(\pi+2).
$$


## Original q-122484

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186162082/q-122484-source-0.png)

Calculate $\displaystyle \int_{C}ds$, where $C$ is a path that traverses a circular segment of radius $2$ once in the counterclockwise direction, as shown above.

[Source solution absent.]

Original five options:

- $\frac{π}{2} + \sqrt{3}$
- $π + 2\sqrt{2}$
- $π + \sqrt{2}$
- $\frac{π}{2} + \sqrt{2}$
- $2π + 3\sqrt{2}$

Observed key and rating absent; independently inferred value π+2√2 and authored moderate level are documented separately.


### Generated raw-source/q-122484

Parameters/profile: `{"r": "2"}`, `raw-q-122484`.

![](images/52/5277642b981910a5da1dd00a1b9aa4db28c7db7fcacf33faf209eea3ec1e93ab.png)

Calculate $\displaystyle \int_{C}ds$, where $C$ is a path that traverses a circular segment of radius $2$ once in the counterclockwise direction, as shown above.

- $\frac{π}{2} + \sqrt{3}$
- $π + 2\sqrt{2}$
- $π + \sqrt{2}$
- $\frac{π}{2} + \sqrt{2}$
- $2π + 3\sqrt{2}$

[Raw source solution attribute absent; no completion inserted.]


### Generated raw-variant/q-122484

Parameters/profile: `{"r": "4"}`, `raw-q-122484`.

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186162082/assets/f48bd2c89e4ba70e6cf2e8283112b8ec37171fb7ae13818be55c3cddbba54234-prompt.png)

Calculate $\displaystyle \int_{C}ds$, where $C$ is a path that traverses a circular segment of radius $4$ once in the counterclockwise direction, as shown above.

- $π + 2\sqrt{3}$
- $2π + 4\sqrt{2}$
- $2π + 2\sqrt{2}$
- $π + 2\sqrt{2}$
- $4π + 6\sqrt{2}$

[Raw source solution attribute absent; no completion inserted.]


### Generated source/q-122484

Parameters/profile: `{"r": "2"}`, `q-122484`.

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186162082/assets/635fe29113cdd73fded034d9257ebb61217d0a6f3673c63c9a7d95fe7d4c8c21-prompt.png)

Calculate $\displaystyle \int_{C}ds$, where $C$ is a path that traverses a circular segment of radius $2$ once in the counterclockwise direction, as shown above.

- $\sqrt{2} + \pi$
- $2 \sqrt{2} + \pi$
- $\frac{\pi}{2} + \sqrt{3}$
- $3 \sqrt{2} + 2 \pi$
- $\sqrt{2} + \frac{\pi}{2}$

The path $C$ is made up of two parts, as shown below:

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186162082/assets/635fe29113cdd73fded034d9257ebb61217d0a6f3673c63c9a7d95fe7d4c8c21-solution.png)

Now, we make use of the following facts:

- If $C={C}_{1}\cup {C}_{2}$ is a piecewise-smooth curve, we have

$$
{\int }_{C}f(x,y)\,\text{d}s={\int }_{{C}_{1}}f(x,y)\,\text{d}s+{\int }_{{C}_{2}}f(x,y)\,\text{d}s.
$$

- The line integral of unity with respect to arc length over $C$ is equal to the arc length $L$ of $C,$ i.e.,

$$
{\int }_{C}\,\text{d}s=L.
$$

The path ${C}_{1}$ is a quarter of a circle of radius $r=2.$ Therefore, we have

$$
{\int }_{{C}_{1}}\,\text{d}s=\frac{1}{4}(2\pi r)=\pi .
$$

The path ${C}_{2}$ is the hypotenuse of a right triangle where both legs have a length of $2.$ Therefore, we have

$$
{\int }_{{C}_{2}}\,\text{d}s=\sqrt{{2}^{2}+{2}^{2}}=2 \sqrt{2}.
$$

Therefore,

$$
{\int }_{C}\,\text{d}s=\pi+2 \sqrt{2}.
$$


### Generated empirical-variant/q-122484

Parameters/profile: `{"r": "4"}`, `q-122484`.

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186162082/assets/f48bd2c89e4ba70e6cf2e8283112b8ec37171fb7ae13818be55c3cddbba54234-prompt.png)

Calculate $\displaystyle \int_{C}ds$, where $C$ is a path that traverses a circular segment of radius $4$ once in the counterclockwise direction, as shown above.

- $2 \sqrt{2} + 2 \pi$
- $4 \sqrt{2} + 2 \pi$
- $6 \sqrt{2} + 4 \pi$
- $\pi + 2 \sqrt{3}$
- $2 \sqrt{2} + \pi$

The path $C$ is made up of two parts, as shown below:

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186162082/assets/f48bd2c89e4ba70e6cf2e8283112b8ec37171fb7ae13818be55c3cddbba54234-solution.png)

Now, we make use of the following facts:

- If $C={C}_{1}\cup {C}_{2}$ is a piecewise-smooth curve, we have

$$
{\int }_{C}f(x,y)\,\text{d}s={\int }_{{C}_{1}}f(x,y)\,\text{d}s+{\int }_{{C}_{2}}f(x,y)\,\text{d}s.
$$

- The line integral of unity with respect to arc length over $C$ is equal to the arc length $L$ of $C,$ i.e.,

$$
{\int }_{C}\,\text{d}s=L.
$$

The path ${C}_{1}$ is a quarter of a circle of radius $r=4.$ Therefore, we have

$$
{\int }_{{C}_{1}}\,\text{d}s=\frac{1}{4}(2\pi r)=2 \pi .
$$

The path ${C}_{2}$ is the hypotenuse of a right triangle where both legs have a length of $4.$ Therefore, we have

$$
{\int }_{{C}_{2}}\,\text{d}s=\sqrt{{4}^{2}+{4}^{2}}=4 \sqrt{2}.
$$

Therefore,

$$
{\int }_{C}\,\text{d}s=2 \pi+4 \sqrt{2}.
$$


## Original q-122828

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186162082/q-122828-source-0.png)

Calculate ${\int }_{C}\,\text{d}s,$ where $C$ is the path shown above.

The path $C$ is made up of three parts, as shown below:

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186162082/q-122828-source-1.png)

Now, we make use of the following facts:

- If $C={C}_{1}\cup {C}_{2}\cup {C}_{3}$ is a piecewise-smooth curve, we have

$$
{\int }_{C}f(x,y)\,\text{d}s={\int }_{{C}_{1}}f(x,y)\,\text{d}s+{\int }_{{C}_{2}}f(x,y)\,\text{d}s+{\int }_{{C}_{3}}f(x,y)\,\text{d}s.
$$

- The line integral of unity with respect to arc length over $C$ is equal to the arc length $L$ of $C,$ i.e.,

$$
{\int }_{C}\,\text{d}s=L.
$$

The paths ${C}_{1}$ and ${C}_{3}$ are line segments of length $3.$ Therefore, we have

$$
{\int }_{{C}_{1}}\,\text{d}s={\int }_{{C}_{3}}\,\text{d}s=3.
$$

The path ${C}_{2}$ is the hypotenuse of a right triangle whose legs have lengths $3$ and $4.$ Therefore, we have

$$
{\int }_{{C}_{2}}\,\text{d}s=\sqrt{{3}^{2}+{4}^{2}}=5.
$$

Therefore,

$$
{\int }_{C}\,\text{d}s=3+5+3=11.
$$

Original five options:

- $9$
- $12$
- $11$
- $8$
- $10$

Observed key: $11$.


### Generated raw-source/q-122828

Parameters/profile: `{"a": "3", "b": "4"}`, `raw-q-122828`.

![](images/39/39a7cb0b31cb5d906803063597ae968be8fba90f048a4d9745225de7c3f8d6db.png)

Calculate ${\int }_{C}\,\text{d}s,$ where $C$ is the path shown above.

- $9$
- $12$
- $11$
- $8$
- $10$

The path $C$ is made up of three parts, as shown below:

![](images/05/058c7b33112329df321e61660df4f2d388f42ca40c0aae5b73a089a0251726e2.png)

Now, we make use of the following facts:

- If $C={C}_{1}\cup {C}_{2}\cup {C}_{3}$ is a piecewise-smooth curve, we have

$$
{\int }_{C}f(x,y)\,\text{d}s={\int }_{{C}_{1}}f(x,y)\,\text{d}s+{\int }_{{C}_{2}}f(x,y)\,\text{d}s+{\int }_{{C}_{3}}f(x,y)\,\text{d}s.
$$

- The line integral of unity with respect to arc length over $C$ is equal to the arc length $L$ of $C,$ i.e.,

$$
{\int }_{C}\,\text{d}s=L.
$$

The paths ${C}_{1}$ and ${C}_{3}$ are line segments of length $3.$ Therefore, we have

$$
{\int }_{{C}_{1}}\,\text{d}s={\int }_{{C}_{3}}\,\text{d}s=3.
$$

The path ${C}_{2}$ is the hypotenuse of a right triangle whose legs have lengths $3$ and $4.$ Therefore, we have

$$
{\int }_{{C}_{2}}\,\text{d}s=\sqrt{{3}^{2}+{4}^{2}}=5.
$$

Therefore,

$$
{\int }_{C}\,\text{d}s=3+5+3=11.
$$


### Generated raw-variant/q-122828

Parameters/profile: `{"a": "6", "b": "8"}`, `raw-q-122828`.

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186162082/assets/10fc32d9eca1cec76cd5ddadce45a9c590c30a7218a56c7b18fb33509947db8f-prompt.png)

Calculate ${\int }_{C}\,\text{d}s,$ where $C$ is the path shown above.

- $18$
- $24$
- $22$
- $16$
- $20$

The path $C$ is made up of three parts, as shown below:

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186162082/assets/10fc32d9eca1cec76cd5ddadce45a9c590c30a7218a56c7b18fb33509947db8f-solution.png)

Now, we make use of the following facts:

- If $C={C}_{1}\cup {C}_{2}\cup {C}_{3}$ is a piecewise-smooth curve, we have

$$
{\int }_{C}f(x,y)\,\text{d}s={\int }_{{C}_{1}}f(x,y)\,\text{d}s+{\int }_{{C}_{2}}f(x,y)\,\text{d}s+{\int }_{{C}_{3}}f(x,y)\,\text{d}s.
$$

- The line integral of unity with respect to arc length over $C$ is equal to the arc length $L$ of $C,$ i.e.,

$$
{\int }_{C}\,\text{d}s=L.
$$

The paths ${C}_{1}$ and ${C}_{3}$ are line segments of length $6.$ Therefore, we have

$$
{\int }_{{C}_{1}}\,\text{d}s={\int }_{{C}_{3}}\,\text{d}s=6.
$$

The path ${C}_{2}$ is the hypotenuse of a right triangle whose legs have lengths $6$ and $8.$ Therefore, we have

$$
{\int }_{{C}_{2}}\,\text{d}s=\sqrt{{6}^{2}+{8}^{2}}=10.
$$

Therefore,

$$
{\int }_{C}\,\text{d}s=6+10+6=22.
$$


### Generated source/q-122828

Parameters/profile: `{"a": "3", "b": "4"}`, `q-122828`.

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186162082/assets/2bcd266ede4545d53e0e43415f7e8d99d1ae6184f8dd962c8211498bfb632e0c-prompt.png)

Calculate ${\int }_{C}\,\text{d}s,$ where $C$ is the path shown above.

- $11$
- $12$
- $9$
- $10$
- $8$

The path $C$ is made up of three parts, as shown below:

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186162082/assets/2bcd266ede4545d53e0e43415f7e8d99d1ae6184f8dd962c8211498bfb632e0c-solution.png)

Now, we make use of the following facts:

- If $C={C}_{1}\cup {C}_{2}\cup {C}_{3}$ is a piecewise-smooth curve, we have

$$
{\int }_{C}f(x,y)\,\text{d}s={\int }_{{C}_{1}}f(x,y)\,\text{d}s+{\int }_{{C}_{2}}f(x,y)\,\text{d}s+{\int }_{{C}_{3}}f(x,y)\,\text{d}s.
$$

- The line integral of unity with respect to arc length over $C$ is equal to the arc length $L$ of $C,$ i.e.,

$$
{\int }_{C}\,\text{d}s=L.
$$

The paths ${C}_{1}$ and ${C}_{3}$ are line segments of length $3.$ Therefore, we have

$$
{\int }_{{C}_{1}}\,\text{d}s={\int }_{{C}_{3}}\,\text{d}s=3.
$$

The path ${C}_{2}$ is the hypotenuse of a right triangle whose legs have lengths $3$ and $4.$ Therefore, we have

$$
{\int }_{{C}_{2}}\,\text{d}s=\sqrt{{3}^{2}+{4}^{2}}=5.
$$

Therefore,

$$
{\int }_{C}\,\text{d}s=3+5+3=11.
$$


### Generated empirical-variant/q-122828

Parameters/profile: `{"a": "6", "b": "8"}`, `q-122828`.

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186162082/assets/10fc32d9eca1cec76cd5ddadce45a9c590c30a7218a56c7b18fb33509947db8f-prompt.png)

Calculate ${\int }_{C}\,\text{d}s,$ where $C$ is the path shown above.

- $22$
- $24$
- $20$
- $18$
- $16$

The path $C$ is made up of three parts, as shown below:

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186162082/assets/10fc32d9eca1cec76cd5ddadce45a9c590c30a7218a56c7b18fb33509947db8f-solution.png)

Now, we make use of the following facts:

- If $C={C}_{1}\cup {C}_{2}\cup {C}_{3}$ is a piecewise-smooth curve, we have

$$
{\int }_{C}f(x,y)\,\text{d}s={\int }_{{C}_{1}}f(x,y)\,\text{d}s+{\int }_{{C}_{2}}f(x,y)\,\text{d}s+{\int }_{{C}_{3}}f(x,y)\,\text{d}s.
$$

- The line integral of unity with respect to arc length over $C$ is equal to the arc length $L$ of $C,$ i.e.,

$$
{\int }_{C}\,\text{d}s=L.
$$

The paths ${C}_{1}$ and ${C}_{3}$ are line segments of length $6.$ Therefore, we have

$$
{\int }_{{C}_{1}}\,\text{d}s={\int }_{{C}_{3}}\,\text{d}s=6.
$$

The path ${C}_{2}$ is the hypotenuse of a right triangle whose legs have lengths $6$ and $8.$ Therefore, we have

$$
{\int }_{{C}_{2}}\,\text{d}s=\sqrt{{6}^{2}+{8}^{2}}=10.
$$

Therefore,

$$
{\int }_{C}\,\text{d}s=6+10+6=22.
$$


## Original q-122843

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186162082/q-122843-source-0.png)

Calculate ${\int }_{C}\,\text{d}s,$ where $C$ is the path shown above.

The path $C$ is made up of two parts, as shown below:

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186162082/q-122843-source-1.png)

Now, we make use of the following facts:

- If $C={C}_{1}\cup {C}_{2}$ is a piecewise-smooth curve, we have

$$
{\int }_{C}f(x,y)\,\text{d}s={\int }_{{C}_{1}}f(x,y)\,\text{d}s+{\int }_{{C}_{2}}f(x,y)\,\text{d}s.
$$

- The line integral of unity with respect to arc length over $C$ is equal to the arc length $L$ of $C,$ i.e.,

$$
{\int }_{C}\,\text{d}s=L.
$$

The path ${C}_{1}$ is three-quarters of a circle of radius $r=2.$ Therefore, we have

$$
{\int }_{{C}_{1}}\,\text{d}s=\frac{3}{4}(2\pi r)=3\pi .
$$

The path ${C}_{2}$ is a line segment of length $2.$ Therefore, we have

$$
{\int }_{{C}_{2}}\,\text{d}s=2.
$$

Therefore,

$$
{\int }_{C}\,\text{d}s=3\pi +2.
$$

Original five options:

- $4\pi +1$
- $3\pi +2$
- $3\pi +4$
- $2\pi +3$
- $\pi +2$

Observed key: $3\pi +2$.


### Generated raw-source/q-122843

Parameters/profile: `{"r": "2"}`, `raw-q-122843`.

![](images/d7/d7844777c0bb540ba337756f45c4d71a8a8e9f9c84372e01542892801efecce3.png)

Calculate ${\int }_{C}\,\text{d}s,$ where $C$ is the path shown above.

- $4\pi +1$
- $3\pi +2$
- $3\pi +4$
- $2\pi +3$
- $\pi +2$

The path $C$ is made up of two parts, as shown below:

![](images/98/98f444851e2df505d4242d1f8e4be0d76f78babd5d9633d9ab0ec84c245fe364.png)

Now, we make use of the following facts:

- If $C={C}_{1}\cup {C}_{2}$ is a piecewise-smooth curve, we have

$$
{\int }_{C}f(x,y)\,\text{d}s={\int }_{{C}_{1}}f(x,y)\,\text{d}s+{\int }_{{C}_{2}}f(x,y)\,\text{d}s.
$$

- The line integral of unity with respect to arc length over $C$ is equal to the arc length $L$ of $C,$ i.e.,

$$
{\int }_{C}\,\text{d}s=L.
$$

The path ${C}_{1}$ is three-quarters of a circle of radius $r=2.$ Therefore, we have

$$
{\int }_{{C}_{1}}\,\text{d}s=\frac{3}{4}(2\pi r)=3\pi .
$$

The path ${C}_{2}$ is a line segment of length $2.$ Therefore, we have

$$
{\int }_{{C}_{2}}\,\text{d}s=2.
$$

Therefore,

$$
{\int }_{C}\,\text{d}s=3\pi +2.
$$


### Generated raw-variant/q-122843

Parameters/profile: `{"r": "4"}`, `raw-q-122843`.

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186162082/assets/a1bf47c8c0377cd18e10ae7d2c6a4619be6da121a35f39d0a24f883c547885b2-prompt.png)

Calculate ${\int }_{C}\,\text{d}s,$ where $C$ is the path shown above.

- $8\pi +2$
- $6\pi +4$
- $6\pi +8$
- $4\pi +6$
- $2\pi +4$

The path $C$ is made up of two parts, as shown below:

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186162082/assets/a1bf47c8c0377cd18e10ae7d2c6a4619be6da121a35f39d0a24f883c547885b2-solution.png)

Now, we make use of the following facts:

- If $C={C}_{1}\cup {C}_{2}$ is a piecewise-smooth curve, we have

$$
{\int }_{C}f(x,y)\,\text{d}s={\int }_{{C}_{1}}f(x,y)\,\text{d}s+{\int }_{{C}_{2}}f(x,y)\,\text{d}s.
$$

- The line integral of unity with respect to arc length over $C$ is equal to the arc length $L$ of $C,$ i.e.,

$$
{\int }_{C}\,\text{d}s=L.
$$

The path ${C}_{1}$ is three-quarters of a circle of radius $r=4.$ Therefore, we have

$$
{\int }_{{C}_{1}}\,\text{d}s=\frac{3}{4}(2\pi r)=6\pi .
$$

The path ${C}_{2}$ is a line segment of length $4.$ Therefore, we have

$$
{\int }_{{C}_{2}}\,\text{d}s=4.
$$

Therefore,

$$
{\int }_{C}\,\text{d}s=6\pi +4.
$$


### Generated source/q-122843

Parameters/profile: `{"r": "2"}`, `q-122843`.

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186162082/assets/438f248030e89f7b190716f2ee8f7235a12064734e57a59b1c464cb330225dda-prompt.png)

Calculate ${\int }_{C}\,\text{d}s,$ where $C$ is the path shown above.

- $4 + 3 \pi$
- $2 + 3 \pi$
- $1 + 4 \pi$
- $2 + \pi$
- $3 + 2 \pi$

The path $C$ is made up of two parts, as shown below:

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186162082/assets/438f248030e89f7b190716f2ee8f7235a12064734e57a59b1c464cb330225dda-solution.png)

Now, we make use of the following facts:

- If $C={C}_{1}\cup {C}_{2}$ is a piecewise-smooth curve, we have

$$
{\int }_{C}f(x,y)\,\text{d}s={\int }_{{C}_{1}}f(x,y)\,\text{d}s+{\int }_{{C}_{2}}f(x,y)\,\text{d}s.
$$

- The line integral of unity with respect to arc length over $C$ is equal to the arc length $L$ of $C,$ i.e.,

$$
{\int }_{C}\,\text{d}s=L.
$$

The path ${C}_{1}$ is three-quarters of a circle of radius $r=2.$ Therefore, we have

$$
{\int }_{{C}_{1}}\,\text{d}s=\frac{3}{4}(2\pi r)=3 \pi .
$$

The path ${C}_{2}$ is a line segment of length $2.$ Therefore, we have

$$
{\int }_{{C}_{2}}\,\text{d}s=2.
$$

Therefore,

$$
{\int }_{C}\,\text{d}s=3 \pi+2.
$$


### Generated empirical-variant/q-122843

Parameters/profile: `{"r": "4"}`, `q-122843`.

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186162082/assets/a1bf47c8c0377cd18e10ae7d2c6a4619be6da121a35f39d0a24f883c547885b2-prompt.png)

Calculate ${\int }_{C}\,\text{d}s,$ where $C$ is the path shown above.

- $8 + 6 \pi$
- $4 + 6 \pi$
- $4 + 2 \pi$
- $2 + 8 \pi$
- $6 + 4 \pi$

The path $C$ is made up of two parts, as shown below:

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186162082/assets/a1bf47c8c0377cd18e10ae7d2c6a4619be6da121a35f39d0a24f883c547885b2-solution.png)

Now, we make use of the following facts:

- If $C={C}_{1}\cup {C}_{2}$ is a piecewise-smooth curve, we have

$$
{\int }_{C}f(x,y)\,\text{d}s={\int }_{{C}_{1}}f(x,y)\,\text{d}s+{\int }_{{C}_{2}}f(x,y)\,\text{d}s.
$$

- The line integral of unity with respect to arc length over $C$ is equal to the arc length $L$ of $C,$ i.e.,

$$
{\int }_{C}\,\text{d}s=L.
$$

The path ${C}_{1}$ is three-quarters of a circle of radius $r=4.$ Therefore, we have

$$
{\int }_{{C}_{1}}\,\text{d}s=\frac{3}{4}(2\pi r)=6 \pi .
$$

The path ${C}_{2}$ is a line segment of length $4.$ Therefore, we have

$$
{\int }_{{C}_{2}}\,\text{d}s=4.
$$

Therefore,

$$
{\int }_{C}\,\text{d}s=6 \pi+4.
$$


## Original q-122845

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186162082/q-122845-source-0.png)

Calculate ${\int }_{C}\,\text{d}s,$ where $C$ is the path shown above.

The path $C$ is made up of two parts, as shown below:

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186162082/q-122845-source-1.png)

Now, we make use of the following facts:

- If $C={C}_{1}\cup {C}_{2}$ is a piecewise-smooth curve, we have

$$
{\int }_{C}f(x,y)\,\text{d}s={\int }_{{C}_{1}}f(x,y)\,\text{d}s+{\int }_{{C}_{2}}f(x,y)\,\text{d}s.
$$

- The line integral of unity with respect to arc length over $C$ is equal to the arc length $L$ of $C,$ i.e.,

$$
{\int }_{C}\,\text{d}s=L.
$$

The path ${C}_{1}$ is the hypotenuse of a right triangle whose legs have lengths $3$ and $4.$ Therefore, we have

$$
{\int }_{{C}_{1}}\,\text{d}s=\sqrt{{3}^{2}+{4}^{2}}=5.
$$

The path ${C}_{2}$ is the hypotenuse of a right triangle whose legs have lengths $2$ and $4.$ Therefore, we have

$$
{\int }_{{C}_{2}}\,\text{d}s=\sqrt{{2}^{2}+{4}^{2}}=2\sqrt{5}.
$$

Therefore,

$$
{\int }_{C}\,\text{d}s=5+2\sqrt{5}.
$$

Original five options:

- $9$
- $2(2+\sqrt{5})$
- $2(3+\sqrt{5})$
- $5+2\sqrt{5}$
- $10$

Observed key: $5+2\sqrt{5}$.


### Generated raw-source/q-122845

Parameters/profile: `{"a": "3", "b": "2", "h": "4"}`, `raw-q-122845`.

![](images/68/68b3f78c29c9d7776efc2a78672ae53fe2e806d7ca6c3d663de8a16c03342132.png)

Calculate ${\int }_{C}\,\text{d}s,$ where $C$ is the path shown above.

- $9$
- $2(2+\sqrt{5})$
- $2(3+\sqrt{5})$
- $5+2\sqrt{5}$
- $10$

The path $C$ is made up of two parts, as shown below:

![](images/27/27c19b56a24315f1105539afc441a33957dddf606b3410b86121e7cb8ed16973.png)

Now, we make use of the following facts:

- If $C={C}_{1}\cup {C}_{2}$ is a piecewise-smooth curve, we have

$$
{\int }_{C}f(x,y)\,\text{d}s={\int }_{{C}_{1}}f(x,y)\,\text{d}s+{\int }_{{C}_{2}}f(x,y)\,\text{d}s.
$$

- The line integral of unity with respect to arc length over $C$ is equal to the arc length $L$ of $C,$ i.e.,

$$
{\int }_{C}\,\text{d}s=L.
$$

The path ${C}_{1}$ is the hypotenuse of a right triangle whose legs have lengths $3$ and $4.$ Therefore, we have

$$
{\int }_{{C}_{1}}\,\text{d}s=\sqrt{{3}^{2}+{4}^{2}}=5.
$$

The path ${C}_{2}$ is the hypotenuse of a right triangle whose legs have lengths $2$ and $4.$ Therefore, we have

$$
{\int }_{{C}_{2}}\,\text{d}s=\sqrt{{2}^{2}+{4}^{2}}=2\sqrt{5}.
$$

Therefore,

$$
{\int }_{C}\,\text{d}s=5+2\sqrt{5}.
$$


### Generated raw-variant/q-122845

Parameters/profile: `{"a": "6", "b": "4", "h": "8"}`, `raw-q-122845`.

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186162082/assets/52d13818ba784cf6bed2c98c2dafe6043e0c99d4927bf15cce0164bd269a366c-prompt.png)

Calculate ${\int }_{C}\,\text{d}s,$ where $C$ is the path shown above.

- $18$
- $4(2+\sqrt{5})$
- $4(3+\sqrt{5})$
- $10+4\sqrt{5}$
- $20$

The path $C$ is made up of two parts, as shown below:

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186162082/assets/52d13818ba784cf6bed2c98c2dafe6043e0c99d4927bf15cce0164bd269a366c-solution.png)

Now, we make use of the following facts:

- If $C={C}_{1}\cup {C}_{2}$ is a piecewise-smooth curve, we have

$$
{\int }_{C}f(x,y)\,\text{d}s={\int }_{{C}_{1}}f(x,y)\,\text{d}s+{\int }_{{C}_{2}}f(x,y)\,\text{d}s.
$$

- The line integral of unity with respect to arc length over $C$ is equal to the arc length $L$ of $C,$ i.e.,

$$
{\int }_{C}\,\text{d}s=L.
$$

The path ${C}_{1}$ is the hypotenuse of a right triangle whose legs have lengths $6$ and $8.$ Therefore, we have

$$
{\int }_{{C}_{1}}\,\text{d}s=\sqrt{{6}^{2}+{8}^{2}}=10.
$$

The path ${C}_{2}$ is the hypotenuse of a right triangle whose legs have lengths $4$ and $8.$ Therefore, we have

$$
{\int }_{{C}_{2}}\,\text{d}s=\sqrt{{4}^{2}+{8}^{2}}=4\sqrt{5}.
$$

Therefore,

$$
{\int }_{C}\,\text{d}s=10+4\sqrt{5}.
$$


### Generated source/q-122845

Parameters/profile: `{"a": "3", "b": "2", "h": "4"}`, `q-122845`.

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186162082/assets/84df7cc003a5966b26e31224a23e154a9e021ca05deaaf5e242c7a79ff2c7718-prompt.png)

Calculate ${\int }_{C}\,\text{d}s,$ where $C$ is the path shown above.

- $2 \sqrt{5} + 6$
- $4 + 2 \sqrt{5}$
- $9$
- $10$
- $2 \sqrt{5} + 5$

The path $C$ is made up of two parts, as shown below:

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186162082/assets/84df7cc003a5966b26e31224a23e154a9e021ca05deaaf5e242c7a79ff2c7718-solution.png)

Now, we make use of the following facts:

- If $C={C}_{1}\cup {C}_{2}$ is a piecewise-smooth curve, we have

$$
{\int }_{C}f(x,y)\,\text{d}s={\int }_{{C}_{1}}f(x,y)\,\text{d}s+{\int }_{{C}_{2}}f(x,y)\,\text{d}s.
$$

- The line integral of unity with respect to arc length over $C$ is equal to the arc length $L$ of $C,$ i.e.,

$$
{\int }_{C}\,\text{d}s=L.
$$

The path ${C}_{1}$ is the hypotenuse of a right triangle whose legs have lengths $3$ and $4.$ Therefore, we have

$$
{\int }_{{C}_{1}}\,\text{d}s=\sqrt{{3}^{2}+{4}^{2}}=5.
$$

The path ${C}_{2}$ is the hypotenuse of a right triangle whose legs have lengths $2$ and $4.$ Therefore, we have

$$
{\int }_{{C}_{2}}\,\text{d}s=\sqrt{{2}^{2}+{4}^{2}}=2 \sqrt{5}.
$$

Therefore,

$$
{\int }_{C}\,\text{d}s=5+2 \sqrt{5}.
$$


### Generated empirical-variant/q-122845

Parameters/profile: `{"a": "6", "b": "4", "h": "8"}`, `q-122845`.

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186162082/assets/52d13818ba784cf6bed2c98c2dafe6043e0c99d4927bf15cce0164bd269a366c-prompt.png)

Calculate ${\int }_{C}\,\text{d}s,$ where $C$ is the path shown above.

- $4 \sqrt{5} + 12$
- $8 + 4 \sqrt{5}$
- $20$
- $18$
- $4 \sqrt{5} + 10$

The path $C$ is made up of two parts, as shown below:

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186162082/assets/52d13818ba784cf6bed2c98c2dafe6043e0c99d4927bf15cce0164bd269a366c-solution.png)

Now, we make use of the following facts:

- If $C={C}_{1}\cup {C}_{2}$ is a piecewise-smooth curve, we have

$$
{\int }_{C}f(x,y)\,\text{d}s={\int }_{{C}_{1}}f(x,y)\,\text{d}s+{\int }_{{C}_{2}}f(x,y)\,\text{d}s.
$$

- The line integral of unity with respect to arc length over $C$ is equal to the arc length $L$ of $C,$ i.e.,

$$
{\int }_{C}\,\text{d}s=L.
$$

The path ${C}_{1}$ is the hypotenuse of a right triangle whose legs have lengths $6$ and $8.$ Therefore, we have

$$
{\int }_{{C}_{1}}\,\text{d}s=\sqrt{{6}^{2}+{8}^{2}}=10.
$$

The path ${C}_{2}$ is the hypotenuse of a right triangle whose legs have lengths $4$ and $8.$ Therefore, we have

$$
{\int }_{{C}_{2}}\,\text{d}s=\sqrt{{4}^{2}+{8}^{2}}=4 \sqrt{5}.
$$

Therefore,

$$
{\int }_{C}\,\text{d}s=10+4 \sqrt{5}.
$$


## Original q-122850

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186162082/q-122850-source-0.png)

Calculate ${\int }_{C}\,\text{d}s,$ where $C$ is the path shown above.

The path $C$ is made up of two parts, as shown below:

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186162082/q-122850-source-1.png)

Calculate ${\int }_{C}\,\text{d}s,$ where $C$ is the path shown above.

Now, we make use of the following facts:

- If $C={C}_{1}\cup {C}_{2}$ is a piecewise-smooth curve, we have

$$
{\int }_{C}f(x,y)\,\text{d}s={\int }_{{C}_{1}}f(x,y)\,\text{d}s+{\int }_{{C}_{2}}f(x,y)\,\text{d}s.
$$

- The line integral of unity with respect to arc length over $C$ is equal to the arc length $L$ of $C,$ i.e.,

$$
{\int }_{C}\,\text{d}s=L.
$$

The path ${C}_{1}$ is a quarter of a circle of radius $r=4.$ Therefore, we have

$$
{\int }_{{C}_{1}}\,\text{d}s=\frac{1}{4}(2\pi r)=2\pi .
$$

The path ${C}_{2}$ is the hypotenuse of a right triangle where both legs have a length of $4.$ Therefore, we have

$$
{\int }_{{C}_{2}}\,\text{d}s=\sqrt{{4}^{2}+{4}^{2}}=4\sqrt{2}.
$$

Therefore,

$$
{\int }_{C}\,\text{d}s=2\pi +4\sqrt{2}=2(\pi +2\sqrt{2}).
$$

Original five options:

- $\frac{3\pi +4\sqrt{2}}{4}$
- $2(2\pi +\sqrt{2})$
- $\frac{\pi +4\sqrt{2}}{4}$
- $2\pi +3\sqrt{2}$
- $2(\pi +2\sqrt{2})$

Observed key: $2(\pi +2\sqrt{2})$.


### Generated raw-source/q-122850

Parameters/profile: `{"r": "4"}`, `raw-q-122850`.

![](images/bf/bf87c4707c0f4a8ab1b5157a13e8c7785da915833c5f9d896a2747af27f70e59.png)

Calculate ${\int }_{C}\,\text{d}s,$ where $C$ is the path shown above.

- $\frac{3\pi +4\sqrt{2}}{4}$
- $2(2\pi +\sqrt{2})$
- $\frac{\pi +4\sqrt{2}}{4}$
- $2\pi +3\sqrt{2}$
- $2(\pi +2\sqrt{2})$

The path $C$ is made up of two parts, as shown below:

![](images/ff/ff52b8e83a9cc9867b25ea3c24ed0f988a27dec73f9e0ab2dfda28ddabb3238a.png)

Calculate ${\int }_{C}\,\text{d}s,$ where $C$ is the path shown above.

Now, we make use of the following facts:

- If $C={C}_{1}\cup {C}_{2}$ is a piecewise-smooth curve, we have

$$
{\int }_{C}f(x,y)\,\text{d}s={\int }_{{C}_{1}}f(x,y)\,\text{d}s+{\int }_{{C}_{2}}f(x,y)\,\text{d}s.
$$

- The line integral of unity with respect to arc length over $C$ is equal to the arc length $L$ of $C,$ i.e.,

$$
{\int }_{C}\,\text{d}s=L.
$$

The path ${C}_{1}$ is a quarter of a circle of radius $r=4.$ Therefore, we have

$$
{\int }_{{C}_{1}}\,\text{d}s=\frac{1}{4}(2\pi r)=2\pi .
$$

The path ${C}_{2}$ is the hypotenuse of a right triangle where both legs have a length of $4.$ Therefore, we have

$$
{\int }_{{C}_{2}}\,\text{d}s=\sqrt{{4}^{2}+{4}^{2}}=4\sqrt{2}.
$$

Therefore,

$$
{\int }_{C}\,\text{d}s=2\pi +4\sqrt{2}=2(\pi +2\sqrt{2}).
$$


### Generated raw-variant/q-122850

Parameters/profile: `{"r": "8"}`, `raw-q-122850`.

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186162082/assets/4fd2baddcd4d4534648102b43f3275e3e416d9b4adf8e71c89f2a453fc10ce89-prompt.png)

Calculate ${\int }_{C}\,\text{d}s,$ where $C$ is the path shown above.

- $\frac{6\pi +8\sqrt{2}}{4}$
- $4(2\pi +\sqrt{2})$
- $\frac{2\pi +8\sqrt{2}}{4}$
- $4\pi +6\sqrt{2}$
- $4(\pi +2\sqrt{2})$

The path $C$ is made up of two parts, as shown below:

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186162082/assets/4fd2baddcd4d4534648102b43f3275e3e416d9b4adf8e71c89f2a453fc10ce89-solution.png)

Calculate ${\int }_{C}\,\text{d}s,$ where $C$ is the path shown above.

Now, we make use of the following facts:

- If $C={C}_{1}\cup {C}_{2}$ is a piecewise-smooth curve, we have

$$
{\int }_{C}f(x,y)\,\text{d}s={\int }_{{C}_{1}}f(x,y)\,\text{d}s+{\int }_{{C}_{2}}f(x,y)\,\text{d}s.
$$

- The line integral of unity with respect to arc length over $C$ is equal to the arc length $L$ of $C,$ i.e.,

$$
{\int }_{C}\,\text{d}s=L.
$$

The path ${C}_{1}$ is a quarter of a circle of radius $r=8.$ Therefore, we have

$$
{\int }_{{C}_{1}}\,\text{d}s=\frac{1}{4}(2\pi r)=4\pi .
$$

The path ${C}_{2}$ is the hypotenuse of a right triangle where both legs have a length of $8.$ Therefore, we have

$$
{\int }_{{C}_{2}}\,\text{d}s=\sqrt{{8}^{2}+{8}^{2}}=8\sqrt{2}.
$$

Therefore,

$$
{\int }_{C}\,\text{d}s=4\pi +8\sqrt{2}=4(\pi +2\sqrt{2}).
$$


### Generated source/q-122850

Parameters/profile: `{"r": "4"}`, `q-122850`.

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186162082/assets/873f879f507f93aa641469bc53a8ca0d4f9634e0020b9a2032207605f84a796b-prompt.png)

Calculate ${\int }_{C}\,\text{d}s,$ where $C$ is the path shown above.

- $\frac{\pi}{4} + \sqrt{2}$
- $2 \sqrt{2} + 4 \pi$
- $\sqrt{2} + \frac{3 \pi}{4}$
- $4 \sqrt{2} + 2 \pi$
- $3 \sqrt{2} + 2 \pi$

The path $C$ is made up of two parts, as shown below:

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186162082/assets/873f879f507f93aa641469bc53a8ca0d4f9634e0020b9a2032207605f84a796b-solution.png)

Calculate ${\int }_{C}\,\text{d}s,$ where $C$ is the path shown above.

Now, we make use of the following facts:

- If $C={C}_{1}\cup {C}_{2}$ is a piecewise-smooth curve, we have

$$
{\int }_{C}f(x,y)\,\text{d}s={\int }_{{C}_{1}}f(x,y)\,\text{d}s+{\int }_{{C}_{2}}f(x,y)\,\text{d}s.
$$

- The line integral of unity with respect to arc length over $C$ is equal to the arc length $L$ of $C,$ i.e.,

$$
{\int }_{C}\,\text{d}s=L.
$$

The path ${C}_{1}$ is a quarter of a circle of radius $r=4.$ Therefore, we have

$$
{\int }_{{C}_{1}}\,\text{d}s=\frac{1}{4}(2\pi r)=2 \pi .
$$

The path ${C}_{2}$ is the hypotenuse of a right triangle where both legs have a length of $4.$ Therefore, we have

$$
{\int }_{{C}_{2}}\,\text{d}s=\sqrt{{4}^{2}+{4}^{2}}=4 \sqrt{2}.
$$

Therefore,

$$
{\int }_{C}\,\text{d}s=2 \pi+4 \sqrt{2}=2(\pi+2\sqrt{2}).
$$


### Generated empirical-variant/q-122850

Parameters/profile: `{"r": "8"}`, `q-122850`.

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186162082/assets/4fd2baddcd4d4534648102b43f3275e3e416d9b4adf8e71c89f2a453fc10ce89-prompt.png)

Calculate ${\int }_{C}\,\text{d}s,$ where $C$ is the path shown above.

- $\frac{\pi}{2} + 2 \sqrt{2}$
- $4 \sqrt{2} + 8 \pi$
- $8 \sqrt{2} + 4 \pi$
- $2 \sqrt{2} + \frac{3 \pi}{2}$
- $6 \sqrt{2} + 4 \pi$

The path $C$ is made up of two parts, as shown below:

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186162082/assets/4fd2baddcd4d4534648102b43f3275e3e416d9b4adf8e71c89f2a453fc10ce89-solution.png)

Calculate ${\int }_{C}\,\text{d}s,$ where $C$ is the path shown above.

Now, we make use of the following facts:

- If $C={C}_{1}\cup {C}_{2}$ is a piecewise-smooth curve, we have

$$
{\int }_{C}f(x,y)\,\text{d}s={\int }_{{C}_{1}}f(x,y)\,\text{d}s+{\int }_{{C}_{2}}f(x,y)\,\text{d}s.
$$

- The line integral of unity with respect to arc length over $C$ is equal to the arc length $L$ of $C,$ i.e.,

$$
{\int }_{C}\,\text{d}s=L.
$$

The path ${C}_{1}$ is a quarter of a circle of radius $r=8.$ Therefore, we have

$$
{\int }_{{C}_{1}}\,\text{d}s=\frac{1}{4}(2\pi r)=4 \pi .
$$

The path ${C}_{2}$ is the hypotenuse of a right triangle where both legs have a length of $8.$ Therefore, we have

$$
{\int }_{{C}_{2}}\,\text{d}s=\sqrt{{8}^{2}+{8}^{2}}=8 \sqrt{2}.
$$

Therefore,

$$
{\int }_{C}\,\text{d}s=4 \pi+8 \sqrt{2}=4(\pi+2\sqrt{2}).
$$


## Authored default variants

Observed empirical banks are explicit replay profiles. These defaults use complete omitted/doubled-piece operations. Hard labels are authored rational-bookkeeping policy.


### easy/semi/0

Parameters: `{"r": "7"}`.

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186162082/assets/8d5662d50adfb024163e50a48ba8f91f314d44fe90b7c823f0fe771fe2ea03ac-prompt.png)

Calculate ${\int }_{C}\,\text{d}s,$ where $C$ is a path that traverses a semicircle of radius $7$ once in the counterclockwise direction, as shown above.

- $7 \pi + 28$
- $14$
- $7 \pi$
- $14 + 7 \pi$
- $14 + 14 \pi$

The path $C$ is made up of two parts, as shown below:

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186162082/assets/8d5662d50adfb024163e50a48ba8f91f314d44fe90b7c823f0fe771fe2ea03ac-solution.png)

Now, we make use of the following facts:

- If $C={C}_{1}\cup {C}_{2}$ is a piecewise-smooth curve, we have

$$
{\int }_{C}f(x,y)\,\text{d}s={\int }_{{C}_{1}}f(x,y)\,\text{d}s+{\int }_{{C}_{2}}f(x,y)\,\text{d}s.
$$

- The line integral of unity with respect to arc length over $C$ is equal to the arc length $L$ of $C,$ i.e.,

$$
{\int }_{C}\,\text{d}s=L.
$$

The path ${C}_{1}$ is a semi-circle of radius $r=7.$ Therefore, we have

$$
{\int }_{{C}_{1}}\,\text{d}s=\pi r=7 \pi .
$$

The path ${C}_{2}$ is a line segment of length $14.$ Therefore, we have

$$
{\int }_{{C}_{2}}\,\text{d}s=14.
$$

Therefore,

$$
{\int }_{C}\,\text{d}s=7 \pi+14=7(\pi+2).
$$


### easy/semi/1

Parameters: `{"r": "3"}`.

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186162082/assets/4c1697d3782c550f5a7fe1cac7ba584e0f7e1f570954a6fd63079f268cc99fde-prompt.png)

Calculate ${\int }_{C}\,\text{d}s,$ where $C$ is a path that traverses a semicircle of radius $3$ once in the counterclockwise direction, as shown above.

- $6$
- $6 + 6 \pi$
- $3 \pi$
- $6 + 3 \pi$
- $3 \pi + 12$

The path $C$ is made up of two parts, as shown below:

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186162082/assets/4c1697d3782c550f5a7fe1cac7ba584e0f7e1f570954a6fd63079f268cc99fde-solution.png)

Now, we make use of the following facts:

- If $C={C}_{1}\cup {C}_{2}$ is a piecewise-smooth curve, we have

$$
{\int }_{C}f(x,y)\,\text{d}s={\int }_{{C}_{1}}f(x,y)\,\text{d}s+{\int }_{{C}_{2}}f(x,y)\,\text{d}s.
$$

- The line integral of unity with respect to arc length over $C$ is equal to the arc length $L$ of $C,$ i.e.,

$$
{\int }_{C}\,\text{d}s=L.
$$

The path ${C}_{1}$ is a semi-circle of radius $r=3.$ Therefore, we have

$$
{\int }_{{C}_{1}}\,\text{d}s=\pi r=3 \pi .
$$

The path ${C}_{2}$ is a line segment of length $6.$ Therefore, we have

$$
{\int }_{{C}_{2}}\,\text{d}s=6.
$$

Therefore,

$$
{\int }_{C}\,\text{d}s=3 \pi+6=3(\pi+2).
$$


### easy/three_quarter/0

Parameters: `{"r": "7"}`.

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186162082/assets/b3628d7589bc05d40a5366de24b19b13a3318b77f49c6c699e991a1fe4b44ade-prompt.png)

Calculate ${\int }_{C}\,\text{d}s,$ where $C$ is the path shown above.

- $14 + \frac{21 \pi}{2}$
- $7$
- $\frac{21 \pi}{2}$
- $7 + \frac{21 \pi}{2}$
- $7 + 21 \pi$

The path $C$ is made up of two parts, as shown below:

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186162082/assets/b3628d7589bc05d40a5366de24b19b13a3318b77f49c6c699e991a1fe4b44ade-solution.png)

Now, we make use of the following facts:

- If $C={C}_{1}\cup {C}_{2}$ is a piecewise-smooth curve, we have

$$
{\int }_{C}f(x,y)\,\text{d}s={\int }_{{C}_{1}}f(x,y)\,\text{d}s+{\int }_{{C}_{2}}f(x,y)\,\text{d}s.
$$

- The line integral of unity with respect to arc length over $C$ is equal to the arc length $L$ of $C,$ i.e.,

$$
{\int }_{C}\,\text{d}s=L.
$$

The path ${C}_{1}$ is three-quarters of a circle of radius $r=7.$ Therefore, we have

$$
{\int }_{{C}_{1}}\,\text{d}s=\frac{3}{4}(2\pi r)=\frac{21 \pi}{2} .
$$

The path ${C}_{2}$ is a line segment of length $7.$ Therefore, we have

$$
{\int }_{{C}_{2}}\,\text{d}s=7.
$$

Therefore,

$$
{\int }_{C}\,\text{d}s=\frac{21 \pi}{2}+7.
$$


### easy/three_quarter/1

Parameters: `{"r": "3"}`.

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186162082/assets/7e399874660a6310f56190f3b9530b7580640ec8edb9c5311c50d206ca1468e1-prompt.png)

Calculate ${\int }_{C}\,\text{d}s,$ where $C$ is the path shown above.

- $3$
- $3 + 9 \pi$
- $\frac{9 \pi}{2}$
- $3 + \frac{9 \pi}{2}$
- $6 + \frac{9 \pi}{2}$

The path $C$ is made up of two parts, as shown below:

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186162082/assets/7e399874660a6310f56190f3b9530b7580640ec8edb9c5311c50d206ca1468e1-solution.png)

Now, we make use of the following facts:

- If $C={C}_{1}\cup {C}_{2}$ is a piecewise-smooth curve, we have

$$
{\int }_{C}f(x,y)\,\text{d}s={\int }_{{C}_{1}}f(x,y)\,\text{d}s+{\int }_{{C}_{2}}f(x,y)\,\text{d}s.
$$

- The line integral of unity with respect to arc length over $C$ is equal to the arc length $L$ of $C,$ i.e.,

$$
{\int }_{C}\,\text{d}s=L.
$$

The path ${C}_{1}$ is three-quarters of a circle of radius $r=3.$ Therefore, we have

$$
{\int }_{{C}_{1}}\,\text{d}s=\frac{3}{4}(2\pi r)=\frac{9 \pi}{2} .
$$

The path ${C}_{2}$ is a line segment of length $3.$ Therefore, we have

$$
{\int }_{{C}_{2}}\,\text{d}s=3.
$$

Therefore,

$$
{\int }_{C}\,\text{d}s=\frac{9 \pi}{2}+3.
$$


### moderate/quarter_closed/0

Parameters: `{"r": "7"}`.

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186162082/assets/ae79863185cbd0fc7a5cb4572a77979aaf03021179c58f4204938d80b7acedc0-prompt.png)

Calculate $\displaystyle \int_{C}ds$, where $C$ is a path that traverses a circular segment of radius $7$ once in the counterclockwise direction, as shown above.

- $\frac{7 \pi}{2} + 14 \sqrt{2}$
- $7 \sqrt{2}$
- $\frac{7 \pi}{2}$
- $7 \sqrt{2} + \frac{7 \pi}{2}$
- $7 \sqrt{2} + 7 \pi$

The path $C$ is made up of two parts, as shown below:

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186162082/assets/ae79863185cbd0fc7a5cb4572a77979aaf03021179c58f4204938d80b7acedc0-solution.png)

Now, we make use of the following facts:

- If $C={C}_{1}\cup {C}_{2}$ is a piecewise-smooth curve, we have

$$
{\int }_{C}f(x,y)\,\text{d}s={\int }_{{C}_{1}}f(x,y)\,\text{d}s+{\int }_{{C}_{2}}f(x,y)\,\text{d}s.
$$

- The line integral of unity with respect to arc length over $C$ is equal to the arc length $L$ of $C,$ i.e.,

$$
{\int }_{C}\,\text{d}s=L.
$$

The path ${C}_{1}$ is a quarter of a circle of radius $r=7.$ Therefore, we have

$$
{\int }_{{C}_{1}}\,\text{d}s=\frac{1}{4}(2\pi r)=\frac{7 \pi}{2} .
$$

The path ${C}_{2}$ is the hypotenuse of a right triangle where both legs have a length of $7.$ Therefore, we have

$$
{\int }_{{C}_{2}}\,\text{d}s=\sqrt{{7}^{2}+{7}^{2}}=7 \sqrt{2}.
$$

Therefore,

$$
{\int }_{C}\,\text{d}s=\frac{7 \pi}{2}+7 \sqrt{2}.
$$


### moderate/quarter_closed/1

Parameters: `{"r": "3"}`.

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186162082/assets/f5c9cb258a41e8838de4673b4b5ad94ee0e206cad2b309c308a807eeca9f0b6c-prompt.png)

Calculate $\displaystyle \int_{C}ds$, where $C$ is a path that traverses a circular segment of radius $3$ once in the counterclockwise direction, as shown above.

- $3 \sqrt{2}$
- $3 \sqrt{2} + 3 \pi$
- $\frac{3 \pi}{2}$
- $3 \sqrt{2} + \frac{3 \pi}{2}$
- $\frac{3 \pi}{2} + 6 \sqrt{2}$

The path $C$ is made up of two parts, as shown below:

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186162082/assets/f5c9cb258a41e8838de4673b4b5ad94ee0e206cad2b309c308a807eeca9f0b6c-solution.png)

Now, we make use of the following facts:

- If $C={C}_{1}\cup {C}_{2}$ is a piecewise-smooth curve, we have

$$
{\int }_{C}f(x,y)\,\text{d}s={\int }_{{C}_{1}}f(x,y)\,\text{d}s+{\int }_{{C}_{2}}f(x,y)\,\text{d}s.
$$

- The line integral of unity with respect to arc length over $C$ is equal to the arc length $L$ of $C,$ i.e.,

$$
{\int }_{C}\,\text{d}s=L.
$$

The path ${C}_{1}$ is a quarter of a circle of radius $r=3.$ Therefore, we have

$$
{\int }_{{C}_{1}}\,\text{d}s=\frac{1}{4}(2\pi r)=\frac{3 \pi}{2} .
$$

The path ${C}_{2}$ is the hypotenuse of a right triangle where both legs have a length of $3.$ Therefore, we have

$$
{\int }_{{C}_{2}}\,\text{d}s=\sqrt{{3}^{2}+{3}^{2}}=3 \sqrt{2}.
$$

Therefore,

$$
{\int }_{C}\,\text{d}s=\frac{3 \pi}{2}+3 \sqrt{2}.
$$


### moderate/three_segments/0

Parameters: `{"a": "9", "b": "12"}`.

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186162082/assets/d4ac6f28500bd6277a3746684b40c34755e373e7eb30557378132222c462f921-prompt.png)

Calculate ${\int }_{C}\,\text{d}s,$ where $C$ is the path shown above.

- $57$
- $24$
- $9$
- $33$
- $42$

The path $C$ is made up of three parts, as shown below:

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186162082/assets/d4ac6f28500bd6277a3746684b40c34755e373e7eb30557378132222c462f921-solution.png)

Now, we make use of the following facts:

- If $C={C}_{1}\cup {C}_{2}\cup {C}_{3}$ is a piecewise-smooth curve, we have

$$
{\int }_{C}f(x,y)\,\text{d}s={\int }_{{C}_{1}}f(x,y)\,\text{d}s+{\int }_{{C}_{2}}f(x,y)\,\text{d}s+{\int }_{{C}_{3}}f(x,y)\,\text{d}s.
$$

- The line integral of unity with respect to arc length over $C$ is equal to the arc length $L$ of $C,$ i.e.,

$$
{\int }_{C}\,\text{d}s=L.
$$

The paths ${C}_{1}$ and ${C}_{3}$ are line segments of length $9.$ Therefore, we have

$$
{\int }_{{C}_{1}}\,\text{d}s={\int }_{{C}_{3}}\,\text{d}s=9.
$$

The path ${C}_{2}$ is the hypotenuse of a right triangle whose legs have lengths $9$ and $12.$ Therefore, we have

$$
{\int }_{{C}_{2}}\,\text{d}s=\sqrt{{9}^{2}+{12}^{2}}=15.
$$

Therefore,

$$
{\int }_{C}\,\text{d}s=9+15+9=33.
$$


### moderate/three_segments/1

Parameters: `{"a": "5", "b": "12"}`.

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186162082/assets/5d0bbd30ef05610ed6416272a9ed7e50ecb804c14857ec167dbab7f7b20e8ca3-prompt.png)

Calculate ${\int }_{C}\,\text{d}s,$ where $C$ is the path shown above.

- $18$
- $28$
- $5$
- $23$
- $41$

The path $C$ is made up of three parts, as shown below:

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186162082/assets/5d0bbd30ef05610ed6416272a9ed7e50ecb804c14857ec167dbab7f7b20e8ca3-solution.png)

Now, we make use of the following facts:

- If $C={C}_{1}\cup {C}_{2}\cup {C}_{3}$ is a piecewise-smooth curve, we have

$$
{\int }_{C}f(x,y)\,\text{d}s={\int }_{{C}_{1}}f(x,y)\,\text{d}s+{\int }_{{C}_{2}}f(x,y)\,\text{d}s+{\int }_{{C}_{3}}f(x,y)\,\text{d}s.
$$

- The line integral of unity with respect to arc length over $C$ is equal to the arc length $L$ of $C,$ i.e.,

$$
{\int }_{C}\,\text{d}s=L.
$$

The paths ${C}_{1}$ and ${C}_{3}$ are line segments of length $5.$ Therefore, we have

$$
{\int }_{{C}_{1}}\,\text{d}s={\int }_{{C}_{3}}\,\text{d}s=5.
$$

The path ${C}_{2}$ is the hypotenuse of a right triangle whose legs have lengths $5$ and $12.$ Therefore, we have

$$
{\int }_{{C}_{2}}\,\text{d}s=\sqrt{{5}^{2}+{12}^{2}}=13.
$$

Therefore,

$$
{\int }_{C}\,\text{d}s=5+13+5=23.
$$


### moderate/two_segments/0

Parameters: `{"a": "8", "h": "6", "b": "7"}`.

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186162082/assets/4448a270f0bdb2d50199f8ac435ee39afa8ea21f5dfa1b1d164b5493ac10be8f-prompt.png)

Calculate ${\int }_{C}\,\text{d}s,$ where $C$ is the path shown above.

- $\sqrt{85}$
- $10$
- $\sqrt{85} + 10$
- $10 + 2 \sqrt{85}$
- $\sqrt{85} + 20$

The path $C$ is made up of two parts, as shown below:

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186162082/assets/4448a270f0bdb2d50199f8ac435ee39afa8ea21f5dfa1b1d164b5493ac10be8f-solution.png)

Now, we make use of the following facts:

- If $C={C}_{1}\cup {C}_{2}$ is a piecewise-smooth curve, we have

$$
{\int }_{C}f(x,y)\,\text{d}s={\int }_{{C}_{1}}f(x,y)\,\text{d}s+{\int }_{{C}_{2}}f(x,y)\,\text{d}s.
$$

- The line integral of unity with respect to arc length over $C$ is equal to the arc length $L$ of $C,$ i.e.,

$$
{\int }_{C}\,\text{d}s=L.
$$

The path ${C}_{1}$ is the hypotenuse of a right triangle whose legs have lengths $8$ and $6.$ Therefore, we have

$$
{\int }_{{C}_{1}}\,\text{d}s=\sqrt{{8}^{2}+{6}^{2}}=10.
$$

The path ${C}_{2}$ is the hypotenuse of a right triangle whose legs have lengths $7$ and $6.$ Therefore, we have

$$
{\int }_{{C}_{2}}\,\text{d}s=\sqrt{{7}^{2}+{6}^{2}}=\sqrt{85}.
$$

Therefore,

$$
{\int }_{C}\,\text{d}s=10+\sqrt{85}.
$$


### moderate/two_segments/1

Parameters: `{"a": "3", "h": "4", "b": "6"}`.

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186162082/assets/423930b63d84f40dee9cc4e5abe76a3550df33446db0d86dd170a03dc63111c8-prompt.png)

Calculate ${\int }_{C}\,\text{d}s,$ where $C$ is the path shown above.

- $2 \sqrt{13}$
- $2 \sqrt{13} + 10$
- $5$
- $5 + 2 \sqrt{13}$
- $5 + 4 \sqrt{13}$

The path $C$ is made up of two parts, as shown below:

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186162082/assets/423930b63d84f40dee9cc4e5abe76a3550df33446db0d86dd170a03dc63111c8-solution.png)

Now, we make use of the following facts:

- If $C={C}_{1}\cup {C}_{2}$ is a piecewise-smooth curve, we have

$$
{\int }_{C}f(x,y)\,\text{d}s={\int }_{{C}_{1}}f(x,y)\,\text{d}s+{\int }_{{C}_{2}}f(x,y)\,\text{d}s.
$$

- The line integral of unity with respect to arc length over $C$ is equal to the arc length $L$ of $C,$ i.e.,

$$
{\int }_{C}\,\text{d}s=L.
$$

The path ${C}_{1}$ is the hypotenuse of a right triangle whose legs have lengths $3$ and $4.$ Therefore, we have

$$
{\int }_{{C}_{1}}\,\text{d}s=\sqrt{{3}^{2}+{4}^{2}}=5.
$$

The path ${C}_{2}$ is the hypotenuse of a right triangle whose legs have lengths $6$ and $4.$ Therefore, we have

$$
{\int }_{{C}_{2}}\,\text{d}s=\sqrt{{6}^{2}+{4}^{2}}=2 \sqrt{13}.
$$

Therefore,

$$
{\int }_{C}\,\text{d}s=5+2 \sqrt{13}.
$$


### moderate/quarter_open/0

Parameters: `{"r": "7"}`.

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186162082/assets/3c6541e33e536c3e30d1945aed831bf1aeeeb7721d17f3e9eb55393c8f80f31e-prompt.png)

Calculate ${\int }_{C}\,\text{d}s,$ where $C$ is the path shown above.

- $\frac{7 \pi}{2} + 14 \sqrt{2}$
- $7 \sqrt{2}$
- $\frac{7 \pi}{2}$
- $7 \sqrt{2} + \frac{7 \pi}{2}$
- $7 \sqrt{2} + 7 \pi$

The path $C$ is made up of two parts, as shown below:

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186162082/assets/3c6541e33e536c3e30d1945aed831bf1aeeeb7721d17f3e9eb55393c8f80f31e-solution.png)

Calculate ${\int }_{C}\,\text{d}s,$ where $C$ is the path shown above.

Now, we make use of the following facts:

- If $C={C}_{1}\cup {C}_{2}$ is a piecewise-smooth curve, we have

$$
{\int }_{C}f(x,y)\,\text{d}s={\int }_{{C}_{1}}f(x,y)\,\text{d}s+{\int }_{{C}_{2}}f(x,y)\,\text{d}s.
$$

- The line integral of unity with respect to arc length over $C$ is equal to the arc length $L$ of $C,$ i.e.,

$$
{\int }_{C}\,\text{d}s=L.
$$

The path ${C}_{1}$ is a quarter of a circle of radius $r=7.$ Therefore, we have

$$
{\int }_{{C}_{1}}\,\text{d}s=\frac{1}{4}(2\pi r)=\frac{7 \pi}{2} .
$$

The path ${C}_{2}$ is the hypotenuse of a right triangle where both legs have a length of $7.$ Therefore, we have

$$
{\int }_{{C}_{2}}\,\text{d}s=\sqrt{{7}^{2}+{7}^{2}}=7 \sqrt{2}.
$$

Therefore,

$$
{\int }_{C}\,\text{d}s=\frac{7 \pi}{2}+7 \sqrt{2}=\frac{7}{2}(\pi+2\sqrt{2}).
$$


### moderate/quarter_open/1

Parameters: `{"r": "3"}`.

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186162082/assets/588b470c6a433e4e0e1bcc7308d685224959d485ae9fc8b48998d658a579e46d-prompt.png)

Calculate ${\int }_{C}\,\text{d}s,$ where $C$ is the path shown above.

- $3 \sqrt{2}$
- $3 \sqrt{2} + 3 \pi$
- $\frac{3 \pi}{2}$
- $3 \sqrt{2} + \frac{3 \pi}{2}$
- $\frac{3 \pi}{2} + 6 \sqrt{2}$

The path $C$ is made up of two parts, as shown below:

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186162082/assets/588b470c6a433e4e0e1bcc7308d685224959d485ae9fc8b48998d658a579e46d-solution.png)

Calculate ${\int }_{C}\,\text{d}s,$ where $C$ is the path shown above.

Now, we make use of the following facts:

- If $C={C}_{1}\cup {C}_{2}$ is a piecewise-smooth curve, we have

$$
{\int }_{C}f(x,y)\,\text{d}s={\int }_{{C}_{1}}f(x,y)\,\text{d}s+{\int }_{{C}_{2}}f(x,y)\,\text{d}s.
$$

- The line integral of unity with respect to arc length over $C$ is equal to the arc length $L$ of $C,$ i.e.,

$$
{\int }_{C}\,\text{d}s=L.
$$

The path ${C}_{1}$ is a quarter of a circle of radius $r=3.$ Therefore, we have

$$
{\int }_{{C}_{1}}\,\text{d}s=\frac{1}{4}(2\pi r)=\frac{3 \pi}{2} .
$$

The path ${C}_{2}$ is the hypotenuse of a right triangle where both legs have a length of $3.$ Therefore, we have

$$
{\int }_{{C}_{2}}\,\text{d}s=\sqrt{{3}^{2}+{3}^{2}}=3 \sqrt{2}.
$$

Therefore,

$$
{\int }_{C}\,\text{d}s=\frac{3 \pi}{2}+3 \sqrt{2}=\frac{3}{2}(\pi+2\sqrt{2}).
$$


### hard/quarter_open/0

Parameters: `{"r": "19/3"}`.

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186162082/assets/4c12bb262cd83fd51199ef9d43c3abb3d3578f52c2c0e69aa88ad84aed21da47-prompt.png)

Calculate ${\int }_{C}\,\text{d}s,$ where $C$ is the path shown above.

- $\frac{19 \pi}{6} + \frac{38 \sqrt{2}}{3}$
- $\frac{19 \sqrt{2}}{3}$
- $\frac{19 \pi}{6}$
- $\frac{19 \sqrt{2}}{3} + \frac{19 \pi}{6}$
- $\frac{19 \sqrt{2}}{3} + \frac{19 \pi}{3}$

The path $C$ is made up of two parts, as shown below:

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186162082/assets/4c12bb262cd83fd51199ef9d43c3abb3d3578f52c2c0e69aa88ad84aed21da47-solution.png)

Calculate ${\int }_{C}\,\text{d}s,$ where $C$ is the path shown above.

Now, we make use of the following facts:

- If $C={C}_{1}\cup {C}_{2}$ is a piecewise-smooth curve, we have

$$
{\int }_{C}f(x,y)\,\text{d}s={\int }_{{C}_{1}}f(x,y)\,\text{d}s+{\int }_{{C}_{2}}f(x,y)\,\text{d}s.
$$

- The line integral of unity with respect to arc length over $C$ is equal to the arc length $L$ of $C,$ i.e.,

$$
{\int }_{C}\,\text{d}s=L.
$$

The path ${C}_{1}$ is a quarter of a circle of radius $r=\frac{19}{3}.$ Therefore, we have

$$
{\int }_{{C}_{1}}\,\text{d}s=\frac{1}{4}(2\pi r)=\frac{19 \pi}{6} .
$$

The path ${C}_{2}$ is the hypotenuse of a right triangle where both legs have a length of $\frac{19}{3}.$ Therefore, we have

$$
{\int }_{{C}_{2}}\,\text{d}s=\sqrt{{\frac{19}{3}}^{2}+{\frac{19}{3}}^{2}}=\frac{19 \sqrt{2}}{3}.
$$

Therefore,

$$
{\int }_{C}\,\text{d}s=\frac{19 \pi}{6}+\frac{19 \sqrt{2}}{3}=\frac{19}{6}(\pi+2\sqrt{2}).
$$


### hard/quarter_open/1

Parameters: `{"r": "17/2"}`.

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186162082/assets/3a984e0626dfba51f7390dc43fa4025e617b55b923a1be2063ce30478dc544c4-prompt.png)

Calculate ${\int }_{C}\,\text{d}s,$ where $C$ is the path shown above.

- $\frac{17 \sqrt{2}}{2}$
- $\frac{17 \sqrt{2}}{2} + \frac{17 \pi}{2}$
- $\frac{17 \pi}{4}$
- $\frac{17 \sqrt{2}}{2} + \frac{17 \pi}{4}$
- $\frac{17 \pi}{4} + 17 \sqrt{2}$

The path $C$ is made up of two parts, as shown below:

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186162082/assets/3a984e0626dfba51f7390dc43fa4025e617b55b923a1be2063ce30478dc544c4-solution.png)

Calculate ${\int }_{C}\,\text{d}s,$ where $C$ is the path shown above.

Now, we make use of the following facts:

- If $C={C}_{1}\cup {C}_{2}$ is a piecewise-smooth curve, we have

$$
{\int }_{C}f(x,y)\,\text{d}s={\int }_{{C}_{1}}f(x,y)\,\text{d}s+{\int }_{{C}_{2}}f(x,y)\,\text{d}s.
$$

- The line integral of unity with respect to arc length over $C$ is equal to the arc length $L$ of $C,$ i.e.,

$$
{\int }_{C}\,\text{d}s=L.
$$

The path ${C}_{1}$ is a quarter of a circle of radius $r=\frac{17}{2}.$ Therefore, we have

$$
{\int }_{{C}_{1}}\,\text{d}s=\frac{1}{4}(2\pi r)=\frac{17 \pi}{4} .
$$

The path ${C}_{2}$ is the hypotenuse of a right triangle where both legs have a length of $\frac{17}{2}.$ Therefore, we have

$$
{\int }_{{C}_{2}}\,\text{d}s=\sqrt{{\frac{17}{2}}^{2}+{\frac{17}{2}}^{2}}=\frac{17 \sqrt{2}}{2}.
$$

Therefore,

$$
{\int }_{C}\,\text{d}s=\frac{17 \pi}{4}+\frac{17 \sqrt{2}}{2}=\frac{17}{4}(\pi+2\sqrt{2}).
$$


### hard/three_segments/0

Parameters: `{"a": "1", "b": "4/3"}`.

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186162082/assets/f77cc2fb0e4b8cb1363e1310ffaf436977b0951a310e90390e432ebeac602902-prompt.png)

Calculate ${\int }_{C}\,\text{d}s,$ where $C$ is the path shown above.

- $\frac{19}{3}$
- $\frac{8}{3}$
- $1$
- $\frac{11}{3}$
- $\frac{14}{3}$

The path $C$ is made up of three parts, as shown below:

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186162082/assets/f77cc2fb0e4b8cb1363e1310ffaf436977b0951a310e90390e432ebeac602902-solution.png)

Now, we make use of the following facts:

- If $C={C}_{1}\cup {C}_{2}\cup {C}_{3}$ is a piecewise-smooth curve, we have

$$
{\int }_{C}f(x,y)\,\text{d}s={\int }_{{C}_{1}}f(x,y)\,\text{d}s+{\int }_{{C}_{2}}f(x,y)\,\text{d}s+{\int }_{{C}_{3}}f(x,y)\,\text{d}s.
$$

- The line integral of unity with respect to arc length over $C$ is equal to the arc length $L$ of $C,$ i.e.,

$$
{\int }_{C}\,\text{d}s=L.
$$

The paths ${C}_{1}$ and ${C}_{3}$ are line segments of length $1.$ Therefore, we have

$$
{\int }_{{C}_{1}}\,\text{d}s={\int }_{{C}_{3}}\,\text{d}s=1.
$$

The path ${C}_{2}$ is the hypotenuse of a right triangle whose legs have lengths $1$ and $\frac{4}{3}.$ Therefore, we have

$$
{\int }_{{C}_{2}}\,\text{d}s=\sqrt{{1}^{2}+{\frac{4}{3}}^{2}}=\frac{5}{3}.
$$

Therefore,

$$
{\int }_{C}\,\text{d}s=1+\frac{5}{3}+1=\frac{11}{3}.
$$


### hard/three_segments/1

Parameters: `{"a": "5/2", "b": "6"}`.

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186162082/assets/7fe482e7bb5e43fd9d926230ba2fe7683e4ceeb5c4b238c5caa193e9243cb775-prompt.png)

Calculate ${\int }_{C}\,\text{d}s,$ where $C$ is the path shown above.

- $9$
- $14$
- $\frac{5}{2}$
- $\frac{23}{2}$
- $\frac{41}{2}$

The path $C$ is made up of three parts, as shown below:

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186162082/assets/7fe482e7bb5e43fd9d926230ba2fe7683e4ceeb5c4b238c5caa193e9243cb775-solution.png)

Now, we make use of the following facts:

- If $C={C}_{1}\cup {C}_{2}\cup {C}_{3}$ is a piecewise-smooth curve, we have

$$
{\int }_{C}f(x,y)\,\text{d}s={\int }_{{C}_{1}}f(x,y)\,\text{d}s+{\int }_{{C}_{2}}f(x,y)\,\text{d}s+{\int }_{{C}_{3}}f(x,y)\,\text{d}s.
$$

- The line integral of unity with respect to arc length over $C$ is equal to the arc length $L$ of $C,$ i.e.,

$$
{\int }_{C}\,\text{d}s=L.
$$

The paths ${C}_{1}$ and ${C}_{3}$ are line segments of length $\frac{5}{2}.$ Therefore, we have

$$
{\int }_{{C}_{1}}\,\text{d}s={\int }_{{C}_{3}}\,\text{d}s=\frac{5}{2}.
$$

The path ${C}_{2}$ is the hypotenuse of a right triangle whose legs have lengths $\frac{5}{2}$ and $6.$ Therefore, we have

$$
{\int }_{{C}_{2}}\,\text{d}s=\sqrt{{\frac{5}{2}}^{2}+{6}^{2}}=\frac{13}{2}.
$$

Therefore,

$$
{\int }_{C}\,\text{d}s=\frac{5}{2}+\frac{13}{2}+\frac{5}{2}=\frac{23}{2}.
$$
