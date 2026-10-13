# Source and variant review

Original capture: math basis 1356. Original payloads remain in source.json. q-105893 has an authored moderate level, correct designation and solution; these are not observed matches.

## Original q-105890

Parameters: `{"a": 500, "k": 2, "below": 400, "above": 600}`. observed

## hard — ivp_integer

Which of the following initial value problems is an inhibited decay problem?



- $\frac{dy}{dt}=-2y(y-500),\,y(0)=400$

- $\frac{dy}{dt}=-2(y-500),\,y(0)=400$

- $\frac{dy}{dt}=-2(y-500),\,y(0)=600$ ✓

- $\frac{dy}{dt}=2(y-500),\,y(0)=600$

- $\frac{dy}{dt}=2y(y-500),\,y(0)=600$

An inhibited decay initial value problem has the form

$$
\frac{dy}{dt}=-k(y-a),\,y(0)={y}_{0}
$$

where $k>0$ is a constant of proportionality, and $y>a$ for all $t>0.$

From the given options, the only inhibited decay problem is

$$
\frac{dy}{dt}=-2(y-500),\,y(0)=600.
$$

In this case, $k=2,a=500,$ and ${y}_{0}=600.$ Notice that ${y}_{0}>a,$ which is required for inhibited decay. 

The other options do not represent inhibited decay. In particular, the initial value problem

$$
\frac{dy}{dt}=-2(y-500),\,y(0)=400,
$$

does *not* represent inhibited decay model because ${y}_{0}=400<a=500.$

## Original q-105893

Parameters: `{"a": 40, "k": 20}`. authored repair; structurally matches rated moderate sources

## moderate — expanded_spaced

Given that $y > 40$ and $t > 0$, which of the following is an inhibited decay equation?



- $\frac{dy}{dt} = 800 - 20y^{2}$

- $\frac{dy}{dt} = 800y - 20y^{2}$

- $\frac{dy}{dt} = 20y^{2} - 800$

- $\frac{dy}{dt} = 800 - 20y$ ✓

- $\frac{dy}{dt} = 800 + 20y$

An inhibited decay equation has the form

$$
\frac{dy}{dt}=-k(y-a),
$$

where $k>0$ is a constant of proportionality, and $y>a$ for all $t>0.$

From the given options, the only inhibited decay equation is

$$
\frac{dy}{dt}=800-20y.
$$

To see this, let's factor the right-hand side of the equation. This gives,

$$
\frac{dy}{dt}=-20(y-40).
$$

In this case, the constant of proportionality is $k=20,$ and $a=40.$ Note that for inhibited decay, we must have $y>40$ for all $t>0.$

## Original q-105898

Parameters: `{"a": 20, "k": 80}`. observed

## easy — factored_signs

Given that $y>20$ and $t>0,$ which of the following is an inhibited decay equation?



- $\frac{dy}{dt}=-80(20-y)$

- $\frac{dy}{dt}=80(y+20)$

- $\frac{dy}{dt}=-80y(20-y)$

- $\frac{dy}{dt}=-80(y-20)$ ✓

- $\frac{dy}{dt}=80y(y+20)$

An inhibited decay equation has the form

$$
\frac{dy}{dt}=-k(y-a),
$$

where $k>0$ is a constant of proportionality, and $y>a$ for all $t>0.$

From the given options, the only inhibited decay equation is

$$
\frac{dy}{dt}=-80(y-20).
$$

In this case, the constant of proportionality is $k=80,$ and $a=20.$ Note that for inhibited decay, we must have $y>20$ for all $t>0.$

## Original q-106647

Parameters: `{"a": 9, "k": 5}`. observed

## easy — factored_powers

Given that $y>9$ and $t>0,$ which of the following is an inhibited decay equation?



- $\frac{dy}{dt}=-5(9-y)$

- $\frac{dy}{dt}=-5y(y+9)$

- $\frac{dy}{dt}=-5{y}^{2}(y-9)$

- $\frac{dy}{dt}=-5({y}^{2}-9)$

- $\frac{dy}{dt}=-5(y-9)$ ✓

An inhibited decay equation has the form

$$
\frac{dy}{dt}=-k(y-a),
$$

where $k>0$ is a constant of proportionality, and $y>a$ for all $t>0.$

