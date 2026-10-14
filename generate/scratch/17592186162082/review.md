# Source and generated review

Worker review; parent independent QA remains pending. All original prompt plots and five solution plots were inspected directly. Each generated entry has one fixed source-shaped solution. Zero source calculator flags were present; requirement remains unknown.


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


### Generated source/q-122481

Parameters/profile: `{"r": "2"}`, `q-122481`.

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186162082/assets/4e09c033ef07c22f3b49c44e2f8d9cce259a01a03ad4406c84650e61ac717947-prompt.png)

Calculate ${\int }_{C}\,\text{d}s,$ where $C$ is a path that traverses a semicircle of radius $2$ once in the counterclockwise direction, as shown above.

- $4 + 2 \pi$
- $8 + 4 \pi$
- $2 + 2 \pi$
- $4 + 4 \pi$
- $2 + 4 \pi$

The path $C$ is made up of two parts, as shown below:

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186162082/assets/4e09c033ef07c22f3b49c44e2f8d9cce259a01a03ad4406c84650e61ac717947-solution.png)

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

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186162082/assets/b18b51a69924c679c0cf84b47757ab93d0cb108df58a58e99f5a05da4909f63d-prompt.png)

Calculate ${\int }_{C}\,\text{d}s,$ where $C$ is a path that traverses a semicircle of radius $4$ once in the counterclockwise direction, as shown above.

- $8 + 4 \pi$
- $16 + 8 \pi$
- $8 + 8 \pi$
- $4 + 4 \pi$
- $4 + 8 \pi$

The path $C$ is made up of two parts, as shown below:

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186162082/assets/b18b51a69924c679c0cf84b47757ab93d0cb108df58a58e99f5a05da4909f63d-solution.png)

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


### Generated source/q-122484

Parameters/profile: `{"r": "2"}`, `q-122484`.

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186162082/assets/cfc6847819f68a554e011fd9f23f406c5f7e8247b00c8cade03b9a06f162ffb5-prompt.png)

Calculate $\displaystyle \int_{C}ds$, where $C$ is a path that traverses a circular segment of radius $2$ once in the counterclockwise direction, as shown above.

- $\sqrt{2} + \pi$
- $2 \sqrt{2} + \pi$
- $\frac{\pi}{2} + \sqrt{3}$
- $3 \sqrt{2} + 2 \pi$
- $\sqrt{2} + \frac{\pi}{2}$

The path $C$ is made up of two parts, as shown below:

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186162082/assets/cfc6847819f68a554e011fd9f23f406c5f7e8247b00c8cade03b9a06f162ffb5-solution.png)

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

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186162082/assets/a1ea736773218a2ba02e82541ad03e120cc47b8239b61da0293232d7196901fa-prompt.png)

Calculate $\displaystyle \int_{C}ds$, where $C$ is a path that traverses a circular segment of radius $4$ once in the counterclockwise direction, as shown above.

- $2 \sqrt{2} + 2 \pi$
- $4 \sqrt{2} + 2 \pi$
- $6 \sqrt{2} + 4 \pi$
- $\pi + 2 \sqrt{3}$
- $2 \sqrt{2} + \pi$

The path $C$ is made up of two parts, as shown below:

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186162082/assets/a1ea736773218a2ba02e82541ad03e120cc47b8239b61da0293232d7196901fa-solution.png)

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


### Generated source/q-122828

Parameters/profile: `{"a": "3", "b": "4"}`, `q-122828`.

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186162082/assets/83462c9bbc69e41122f2f5c8ff18d24da2ccb3dd066dd9e673410809300be383-prompt.png)

Calculate ${\int }_{C}\,\text{d}s,$ where $C$ is the path shown above.

- $11$
- $12$
- $9$
- $10$
- $8$

The path $C$ is made up of three parts, as shown below:

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186162082/assets/83462c9bbc69e41122f2f5c8ff18d24da2ccb3dd066dd9e673410809300be383-solution.png)

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

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186162082/assets/2e6bfad638e45e1f48e5e930e737ebe57f5f925578cec23c2905f0894ca4430d-prompt.png)