From the given options, the only inhibited decay equation is

$$
\frac{dy}{dt}=-5(y-9).
$$

In this case, the constant of proportionality is $k=5,$ and $a=9.$ Note that for inhibited decay, we must have $y>9$ for all $t>0.$

## Original q-106651

Parameters: `{"a": 8, "k": 22}`. observed

## moderate — expanded

Given that $y>8$ and $t>0,$ which of the following is an inhibited decay equation?



- $\frac{dy}{dt}=22{y}^{2}-176$

- $\frac{dy}{dt}=176-22{y}^{2}$

- $\frac{dy}{dt}=176y-22{y}^{2}$

- $\frac{dy}{dt}=176+22y$

- $\frac{dy}{dt}=176-22y$ ✓

An inhibited decay equation has the form

$$
\frac{dy}{dt}=-k(y-a),
$$

where $k>0$ is a constant of proportionality, and $y>a$ for all $t>0.$

From the given options, the only inhibited decay equation is

$$
\frac{dy}{dt}=176-22y.
$$

To see this, let's factor the right-hand side of the equation. This gives,

$$
\frac{dy}{dt}=-22(y-8).
$$

In this case, the constant of proportionality is $k=22,$ and $a=8.$ Note that for inhibited decay, we must have $y>8$ for all $t>0.$

## Original q-15591

Parameters: `{"a": 1500, "k": "0.002", "below": 1000, "above": 3000}`. observed

## hard — ivp_decimal_grouped

Which of the following initial value problems is an inhibited decay problem?



- $\frac{dy}{dt}=0.002y(y-1\,500),\,y(0)=3\,000$

- $\frac{dy}{dt}=-0.002y(y-1\,500),\,y(0)=1\,000$

- $\frac{dy}{dt}=-0.002(y-1\,500),\,y(0)=3\,000$ ✓

- $\frac{dy}{dt}=-0.002(y-1\,500),\,y(0)=1\,000$

- $\frac{dy}{dt}=0.002(y-1\,500),\,y(0)=3\,000$

An inhibited decay initial value problem has the form

$$
\frac{dy}{dt}=-k(y-a),\,y(0)={y}_{0}
$$

where $k>0$ is a constant of proportionality, and $y>a$ for all $t>0.$

From the given options, the only inhibited decay problem is

$$
\frac{dy}{dt}=-0.002(y-1\,500),\,y(0)=3\,000.
$$

In this case, $k=0.002,a=1\,500,$ and ${y}_{0}=3\,000.$ Notice that ${y}_{0}>a,$ which is required for inhibited decay. 

The other options do not represent inhibited decay. In particular, the initial value problem

$$
\frac{dy}{dt}=-0.002(y-1\,500),\,y(0)=1\,000,
$$

does *not* represent inhibited decay model because ${y}_{0}=1\,000<a=1\,500.$

## Original q-106654

Parameters: `{"a": 30, "k": 28}`. observed

## moderate — expanded

Given that $y>30$ and $t>0,$ which of the following is an inhibited decay equation?



- $\frac{dy}{dt}=28{y}^{2}-840$

- $\frac{dy}{dt}=840-28{y}^{2}$

- $\frac{dy}{dt}=840y-28{y}^{2}$

- $\frac{dy}{dt}=840+28y$

- $\frac{dy}{dt}=840-28y$ ✓

An inhibited decay equation has the form

$$
\frac{dy}{dt}=-k(y-a),
$$

where $k>0$ is a constant of proportionality, and $y>a$ for all $t>0.$

From the given options, the only inhibited decay equation is

$$
\frac{dy}{dt}=840-28y.
$$

To see this, let's factor the right-hand side of the equation. This gives,

$$
\frac{dy}{dt}=-28(y-30).
$$

In this case, the constant of proportionality is $k=28,$ and $a=30.$ Note that for inhibited decay, we must have $y>30$ for all $t>0.$

## Generated parameter variant (authored sampling bounds)

## easy — factored_signs

Given that $y>62$ and $t>0,$ which of the following is an inhibited decay equation?



- $\frac{dy}{dt}=36y(y+62)$

- $\frac{dy}{dt}=-36y(62-y)$

- $\frac{dy}{dt}=36(y+62)$

- $\frac{dy}{dt}=-36(62-y)$

- $\frac{dy}{dt}=-36(y-62)$ ✓

An inhibited decay equation has the form

$$
\frac{dy}{dt}=-k(y-a),
$$

where $k>0$ is a constant of proportionality, and $y>a$ for all $t>0.$

From the given options, the only inhibited decay equation is

$$
\frac{dy}{dt}=-36(y-62).
$$

In this case, the constant of proportionality is $k=36,$ and $a=62.$ Note that for inhibited decay, we must have $y>62$ for all $t>0.$

## Generated parameter variant (authored sampling bounds)

## easy — factored_signs

Given that $y>3$ and $t>0,$ which of the following is an inhibited decay equation?



- $\frac{dy}{dt}=-62y(3-y)$

- $\frac{dy}{dt}=-62(3-y)$

- $\frac{dy}{dt}=-62(y-3)$ ✓

- $\frac{dy}{dt}=62y(y+3)$

- $\frac{dy}{dt}=62(y+3)$

An inhibited decay equation has the form

$$
\frac{dy}{dt}=-k(y-a),
$$

where $k>0$ is a constant of proportionality, and $y>a$ for all $t>0.$

From the given options, the only inhibited decay equation is

$$
\frac{dy}{dt}=-62(y-3).
$$

In this case, the constant of proportionality is $k=62,$ and $a=3.$ Note that for inhibited decay, we must have $y>3$ for all $t>0.$

## Generated parameter variant (authored sampling bounds)

## easy — factored_powers

Given that $y>62$ and $t>0,$ which of the following is an inhibited decay equation?



- $\frac{dy}{dt}=-36(y-62)$ ✓

- $\frac{dy}{dt}=-36{y}^{2}(y-62)$

- $\frac{dy}{dt}=-36y(y+62)$

- $\frac{dy}{dt}=-36(62-y)$

- $\frac{dy}{dt}=-36({y}^{2}-62)$

An inhibited decay equation has the form

$$
\frac{dy}{dt}=-k(y-a),
$$

where $k>0$ is a constant of proportionality, and $y>a$ for all $t>0.$

From the given options, the only inhibited decay equation is

$$
\frac{dy}{dt}=-36(y-62).
$$

In this case, the constant of proportionality is $k=36,$ and $a=62.$ Note that for inhibited decay, we must have $y>62$ for all $t>0.$

## Generated parameter variant (authored sampling bounds)

## easy — factored_powers

Given that $y>3$ and $t>0,$ which of the following is an inhibited decay equation?



- $\frac{dy}{dt}=-62{y}^{2}(y-3)$

- $\frac{dy}{dt}=-62(3-y)$

- $\frac{dy}{dt}=-62({y}^{2}-3)$

- $\frac{dy}{dt}=-62(y-3)$ ✓

- $\frac{dy}{dt}=-62y(y+3)$

An inhibited decay equation has the form

$$
\frac{dy}{dt}=-k(y-a),
$$

where $k>0$ is a constant of proportionality, and $y>a$ for all $t>0.$

From the given options, the only inhibited decay equation is

$$
\frac{dy}{dt}=-62(y-3).
$$

In this case, the constant of proportionality is $k=62,$ and $a=3.$ Note that for inhibited decay, we must have $y>3$ for all $t>0.$

## Generated parameter variant (authored sampling bounds)

## moderate — expanded

Given that $y>62$ and $t>0,$ which of the following is an inhibited decay equation?



- $\frac{dy}{dt}=2232-36y$ ✓

- $\frac{dy}{dt}=2232y-36{y}^{2}$

- $\frac{dy}{dt}=2232-36{y}^{2}$

- $\frac{dy}{dt}=36{y}^{2}-2232$

- $\frac{dy}{dt}=2232+36y$

An inhibited decay equation has the form

$$
\frac{dy}{dt}=-k(y-a),
$$

where $k>0$ is a constant of proportionality, and $y>a$ for all $t>0.$

From the given options, the only inhibited decay equation is

$$
\frac{dy}{dt}=2232-36y.
$$

To see this, let's factor the right-hand side of the equation. This gives,

$$
\frac{dy}{dt}=-36(y-62).
$$

In this case, the constant of proportionality is $k=36,$ and $a=62.$ Note that for inhibited decay, we must have $y>62$ for all $t>0.$