Calculate ${\int }_{C}\,\text{d}s,$ where $C$ is the path shown above.

- $22$
- $24$
- $20$
- $18$
- $16$

The path $C$ is made up of three parts, as shown below:

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186162082/assets/2e6bfad638e45e1f48e5e930e737ebe57f5f925578cec23c2905f0894ca4430d-solution.png)

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


### Generated source/q-122843

Parameters/profile: `{"r": "2"}`, `q-122843`.

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186162082/assets/fc878bf96b0ccec5b9ec489ea965340f8bcf4666a715823f7793f942cbc3f305-prompt.png)

Calculate ${\int }_{C}\,\text{d}s,$ where $C$ is the path shown above.

- $4 + 3 \pi$
- $2 + 3 \pi$
- $1 + 4 \pi$
- $2 + \pi$
- $3 + 2 \pi$

The path $C$ is made up of two parts, as shown below:

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186162082/assets/fc878bf96b0ccec5b9ec489ea965340f8bcf4666a715823f7793f942cbc3f305-solution.png)

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

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186162082/assets/77369a6a1304aeb3222961bfb4000987398e5cb7ccdd210b505d5b1b5836498f-prompt.png)

Calculate ${\int }_{C}\,\text{d}s,$ where $C$ is the path shown above.

- $8 + 6 \pi$
- $4 + 6 \pi$
- $4 + 2 \pi$
- $2 + 8 \pi$
- $6 + 4 \pi$

The path $C$ is made up of two parts, as shown below:

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186162082/assets/77369a6a1304aeb3222961bfb4000987398e5cb7ccdd210b505d5b1b5836498f-solution.png)

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


### Generated source/q-122845

Parameters/profile: `{"a": "3", "b": "2", "h": "4"}`, `q-122845`.

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186162082/assets/218d1c965665d841a24326bcb772258d4e032941e9659aabc2ecf43658221332-prompt.png)

Calculate ${\int }_{C}\,\text{d}s,$ where $C$ is the path shown above.

- $2 \sqrt{5} + 6$
- $4 + 2 \sqrt{5}$
- $9$
- $10$
- $2 \sqrt{5} + 5$

The path $C$ is made up of two parts, as shown below:

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186162082/assets/218d1c965665d841a24326bcb772258d4e032941e9659aabc2ecf43658221332-solution.png)

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

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186162082/assets/8dd1b8e2ecbcc9bc27218d378b33705c77465d5f1020eaa19c50f36e7db58943-prompt.png)

Calculate ${\int }_{C}\,\text{d}s,$ where $C$ is the path shown above.

- $4 \sqrt{5} + 12$
- $8 + 4 \sqrt{5}$
- $20$
- $18$
- $4 \sqrt{5} + 10$

The path $C$ is made up of two parts, as shown below:

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186162082/assets/8dd1b8e2ecbcc9bc27218d378b33705c77465d5f1020eaa19c50f36e7db58943-solution.png)

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


### Generated source/q-122850

Parameters/profile: `{"r": "4"}`, `q-122850`.

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186162082/assets/ec3f6c71d0429436a92f26e7aa7ae5a4d6fb3e3c44d4baa670d929d0ccc438aa-prompt.png)

Calculate ${\int }_{C}\,\text{d}s,$ where $C$ is the path shown above.

- $\frac{\pi}{4} + \sqrt{2}$
- $2 \sqrt{2} + 4 \pi$
- $\sqrt{2} + \frac{3 \pi}{4}$
- $4 \sqrt{2} + 2 \pi$
- $3 \sqrt{2} + 2 \pi$

The path $C$ is made up of two parts, as shown below:

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186162082/assets/ec3f6c71d0429436a92f26e7aa7ae5a4d6fb3e3c44d4baa670d929d0ccc438aa-solution.png)

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

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186162082/assets/c52f573df24b41ca4a05317a827f49f7baef9324780f94ef2b60644850358a47-prompt.png)