## Generated parameter variant (authored sampling bounds)

## moderate — expanded

Given that $y>3$ and $t>0,$ which of the following is an inhibited decay equation?



- $\frac{dy}{dt}=186y-62{y}^{2}$

- $\frac{dy}{dt}=62{y}^{2}-186$

- $\frac{dy}{dt}=186+62y$

- $\frac{dy}{dt}=186-62y$ ✓

- $\frac{dy}{dt}=186-62{y}^{2}$

An inhibited decay equation has the form

$$
\frac{dy}{dt}=-k(y-a),
$$

where $k>0$ is a constant of proportionality, and $y>a$ for all $t>0.$

From the given options, the only inhibited decay equation is

$$
\frac{dy}{dt}=186-62y.
$$

To see this, let's factor the right-hand side of the equation. This gives,

$$
\frac{dy}{dt}=-62(y-3).
$$

In this case, the constant of proportionality is $k=62,$ and $a=3.$ Note that for inhibited decay, we must have $y>3$ for all $t>0.$

## Generated parameter variant (authored sampling bounds)

## moderate — expanded_spaced

Given that $y > 62$ and $t > 0$, which of the following is an inhibited decay equation?



- $\frac{dy}{dt} = 2232 + 36y$

- $\frac{dy}{dt} = 36y^{2} - 2232$

- $\frac{dy}{dt} = 2232y - 36y^{2}$

- $\frac{dy}{dt} = 2232 - 36y^{2}$

- $\frac{dy}{dt} = 2232 - 36y$ ✓

An inhibited decay equation has the form

$$
\frac{dy}{dt}=-k(y-a),
$$

where $k>0$ is a constant of proportionality, and $y>a$ for all $t>0.$

From the given options, the only inhibited decay equation is

$$
\frac{dy}{dt}=2232-36y.
$$

To see this, let's factor the right-hand side of the equation. This gives,

$$
\frac{dy}{dt}=-36(y-62).
$$

In this case, the constant of proportionality is $k=36,$ and $a=62.$ Note that for inhibited decay, we must have $y>62$ for all $t>0.$

## Generated parameter variant (authored sampling bounds)

## moderate — expanded_spaced

Given that $y > 3$ and $t > 0$, which of the following is an inhibited decay equation?



- $\frac{dy}{dt} = 62y^{2} - 186$

- $\frac{dy}{dt} = 186 - 62y^{2}$

- $\frac{dy}{dt} = 186 - 62y$ ✓

- $\frac{dy}{dt} = 186 + 62y$

- $\frac{dy}{dt} = 186y - 62y^{2}$

An inhibited decay equation has the form

$$
\frac{dy}{dt}=-k(y-a),
$$

where $k>0$ is a constant of proportionality, and $y>a$ for all $t>0.$

From the given options, the only inhibited decay equation is

$$
\frac{dy}{dt}=186-62y.
$$

To see this, let's factor the right-hand side of the equation. This gives,

$$
\frac{dy}{dt}=-62(y-3).
$$

In this case, the constant of proportionality is $k=62,$ and $a=3.$ Note that for inhibited decay, we must have $y>3$ for all $t>0.$

## Generated parameter variant (authored sampling bounds)

## hard — ivp_integer

Which of the following initial value problems is an inhibited decay problem?



- $\frac{dy}{dt}=0.025(y-1000),\,y(0)=2000$

- $\frac{dy}{dt}=-0.025y(y-1000),\,y(0)=400$

- $\frac{dy}{dt}=-0.025(y-1000),\,y(0)=2000$ ✓

- $\frac{dy}{dt}=-0.025(y-1000),\,y(0)=400$

- $\frac{dy}{dt}=0.025y(y-1000),\,y(0)=2000$

An inhibited decay initial value problem has the form

$$
\frac{dy}{dt}=-k(y-a),\,y(0)={y}_{0}
$$

where $k>0$ is a constant of proportionality, and $y>a$ for all $t>0.$

From the given options, the only inhibited decay problem is

$$
\frac{dy}{dt}=-0.025(y-1000),\,y(0)=2000.
$$

In this case, $k=0.025,a=1000,$ and ${y}_{0}=2000.$ Notice that ${y}_{0}>a,$ which is required for inhibited decay. 

The other options do not represent inhibited decay. In particular, the initial value problem

$$
\frac{dy}{dt}=-0.025(y-1000),\,y(0)=400,
$$

does *not* represent inhibited decay model because ${y}_{0}=400<a=1000.$

## Generated parameter variant (authored sampling bounds)

## hard — ivp_integer

Which of the following initial value problems is an inhibited decay problem?



- $\frac{dy}{dt}=0.5(y-20),\,y(0)=60$

- $\frac{dy}{dt}=-0.5y(y-20),\,y(0)=16$

- $\frac{dy}{dt}=0.5y(y-20),\,y(0)=60$

- $\frac{dy}{dt}=-0.5(y-20),\,y(0)=16$

- $\frac{dy}{dt}=-0.5(y-20),\,y(0)=60$ ✓

An inhibited decay initial value problem has the form

$$
\frac{dy}{dt}=-k(y-a),\,y(0)={y}_{0}
$$

where $k>0$ is a constant of proportionality, and $y>a$ for all $t>0.$

From the given options, the only inhibited decay problem is

$$
\frac{dy}{dt}=-0.5(y-20),\,y(0)=60.
$$

In this case, $k=0.5,a=20,$ and ${y}_{0}=60.$ Notice that ${y}_{0}>a,$ which is required for inhibited decay. 

The other options do not represent inhibited decay. In particular, the initial value problem

$$
\frac{dy}{dt}=-0.5(y-20),\,y(0)=16,
$$

does *not* represent inhibited decay model because ${y}_{0}=16<a=20.$

## Generated parameter variant (authored sampling bounds)

## hard — ivp_decimal_grouped

Which of the following initial value problems is an inhibited decay problem?



- $\frac{dy}{dt}=-0.025(y-1\,000),\,y(0)=400$

- $\frac{dy}{dt}=0.025y(y-1\,000),\,y(0)=2\,000$

- $\frac{dy}{dt}=-0.025(y-1\,000),\,y(0)=2\,000$ ✓

- $\frac{dy}{dt}=-0.025y(y-1\,000),\,y(0)=400$

- $\frac{dy}{dt}=0.025(y-1\,000),\,y(0)=2\,000$

An inhibited decay initial value problem has the form

$$
\frac{dy}{dt}=-k(y-a),\,y(0)={y}_{0}
$$

where $k>0$ is a constant of proportionality, and $y>a$ for all $t>0.$

From the given options, the only inhibited decay problem is

$$
\frac{dy}{dt}=-0.025(y-1\,000),\,y(0)=2\,000.
$$

In this case, $k=0.025,a=1\,000,$ and ${y}_{0}=2\,000.$ Notice that ${y}_{0}>a,$ which is required for inhibited decay. 

The other options do not represent inhibited decay. In particular, the initial value problem

$$
\frac{dy}{dt}=-0.025(y-1\,000),\,y(0)=400,
$$

does *not* represent inhibited decay model because ${y}_{0}=400<a=1\,000.$

## Generated parameter variant (authored sampling bounds)

## hard — ivp_decimal_grouped

Which of the following initial value problems is an inhibited decay problem?



- $\frac{dy}{dt}=-0.5(y-20),\,y(0)=16$

- $\frac{dy}{dt}=0.5y(y-20),\,y(0)=60$

- $\frac{dy}{dt}=0.5(y-20),\,y(0)=60$

- $\frac{dy}{dt}=-0.5y(y-20),\,y(0)=16$

- $\frac{dy}{dt}=-0.5(y-20),\,y(0)=60$ ✓

An inhibited decay initial value problem has the form

$$
\frac{dy}{dt}=-k(y-a),\,y(0)={y}_{0}
$$

where $k>0$ is a constant of proportionality, and $y>a$ for all $t>0.$

From the given options, the only inhibited decay problem is

$$
\frac{dy}{dt}=-0.5(y-20),\,y(0)=60.
$$

In this case, $k=0.5,a=20,$ and ${y}_{0}=60.$ Notice that ${y}_{0}>a,$ which is required for inhibited decay. 

The other options do not represent inhibited decay. In particular, the initial value problem

$$
\frac{dy}{dt}=-0.5(y-20),\,y(0)=16,
$$

does *not* represent inhibited decay model because ${y}_{0}=16<a=20.$