Calculate ${\int }_{C}\,\text{d}s,$ where $C$ is the path shown above.

- $\frac{\pi}{2} + 2 \sqrt{2}$
- $4 \sqrt{2} + 8 \pi$
- $8 \sqrt{2} + 4 \pi$
- $2 \sqrt{2} + \frac{3 \pi}{2}$
- $6 \sqrt{2} + 4 \pi$

The path $C$ is made up of two parts, as shown below:

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186162082/assets/c52f573df24b41ca4a05317a827f49f7baef9324780f94ef2b60644850358a47-solution.png)

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

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186162082/assets/a801a97b972547e12e0ffe0ac1e182c74f3d2966c60ac0ed2c4c20a22ffa4900-prompt.png)

Calculate ${\int }_{C}\,\text{d}s,$ where $C$ is a path that traverses a semicircle of radius $7$ once in the counterclockwise direction, as shown above.

- $7 \pi + 28$
- $14$
- $7 \pi$
- $14 + 7 \pi$
- $14 + 14 \pi$

The path $C$ is made up of two parts, as shown below:

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186162082/assets/a801a97b972547e12e0ffe0ac1e182c74f3d2966c60ac0ed2c4c20a22ffa4900-solution.png)

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

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186162082/assets/7d4ffd818da8c9aba458feec6aca0d5cd51ea3c906f92bda2137b7538c75e1b9-prompt.png)

Calculate ${\int }_{C}\,\text{d}s,$ where $C$ is a path that traverses a semicircle of radius $3$ once in the counterclockwise direction, as shown above.

- $6$
- $6 + 6 \pi$
- $3 \pi$
- $6 + 3 \pi$
- $3 \pi + 12$

The path $C$ is made up of two parts, as shown below:

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186162082/assets/7d4ffd818da8c9aba458feec6aca0d5cd51ea3c906f92bda2137b7538c75e1b9-solution.png)

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

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186162082/assets/09995458e946894631c6ca08096f145b78cc902ec7e88445ba6a53782c0bc669-prompt.png)

Calculate ${\int }_{C}\,\text{d}s,$ where $C$ is the path shown above.

- $14 + \frac{21 \pi}{2}$
- $7$
- $\frac{21 \pi}{2}$
- $7 + \frac{21 \pi}{2}$
- $7 + 21 \pi$

The path $C$ is made up of two parts, as shown below:

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186162082/assets/09995458e946894631c6ca08096f145b78cc902ec7e88445ba6a53782c0bc669-solution.png)

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

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186162082/assets/6b825e121f91e2fc72ef0693987c7107fff8f77e86db8749e7739090994589b9-prompt.png)

Calculate ${\int }_{C}\,\text{d}s,$ where $C$ is the path shown above.

- $3$
- $3 + 9 \pi$
- $\frac{9 \pi}{2}$
- $3 + \frac{9 \pi}{2}$
- $6 + \frac{9 \pi}{2}$

The path $C$ is made up of two parts, as shown below:

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186162082/assets/6b825e121f91e2fc72ef0693987c7107fff8f77e86db8749e7739090994589b9-solution.png)

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

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186162082/assets/8067898e2a5c3fc618ec3be496c2065808126502e11c252300acad426043b840-prompt.png)

Calculate $\displaystyle \int_{C}ds$, where $C$ is a path that traverses a circular segment of radius $7$ once in the counterclockwise direction, as shown above.

- $\frac{7 \pi}{2} + 14 \sqrt{2}$
- $7 \sqrt{2}$
- $\frac{7 \pi}{2}$
- $7 \sqrt{2} + \frac{7 \pi}{2}$
- $7 \sqrt{2} + 7 \pi$

The path $C$ is made up of two parts, as shown below:

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186162082/assets/8067898e2a5c3fc618ec3be496c2065808126502e11c252300acad426043b840-solution.png)

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

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186162082/assets/ae3d630fee8f5dbef4121171e402fc882974f859fbb2c1f7b5802fb6d5dcfb3b-prompt.png)

Calculate $\displaystyle \int_{C}ds$, where $C$ is a path that traverses a circular segment of radius $3$ once in the counterclockwise direction, as shown above.

- $3 \sqrt{2}$
- $3 \sqrt{2} + 3 \pi$
- $\frac{3 \pi}{2}$
- $3 \sqrt{2} + \frac{3 \pi}{2}$
- $\frac{3 \pi}{2} + 6 \sqrt{2}$

The path $C$ is made up of two parts, as shown below:

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186162082/assets/ae3d630fee8f5dbef4121171e402fc882974f859fbb2c1f7b5802fb6d5dcfb3b-solution.png)

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

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186162082/assets/2ee0b22b838f254b56b2aa1abc72589450b68a7578c91c4cd462e56a9fdab1b7-prompt.png)

Calculate ${\int }_{C}\,\text{d}s,$ where $C$ is the path shown above.

- $57$
- $24$
- $9$
- $33$
- $42$

The path $C$ is made up of three parts, as shown below:

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186162082/assets/2ee0b22b838f254b56b2aa1abc72589450b68a7578c91c4cd462e56a9fdab1b7-solution.png)

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

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186162082/assets/03094198c38bec46787b6b7f57ee7e6f14a783cced1d525d52597babd0b3e36b-prompt.png)

Calculate ${\int }_{C}\,\text{d}s,$ where $C$ is the path shown above.

- $18$
- $28$
- $5$
- $23$
- $41$

The path $C$ is made up of three parts, as shown below:

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186162082/assets/03094198c38bec46787b6b7f57ee7e6f14a783cced1d525d52597babd0b3e36b-solution.png)

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

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186162082/assets/6b3551a81ee5aed87516737ba6eebf11e3ef8edb84a23e3d6d7027828a5406ee-prompt.png)

Calculate ${\int }_{C}\,\text{d}s,$ where $C$ is the path shown above.

- $\sqrt{85}$
- $10$
- $\sqrt{85} + 10$
- $10 + 2 \sqrt{85}$
- $\sqrt{85} + 20$

The path $C$ is made up of two parts, as shown below:

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186162082/assets/6b3551a81ee5aed87516737ba6eebf11e3ef8edb84a23e3d6d7027828a5406ee-solution.png)

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

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186162082/assets/54926e27236f6d66035a5007ab22aba49bd52824ee302f758f46fd19cb6cb955-prompt.png)

Calculate ${\int }_{C}\,\text{d}s,$ where $C$ is the path shown above.

- $2 \sqrt{13}$
- $2 \sqrt{13} + 10$
- $5$
- $5 + 2 \sqrt{13}$
- $5 + 4 \sqrt{13}$

The path $C$ is made up of two parts, as shown below:

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186162082/assets/54926e27236f6d66035a5007ab22aba49bd52824ee302f758f46fd19cb6cb955-solution.png)

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

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186162082/assets/cfa83e25729c9a292e4a9a3aec3c5a888dcd0a66ba3a4c6062fdb0c935136d85-prompt.png)

Calculate ${\int }_{C}\,\text{d}s,$ where $C$ is the path shown above.

- $\frac{7 \pi}{2} + 14 \sqrt{2}$
- $7 \sqrt{2}$
- $\frac{7 \pi}{2}$
- $7 \sqrt{2} + \frac{7 \pi}{2}$
- $7 \sqrt{2} + 7 \pi$

The path $C$ is made up of two parts, as shown below:

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186162082/assets/cfa83e25729c9a292e4a9a3aec3c5a888dcd0a66ba3a4c6062fdb0c935136d85-solution.png)

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

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186162082/assets/21c5d215a00f891c3b598236817231697767c3ddc72e1e978ce5a6fc28baa2da-prompt.png)

Calculate ${\int }_{C}\,\text{d}s,$ where $C$ is the path shown above.

- $3 \sqrt{2}$
- $3 \sqrt{2} + 3 \pi$
- $\frac{3 \pi}{2}$
- $3 \sqrt{2} + \frac{3 \pi}{2}$
- $\frac{3 \pi}{2} + 6 \sqrt{2}$

The path $C$ is made up of two parts, as shown below:

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186162082/assets/21c5d215a00f891c3b598236817231697767c3ddc72e1e978ce5a6fc28baa2da-solution.png)

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

Parameters: `{"r": "17/3"}`.

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186162082/assets/7e4148fbc4e02629d2f1fc7ccdcf5035a56ea9d1adc289861f55ee2d198fdc16-prompt.png)

Calculate ${\int }_{C}\,\text{d}s,$ where $C$ is the path shown above.

- $\frac{17 \pi}{6} + \frac{34 \sqrt{2}}{3}$
- $\frac{17 \sqrt{2}}{3}$
- $\frac{17 \pi}{6}$
- $\frac{17 \sqrt{2}}{3} + \frac{17 \pi}{6}$
- $\frac{17 \sqrt{2}}{3} + \frac{17 \pi}{3}$

The path $C$ is made up of two parts, as shown below:

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186162082/assets/7e4148fbc4e02629d2f1fc7ccdcf5035a56ea9d1adc289861f55ee2d198fdc16-solution.png)

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

The path ${C}_{1}$ is a quarter of a circle of radius $r=\frac{17}{3}.$ Therefore, we have

$$
{\int }_{{C}_{1}}\,\text{d}s=\frac{1}{4}(2\pi r)=\frac{17 \pi}{6} .
$$

The path ${C}_{2}$ is the hypotenuse of a right triangle where both legs have a length of $\frac{17}{3}.$ Therefore, we have

$$
{\int }_{{C}_{2}}\,\text{d}s=\sqrt{{\frac{17}{3}}^{2}+{\frac{17}{3}}^{2}}=\frac{17 \sqrt{2}}{3}.
$$

Therefore,

$$
{\int }_{C}\,\text{d}s=\frac{17 \pi}{6}+\frac{17 \sqrt{2}}{3}=\frac{17}{6}(\pi+2\sqrt{2}).
$$


### hard/quarter_open/1

Parameters: `{"r": "17/2"}`.

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186162082/assets/22003bd7dcb82f4e3d5cfccbc2e45ddf07e553466dce3ca79fdd6e5995a55b2e-prompt.png)

Calculate ${\int }_{C}\,\text{d}s,$ where $C$ is the path shown above.

- $\frac{17 \sqrt{2}}{2}$
- $\frac{17 \sqrt{2}}{2} + \frac{17 \pi}{2}$
- $\frac{17 \pi}{4}$
- $\frac{17 \sqrt{2}}{2} + \frac{17 \pi}{4}$
- $\frac{17 \pi}{4} + 17 \sqrt{2}$

The path $C$ is made up of two parts, as shown below:

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186162082/assets/22003bd7dcb82f4e3d5cfccbc2e45ddf07e553466dce3ca79fdd6e5995a55b2e-solution.png)

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

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186162082/assets/1a44af6424ff3a1b6f4b743a2e12ecc8d5ba7f80ce32e31ba5a198855679aa3f-prompt.png)

Calculate ${\int }_{C}\,\text{d}s,$ where $C$ is the path shown above.

- $\frac{19}{3}$
- $\frac{8}{3}$
- $1$
- $\frac{11}{3}$
- $\frac{14}{3}$

The path $C$ is made up of three parts, as shown below:

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186162082/assets/1a44af6424ff3a1b6f4b743a2e12ecc8d5ba7f80ce32e31ba5a198855679aa3f-solution.png)

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

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186162082/assets/ebc8dc5df98fd9f7c37e96a051bda9c278b31e1133040a5da8ddf5e71476b05f-prompt.png)

Calculate ${\int }_{C}\,\text{d}s,$ where $C$ is the path shown above.

- $9$
- $14$
- $\frac{5}{2}$
- $\frac{23}{2}$
- $\frac{41}{2}$

The path $C$ is made up of three parts, as shown below:

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186162082/assets/ebc8dc5df98fd9f7c37e96a051bda9c278b31e1133040a5da8ddf5e71476b05f-solution.png)

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
