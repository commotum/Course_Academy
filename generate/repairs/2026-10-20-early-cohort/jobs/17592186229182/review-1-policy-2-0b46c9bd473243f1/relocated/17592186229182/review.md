# Originals (opaque/incomplete evidence, ineligible)

q-336439 | observed:q-336439 | unrated original | eligible=False

An aquarium initially holds $300L$ of water containing $6kg$ of dissolved minerals.
A solution containing $0.03kg/L$ of dissolved minerals is pumped into the aquarium at a rate of $24L/min$, while the completely mixed water is drained out at a rate of $36L/min$. If the amount of minerals $Q(t)$, in kilograms, in the tank $t$ minutes after pumping begins is given by
$Q(t) = α(1 - \frac{t}{25}) + β(1 - \frac{t}{25})^{3}$
where $α$ and $β$ are constants, what is the value of $α + β$?

> A scientific calculator is required to answer this question.

- $10$
- $15$
- $8$
- $12$
- $6$

[Original omits worked solution.]

---
q-336738 | observed:q-336738 | unrated original | eligible=False

A storage tank initially holds $600L$ of liquid containing $5kg$ of dissolved stabilizer.
A feed solution containing $0.04kg/L$ of the stabilizer is pumped into the tank at a rate of $15L/min$, while the completely mixed liquid is drained out at a rate of $10L/min$.
Find, rounded to two decimal places, the amount of stabilizer in the tank $10$ minutes after pumping begins.

> A scientific calculator is required to answer this question.

- $9.81kg$
- $9.18kg$
- $8.63kg$
- $8.21kg$
- $7.99kg$

[Original omits worked solution.]

---
q-336743 | observed:q-336743 | :question.difficulty/hard | eligible=False

A processing tank initially holds $420\,\text{L}$ of liquid containing $10\,\text{kg}$ of dissolved preservative.
A feed solution containing $0.05\,\text{kg/L}$ of the preservative is pumped into the tank at a rate of $18\,\text{L/min},$ while the completely mixed liquid is drained out at a rate of $12\,\text{L/min}.$
Find, rounded to two decimal places, the amount of preservative in the tank $15$ minutes after pumping begins.

- $18.04\,\text{kg}$ [correct]
- $17.94\,\text{kg}$
- $17.34\,\text{kg}$
- $19.01\,\text{kg}$
- $18.42\,\text{kg}$

Let $Q$ be the amount of preservative in the tank at time $t,$ in minutes. Then, the derivative 

$$
\frac{dQ}{dt}
$$

describes how this amount changes with respect to time $t.$ This is equal to the rate at which preservative enters the tank minus the rate at which preservative leaves the tank.

$$
\frac{dQ}{dt}={Q}_{\text{in}}^{′}-{Q}_{\text{out}}^{′}
$$

Note that the units of $\frac{dQ}{dt},{Q}_{\text{in}}^{′}$ and ${Q}_{\text{out}}^{′}$ are $\text{kg}/\text{min}.$ Now, let's compute the required rates of change in steps.

**Step 1**: Calculating the rate at which preservative enters the tank.

Note that a feed solution containing $0.05\,\text{kg/L}$ of the preservative enters the tank at a rate of $18\,\text{L/min}.$ So, the rate at which the *preservative* enters the tank is 

$$
\begin{aligned}{Q}_{\text{in}}^{′} & =(0.05\,\frac{\text{kg}}{\text{L}})\cdot (18\,\frac{\text{L}}{\text{min}}) \\  & =(0.05\,\frac{\text{kg}}{\cancel{\text{L}}})\cdot (18\,\frac{\cancel{\text{L}}}{\text{min}}) \\  & =0.9\,\frac{\text{kg}}{\text{min}}.\end{aligned}
$$

**Step 2**: Calculating the rate at which preservative exits the tank.

To find the rate at which preservative leaves the tank, we must first determine the volume of liquid in the tank at time $t.$

The tank initially contains $420\,\text{L}$ of liquid; a solution enters at $18\,\text{L/min}$ and leaves at $12\,\text{L/min}.$
As a result, the volume of liquid in the tank after $t$ minutes is 

$$
420+18t-12t=(420+6t)\,\text{L}.
$$

Since $Q$ is the amount of preservative in the tank, the *concentration* of the mixed solution at time $t$ is

$$
\frac{Q}{420+6t}\,\text{kg/L}.
$$

Therefore, as the completely mixed liquid leaves at a rate of $12\,\text{L/min},$ *preservative* leaves at a rate of

$$
\begin{aligned}{Q}_{\text{out}}^{′} & =(12\,\frac{\text{L}}{\text{min}})\cdot (\frac{Q}{420+6t}\,\frac{\text{kg}}{\text{L}}) \\  & =(12\,\frac{\cancel{\text{L}}}{\text{min}})\cdot (\frac{Q}{420+6t}\,\frac{\text{kg}}{\cancel{\text{L}}}) \\  & =\frac{12Q}{420+6t}\,\frac{\text{kg}}{\text{min}} \\  & =\frac{2Q}{70+t}\,\frac{\text{kg}}{\text{min}}.\end{aligned}
$$

**Step 3**: Calculate the overall rate of change.

The rate of change equals the rate of entry minus the rate of exit. Therefore, 

$$
\begin{aligned}\frac{dQ}{dt} & ={Q}_{\text{in}}^{′}-{Q}_{\text{out}}^{′} \\  & =0.9-\frac{2Q}{70+t}\end{aligned}
$$

which gives the equation

$$
\begin{aligned}\frac{dQ}{dt}+\frac{2}{70+t}Q=0.9.\end{aligned}
$$

**Step 4**: Integrate the equation.

This is a first-order linear equation with variable coefficients. So we find the general solution using an integrating factor:

$$
\begin{aligned}I(t) & ={e}^{\int 2/(70+t)\,dt} \\  & ={e}^{2\operatorname{ln}⁡|70+t|} \\  & ={e}^{\operatorname{ln}⁡(70+t)^{2}} \\  & =(70+t)^{2}\end{aligned}
$$

Multiplying both sides of the differential equation by $I(t)=(70+t)^{2}$ yields

$$
\begin{aligned}(70+t)^{2}\cdot (\frac{dQ}{dt}+\frac{2}{70+t}Q) & =(70+t)^{2}\cdot 0.9 \\ (70+t)^{2}\frac{dQ}{dt}+2(70+t)Q & =0.9(70+t)^{2} \\ \frac{d}{dt}(Q(70+t)^{2}) & =0.9(70+t)^{2}.\end{aligned}
$$

Now, we integrate with respect to $t:$

$$
\begin{aligned}\int \frac{d}{dt}(Q(70+t)^{2})\,dt & =\int 0.9(70+t)^{2}\,dt \\ Q(70+t)^{2} & =0.9\cdot \frac{1}{3}(70+t)^{3}+C \\ Q(t) & =0.3(70+t)+\frac{C}{(70+t)^{2}}\end{aligned}
$$

Note that $C$ is a constant of integration.

We're told that the tank initially contains $10\,\text{kg}$ of preservative. So, we can apply the initial condition $Q(0)=10,$ and solve for $C:$

$$
\begin{aligned}Q(0) & =10 \\ 0.3(70+0)+\frac{C}{(70+0)^{2}} & =10 \\ 21+\frac{C}{{70}^{2}} & =10 \\ \frac{C}{{70}^{2}} & =-11 \\ C & =-11(70)^{2}\end{aligned}
$$

Finally, we obtain the following expression for $Q(t):$

$$
\begin{aligned}Q(t) & =0.3(70+t)-\frac{11(70)^{2}}{(70+t)^{2}} \\  & =0.3(70+t)-11{(\frac{70}{70+t})}^{2}.\end{aligned}
$$

Finally,  the amount of preservative in the tank $15$ minutes after pumping begins is

$$
\begin{aligned}Q(15) & =0.3(70+15)-11{(\frac{70}{70+15})}^{2} \\  & =25.5-11{(\frac{70}{85})}^{2} \\  & ≈18.04\,\text{kg},\end{aligned}
$$

rounded to two decimal places.

---
q-339394 | observed:q-339394 | :question.difficulty/moderate | eligible=False

A juice-processing tank initially holds $400\,\text{L}$ of liquid containing $4\,\text{kg}$ of dissolved sugar.
A solution containing $0.03\,\text{kg/L}$ of dissolved sugar is pumped into the tank at a rate of $20\,\text{L/min},$ while the completely mixed liquid is drained out at a rate of $30\,\text{L/min}.$ If the amount of sugar $Q(t),$ in kilograms, in the tank $t$ minutes after pumping begins is given by

$$
Q(t)=\alpha \,(1-\frac{t}{40})+\beta {(1-\frac{t}{40})}^{3}
$$

where $\alpha $ and $\beta $ are constants, what is the value of $\alpha -\beta ?$

- $30$
- $15$
- $20$ [correct]
- $24$
- $18$

Since $Q$ is the amount of salt in the tank at time $t,$ the derivative 

$$
\frac{dQ}{dt}
$$

describes how this amount changes with respect to time $t,$ in minutes. This is equal to the rate at which sugar enters the tank minus the rate at which sugar leaves the tank.

$$
\frac{dQ}{dt}={Q}_{\text{in}}^{′}-{Q}_{\text{out}}^{′}
$$

Note that the units of $\frac{dQ}{dt},{Q}_{\text{in}}^{′}$ and ${Q}_{\text{out}}^{′}$ are $\text{kg}/\text{min}.$ Now, let's compute the required rates of change in steps.

**Step 1**: Calculating the rate at which sugar enter the tank.

First, note that a liquid solution containing $0.03\,\text{kg/L}$ of sugar enters the tank at a rate of $20\,\text{L/min}.$ So, the rate at which the *sugar* enters the tank is 

$$
\begin{aligned}{Q}_{\text{in}}^{′} & =(0.03\,\frac{\text{kg}}{\text{L}})\cdot (20\,\frac{\text{L}}{\text{min}}) \\  & =(0.03\,\frac{\text{kg}}{\cancel{\text{L}}})\cdot (20\,\frac{\cancel{\text{L}}}{\text{min}}) \\  & =0.6\,\frac{\text{kg}}{\text{min}}.\end{aligned}
$$

**Step 2**: Calculating the rate at which sugar exit the tank.

To find the rate at which sugar leaves the tank, we must first determine the volume of liquid in the tank at time $t.$

The tank initially contains $400\,\text{L}$ of liquid; a solution enters at $20\,\text{L/min}$ and leaves at $30\,\text{L/min}.$
As a result, the amount of liquid in the tank after $t$ minutes is 

$$
400+20t-30t=(400-10t)\,\text{L}.
$$

Since $Q$ is the amount of sugar in the tank, the *concentration* of the mixed solution at time $t$ is

$$
\frac{Q}{400-10t}\,\text{kg/L}.
$$

Therefore, as the completely mixed liquid leaves at a rate of $30\,\text{L/min},$ *sugar* leaves at a rate of

$$
\begin{aligned}{Q}_{\text{out}}^{′} & =(30\,\frac{\text{L}}{\text{min}})\cdot (\frac{Q}{400-10t}\,\frac{\text{kg}}{\text{L}}) \\  & =(30\,\frac{\cancel{\text{L}}}{\text{min}})\cdot (\frac{Q}{400-10t}\,\frac{\text{kg}}{\cancel{\text{L}}}) \\  & =\frac{30Q}{400-10t}\,\frac{\text{kg}}{\text{min}} \\  & =\frac{3Q}{40-t}\,\frac{\text{kg}}{\text{min}}.\end{aligned}
$$

**Step 3**: Calculate the overall rate of change.

The rate of change equals the rate of entry minus the rate of exit. Therefore, 

$$
\begin{aligned}\frac{dQ}{dt} & ={Q}_{\text{in}}^{′}-{Q}_{\text{out}}^{′} \\  & =0.6-\frac{3Q}{40-t}\end{aligned}
$$

which gives the equation

$$
\begin{aligned}\frac{dQ}{dt}+\frac{3}{40-t}Q=0.6.\end{aligned}
$$

**Step 4**: Integrate the equation.

This is a first-order linear equation with variable coefficients. So we find the general solution using an integrating factor:

$$
\begin{aligned}I(t) & ={e}^{\int 3/(40-t)\,dt} \\  & ={e}^{-3\operatorname{ln}⁡|40-t|} \\  & ={e}^{\operatorname{ln}⁡(40-t)^{-3}} \\  & =(40-t)^{-3}\end{aligned}
$$

Multiplying both sides of the differential equation by $I(t)=(40-t)^{-3}$ yields

$$
\begin{aligned}(40-t)^{-3}\cdot (\frac{dQ}{dt}+\frac{3}{40-t}Q) & =(40-t)^{-3}\cdot 0.6 \\ (40-t)^{-3}\frac{dQ}{dt}+3(40-t)^{-4}Q & =0.6(40-t)^{-3} \\ \frac{d}{dt}(Q(40-t)^{-3}) & =0.6(40-t)^{-3}.\end{aligned}
$$

Now, we integrate with respect to $t:$

$$
\begin{aligned}\int \frac{d}{dt}(Q(40-t)^{-3})\,dt & =\int 0.6(40-t)^{-3}\,dt \\ Q(40-t)^{-3} & =0.6\cdot \frac{1}{2}(40-t)^{-2}+C \\ Q(t) & =0.3(40-t)+C(40-t)^{3}\end{aligned}
$$

Note that $C$ is a constant of integration.

We're told that the tank initially contains $4\,\text{kg}$ of sugar. So, we can apply the initial condition $Q(0)=4,$ and solve for $C:$

$$
\begin{aligned}Q(0) & =4 \\ C(40-0)^{3}+0.3(40-0) & =4 \\ C(40)^{3}+12 & =4 \\ C & =-\frac{8}{{40}^{3}}\end{aligned}
$$

Finally, we obtain the following expression for $Q(t):$

$$
\begin{aligned}Q(t) & =0.3(40-t)-\frac{8}{{40}^{3}}(40-t)^{3} \\  & =0.3\cdot 40\,(\frac{40-t}{40})-8{(\frac{40-t}{40})}^{3} \\  & =12\,(1-\frac{t}{40})-8{(1-\frac{t}{40})}^{3}.\end{aligned}
$$

Finally, we have $\alpha =12,\beta =-8,$ and

$$
\alpha -\beta =12-(-8)=20.
$$

---
q-339396 | observed:q-339396 | :question.difficulty/moderate | eligible=False

A fruit syrup tank initially holds $240\,\text{L}$ of liquid containing $7\,\text{kg}$ of dissolved sweetener.
A solution containing $0.05\,\text{kg/L}$ of dissolved sweetener is pumped into the tank at a rate of $24\,\text{L/min},$ while the completely mixed liquid is drained out at a rate of $32\,\text{L/min}.$ If the amount of sweetener $Q(t),$ in kilograms, in the tank $t$ minutes after pumping begins is given by

$$
Q(t)=\alpha \,(1-\frac{t}{30})+\beta {(1-\frac{t}{30})}^{4}
$$

where $\alpha $ and $\beta $ are constants, what is the value of $\alpha -\beta ?$

- $14$
- $26$
- $20$
- $29$
- $17$ [correct]

Since $Q$ is the amount of salt in the tank at time $t,$ the derivative 

$$
\frac{dQ}{dt}
$$

describes how this amount changes with respect to time $t,$ in minutes. This is equal to the rate at which sweetener enters the tank minus the rate at which sweetener leaves the tank.

$$
\frac{dQ}{dt}={Q}_{\text{in}}^{′}-{Q}_{\text{out}}^{′}
$$

Note that the units of $\frac{dQ}{dt},{Q}_{\text{in}}^{′}$ and ${Q}_{\text{out}}^{′}$ are $\text{kg}/\text{min}.$ Now, let's compute the required rates of change in steps.

**Step 1**: Calculating the rate at which sweetener enter the tank.

First, note that a solution containing $0.05\,\text{kg/L}$ of sweetener enters the tank at a rate of $24\,\text{L/min}.$ So, the rate at which the *sweetener* enters the tank is 

$$
\begin{aligned}{Q}_{\text{in}}^{′} & =(0.05\,\frac{\text{kg}}{\text{L}})\cdot (24\,\frac{\text{L}}{\text{min}}) \\  & =(0.05\,\frac{\text{kg}}{\cancel{\text{L}}})\cdot (24\,\frac{\cancel{\text{L}}}{\text{min}}) \\  & =1.2\,\frac{\text{kg}}{\text{min}}.\end{aligned}
$$

**Step 2**: Calculating the rate at which sweetener exit the tank.

To find the rate at which sweetener leaves the tank, we must first determine the volume of liquid in the tank at time $t.$

The tank initially contains $240\,\text{L}$ of liquid; a solution enters at $24\,\text{L/min}$ and leaves at $32\,\text{L/min}.$
As a result, the amount of liquid in the tank after $t$ minutes is 

$$
240+24t-32t=(240-8t)\,\text{L}.
$$

Since $Q$ is the amount of sweetener in the tank, the *concentration* of the mixed solution at time $t$ is

$$
\frac{Q}{240-8t}\,\text{kg/L}.
$$

Therefore, as the completely mixed liquid leaves at a rate of $32\,\text{L/min},$ *sweetener* leaves at a rate of

$$
\begin{aligned}{Q}_{\text{out}}^{′} & =(32\,\frac{\text{L}}{\text{min}})\cdot (\frac{Q}{240-8t}\,\frac{\text{kg}}{\text{L}}) \\  & =(32\,\frac{\cancel{\text{L}}}{\text{min}})\cdot (\frac{Q}{240-8t}\,\frac{\text{kg}}{\cancel{\text{L}}}) \\  & =\frac{32Q}{240-8t}\,\frac{\text{kg}}{\text{min}} \\  & =\frac{4Q}{30-t}\,\frac{\text{kg}}{\text{min}}.\end{aligned}
$$

**Step 3**: Calculate the overall rate of change.

The rate of change equals the rate of entry minus the rate of exit. Therefore, 

$$
\begin{aligned}\frac{dQ}{dt} & ={Q}_{\text{in}}^{′}-{Q}_{\text{out}}^{′} \\  & =1.2-\frac{4Q}{30-t}\end{aligned}
$$

which gives the equation

$$
\begin{aligned}\frac{dQ}{dt}+\frac{4}{30-t}Q=1.2.\end{aligned}
$$

**Step 4**: Integrate the equation.

This is a first-order linear equation with variable coefficients. So we find the general solution using an integrating factor:

$$
\begin{aligned}I(t) & ={e}^{\int 4/(30-t)\,dt} \\  & ={e}^{-4\operatorname{ln}⁡|30-t|} \\  & ={e}^{\operatorname{ln}⁡(30-t)^{-4}} \\  & =(30-t)^{-4}\end{aligned}
$$

Multiplying both sides of the differential equation by $I(t)=(30-t)^{-4}$ yields

$$
\begin{aligned}(30-t)^{-4}\cdot (\frac{dQ}{dt}+\frac{4}{30-t}Q) & =(30-t)^{-4}\cdot 1.2 \\ (30-t)^{-4}\frac{dQ}{dt}+4(30-t)^{-5}Q & =1.2(30-t)^{-4} \\ \frac{d}{dt}(Q(30-t)^{-4}) & =1.2(30-t)^{-4}.\end{aligned}
$$

Now, we integrate with respect to $t:$

$$
\begin{aligned}\int \frac{d}{dt}(Q(30-t)^{-4})\,dt & =\int 1.2(30-t)^{-4}\,dt \\ Q(30-t)^{-4} & =1.2\cdot \frac{1}{3}(30-t)^{-3}+C \\ Q(t) & =0.4(30-t)+C(30-t)^{4}\end{aligned}
$$

Note that $C$ is a constant of integration.

We're told that the tank initially contains $7\,\text{kg}$ of sweetener. So, we can apply the initial condition $Q(0)=7,$ and solve for $C:$

$$
\begin{aligned}Q(0) & =7 \\ C(30-0)^{4}+0.4(30-0) & =7 \\ C(30)^{4}+12 & =7 \\ C & =-\frac{5}{{30}^{4}}\end{aligned}
$$

Finally, we obtain the following expression for $Q(t):$

$$
\begin{aligned}Q(t) & =0.4(30-t)-\frac{5}{{30}^{4}}(30-t)^{4} \\  & =0.4\cdot 30\,(\frac{30-t}{30})-5{(\frac{30-t}{30})}^{4} \\  & =12\,(1-\frac{t}{30})-5{(1-\frac{t}{30})}^{4}.\end{aligned}
$$

Finally, we have $\alpha =12,\beta =-5,$ and

$$
\alpha -\beta =12-(-5)=17.
$$

---
q-339399 | observed:q-339399 | :question.difficulty/hard | eligible=False

A coolant reservoir initially holds $400\,\text{L}$ of liquid containing $6\,\text{kg}$ of dissolved corrosion inhibitor.
A feed solution containing $0.05\,\text{kg/L}$ of the inhibitor is pumped into the reservoir at a rate of $16\,\text{L/min},$ while the completely mixed liquid is drained out at a rate of $12\,\text{L/min}.$
Find, rounded to two decimal places, the amount of inhibitor in the reservoir $12$ minutes after pumping begins.

- $12.97\,\text{kg}$
- $12.44\,\text{kg}$ [correct]
- $13.21\,\text{kg}$
- $10.88\,\text{kg}$
- $11.92\,\text{kg}$

Let $Q$ be the amount of inhibitor in the reservoir at time $t,$ in minutes. Then, the derivative 

$$
\frac{dQ}{dt}
$$

describes how this amount changes with respect to time $t.$ This is equal to the rate at which inhibitor enters the tank minus the rate at which inhibitor leaves the tank.

$$
\frac{dQ}{dt}={Q}_{\text{in}}^{′}-{Q}_{\text{out}}^{′}
$$

Note that the units of $\frac{dQ}{dt},{Q}_{\text{in}}^{′}$ and ${Q}_{\text{out}}^{′}$ are $\text{kg}/\text{min}.$ Now, let's compute the required rates of change in steps.

**Step 1**: Calculating the rate at which inhibitor enters the reservoir.

Note that a feed solution containing $0.05\,\text{kg/L}$ of the inhibitor enters the reservoir at a rate of $16\,\text{L/min}.$ So, the rate at which the *inhibitor* enters the reservoir is 

$$
\begin{aligned}{Q}_{\text{in}}^{′} & =(0.05\,\frac{\text{kg}}{\text{L}})\cdot (16\,\frac{\text{L}}{\text{min}}) \\  & =(0.05\,\frac{\text{kg}}{\cancel{\text{L}}})\cdot (16\,\frac{\cancel{\text{L}}}{\text{min}}) \\  & =0.8\,\frac{\text{kg}}{\text{min}}.\end{aligned}
$$

**Step 2**: Calculating the rate at which inhibitor exits the reservoir.

To find the rate at which inhibitor leaves the reservoir, we must first determine the volume of liquid in the reservoir at time $t.$

The reservoir initially contains $400\,\text{L}$ of liquid; a solution enters at $16\,\text{L/min}$ and leaves at $12\,\text{L/min}.$
As a result, the volume of liquid in the reservoir after $t$ minutes is 

$$
400+16t-12t=(400+4t)\,\text{L}.
$$

Since $Q$ is the amount of inhibitor in the reservoir, the *concentration* of the mixed solution at time $t$ is

$$
\frac{Q}{400+4t}\,\text{kg/L}.
$$

Therefore, as the completely mixed liquid leaves at a rate of $12\,\text{L/min},$ *inhibitor* leaves at a rate of

$$
\begin{aligned}{Q}_{\text{out}}^{′} & =(12\,\frac{\text{L}}{\text{min}})\cdot (\frac{Q}{400+4t}\,\frac{\text{kg}}{\text{L}}) \\  & =(12\,\frac{\cancel{\text{L}}}{\text{min}})\cdot (\frac{Q}{400+4t}\,\frac{\text{kg}}{\cancel{\text{L}}}) \\  & =\frac{12Q}{400+4t}\,\frac{\text{kg}}{\text{min}} \\  & =\frac{3Q}{100+t}\,\frac{\text{kg}}{\text{min}}.\end{aligned}
$$

**Step 3**: Calculate the overall rate of change.

The rate of change equals the rate of entry minus the rate of exit. Therefore, 

$$
\begin{aligned}\frac{dQ}{dt} & ={Q}_{\text{in}}^{′}-{Q}_{\text{out}}^{′} \\  & =0.8-\frac{3Q}{100+t}\end{aligned}
$$

which gives the equation

$$
\begin{aligned}\frac{dQ}{dt}+\frac{3}{100+t}Q=0.8.\end{aligned}
$$

**Step 4**: Integrate the equation.

This is a first-order linear equation with variable coefficients. So we find the general solution using an integrating factor:

$$
\begin{aligned}I(t) & ={e}^{\int 3/(100+t)\,dt} \\  & ={e}^{3\operatorname{ln}⁡|100+t|} \\  & ={e}^{\operatorname{ln}⁡(100+t)^{3}} \\  & =(100+t)^{3}\end{aligned}
$$

Multiplying both sides of the differential equation by $I(t)=(100+t)^{3}$ yields

$$
\begin{aligned}(100+t)^{3}\cdot (\frac{dQ}{dt}+\frac{3}{100+t}Q) & =(100+t)^{3}\cdot 0.8 \\ (100+t)^{3}\frac{dQ}{dt}+3(100+t)^{2}Q & =0.8(100+t)^{3} \\ \frac{d}{dt}(Q(100+t)^{3}) & =0.8(100+t)^{3}.\end{aligned}
$$

Now, we integrate with respect to $t:$

$$
\begin{aligned}\int \frac{d}{dt}(Q(100+t)^{3})\,dt & =\int 0.8(100+t)^{3}\,dt \\ Q(100+t)^{3} & =0.8\cdot \frac{1}{4}(100+t)^{4}+C \\ Q(t) & =0.2(100+t)+\frac{C}{(100+t)^{3}}\end{aligned}
$$

Note that $C$ is a constant of integration.

We're told that the reservoir initially contains $6\,\text{kg}$ of inhibitor. So, we can apply the initial condition $Q(0)=6,$ and solve for $C:$

$$
\begin{aligned}Q(0) & =6 \\ 0.2(100+0)+\frac{C}{(100+0)^{3}} & =6 \\ 20+\frac{C}{{100}^{3}} & =6 \\ \frac{C}{{100}^{3}} & =-14 \\ C & =-14(100)^{3}\end{aligned}
$$

Finally, we obtain the following expression for $Q(t):$

$$
\begin{aligned}Q(t) & =0.2(100+t)-\frac{14(100)^{3}}{(100+t)^{3}} \\  & =0.2(100+t)-14{(\frac{100}{100+t})}^{3}.\end{aligned}
$$

Finally,  the amount of inhibitor in the reservoir $12$ minutes after pumping begins is

$$
\begin{aligned}Q(12) & =0.2(100+12)-14{(\frac{100}{100+12})}^{3} \\  & =22.4-14{(\frac{25}{28})}^{3} \\  & ≈12.44\,\text{kg},\end{aligned}
$$

rounded to two decimal places.

---
q-339400 | observed:q-339400 | :question.difficulty/hard | eligible=False

A fermentation vat initially holds $500\,\text{L}$ of liquid containing $8\,\text{kg}$ of dissolved nutrient.
A feed solution containing $0.06\,\text{kg/L}$ of the nutrient is pumped into the vat at a rate of $10\,\text{L/min},$ while the completely mixed liquid is drained out at a rate of $5\,\text{L/min}.$
Find, rounded to two decimal places, the amount of nutrient in the vat $8$ minutes after pumping begins.

- $12.03\,\text{kg}$ [correct]
- $10.94\,\text{kg}$
- $11.58\,\text{kg}$
- $13.12\,\text{kg}$
- $12.67\,\text{kg}$

Let $Q$ be the amount of nutrient in the vat at time $t,$ in minutes. Then, the derivative 

$$
\frac{dQ}{dt}
$$

describes how this amount changes with respect to time $t.$ This is equal to the rate at which nutrient enters the tank minus the rate at which nutrient leaves the tank.

$$
\frac{dQ}{dt}={Q}_{\text{in}}^{′}-{Q}_{\text{out}}^{′}
$$

Note that the units of $\frac{dQ}{dt},{Q}_{\text{in}}^{′}$ and ${Q}_{\text{out}}^{′}$ are $\text{kg}/\text{min}.$ Now, let's compute the required rates of change in steps.

**Step 1**: Calculating the rate at which nutrient enters the vat.

Note that a feed solution containing $0.06\,\text{kg/L}$ of the nutrient enters the vat at a rate of $10\,\text{L/min}.$ So, the rate at which the *nutrient* enters the vat is 

$$
\begin{aligned}{Q}_{\text{in}}^{′} & =(0.06\,\frac{\text{kg}}{\text{L}})\cdot (10\,\frac{\text{L}}{\text{min}}) \\  & =(0.06\,\frac{\text{kg}}{\cancel{\text{L}}})\cdot (10\,\frac{\cancel{\text{L}}}{\text{min}}) \\  & =0.6\,\frac{\text{kg}}{\text{min}}.\end{aligned}
$$

**Step 2**: Calculating the rate at which nutrient exits the vat.

To find the rate at which nutrient leaves the vat, we must first determine the volume of liquid in the vat at time $t.$

The vat initially contains $500\,\text{L}$ of liquid; a solution enters at $10\,\text{L/min}$ and leaves at $5\,\text{L/min}.$
As a result, the volume of liquid in the vat after $t$ minutes is 

$$
500+10t-5t=(500+5t)\,\text{L}.
$$

Since $Q$ is the amount of nutrient in the vat, the *concentration* of the mixed solution at time $t$ is

$$
\frac{Q}{500+5t}\,\text{kg/L}.
$$

Therefore, as the completely mixed liquid leaves at a rate of $5\,\text{L/min},$ *nutrient* leaves at a rate of

$$
\begin{aligned}{Q}_{\text{out}}^{′} & =(5\,\frac{\text{L}}{\text{min}})\cdot (\frac{Q}{500+5t}\,\frac{\text{kg}}{\text{L}}) \\  & =(5\,\frac{\cancel{\text{L}}}{\text{min}})\cdot (\frac{Q}{500+5t}\,\frac{\text{kg}}{\cancel{\text{L}}}) \\  & =\frac{5Q}{500+5t}\,\frac{\text{kg}}{\text{min}} \\  & =\frac{Q}{100+t}\,\frac{\text{kg}}{\text{min}}.\end{aligned}
$$

**Step 3**: Calculate the overall rate of change.

The rate of change equals the rate of entry minus the rate of exit. Therefore, 

$$
\begin{aligned}\frac{dQ}{dt} & ={Q}_{\text{in}}^{′}-{Q}_{\text{out}}^{′} \\  & =0.6-\frac{Q}{100+t}\end{aligned}
$$

which gives the equation

$$
\begin{aligned}\frac{dQ}{dt}+\frac{1}{100+t}Q=0.6.\end{aligned}
$$

**Step 4**: Integrate the equation.

This is a first-order linear equation with variable coefficients. So we find the general solution using an integrating factor:

$$
\begin{aligned}I(t) & ={e}^{\int 1/(100+t)\,dt} \\  & ={e}^{\operatorname{ln}⁡|100+t|} \\  & =100+t\end{aligned}
$$

Multiplying both sides of the differential equation by $I(t)=100+t$ yields

$$
\begin{aligned}(100+t)\cdot (\frac{dQ}{dt}+\frac{1}{100+t}Q) & =(100+t)\cdot 0.6 \\ (100+t)\frac{dQ}{dt}+Q & =0.6(100+t) \\ \frac{d}{dt}(Q(100+t)) & =0.6(100+t).\end{aligned}
$$

Now, we integrate with respect to $t:$

$$
\begin{aligned}\int \frac{d}{dt}(Q(100+t))\,dt & =\int 0.6(100+t)\,dt \\ Q(100+t) & =0.6\cdot \frac{1}{2}(100+t)^{2}+C \\ Q(t) & =0.3(100+t)+\frac{C}{100+t}\end{aligned}
$$

Note that $C$ is a constant of integration.

We're told that the vat initially contains $8\,\text{kg}$ of nutrient. So, we can apply the initial condition $Q(0)=8,$ and solve for $C:$

$$
\begin{aligned}Q(0) & =8 \\ 0.3(100+0)+\frac{C}{100+0} & =8 \\ 30+\frac{C}{100} & =8 \\ \frac{C}{100} & =-22 \\ C & =-2200\end{aligned}
$$

Finally, we obtain the following expression for $Q(t):$

$$
\begin{aligned}Q(t) & =0.3(100+t)-\frac{2200}{100+t}.\end{aligned}
$$

Finally,  the amount of nutrient in the vat $8$ minutes after pumping begins is

$$
\begin{aligned}Q(8) & =0.3(100+8)-\frac{2200}{100+8} \\  & =32.4-\frac{2200}{108} \\  & ≈12.03\,\text{kg},\end{aligned}
$$

rounded to two decimal places.

# Generated variants (origin/eligibility explicit)

q-336439 | observed:q-336439 | unrated original | eligible=False

An aquarium initially holds $300L$ of water containing $7.2kg$ of dissolved minerals.
A solution containing $0.036kg/L$ of dissolved minerals is pumped into the aquarium at a rate of $24L/min$, while the completely mixed water is drained out at a rate of $36L/min$. If the amount of minerals $Q(t)$, in kilograms, in the tank $t$ minutes after pumping begins is given by
$Q(t) = α(1 - \frac{t}{25}) + β(1 - \frac{t}{25})^{3}$
where $α$ and $β$ are constants, what is the value of $α + β$?

> A scientific calculator is required to answer this question.

- $12$
- $18$
- $9.6$
- $14.4$
- $7.2$

[Original omits worked solution.]

---
q-336439 | observed:q-336439 | unrated original | eligible=False

An aquarium initially holds $300L$ of water containing $7.5kg$ of dissolved minerals.
A solution containing $0.0375kg/L$ of dissolved minerals is pumped into the aquarium at a rate of $24L/min$, while the completely mixed water is drained out at a rate of $36L/min$. If the amount of minerals $Q(t)$, in kilograms, in the tank $t$ minutes after pumping begins is given by
$Q(t) = α(1 - \frac{t}{25}) + β(1 - \frac{t}{25})^{3}$
where $α$ and $β$ are constants, what is the value of $α + β$?

> A scientific calculator is required to answer this question.

- $12.5$
- $18.75$
- $10$
- $15$
- $7.5$

[Original omits worked solution.]

---
q-336439 | authored-operations | :question.difficulty/easy | eligible=True

An aquarium initially holds $1200L$ of water containing $35kg$ of dissolved minerals.
A solution containing $0.04kg/L$ of dissolved minerals is pumped into the aquarium at a rate of $24L/min$, while the completely mixed water is drained out at a rate of $36L/min$. If the amount of minerals $Q(t)$, in kilograms, in the tank $t$ minutes after pumping begins is given by
$Q(t) = α(1 - \frac{t}{100}) + β(1 - \frac{t}{100})^{3}$
where $α$ and $β$ are constants, what is the value of $α + β$?

> A scientific calculator is required to answer this question.

- $83$
- $61$
- $48$
- $13$
- $35$ [correct]

At $t=0,$ the supplied model gives $Q(0)=\alpha(1-0/100)+\beta(1-0/100)^{3}=\alpha+\beta.$ The initial amount is $35\,\text{kg},$ so $\alpha+\beta=35.$

---
q-336439 | authored-operations | :question.difficulty/easy | eligible=True

An aquarium initially holds $800L$ of water containing $40kg$ of dissolved minerals.
A solution containing $0.07kg/L$ of dissolved minerals is pumped into the aquarium at a rate of $20L/min$, while the completely mixed water is drained out at a rate of $30L/min$. If the amount of minerals $Q(t)$, in kilograms, in the tank $t$ minutes after pumping begins is given by
$Q(t) = α(1 - \frac{t}{80}) + β(1 - \frac{t}{80})^{3}$
where $α$ and $β$ are constants, what is the value of $α + β$?

> A scientific calculator is required to answer this question.

- $56$
- $16$
- $40$ [correct]
- $72$
- $96$

At $t=0,$ the supplied model gives $Q(0)=\alpha(1-0/80)+\beta(1-0/80)^{3}=\alpha+\beta.$ The initial amount is $40\,\text{kg},$ so $\alpha+\beta=40.$

---
q-336738 | observed:q-336738 | unrated original | eligible=False

A storage tank initially holds $600L$ of liquid containing $6kg$ of dissolved stabilizer.
A feed solution containing $0.048kg/L$ of the stabilizer is pumped into the tank at a rate of $15L/min$, while the completely mixed liquid is drained out at a rate of $10L/min$.
Find, rounded to two decimal places, the amount of stabilizer in the tank $10$ minutes after pumping begins.

> A scientific calculator is required to answer this question.

- $11.77kg$
- $11.01kg$
- $10.35kg$
- $9.85kg$
- $9.59kg$

[Original omits worked solution.]

---
q-336738 | observed:q-336738 | unrated original | eligible=False

A storage tank initially holds $600L$ of liquid containing $6.25kg$ of dissolved stabilizer.
A feed solution containing $0.05kg/L$ of the stabilizer is pumped into the tank at a rate of $15L/min$, while the completely mixed liquid is drained out at a rate of $10L/min$.
Find, rounded to two decimal places, the amount of stabilizer in the tank $10$ minutes after pumping begins.

> A scientific calculator is required to answer this question.

- $12.26kg$
- $11.47kg$
- $10.79kg$
- $10.26kg$
- $9.99kg$

[Original omits worked solution.]

---
q-336738 | authored-operations | :question.difficulty/hard | eligible=True

A storage tank initially holds $800L$ of liquid containing $13kg$ of dissolved stabilizer.
A feed solution containing $0.07kg/L$ of the stabilizer is pumped into the tank at a rate of $24L/min$, while the completely mixed liquid is drained out at a rate of $16L/min$.
Find, rounded to two decimal places, the amount of stabilizer in the tank $4$ minutes after pumping begins.

> A scientific calculator is required to answer this question.

- $58.24\,\text{kg}$
- $18.46\,\text{kg}$
- $12.02\,\text{kg}$
- $20.01\,\text{kg}$
- $18.48\,\text{kg}$ [correct]

Let $Q$ be the amount of dissolved substance in the tank at time $t,$ in minutes. The amount entering minus the amount leaving gives
$$\frac{dQ}{dt}=Q'_{\text{in}}-Q'_{\text{out}}.$$
The units of these rates are $\text{kg/min}.$

**Step 1**: Calculating the rate at which substance enters the tank.
$$\begin{aligned}Q'_{\text{in}}&=(0.07\,\frac{\text{kg}}{\text{L}})\cdot(24\,\frac{\text{L}}{\text{min}})\\
&=(0.07\,\frac{\text{kg}}{\cancel{\text{L}}})\cdot(24\,\frac{\cancel{\text{L}}}{\text{min}})\\&=1.68\,\text{kg/min}.\end{aligned}$$

**Step 2**: Calculating the rate at which substance exits the tank.
The volume is
$$V(t)=800+24t-16t=(800+8t)\,\text{L}.$$
The concentration is $\frac{Q}{800+8t}\,\text{kg/L}.$ Hence,
$$\begin{aligned}Q'_{\text{out}}&=(16\,\frac{\text{L}}{\text{min}})\cdot(\frac{Q}{800+8t}\,\frac{\text{kg}}{\text{L}})\\
&=(16\,\frac{\cancel{\text{L}}}{\text{min}})\cdot(\frac{Q}{800+8t}\,\frac{\text{kg}}{\cancel{\text{L}}})\\
&=\frac{16Q}{800+8t}\,\text{kg/min}=\frac{2Q}{100+t}\,\text{kg/min}.\end{aligned}$$

**Step 3**: Calculate the overall rate of change.
$$\begin{aligned}\frac{dQ}{dt}&=Q'_{\text{in}}-Q'_{\text{out}}\\&=1.68-\frac{2Q}{100+t}.\end{aligned}$$
Thus,
$$\frac{dQ}{dt}+\frac{2}{100+t}Q=1.68.$$

**Step 4**: Integrate the equation.
This is a first-order linear equation with variable coefficients. So we find the general solution using an integrating factor:
$$\begin{aligned}I(t)&=e^{\int 2/(100+t)\,dt}\\&=e^{2\ln|100+t|}\\&=e^{\ln (100+t)^{2}}\\&=(100+t)^{2}.\end{aligned}$$
Multiplying both sides by $I(t)=(100+t)^{2}$ yields
$$\begin{aligned}(100+t)^{2}\cdot(\frac{dQ}{dt}+\frac{2}{100+t}Q)&=(100+t)^{2}\cdot 1.68\\
(100+t)^{2}\frac{dQ}{dt}+2(100+t)^{1}Q&=1.68(100+t)^{2}\\\frac{d}{dt}(Q(100+t)^{2})&=1.68(100+t)^{2}.\end{aligned}$$
Now, we integrate with respect to $t:$
$$\begin{aligned}\int\frac{d}{dt}(Q(100+t)^{2})\,dt&=\int 1.68(100+t)^{2}\,dt\\Q(100+t)^{2}&=1.68\cdot\frac{1}{3}(100+t)^{3}+C\\Q(t)&=0.56(100+t)+C(100+t)^{-2}.\end{aligned}$$
Note that $C$ is a constant of integration.
The initial condition is $Q(0)=13.$ Thus,
$$\begin{aligned}0.56(100+0)+C(100+0)^{-2}&=13\\
56+C(100)^{-2}&=13\\C(100)^{-2}&=-43\\C&=-430000.\end{aligned}$$
Finally, we obtain the following expression for $Q(t):$
$$Q(t)=\frac{14 t}{25} + 56 - \frac{430000}{\left(t + 100\right)^{2}}.$$
Finally, the amount in the tank $4$ minutes after pumping begins is
$$\begin{aligned}Q(4)&=0.56(100+4)-43(\frac{100}{100+4})^{2}\\&=58.24-43(\frac{25}{26})^{2}\\&\approx 18.48\,\text{kg}.\end{aligned}$$
This is rounded to two decimal places.

---
q-336738 | authored-operations | :question.difficulty/hard | eligible=True

A storage tank initially holds $640L$ of liquid containing $15kg$ of dissolved stabilizer.
A feed solution containing $0.07kg/L$ of the stabilizer is pumped into the tank at a rate of $24L/min$, while the completely mixed liquid is drained out at a rate of $16L/min$.
Find, rounded to two decimal places, the amount of stabilizer in the tank $11$ minutes after pumping begins.

> A scientific calculator is required to answer this question.

- $27.93\,\text{kg}$ [correct]
- $30.71\,\text{kg}$
- $50.96\,\text{kg}$
- $27.55\,\text{kg}$
- $11.59\,\text{kg}$

Let $Q$ be the amount of dissolved substance in the tank at time $t,$ in minutes. The amount entering minus the amount leaving gives
$$\frac{dQ}{dt}=Q'_{\text{in}}-Q'_{\text{out}}.$$
The units of these rates are $\text{kg/min}.$

**Step 1**: Calculating the rate at which substance enters the tank.
$$\begin{aligned}Q'_{\text{in}}&=(0.07\,\frac{\text{kg}}{\text{L}})\cdot(24\,\frac{\text{L}}{\text{min}})\\
&=(0.07\,\frac{\text{kg}}{\cancel{\text{L}}})\cdot(24\,\frac{\cancel{\text{L}}}{\text{min}})\\&=1.68\,\text{kg/min}.\end{aligned}$$

**Step 2**: Calculating the rate at which substance exits the tank.
The volume is
$$V(t)=640+24t-16t=(640+8t)\,\text{L}.$$
The concentration is $\frac{Q}{640+8t}\,\text{kg/L}.$ Hence,
$$\begin{aligned}Q'_{\text{out}}&=(16\,\frac{\text{L}}{\text{min}})\cdot(\frac{Q}{640+8t}\,\frac{\text{kg}}{\text{L}})\\
&=(16\,\frac{\cancel{\text{L}}}{\text{min}})\cdot(\frac{Q}{640+8t}\,\frac{\text{kg}}{\cancel{\text{L}}})\\
&=\frac{16Q}{640+8t}\,\text{kg/min}=\frac{2Q}{80+t}\,\text{kg/min}.\end{aligned}$$

**Step 3**: Calculate the overall rate of change.
$$\begin{aligned}\frac{dQ}{dt}&=Q'_{\text{in}}-Q'_{\text{out}}\\&=1.68-\frac{2Q}{80+t}.\end{aligned}$$
Thus,
$$\frac{dQ}{dt}+\frac{2}{80+t}Q=1.68.$$

**Step 4**: Integrate the equation.
This is a first-order linear equation with variable coefficients. So we find the general solution using an integrating factor:
$$\begin{aligned}I(t)&=e^{\int 2/(80+t)\,dt}\\&=e^{2\ln|80+t|}\\&=e^{\ln (80+t)^{2}}\\&=(80+t)^{2}.\end{aligned}$$
Multiplying both sides by $I(t)=(80+t)^{2}$ yields
$$\begin{aligned}(80+t)^{2}\cdot(\frac{dQ}{dt}+\frac{2}{80+t}Q)&=(80+t)^{2}\cdot 1.68\\
(80+t)^{2}\frac{dQ}{dt}+2(80+t)^{1}Q&=1.68(80+t)^{2}\\\frac{d}{dt}(Q(80+t)^{2})&=1.68(80+t)^{2}.\end{aligned}$$
Now, we integrate with respect to $t:$
$$\begin{aligned}\int\frac{d}{dt}(Q(80+t)^{2})\,dt&=\int 1.68(80+t)^{2}\,dt\\Q(80+t)^{2}&=1.68\cdot\frac{1}{3}(80+t)^{3}+C\\Q(t)&=0.56(80+t)+C(80+t)^{-2}.\end{aligned}$$
Note that $C$ is a constant of integration.
The initial condition is $Q(0)=15.$ Thus,
$$\begin{aligned}0.56(80+0)+C(80+0)^{-2}&=15\\
44.8+C(80)^{-2}&=15\\C(80)^{-2}&=-29.8\\C&=-190720.\end{aligned}$$
Finally, we obtain the following expression for $Q(t):$
$$Q(t)=\frac{14 t}{25} + \frac{224}{5} - \frac{190720}{\left(t + 80\right)^{2}}.$$
Finally, the amount in the tank $11$ minutes after pumping begins is
$$\begin{aligned}Q(11)&=0.56(80+11)-29.8(\frac{80}{80+11})^{2}\\&=50.96-29.8(\frac{80}{91})^{2}\\&\approx 27.93\,\text{kg}.\end{aligned}$$
This is rounded to two decimal places.

---
q-336743 | observed:q-336743 | :question.difficulty/hard | eligible=False

A processing tank initially holds $420\,\text{L}$ of liquid containing $12\,\text{kg}$ of dissolved preservative.
A feed solution containing $0.06\,\text{kg/L}$ of the preservative is pumped into the tank at a rate of $18\,\text{L/min},$ while the completely mixed liquid is drained out at a rate of $12\,\text{L/min}.$
Find, rounded to two decimal places, the amount of preservative in the tank $15$ minutes after pumping begins.

- $21.65\,\text{kg}$ [correct]
- $21.53\,\text{kg}$
- $20.81\,\text{kg}$
- $22.81\,\text{kg}$
- $22.11\,\text{kg}$

Let $Q$ be the amount of preservative in the tank at time $t,$ in minutes. Then, the derivative 

$$
\frac{dQ}{dt}
$$

describes how this amount changes with respect to time $t.$ This is equal to the rate at which preservative enters the tank minus the rate at which preservative leaves the tank.

$$
\frac{dQ}{dt}={Q}_{\text{in}}^{′}-{Q}_{\text{out}}^{′}
$$

Note that the units of $\frac{dQ}{dt},{Q}_{\text{in}}^{′}$ and ${Q}_{\text{out}}^{′}$ are $\text{kg}/\text{min}.$ Now, let's compute the required rates of change in steps.

**Step 1**: Calculating the rate at which preservative enters the tank.

Note that a feed solution containing $0.06\,\text{kg/L}$ of the preservative enters the tank at a rate of $18\,\text{L/min}.$ So, the rate at which the *preservative* enters the tank is 

$$
\begin{aligned}{Q}_{\text{in}}^{′} & =(0.06\,\frac{\text{kg}}{\text{L}})\cdot (18\,\frac{\text{L}}{\text{min}}) \\  & =(0.06\,\frac{\text{kg}}{\cancel{\text{L}}})\cdot (18\,\frac{\cancel{\text{L}}}{\text{min}}) \\  & =1.08\,\frac{\text{kg}}{\text{min}}.\end{aligned}
$$

**Step 2**: Calculating the rate at which preservative exits the tank.

To find the rate at which preservative leaves the tank, we must first determine the volume of liquid in the tank at time $t.$

The tank initially contains $420\,\text{L}$ of liquid; a solution enters at $18\,\text{L/min}$ and leaves at $12\,\text{L/min}.$
As a result, the volume of liquid in the tank after $t$ minutes is 

$$
420+18t-12t=(420+6t)\,\text{L}.
$$

Since $Q$ is the amount of preservative in the tank, the *concentration* of the mixed solution at time $t$ is

$$
\frac{Q}{420+6t}\,\text{kg/L}.
$$

Therefore, as the completely mixed liquid leaves at a rate of $12\,\text{L/min},$ *preservative* leaves at a rate of

$$
\begin{aligned}{Q}_{\text{out}}^{′} & =(12\,\frac{\text{L}}{\text{min}})\cdot (\frac{Q}{420+6t}\,\frac{\text{kg}}{\text{L}}) \\  & =(12\,\frac{\cancel{\text{L}}}{\text{min}})\cdot (\frac{Q}{420+6t}\,\frac{\text{kg}}{\cancel{\text{L}}}) \\  & =\frac{12Q}{420+6t}\,\frac{\text{kg}}{\text{min}} \\  & =\frac{2Q}{70+t}\,\frac{\text{kg}}{\text{min}}.\end{aligned}
$$

**Step 3**: Calculate the overall rate of change.

The rate of change equals the rate of entry minus the rate of exit. Therefore, 

$$
\begin{aligned}\frac{dQ}{dt} & ={Q}_{\text{in}}^{′}-{Q}_{\text{out}}^{′} \\  & =1.08-\frac{2Q}{70+t}\end{aligned}
$$

which gives the equation

$$
\begin{aligned}\frac{dQ}{dt}+\frac{2}{70+t}Q=1.08.\end{aligned}
$$

**Step 4**: Integrate the equation.

This is a first-order linear equation with variable coefficients. So we find the general solution using an integrating factor:

$$
\begin{aligned}I(t) & ={e}^{\int 2/(70+t)\,dt} \\  & ={e}^{2\operatorname{ln}⁡|70+t|} \\  & ={e}^{\operatorname{ln}⁡(70+t)^{2}} \\  & =(70+t)^{2}\end{aligned}
$$

Multiplying both sides of the differential equation by $I(t)=(70+t)^{2}$ yields

$$
\begin{aligned}(70+t)^{2}\cdot (\frac{dQ}{dt}+\frac{2}{70+t}Q) & =(70+t)^{2}\cdot 1.08 \\ (70+t)^{2}\frac{dQ}{dt}+2(70+t)Q & =1.08(70+t)^{2} \\ \frac{d}{dt}(Q(70+t)^{2}) & =1.08(70+t)^{2}.\end{aligned}
$$

Now, we integrate with respect to $t:$

$$
\begin{aligned}\int \frac{d}{dt}(Q(70+t)^{2})\,dt & =\int 1.08(70+t)^{2}\,dt \\ Q(70+t)^{2} & =1.08\cdot \frac{1}{3}(70+t)^{3}+C \\ Q(t) & =0.36(70+t)+\frac{C}{(70+t)^{2}}\end{aligned}
$$

Note that $C$ is a constant of integration.

We're told that the tank initially contains $12\,\text{kg}$ of preservative. So, we can apply the initial condition $Q(0)=12,$ and solve for $C:$

$$
\begin{aligned}Q(0) & =12 \\ 0.36(70+0)+\frac{C}{(70+0)^{2}} & =12 \\ 25.2+\frac{C}{{70}^{2}} & =12 \\ \frac{C}{{70}^{2}} & =-13.2 \\ C & =-13.2(70)^{2}\end{aligned}
$$

Finally, we obtain the following expression for $Q(t):$

$$
\begin{aligned}Q(t) & =0.36(70+t)-\frac{13.2(70)^{2}}{(70+t)^{2}} \\  & =0.36(70+t)-13.2{(\frac{70}{70+t})}^{2}.\end{aligned}
$$

Finally,  the amount of preservative in the tank $15$ minutes after pumping begins is

$$
\begin{aligned}Q(15) & =0.36(70+15)-13.2{(\frac{70}{70+15})}^{2} \\  & =30.6-13.2{(\frac{70}{85})}^{2} \\  & ≈21.65\,\text{kg},\end{aligned}
$$

rounded to two decimal places.

---
q-336743 | observed:q-336743 | :question.difficulty/hard | eligible=False

A processing tank initially holds $420\,\text{L}$ of liquid containing $12.5\,\text{kg}$ of dissolved preservative.
A feed solution containing $0.0625\,\text{kg/L}$ of the preservative is pumped into the tank at a rate of $18\,\text{L/min},$ while the completely mixed liquid is drained out at a rate of $12\,\text{L/min}.$
Find, rounded to two decimal places, the amount of preservative in the tank $15$ minutes after pumping begins.

- $22.55\,\text{kg}$ [correct]
- $22.43\,\text{kg}$
- $21.68\,\text{kg}$
- $23.76\,\text{kg}$
- $23.03\,\text{kg}$

Let $Q$ be the amount of preservative in the tank at time $t,$ in minutes. Then, the derivative 

$$
\frac{dQ}{dt}
$$

describes how this amount changes with respect to time $t.$ This is equal to the rate at which preservative enters the tank minus the rate at which preservative leaves the tank.

$$
\frac{dQ}{dt}={Q}_{\text{in}}^{′}-{Q}_{\text{out}}^{′}
$$

Note that the units of $\frac{dQ}{dt},{Q}_{\text{in}}^{′}$ and ${Q}_{\text{out}}^{′}$ are $\text{kg}/\text{min}.$ Now, let's compute the required rates of change in steps.

**Step 1**: Calculating the rate at which preservative enters the tank.

Note that a feed solution containing $0.0625\,\text{kg/L}$ of the preservative enters the tank at a rate of $18\,\text{L/min}.$ So, the rate at which the *preservative* enters the tank is 

$$
\begin{aligned}{Q}_{\text{in}}^{′} & =(0.0625\,\frac{\text{kg}}{\text{L}})\cdot (18\,\frac{\text{L}}{\text{min}}) \\  & =(0.0625\,\frac{\text{kg}}{\cancel{\text{L}}})\cdot (18\,\frac{\cancel{\text{L}}}{\text{min}}) \\  & =1.125\,\frac{\text{kg}}{\text{min}}.\end{aligned}
$$

**Step 2**: Calculating the rate at which preservative exits the tank.

To find the rate at which preservative leaves the tank, we must first determine the volume of liquid in the tank at time $t.$

The tank initially contains $420\,\text{L}$ of liquid; a solution enters at $18\,\text{L/min}$ and leaves at $12\,\text{L/min}.$
As a result, the volume of liquid in the tank after $t$ minutes is 

$$
420+18t-12t=(420+6t)\,\text{L}.
$$

Since $Q$ is the amount of preservative in the tank, the *concentration* of the mixed solution at time $t$ is

$$
\frac{Q}{420+6t}\,\text{kg/L}.
$$

Therefore, as the completely mixed liquid leaves at a rate of $12\,\text{L/min},$ *preservative* leaves at a rate of

$$
\begin{aligned}{Q}_{\text{out}}^{′} & =(12\,\frac{\text{L}}{\text{min}})\cdot (\frac{Q}{420+6t}\,\frac{\text{kg}}{\text{L}}) \\  & =(12\,\frac{\cancel{\text{L}}}{\text{min}})\cdot (\frac{Q}{420+6t}\,\frac{\text{kg}}{\cancel{\text{L}}}) \\  & =\frac{12Q}{420+6t}\,\frac{\text{kg}}{\text{min}} \\  & =\frac{2Q}{70+t}\,\frac{\text{kg}}{\text{min}}.\end{aligned}
$$

**Step 3**: Calculate the overall rate of change.

The rate of change equals the rate of entry minus the rate of exit. Therefore, 

$$
\begin{aligned}\frac{dQ}{dt} & ={Q}_{\text{in}}^{′}-{Q}_{\text{out}}^{′} \\  & =1.125-\frac{2Q}{70+t}\end{aligned}
$$

which gives the equation

$$
\begin{aligned}\frac{dQ}{dt}+\frac{2}{70+t}Q=1.125.\end{aligned}
$$

**Step 4**: Integrate the equation.

This is a first-order linear equation with variable coefficients. So we find the general solution using an integrating factor:

$$
\begin{aligned}I(t) & ={e}^{\int 2/(70+t)\,dt} \\  & ={e}^{2\operatorname{ln}⁡|70+t|} \\  & ={e}^{\operatorname{ln}⁡(70+t)^{2}} \\  & =(70+t)^{2}\end{aligned}
$$

Multiplying both sides of the differential equation by $I(t)=(70+t)^{2}$ yields

$$
\begin{aligned}(70+t)^{2}\cdot (\frac{dQ}{dt}+\frac{2}{70+t}Q) & =(70+t)^{2}\cdot 1.125 \\ (70+t)^{2}\frac{dQ}{dt}+2(70+t)Q & =1.125(70+t)^{2} \\ \frac{d}{dt}(Q(70+t)^{2}) & =1.125(70+t)^{2}.\end{aligned}
$$

Now, we integrate with respect to $t:$

$$
\begin{aligned}\int \frac{d}{dt}(Q(70+t)^{2})\,dt & =\int 1.125(70+t)^{2}\,dt \\ Q(70+t)^{2} & =1.125\cdot \frac{1}{3}(70+t)^{3}+C \\ Q(t) & =0.375(70+t)+\frac{C}{(70+t)^{2}}\end{aligned}
$$

Note that $C$ is a constant of integration.

We're told that the tank initially contains $12.5\,\text{kg}$ of preservative. So, we can apply the initial condition $Q(0)=12.5,$ and solve for $C:$

$$
\begin{aligned}Q(0) & =12.5 \\ 0.375(70+0)+\frac{C}{(70+0)^{2}} & =12.5 \\ 26.25+\frac{C}{{70}^{2}} & =12.5 \\ \frac{C}{{70}^{2}} & =-13.75 \\ C & =-13.75(70)^{2}\end{aligned}
$$

Finally, we obtain the following expression for $Q(t):$

$$
\begin{aligned}Q(t) & =0.375(70+t)-\frac{13.75(70)^{2}}{(70+t)^{2}} \\  & =0.375(70+t)-13.75{(\frac{70}{70+t})}^{2}.\end{aligned}
$$

Finally,  the amount of preservative in the tank $15$ minutes after pumping begins is

$$
\begin{aligned}Q(15) & =0.375(70+15)-13.75{(\frac{70}{70+15})}^{2} \\  & =31.875-13.75{(\frac{70}{85})}^{2} \\  & ≈22.55\,\text{kg},\end{aligned}
$$

rounded to two decimal places.

---
q-336743 | authored-operations | :question.difficulty/hard | eligible=True

A processing tank initially holds $800\,\text{L}$ of liquid containing $13\,\text{kg}$ of dissolved preservative.
A feed solution containing $0.07\,\text{kg/L}$ of the preservative is pumped into the tank at a rate of $24\,\text{L/min},$ while the completely mixed liquid is drained out at a rate of $16\,\text{L/min}.$
Find, rounded to two decimal places, the amount of preservative in the tank $4$ minutes after pumping begins.

- $58.24\,\text{kg}$
- $18.46\,\text{kg}$
- $12.02\,\text{kg}$
- $20.01\,\text{kg}$
- $18.48\,\text{kg}$ [correct]

Let $Q$ be the amount of dissolved substance in the tank at time $t,$ in minutes. The amount entering minus the amount leaving gives
$$\frac{dQ}{dt}=Q'_{\text{in}}-Q'_{\text{out}}.$$
The units of these rates are $\text{kg/min}.$

**Step 1**: Calculating the rate at which substance enters the tank.
$$\begin{aligned}Q'_{\text{in}}&=(0.07\,\frac{\text{kg}}{\text{L}})\cdot(24\,\frac{\text{L}}{\text{min}})\\
&=(0.07\,\frac{\text{kg}}{\cancel{\text{L}}})\cdot(24\,\frac{\cancel{\text{L}}}{\text{min}})\\&=1.68\,\text{kg/min}.\end{aligned}$$

**Step 2**: Calculating the rate at which substance exits the tank.
The volume is
$$V(t)=800+24t-16t=(800+8t)\,\text{L}.$$
The concentration is $\frac{Q}{800+8t}\,\text{kg/L}.$ Hence,
$$\begin{aligned}Q'_{\text{out}}&=(16\,\frac{\text{L}}{\text{min}})\cdot(\frac{Q}{800+8t}\,\frac{\text{kg}}{\text{L}})\\
&=(16\,\frac{\cancel{\text{L}}}{\text{min}})\cdot(\frac{Q}{800+8t}\,\frac{\text{kg}}{\cancel{\text{L}}})\\
&=\frac{16Q}{800+8t}\,\text{kg/min}=\frac{2Q}{100+t}\,\text{kg/min}.\end{aligned}$$

**Step 3**: Calculate the overall rate of change.
$$\begin{aligned}\frac{dQ}{dt}&=Q'_{\text{in}}-Q'_{\text{out}}\\&=1.68-\frac{2Q}{100+t}.\end{aligned}$$
Thus,
$$\frac{dQ}{dt}+\frac{2}{100+t}Q=1.68.$$

**Step 4**: Integrate the equation.
This is a first-order linear equation with variable coefficients. So we find the general solution using an integrating factor:
$$\begin{aligned}I(t)&=e^{\int 2/(100+t)\,dt}\\&=e^{2\ln|100+t|}\\&=e^{\ln (100+t)^{2}}\\&=(100+t)^{2}.\end{aligned}$$
Multiplying both sides by $I(t)=(100+t)^{2}$ yields
$$\begin{aligned}(100+t)^{2}\cdot(\frac{dQ}{dt}+\frac{2}{100+t}Q)&=(100+t)^{2}\cdot 1.68\\
(100+t)^{2}\frac{dQ}{dt}+2(100+t)^{1}Q&=1.68(100+t)^{2}\\\frac{d}{dt}(Q(100+t)^{2})&=1.68(100+t)^{2}.\end{aligned}$$
Now, we integrate with respect to $t:$
$$\begin{aligned}\int\frac{d}{dt}(Q(100+t)^{2})\,dt&=\int 1.68(100+t)^{2}\,dt\\Q(100+t)^{2}&=1.68\cdot\frac{1}{3}(100+t)^{3}+C\\Q(t)&=0.56(100+t)+C(100+t)^{-2}.\end{aligned}$$
Note that $C$ is a constant of integration.
The initial condition is $Q(0)=13.$ Thus,
$$\begin{aligned}0.56(100+0)+C(100+0)^{-2}&=13\\
56+C(100)^{-2}&=13\\C(100)^{-2}&=-43\\C&=-430000.\end{aligned}$$
Finally, we obtain the following expression for $Q(t):$
$$Q(t)=\frac{14 t}{25} + 56 - \frac{430000}{\left(t + 100\right)^{2}}.$$
Finally, the amount in the tank $4$ minutes after pumping begins is
$$\begin{aligned}Q(4)&=0.56(100+4)-43(\frac{100}{100+4})^{2}\\&=58.24-43(\frac{25}{26})^{2}\\&\approx 18.48\,\text{kg}.\end{aligned}$$
This is rounded to two decimal places.

---
q-336743 | authored-operations | :question.difficulty/hard | eligible=True

A processing tank initially holds $640\,\text{L}$ of liquid containing $15\,\text{kg}$ of dissolved preservative.
A feed solution containing $0.07\,\text{kg/L}$ of the preservative is pumped into the tank at a rate of $24\,\text{L/min},$ while the completely mixed liquid is drained out at a rate of $16\,\text{L/min}.$
Find, rounded to two decimal places, the amount of preservative in the tank $11$ minutes after pumping begins.

- $27.93\,\text{kg}$ [correct]
- $30.71\,\text{kg}$
- $50.96\,\text{kg}$
- $27.55\,\text{kg}$
- $11.59\,\text{kg}$

Let $Q$ be the amount of dissolved substance in the tank at time $t,$ in minutes. The amount entering minus the amount leaving gives
$$\frac{dQ}{dt}=Q'_{\text{in}}-Q'_{\text{out}}.$$
The units of these rates are $\text{kg/min}.$

**Step 1**: Calculating the rate at which substance enters the tank.
$$\begin{aligned}Q'_{\text{in}}&=(0.07\,\frac{\text{kg}}{\text{L}})\cdot(24\,\frac{\text{L}}{\text{min}})\\
&=(0.07\,\frac{\text{kg}}{\cancel{\text{L}}})\cdot(24\,\frac{\cancel{\text{L}}}{\text{min}})\\&=1.68\,\text{kg/min}.\end{aligned}$$

**Step 2**: Calculating the rate at which substance exits the tank.
The volume is
$$V(t)=640+24t-16t=(640+8t)\,\text{L}.$$
The concentration is $\frac{Q}{640+8t}\,\text{kg/L}.$ Hence,
$$\begin{aligned}Q'_{\text{out}}&=(16\,\frac{\text{L}}{\text{min}})\cdot(\frac{Q}{640+8t}\,\frac{\text{kg}}{\text{L}})\\
&=(16\,\frac{\cancel{\text{L}}}{\text{min}})\cdot(\frac{Q}{640+8t}\,\frac{\text{kg}}{\cancel{\text{L}}})\\
&=\frac{16Q}{640+8t}\,\text{kg/min}=\frac{2Q}{80+t}\,\text{kg/min}.\end{aligned}$$

**Step 3**: Calculate the overall rate of change.
$$\begin{aligned}\frac{dQ}{dt}&=Q'_{\text{in}}-Q'_{\text{out}}\\&=1.68-\frac{2Q}{80+t}.\end{aligned}$$
Thus,
$$\frac{dQ}{dt}+\frac{2}{80+t}Q=1.68.$$

**Step 4**: Integrate the equation.
This is a first-order linear equation with variable coefficients. So we find the general solution using an integrating factor:
$$\begin{aligned}I(t)&=e^{\int 2/(80+t)\,dt}\\&=e^{2\ln|80+t|}\\&=e^{\ln (80+t)^{2}}\\&=(80+t)^{2}.\end{aligned}$$
Multiplying both sides by $I(t)=(80+t)^{2}$ yields
$$\begin{aligned}(80+t)^{2}\cdot(\frac{dQ}{dt}+\frac{2}{80+t}Q)&=(80+t)^{2}\cdot 1.68\\
(80+t)^{2}\frac{dQ}{dt}+2(80+t)^{1}Q&=1.68(80+t)^{2}\\\frac{d}{dt}(Q(80+t)^{2})&=1.68(80+t)^{2}.\end{aligned}$$
Now, we integrate with respect to $t:$
$$\begin{aligned}\int\frac{d}{dt}(Q(80+t)^{2})\,dt&=\int 1.68(80+t)^{2}\,dt\\Q(80+t)^{2}&=1.68\cdot\frac{1}{3}(80+t)^{3}+C\\Q(t)&=0.56(80+t)+C(80+t)^{-2}.\end{aligned}$$
Note that $C$ is a constant of integration.
The initial condition is $Q(0)=15.$ Thus,
$$\begin{aligned}0.56(80+0)+C(80+0)^{-2}&=15\\
44.8+C(80)^{-2}&=15\\C(80)^{-2}&=-29.8\\C&=-190720.\end{aligned}$$
Finally, we obtain the following expression for $Q(t):$
$$Q(t)=\frac{14 t}{25} + \frac{224}{5} - \frac{190720}{\left(t + 80\right)^{2}}.$$
Finally, the amount in the tank $11$ minutes after pumping begins is
$$\begin{aligned}Q(11)&=0.56(80+11)-29.8(\frac{80}{80+11})^{2}\\&=50.96-29.8(\frac{80}{91})^{2}\\&\approx 27.93\,\text{kg}.\end{aligned}$$
This is rounded to two decimal places.

---
q-339394 | observed:q-339394 | :question.difficulty/moderate | eligible=False

A juice-processing tank initially holds $400\,\text{L}$ of liquid containing $4.8\,\text{kg}$ of dissolved sugar.
A solution containing $0.036\,\text{kg/L}$ of dissolved sugar is pumped into the tank at a rate of $20\,\text{L/min},$ while the completely mixed liquid is drained out at a rate of $30\,\text{L/min}.$ If the amount of sugar $Q(t),$ in kilograms, in the tank $t$ minutes after pumping begins is given by

$$
Q(t)=\alpha \,(1-\frac{t}{40})+\beta {(1-\frac{t}{40})}^{3}
$$

where $\alpha $ and $\beta $ are constants, what is the value of $\alpha -\beta ?$

- $36$
- $18$
- $24$ [correct]
- $28.8$
- $21.6$

Since $Q$ is the amount of salt in the tank at time $t,$ the derivative 

$$
\frac{dQ}{dt}
$$

describes how this amount changes with respect to time $t,$ in minutes. This is equal to the rate at which sugar enters the tank minus the rate at which sugar leaves the tank.

$$
\frac{dQ}{dt}={Q}_{\text{in}}^{′}-{Q}_{\text{out}}^{′}
$$

Note that the units of $\frac{dQ}{dt},{Q}_{\text{in}}^{′}$ and ${Q}_{\text{out}}^{′}$ are $\text{kg}/\text{min}.$ Now, let's compute the required rates of change in steps.

**Step 1**: Calculating the rate at which sugar enter the tank.

First, note that a liquid solution containing $0.036\,\text{kg/L}$ of sugar enters the tank at a rate of $20\,\text{L/min}.$ So, the rate at which the *sugar* enters the tank is 

$$
\begin{aligned}{Q}_{\text{in}}^{′} & =(0.036\,\frac{\text{kg}}{\text{L}})\cdot (20\,\frac{\text{L}}{\text{min}}) \\  & =(0.036\,\frac{\text{kg}}{\cancel{\text{L}}})\cdot (20\,\frac{\cancel{\text{L}}}{\text{min}}) \\  & =0.72\,\frac{\text{kg}}{\text{min}}.\end{aligned}
$$

**Step 2**: Calculating the rate at which sugar exit the tank.

To find the rate at which sugar leaves the tank, we must first determine the volume of liquid in the tank at time $t.$

The tank initially contains $400\,\text{L}$ of liquid; a solution enters at $20\,\text{L/min}$ and leaves at $30\,\text{L/min}.$
As a result, the amount of liquid in the tank after $t$ minutes is 

$$
400+20t-30t=(400-10t)\,\text{L}.
$$

Since $Q$ is the amount of sugar in the tank, the *concentration* of the mixed solution at time $t$ is

$$
\frac{Q}{400-10t}\,\text{kg/L}.
$$

Therefore, as the completely mixed liquid leaves at a rate of $30\,\text{L/min},$ *sugar* leaves at a rate of

$$
\begin{aligned}{Q}_{\text{out}}^{′} & =(30\,\frac{\text{L}}{\text{min}})\cdot (\frac{Q}{400-10t}\,\frac{\text{kg}}{\text{L}}) \\  & =(30\,\frac{\cancel{\text{L}}}{\text{min}})\cdot (\frac{Q}{400-10t}\,\frac{\text{kg}}{\cancel{\text{L}}}) \\  & =\frac{30Q}{400-10t}\,\frac{\text{kg}}{\text{min}} \\  & =\frac{3Q}{40-t}\,\frac{\text{kg}}{\text{min}}.\end{aligned}
$$

**Step 3**: Calculate the overall rate of change.

The rate of change equals the rate of entry minus the rate of exit. Therefore, 

$$
\begin{aligned}\frac{dQ}{dt} & ={Q}_{\text{in}}^{′}-{Q}_{\text{out}}^{′} \\  & =0.72-\frac{3Q}{40-t}\end{aligned}
$$

which gives the equation

$$
\begin{aligned}\frac{dQ}{dt}+\frac{3}{40-t}Q=0.72.\end{aligned}
$$

**Step 4**: Integrate the equation.

This is a first-order linear equation with variable coefficients. So we find the general solution using an integrating factor:

$$
\begin{aligned}I(t) & ={e}^{\int 3/(40-t)\,dt} \\  & ={e}^{-3\operatorname{ln}⁡|40-t|} \\  & ={e}^{\operatorname{ln}⁡(40-t)^{-3}} \\  & =(40-t)^{-3}\end{aligned}
$$

Multiplying both sides of the differential equation by $I(t)=(40-t)^{-3}$ yields

$$
\begin{aligned}(40-t)^{-3}\cdot (\frac{dQ}{dt}+\frac{3}{40-t}Q) & =(40-t)^{-3}\cdot 0.72 \\ (40-t)^{-3}\frac{dQ}{dt}+3(40-t)^{-4}Q & =0.72(40-t)^{-3} \\ \frac{d}{dt}(Q(40-t)^{-3}) & =0.72(40-t)^{-3}.\end{aligned}
$$

Now, we integrate with respect to $t:$

$$
\begin{aligned}\int \frac{d}{dt}(Q(40-t)^{-3})\,dt & =\int 0.72(40-t)^{-3}\,dt \\ Q(40-t)^{-3} & =0.72\cdot \frac{1}{2}(40-t)^{-2}+C \\ Q(t) & =0.36(40-t)+C(40-t)^{3}\end{aligned}
$$

Note that $C$ is a constant of integration.

We're told that the tank initially contains $4.8\,\text{kg}$ of sugar. So, we can apply the initial condition $Q(0)=4.8,$ and solve for $C:$

$$
\begin{aligned}Q(0) & =4.8 \\ C(40-0)^{3}+0.36(40-0) & =4.8 \\ C(40)^{3}+14.4 & =4.8 \\ C & =-\frac{9.6}{{40}^{3}}\end{aligned}
$$

Finally, we obtain the following expression for $Q(t):$

$$
\begin{aligned}Q(t) & =0.36(40-t)-\frac{9.6}{{40}^{3}}(40-t)^{3} \\  & =0.36\cdot 40\,(\frac{40-t}{40})-9.6{(\frac{40-t}{40})}^{3} \\  & =14.4\,(1-\frac{t}{40})-9.6{(1-\frac{t}{40})}^{3}.\end{aligned}
$$

Finally, we have $\alpha =14.4,\beta =-9.6,$ and

$$
\alpha -\beta =14.4-(-9.6)=24.
$$

---
q-339394 | observed:q-339394 | :question.difficulty/moderate | eligible=False

A juice-processing tank initially holds $400\,\text{L}$ of liquid containing $5\,\text{kg}$ of dissolved sugar.
A solution containing $0.0375\,\text{kg/L}$ of dissolved sugar is pumped into the tank at a rate of $20\,\text{L/min},$ while the completely mixed liquid is drained out at a rate of $30\,\text{L/min}.$ If the amount of sugar $Q(t),$ in kilograms, in the tank $t$ minutes after pumping begins is given by

$$
Q(t)=\alpha \,(1-\frac{t}{40})+\beta {(1-\frac{t}{40})}^{3}
$$

where $\alpha $ and $\beta $ are constants, what is the value of $\alpha -\beta ?$

- $37.5$
- $18.75$
- $25$ [correct]
- $30$
- $22.5$

Since $Q$ is the amount of salt in the tank at time $t,$ the derivative 

$$
\frac{dQ}{dt}
$$

describes how this amount changes with respect to time $t,$ in minutes. This is equal to the rate at which sugar enters the tank minus the rate at which sugar leaves the tank.

$$
\frac{dQ}{dt}={Q}_{\text{in}}^{′}-{Q}_{\text{out}}^{′}
$$

Note that the units of $\frac{dQ}{dt},{Q}_{\text{in}}^{′}$ and ${Q}_{\text{out}}^{′}$ are $\text{kg}/\text{min}.$ Now, let's compute the required rates of change in steps.

**Step 1**: Calculating the rate at which sugar enter the tank.

First, note that a liquid solution containing $0.0375\,\text{kg/L}$ of sugar enters the tank at a rate of $20\,\text{L/min}.$ So, the rate at which the *sugar* enters the tank is 

$$
\begin{aligned}{Q}_{\text{in}}^{′} & =(0.0375\,\frac{\text{kg}}{\text{L}})\cdot (20\,\frac{\text{L}}{\text{min}}) \\  & =(0.0375\,\frac{\text{kg}}{\cancel{\text{L}}})\cdot (20\,\frac{\cancel{\text{L}}}{\text{min}}) \\  & =0.75\,\frac{\text{kg}}{\text{min}}.\end{aligned}
$$

**Step 2**: Calculating the rate at which sugar exit the tank.

To find the rate at which sugar leaves the tank, we must first determine the volume of liquid in the tank at time $t.$

The tank initially contains $400\,\text{L}$ of liquid; a solution enters at $20\,\text{L/min}$ and leaves at $30\,\text{L/min}.$
As a result, the amount of liquid in the tank after $t$ minutes is 

$$
400+20t-30t=(400-10t)\,\text{L}.
$$

Since $Q$ is the amount of sugar in the tank, the *concentration* of the mixed solution at time $t$ is

$$
\frac{Q}{400-10t}\,\text{kg/L}.
$$

Therefore, as the completely mixed liquid leaves at a rate of $30\,\text{L/min},$ *sugar* leaves at a rate of

$$
\begin{aligned}{Q}_{\text{out}}^{′} & =(30\,\frac{\text{L}}{\text{min}})\cdot (\frac{Q}{400-10t}\,\frac{\text{kg}}{\text{L}}) \\  & =(30\,\frac{\cancel{\text{L}}}{\text{min}})\cdot (\frac{Q}{400-10t}\,\frac{\text{kg}}{\cancel{\text{L}}}) \\  & =\frac{30Q}{400-10t}\,\frac{\text{kg}}{\text{min}} \\  & =\frac{3Q}{40-t}\,\frac{\text{kg}}{\text{min}}.\end{aligned}
$$

**Step 3**: Calculate the overall rate of change.

The rate of change equals the rate of entry minus the rate of exit. Therefore, 

$$
\begin{aligned}\frac{dQ}{dt} & ={Q}_{\text{in}}^{′}-{Q}_{\text{out}}^{′} \\  & =0.75-\frac{3Q}{40-t}\end{aligned}
$$

which gives the equation

$$
\begin{aligned}\frac{dQ}{dt}+\frac{3}{40-t}Q=0.75.\end{aligned}
$$

**Step 4**: Integrate the equation.

This is a first-order linear equation with variable coefficients. So we find the general solution using an integrating factor:

$$
\begin{aligned}I(t) & ={e}^{\int 3/(40-t)\,dt} \\  & ={e}^{-3\operatorname{ln}⁡|40-t|} \\  & ={e}^{\operatorname{ln}⁡(40-t)^{-3}} \\  & =(40-t)^{-3}\end{aligned}
$$

Multiplying both sides of the differential equation by $I(t)=(40-t)^{-3}$ yields

$$
\begin{aligned}(40-t)^{-3}\cdot (\frac{dQ}{dt}+\frac{3}{40-t}Q) & =(40-t)^{-3}\cdot 0.75 \\ (40-t)^{-3}\frac{dQ}{dt}+3(40-t)^{-4}Q & =0.75(40-t)^{-3} \\ \frac{d}{dt}(Q(40-t)^{-3}) & =0.75(40-t)^{-3}.\end{aligned}
$$

Now, we integrate with respect to $t:$

$$
\begin{aligned}\int \frac{d}{dt}(Q(40-t)^{-3})\,dt & =\int 0.75(40-t)^{-3}\,dt \\ Q(40-t)^{-3} & =0.75\cdot \frac{1}{2}(40-t)^{-2}+C \\ Q(t) & =0.375(40-t)+C(40-t)^{3}\end{aligned}
$$

Note that $C$ is a constant of integration.

We're told that the tank initially contains $5\,\text{kg}$ of sugar. So, we can apply the initial condition $Q(0)=5,$ and solve for $C:$

$$
\begin{aligned}Q(0) & =5 \\ C(40-0)^{3}+0.375(40-0) & =5 \\ C(40)^{3}+15 & =5 \\ C & =-\frac{10}{{40}^{3}}\end{aligned}
$$

Finally, we obtain the following expression for $Q(t):$

$$
\begin{aligned}Q(t) & =0.375(40-t)-\frac{10}{{40}^{3}}(40-t)^{3} \\  & =0.375\cdot 40\,(\frac{40-t}{40})-10{(\frac{40-t}{40})}^{3} \\  & =15\,(1-\frac{t}{40})-10{(1-\frac{t}{40})}^{3}.\end{aligned}
$$

Finally, we have $\alpha =15,\beta =-10,$ and

$$
\alpha -\beta =15-(-10)=25.
$$

---
q-339394 | authored-operations | :question.difficulty/moderate | eligible=True

A juice-processing tank initially holds $400\,\text{L}$ of liquid containing $16\,\text{kg}$ of dissolved sugar.
A solution containing $0.05\,\text{kg/L}$ of dissolved sugar is pumped into the tank at a rate of $16\,\text{L/min},$ while the completely mixed liquid is drained out at a rate of $24\,\text{L/min}.$ If the amount of sugar $Q(t),$ in kilograms, in the tank $t$ minutes after pumping begins is given by

$$
Q(t)=\alpha \,(1-\frac{t}{50})+\beta {(1-\frac{t}{50})}^{3}
$$

where $\alpha $ and $\beta $ are constants, what is the value of $\alpha -\beta ?$

- $36$
- $16$
- $40$
- $24$ [correct]
- $20$

Let $Q$ be the amount of dissolved substance in the tank at time $t,$ in minutes. The amount entering minus the amount leaving gives
$$\frac{dQ}{dt}=Q'_{\text{in}}-Q'_{\text{out}}.$$
The units of these rates are $\text{kg/min}.$

**Step 1**: Calculating the rate at which substance enters the tank.
$$\begin{aligned}Q'_{\text{in}}&=(0.05\,\frac{\text{kg}}{\text{L}})\cdot(16\,\frac{\text{L}}{\text{min}})\\
&=(0.05\,\frac{\text{kg}}{\cancel{\text{L}}})\cdot(16\,\frac{\cancel{\text{L}}}{\text{min}})\\&=0.8\,\text{kg/min}.\end{aligned}$$

**Step 2**: Calculating the rate at which substance exits the tank.
The volume is
$$V(t)=400+16t-24t=(400-8t)\,\text{L}.$$
The concentration is $\frac{Q}{400-8t}\,\text{kg/L}.$ Hence,
$$\begin{aligned}Q'_{\text{out}}&=(24\,\frac{\text{L}}{\text{min}})\cdot(\frac{Q}{400-8t}\,\frac{\text{kg}}{\text{L}})\\
&=(24\,\frac{\cancel{\text{L}}}{\text{min}})\cdot(\frac{Q}{400-8t}\,\frac{\text{kg}}{\cancel{\text{L}}})\\
&=\frac{24Q}{400-8t}\,\text{kg/min}=\frac{3Q}{50-t}\,\text{kg/min}.\end{aligned}$$

**Step 3**: Calculate the overall rate of change.
$$\begin{aligned}\frac{dQ}{dt}&=Q'_{\text{in}}-Q'_{\text{out}}\\&=0.8-\frac{3Q}{50-t}.\end{aligned}$$
Thus,
$$\frac{dQ}{dt}+\frac{3}{50-t}Q=0.8.$$

**Step 4**: Integrate the equation.
This is a first-order linear equation with variable coefficients. So we find the general solution using an integrating factor:
$$\begin{aligned}I(t)&=e^{\int 3/(50-t)\,dt}\\&=e^{-3\ln|50-t|}\\&=e^{\ln (50-t)^{-3}}\\&=(50-t)^{-3}.\end{aligned}$$
Multiplying both sides by $I(t)=(50-t)^{-3}$ yields
$$\begin{aligned}(50-t)^{-3}\cdot(\frac{dQ}{dt}+\frac{3}{50-t}Q)&=(50-t)^{-3}\cdot 0.8\\
(50-t)^{-3}\frac{dQ}{dt}+3(50-t)^{-4}Q&=0.8(50-t)^{-3}\\\frac{d}{dt}(Q(50-t)^{-3})&=0.8(50-t)^{-3}.\end{aligned}$$
Now, we integrate with respect to $t:$
$$\begin{aligned}\int\frac{d}{dt}(Q(50-t)^{-3})\,dt&=\int 0.8(50-t)^{-3}\,dt\\Q(50-t)^{-3}&=0.8\cdot\frac{1}{2}(50-t)^{-2}+C\\Q(t)&=0.4(50-t)+C(50-t)^{3}.\end{aligned}$$
Note that $C$ is a constant of integration.
The initial condition is $Q(0)=16.$ Thus,
$$\begin{aligned}0.4(50-0)+C(50-0)^{3}&=16\\
20+C(50)^{3}&=16\\C(50)^{3}&=-4\\C&=- \frac{1}{31250}.\end{aligned}$$
Finally, we obtain the following expression for $Q(t):$
$$Q(t)=- \frac{2 t}{5} - \frac{\left(50 - t\right)^{3}}{31250} + 20.$$
Writing this in the supplied normalized form gives
$$Q(t)=20(1-\frac{t}{50})-4(1-\frac{t}{50})^{3}.$$
Finally, we have $\alpha=20,\beta=-4,$ and
$$\alpha-\beta=20-(-4)=24.$$

---
q-339394 | authored-operations | :question.difficulty/moderate | eligible=True

A juice-processing tank initially holds $600\,\text{L}$ of liquid containing $21\,\text{kg}$ of dissolved sugar.
A solution containing $0.05\,\text{kg/L}$ of dissolved sugar is pumped into the tank at a rate of $24\,\text{L/min},$ while the completely mixed liquid is drained out at a rate of $36\,\text{L/min}.$ If the amount of sugar $Q(t),$ in kilograms, in the tank $t$ minutes after pumping begins is given by

$$
Q(t)=\alpha \,(1-\frac{t}{50})+\beta {(1-\frac{t}{50})}^{3}
$$

where $\alpha $ and $\beta $ are constants, what is the value of $\alpha -\beta ?$

- $30$
- $60$
- $21$
- $39$ [correct]
- $51$

Let $Q$ be the amount of dissolved substance in the tank at time $t,$ in minutes. The amount entering minus the amount leaving gives
$$\frac{dQ}{dt}=Q'_{\text{in}}-Q'_{\text{out}}.$$
The units of these rates are $\text{kg/min}.$

**Step 1**: Calculating the rate at which substance enters the tank.
$$\begin{aligned}Q'_{\text{in}}&=(0.05\,\frac{\text{kg}}{\text{L}})\cdot(24\,\frac{\text{L}}{\text{min}})\\
&=(0.05\,\frac{\text{kg}}{\cancel{\text{L}}})\cdot(24\,\frac{\cancel{\text{L}}}{\text{min}})\\&=1.2\,\text{kg/min}.\end{aligned}$$

**Step 2**: Calculating the rate at which substance exits the tank.
The volume is
$$V(t)=600+24t-36t=(600-12t)\,\text{L}.$$
The concentration is $\frac{Q}{600-12t}\,\text{kg/L}.$ Hence,
$$\begin{aligned}Q'_{\text{out}}&=(36\,\frac{\text{L}}{\text{min}})\cdot(\frac{Q}{600-12t}\,\frac{\text{kg}}{\text{L}})\\
&=(36\,\frac{\cancel{\text{L}}}{\text{min}})\cdot(\frac{Q}{600-12t}\,\frac{\text{kg}}{\cancel{\text{L}}})\\
&=\frac{36Q}{600-12t}\,\text{kg/min}=\frac{3Q}{50-t}\,\text{kg/min}.\end{aligned}$$

**Step 3**: Calculate the overall rate of change.
$$\begin{aligned}\frac{dQ}{dt}&=Q'_{\text{in}}-Q'_{\text{out}}\\&=1.2-\frac{3Q}{50-t}.\end{aligned}$$
Thus,
$$\frac{dQ}{dt}+\frac{3}{50-t}Q=1.2.$$

**Step 4**: Integrate the equation.
This is a first-order linear equation with variable coefficients. So we find the general solution using an integrating factor:
$$\begin{aligned}I(t)&=e^{\int 3/(50-t)\,dt}\\&=e^{-3\ln|50-t|}\\&=e^{\ln (50-t)^{-3}}\\&=(50-t)^{-3}.\end{aligned}$$
Multiplying both sides by $I(t)=(50-t)^{-3}$ yields
$$\begin{aligned}(50-t)^{-3}\cdot(\frac{dQ}{dt}+\frac{3}{50-t}Q)&=(50-t)^{-3}\cdot 1.2\\
(50-t)^{-3}\frac{dQ}{dt}+3(50-t)^{-4}Q&=1.2(50-t)^{-3}\\\frac{d}{dt}(Q(50-t)^{-3})&=1.2(50-t)^{-3}.\end{aligned}$$
Now, we integrate with respect to $t:$
$$\begin{aligned}\int\frac{d}{dt}(Q(50-t)^{-3})\,dt&=\int 1.2(50-t)^{-3}\,dt\\Q(50-t)^{-3}&=1.2\cdot\frac{1}{2}(50-t)^{-2}+C\\Q(t)&=0.6(50-t)+C(50-t)^{3}.\end{aligned}$$
Note that $C$ is a constant of integration.
The initial condition is $Q(0)=21.$ Thus,
$$\begin{aligned}0.6(50-0)+C(50-0)^{3}&=21\\
30+C(50)^{3}&=21\\C(50)^{3}&=-9\\C&=- \frac{9}{125000}.\end{aligned}$$
Finally, we obtain the following expression for $Q(t):$
$$Q(t)=- \frac{3 t}{5} - \frac{9 \left(50 - t\right)^{3}}{125000} + 30.$$
Writing this in the supplied normalized form gives
$$Q(t)=30(1-\frac{t}{50})-9(1-\frac{t}{50})^{3}.$$
Finally, we have $\alpha=30,\beta=-9,$ and
$$\alpha-\beta=30-(-9)=39.$$

---
q-339396 | observed:q-339396 | :question.difficulty/moderate | eligible=False

A fruit syrup tank initially holds $240\,\text{L}$ of liquid containing $8.4\,\text{kg}$ of dissolved sweetener.
A solution containing $0.06\,\text{kg/L}$ of dissolved sweetener is pumped into the tank at a rate of $24\,\text{L/min},$ while the completely mixed liquid is drained out at a rate of $32\,\text{L/min}.$ If the amount of sweetener $Q(t),$ in kilograms, in the tank $t$ minutes after pumping begins is given by

$$
Q(t)=\alpha \,(1-\frac{t}{30})+\beta {(1-\frac{t}{30})}^{4}
$$

where $\alpha $ and $\beta $ are constants, what is the value of $\alpha -\beta ?$

- $16.8$
- $31.2$
- $24$
- $34.8$
- $20.4$ [correct]

Since $Q$ is the amount of salt in the tank at time $t,$ the derivative 

$$
\frac{dQ}{dt}
$$

describes how this amount changes with respect to time $t,$ in minutes. This is equal to the rate at which sweetener enters the tank minus the rate at which sweetener leaves the tank.

$$
\frac{dQ}{dt}={Q}_{\text{in}}^{′}-{Q}_{\text{out}}^{′}
$$

Note that the units of $\frac{dQ}{dt},{Q}_{\text{in}}^{′}$ and ${Q}_{\text{out}}^{′}$ are $\text{kg}/\text{min}.$ Now, let's compute the required rates of change in steps.

**Step 1**: Calculating the rate at which sweetener enter the tank.

First, note that a solution containing $0.06\,\text{kg/L}$ of sweetener enters the tank at a rate of $24\,\text{L/min}.$ So, the rate at which the *sweetener* enters the tank is 

$$
\begin{aligned}{Q}_{\text{in}}^{′} & =(0.06\,\frac{\text{kg}}{\text{L}})\cdot (24\,\frac{\text{L}}{\text{min}}) \\  & =(0.06\,\frac{\text{kg}}{\cancel{\text{L}}})\cdot (24\,\frac{\cancel{\text{L}}}{\text{min}}) \\  & =1.44\,\frac{\text{kg}}{\text{min}}.\end{aligned}
$$

**Step 2**: Calculating the rate at which sweetener exit the tank.

To find the rate at which sweetener leaves the tank, we must first determine the volume of liquid in the tank at time $t.$

The tank initially contains $240\,\text{L}$ of liquid; a solution enters at $24\,\text{L/min}$ and leaves at $32\,\text{L/min}.$
As a result, the amount of liquid in the tank after $t$ minutes is 

$$
240+24t-32t=(240-8t)\,\text{L}.
$$

Since $Q$ is the amount of sweetener in the tank, the *concentration* of the mixed solution at time $t$ is

$$
\frac{Q}{240-8t}\,\text{kg/L}.
$$

Therefore, as the completely mixed liquid leaves at a rate of $32\,\text{L/min},$ *sweetener* leaves at a rate of

$$
\begin{aligned}{Q}_{\text{out}}^{′} & =(32\,\frac{\text{L}}{\text{min}})\cdot (\frac{Q}{240-8t}\,\frac{\text{kg}}{\text{L}}) \\  & =(32\,\frac{\cancel{\text{L}}}{\text{min}})\cdot (\frac{Q}{240-8t}\,\frac{\text{kg}}{\cancel{\text{L}}}) \\  & =\frac{32Q}{240-8t}\,\frac{\text{kg}}{\text{min}} \\  & =\frac{4Q}{30-t}\,\frac{\text{kg}}{\text{min}}.\end{aligned}
$$

**Step 3**: Calculate the overall rate of change.

The rate of change equals the rate of entry minus the rate of exit. Therefore, 

$$
\begin{aligned}\frac{dQ}{dt} & ={Q}_{\text{in}}^{′}-{Q}_{\text{out}}^{′} \\  & =1.44-\frac{4Q}{30-t}\end{aligned}
$$

which gives the equation

$$
\begin{aligned}\frac{dQ}{dt}+\frac{4}{30-t}Q=1.44.\end{aligned}
$$

**Step 4**: Integrate the equation.

This is a first-order linear equation with variable coefficients. So we find the general solution using an integrating factor:

$$
\begin{aligned}I(t) & ={e}^{\int 4/(30-t)\,dt} \\  & ={e}^{-4\operatorname{ln}⁡|30-t|} \\  & ={e}^{\operatorname{ln}⁡(30-t)^{-4}} \\  & =(30-t)^{-4}\end{aligned}
$$

Multiplying both sides of the differential equation by $I(t)=(30-t)^{-4}$ yields

$$
\begin{aligned}(30-t)^{-4}\cdot (\frac{dQ}{dt}+\frac{4}{30-t}Q) & =(30-t)^{-4}\cdot 1.44 \\ (30-t)^{-4}\frac{dQ}{dt}+4(30-t)^{-5}Q & =1.44(30-t)^{-4} \\ \frac{d}{dt}(Q(30-t)^{-4}) & =1.44(30-t)^{-4}.\end{aligned}
$$

Now, we integrate with respect to $t:$

$$
\begin{aligned}\int \frac{d}{dt}(Q(30-t)^{-4})\,dt & =\int 1.44(30-t)^{-4}\,dt \\ Q(30-t)^{-4} & =1.44\cdot \frac{1}{3}(30-t)^{-3}+C \\ Q(t) & =0.48(30-t)+C(30-t)^{4}\end{aligned}
$$

Note that $C$ is a constant of integration.

We're told that the tank initially contains $8.4\,\text{kg}$ of sweetener. So, we can apply the initial condition $Q(0)=8.4,$ and solve for $C:$

$$
\begin{aligned}Q(0) & =8.4 \\ C(30-0)^{4}+0.48(30-0) & =8.4 \\ C(30)^{4}+14.4 & =8.4 \\ C & =-\frac{6}{{30}^{4}}\end{aligned}
$$

Finally, we obtain the following expression for $Q(t):$

$$
\begin{aligned}Q(t) & =0.48(30-t)-\frac{6}{{30}^{4}}(30-t)^{4} \\  & =0.48\cdot 30\,(\frac{30-t}{30})-6{(\frac{30-t}{30})}^{4} \\  & =14.4\,(1-\frac{t}{30})-6{(1-\frac{t}{30})}^{4}.\end{aligned}
$$

Finally, we have $\alpha =14.4,\beta =-6,$ and

$$
\alpha -\beta =14.4-(-6)=20.4.
$$

---
q-339396 | observed:q-339396 | :question.difficulty/moderate | eligible=False

A fruit syrup tank initially holds $240\,\text{L}$ of liquid containing $8.75\,\text{kg}$ of dissolved sweetener.
A solution containing $0.0625\,\text{kg/L}$ of dissolved sweetener is pumped into the tank at a rate of $24\,\text{L/min},$ while the completely mixed liquid is drained out at a rate of $32\,\text{L/min}.$ If the amount of sweetener $Q(t),$ in kilograms, in the tank $t$ minutes after pumping begins is given by

$$
Q(t)=\alpha \,(1-\frac{t}{30})+\beta {(1-\frac{t}{30})}^{4}
$$

where $\alpha $ and $\beta $ are constants, what is the value of $\alpha -\beta ?$

- $17.5$
- $32.5$
- $25$
- $36.25$
- $21.25$ [correct]

Since $Q$ is the amount of salt in the tank at time $t,$ the derivative 

$$
\frac{dQ}{dt}
$$

describes how this amount changes with respect to time $t,$ in minutes. This is equal to the rate at which sweetener enters the tank minus the rate at which sweetener leaves the tank.

$$
\frac{dQ}{dt}={Q}_{\text{in}}^{′}-{Q}_{\text{out}}^{′}
$$

Note that the units of $\frac{dQ}{dt},{Q}_{\text{in}}^{′}$ and ${Q}_{\text{out}}^{′}$ are $\text{kg}/\text{min}.$ Now, let's compute the required rates of change in steps.

**Step 1**: Calculating the rate at which sweetener enter the tank.

First, note that a solution containing $0.0625\,\text{kg/L}$ of sweetener enters the tank at a rate of $24\,\text{L/min}.$ So, the rate at which the *sweetener* enters the tank is 

$$
\begin{aligned}{Q}_{\text{in}}^{′} & =(0.0625\,\frac{\text{kg}}{\text{L}})\cdot (24\,\frac{\text{L}}{\text{min}}) \\  & =(0.0625\,\frac{\text{kg}}{\cancel{\text{L}}})\cdot (24\,\frac{\cancel{\text{L}}}{\text{min}}) \\  & =1.5\,\frac{\text{kg}}{\text{min}}.\end{aligned}
$$

**Step 2**: Calculating the rate at which sweetener exit the tank.

To find the rate at which sweetener leaves the tank, we must first determine the volume of liquid in the tank at time $t.$

The tank initially contains $240\,\text{L}$ of liquid; a solution enters at $24\,\text{L/min}$ and leaves at $32\,\text{L/min}.$
As a result, the amount of liquid in the tank after $t$ minutes is 

$$
240+24t-32t=(240-8t)\,\text{L}.
$$

Since $Q$ is the amount of sweetener in the tank, the *concentration* of the mixed solution at time $t$ is

$$
\frac{Q}{240-8t}\,\text{kg/L}.
$$

Therefore, as the completely mixed liquid leaves at a rate of $32\,\text{L/min},$ *sweetener* leaves at a rate of

$$
\begin{aligned}{Q}_{\text{out}}^{′} & =(32\,\frac{\text{L}}{\text{min}})\cdot (\frac{Q}{240-8t}\,\frac{\text{kg}}{\text{L}}) \\  & =(32\,\frac{\cancel{\text{L}}}{\text{min}})\cdot (\frac{Q}{240-8t}\,\frac{\text{kg}}{\cancel{\text{L}}}) \\  & =\frac{32Q}{240-8t}\,\frac{\text{kg}}{\text{min}} \\  & =\frac{4Q}{30-t}\,\frac{\text{kg}}{\text{min}}.\end{aligned}
$$

**Step 3**: Calculate the overall rate of change.

The rate of change equals the rate of entry minus the rate of exit. Therefore, 

$$
\begin{aligned}\frac{dQ}{dt} & ={Q}_{\text{in}}^{′}-{Q}_{\text{out}}^{′} \\  & =1.5-\frac{4Q}{30-t}\end{aligned}
$$

which gives the equation

$$
\begin{aligned}\frac{dQ}{dt}+\frac{4}{30-t}Q=1.5.\end{aligned}
$$

**Step 4**: Integrate the equation.

This is a first-order linear equation with variable coefficients. So we find the general solution using an integrating factor:

$$
\begin{aligned}I(t) & ={e}^{\int 4/(30-t)\,dt} \\  & ={e}^{-4\operatorname{ln}⁡|30-t|} \\  & ={e}^{\operatorname{ln}⁡(30-t)^{-4}} \\  & =(30-t)^{-4}\end{aligned}
$$

Multiplying both sides of the differential equation by $I(t)=(30-t)^{-4}$ yields

$$
\begin{aligned}(30-t)^{-4}\cdot (\frac{dQ}{dt}+\frac{4}{30-t}Q) & =(30-t)^{-4}\cdot 1.5 \\ (30-t)^{-4}\frac{dQ}{dt}+4(30-t)^{-5}Q & =1.5(30-t)^{-4} \\ \frac{d}{dt}(Q(30-t)^{-4}) & =1.5(30-t)^{-4}.\end{aligned}
$$

Now, we integrate with respect to $t:$

$$
\begin{aligned}\int \frac{d}{dt}(Q(30-t)^{-4})\,dt & =\int 1.5(30-t)^{-4}\,dt \\ Q(30-t)^{-4} & =1.5\cdot \frac{1}{3}(30-t)^{-3}+C \\ Q(t) & =0.5(30-t)+C(30-t)^{4}\end{aligned}
$$

Note that $C$ is a constant of integration.

We're told that the tank initially contains $8.75\,\text{kg}$ of sweetener. So, we can apply the initial condition $Q(0)=8.75,$ and solve for $C:$

$$
\begin{aligned}Q(0) & =8.75 \\ C(30-0)^{4}+0.5(30-0) & =8.75 \\ C(30)^{4}+15 & =8.75 \\ C & =-\frac{6.25}{{30}^{4}}\end{aligned}
$$

Finally, we obtain the following expression for $Q(t):$

$$
\begin{aligned}Q(t) & =0.5(30-t)-\frac{6.25}{{30}^{4}}(30-t)^{4} \\  & =0.5\cdot 30\,(\frac{30-t}{30})-6.25{(\frac{30-t}{30})}^{4} \\  & =15\,(1-\frac{t}{30})-6.25{(1-\frac{t}{30})}^{4}.\end{aligned}
$$

Finally, we have $\alpha =15,\beta =-6.25,$ and

$$
\alpha -\beta =15-(-6.25)=21.25.
$$

---
q-339396 | authored-operations | :question.difficulty/moderate | eligible=True

A fruit syrup tank initially holds $400\,\text{L}$ of liquid containing $16\,\text{kg}$ of dissolved sweetener.
A solution containing $0.05\,\text{kg/L}$ of dissolved sweetener is pumped into the tank at a rate of $24\,\text{L/min},$ while the completely mixed liquid is drained out at a rate of $32\,\text{L/min}.$ If the amount of sweetener $Q(t),$ in kilograms, in the tank $t$ minutes after pumping begins is given by

$$
Q(t)=\alpha \,(1-\frac{t}{50})+\beta {(1-\frac{t}{50})}^{4}
$$

where $\alpha $ and $\beta $ are constants, what is the value of $\alpha -\beta ?$

- $36$
- $16$
- $40$
- $24$ [correct]
- $20$

Let $Q$ be the amount of dissolved substance in the tank at time $t,$ in minutes. The amount entering minus the amount leaving gives
$$\frac{dQ}{dt}=Q'_{\text{in}}-Q'_{\text{out}}.$$
The units of these rates are $\text{kg/min}.$

**Step 1**: Calculating the rate at which substance enters the tank.
$$\begin{aligned}Q'_{\text{in}}&=(0.05\,\frac{\text{kg}}{\text{L}})\cdot(24\,\frac{\text{L}}{\text{min}})\\
&=(0.05\,\frac{\text{kg}}{\cancel{\text{L}}})\cdot(24\,\frac{\cancel{\text{L}}}{\text{min}})\\&=1.2\,\text{kg/min}.\end{aligned}$$

**Step 2**: Calculating the rate at which substance exits the tank.
The volume is
$$V(t)=400+24t-32t=(400-8t)\,\text{L}.$$
The concentration is $\frac{Q}{400-8t}\,\text{kg/L}.$ Hence,
$$\begin{aligned}Q'_{\text{out}}&=(32\,\frac{\text{L}}{\text{min}})\cdot(\frac{Q}{400-8t}\,\frac{\text{kg}}{\text{L}})\\
&=(32\,\frac{\cancel{\text{L}}}{\text{min}})\cdot(\frac{Q}{400-8t}\,\frac{\text{kg}}{\cancel{\text{L}}})\\
&=\frac{32Q}{400-8t}\,\text{kg/min}=\frac{4Q}{50-t}\,\text{kg/min}.\end{aligned}$$

**Step 3**: Calculate the overall rate of change.
$$\begin{aligned}\frac{dQ}{dt}&=Q'_{\text{in}}-Q'_{\text{out}}\\&=1.2-\frac{4Q}{50-t}.\end{aligned}$$
Thus,
$$\frac{dQ}{dt}+\frac{4}{50-t}Q=1.2.$$

**Step 4**: Integrate the equation.
This is a first-order linear equation with variable coefficients. So we find the general solution using an integrating factor:
$$\begin{aligned}I(t)&=e^{\int 4/(50-t)\,dt}\\&=e^{-4\ln|50-t|}\\&=e^{\ln (50-t)^{-4}}\\&=(50-t)^{-4}.\end{aligned}$$
Multiplying both sides by $I(t)=(50-t)^{-4}$ yields
$$\begin{aligned}(50-t)^{-4}\cdot(\frac{dQ}{dt}+\frac{4}{50-t}Q)&=(50-t)^{-4}\cdot 1.2\\
(50-t)^{-4}\frac{dQ}{dt}+4(50-t)^{-5}Q&=1.2(50-t)^{-4}\\\frac{d}{dt}(Q(50-t)^{-4})&=1.2(50-t)^{-4}.\end{aligned}$$
Now, we integrate with respect to $t:$
$$\begin{aligned}\int\frac{d}{dt}(Q(50-t)^{-4})\,dt&=\int 1.2(50-t)^{-4}\,dt\\Q(50-t)^{-4}&=1.2\cdot\frac{1}{3}(50-t)^{-3}+C\\Q(t)&=0.4(50-t)+C(50-t)^{4}.\end{aligned}$$
Note that $C$ is a constant of integration.
The initial condition is $Q(0)=16.$ Thus,
$$\begin{aligned}0.4(50-0)+C(50-0)^{4}&=16\\
20+C(50)^{4}&=16\\C(50)^{4}&=-4\\C&=- \frac{1}{1562500}.\end{aligned}$$
Finally, we obtain the following expression for $Q(t):$
$$Q(t)=- \frac{2 t}{5} - \frac{\left(50 - t\right)^{4}}{1562500} + 20.$$
Writing this in the supplied normalized form gives
$$Q(t)=20(1-\frac{t}{50})-4(1-\frac{t}{50})^{4}.$$
Finally, we have $\alpha=20,\beta=-4,$ and
$$\alpha-\beta=20-(-4)=24.$$

---
q-339396 | authored-operations | :question.difficulty/moderate | eligible=True

A fruit syrup tank initially holds $600\,\text{L}$ of liquid containing $21\,\text{kg}$ of dissolved sweetener.
A solution containing $0.05\,\text{kg/L}$ of dissolved sweetener is pumped into the tank at a rate of $36\,\text{L/min},$ while the completely mixed liquid is drained out at a rate of $48\,\text{L/min}.$ If the amount of sweetener $Q(t),$ in kilograms, in the tank $t$ minutes after pumping begins is given by

$$
Q(t)=\alpha \,(1-\frac{t}{50})+\beta {(1-\frac{t}{50})}^{4}
$$

where $\alpha $ and $\beta $ are constants, what is the value of $\alpha -\beta ?$

- $30$
- $60$
- $21$
- $39$ [correct]
- $51$

Let $Q$ be the amount of dissolved substance in the tank at time $t,$ in minutes. The amount entering minus the amount leaving gives
$$\frac{dQ}{dt}=Q'_{\text{in}}-Q'_{\text{out}}.$$
The units of these rates are $\text{kg/min}.$

**Step 1**: Calculating the rate at which substance enters the tank.
$$\begin{aligned}Q'_{\text{in}}&=(0.05\,\frac{\text{kg}}{\text{L}})\cdot(36\,\frac{\text{L}}{\text{min}})\\
&=(0.05\,\frac{\text{kg}}{\cancel{\text{L}}})\cdot(36\,\frac{\cancel{\text{L}}}{\text{min}})\\&=1.8\,\text{kg/min}.\end{aligned}$$

**Step 2**: Calculating the rate at which substance exits the tank.
The volume is
$$V(t)=600+36t-48t=(600-12t)\,\text{L}.$$
The concentration is $\frac{Q}{600-12t}\,\text{kg/L}.$ Hence,
$$\begin{aligned}Q'_{\text{out}}&=(48\,\frac{\text{L}}{\text{min}})\cdot(\frac{Q}{600-12t}\,\frac{\text{kg}}{\text{L}})\\
&=(48\,\frac{\cancel{\text{L}}}{\text{min}})\cdot(\frac{Q}{600-12t}\,\frac{\text{kg}}{\cancel{\text{L}}})\\
&=\frac{48Q}{600-12t}\,\text{kg/min}=\frac{4Q}{50-t}\,\text{kg/min}.\end{aligned}$$

**Step 3**: Calculate the overall rate of change.
$$\begin{aligned}\frac{dQ}{dt}&=Q'_{\text{in}}-Q'_{\text{out}}\\&=1.8-\frac{4Q}{50-t}.\end{aligned}$$
Thus,
$$\frac{dQ}{dt}+\frac{4}{50-t}Q=1.8.$$

**Step 4**: Integrate the equation.
This is a first-order linear equation with variable coefficients. So we find the general solution using an integrating factor:
$$\begin{aligned}I(t)&=e^{\int 4/(50-t)\,dt}\\&=e^{-4\ln|50-t|}\\&=e^{\ln (50-t)^{-4}}\\&=(50-t)^{-4}.\end{aligned}$$
Multiplying both sides by $I(t)=(50-t)^{-4}$ yields
$$\begin{aligned}(50-t)^{-4}\cdot(\frac{dQ}{dt}+\frac{4}{50-t}Q)&=(50-t)^{-4}\cdot 1.8\\
(50-t)^{-4}\frac{dQ}{dt}+4(50-t)^{-5}Q&=1.8(50-t)^{-4}\\\frac{d}{dt}(Q(50-t)^{-4})&=1.8(50-t)^{-4}.\end{aligned}$$
Now, we integrate with respect to $t:$
$$\begin{aligned}\int\frac{d}{dt}(Q(50-t)^{-4})\,dt&=\int 1.8(50-t)^{-4}\,dt\\Q(50-t)^{-4}&=1.8\cdot\frac{1}{3}(50-t)^{-3}+C\\Q(t)&=0.6(50-t)+C(50-t)^{4}.\end{aligned}$$
Note that $C$ is a constant of integration.
The initial condition is $Q(0)=21.$ Thus,
$$\begin{aligned}0.6(50-0)+C(50-0)^{4}&=21\\
30+C(50)^{4}&=21\\C(50)^{4}&=-9\\C&=- \frac{9}{6250000}.\end{aligned}$$
Finally, we obtain the following expression for $Q(t):$
$$Q(t)=- \frac{3 t}{5} - \frac{9 \left(50 - t\right)^{4}}{6250000} + 30.$$
Writing this in the supplied normalized form gives
$$Q(t)=30(1-\frac{t}{50})-9(1-\frac{t}{50})^{4}.$$
Finally, we have $\alpha=30,\beta=-9,$ and
$$\alpha-\beta=30-(-9)=39.$$

---
q-339399 | observed:q-339399 | :question.difficulty/hard | eligible=False

A coolant reservoir initially holds $400\,\text{L}$ of liquid containing $7.2\,\text{kg}$ of dissolved corrosion inhibitor.
A feed solution containing $0.06\,\text{kg/L}$ of the inhibitor is pumped into the reservoir at a rate of $16\,\text{L/min},$ while the completely mixed liquid is drained out at a rate of $12\,\text{L/min}.$
Find, rounded to two decimal places, the amount of inhibitor in the reservoir $12$ minutes after pumping begins.

- $15.56\,\text{kg}$
- $14.92\,\text{kg}$ [correct]
- $15.84\,\text{kg}$
- $13.05\,\text{kg}$
- $14.30\,\text{kg}$

Let $Q$ be the amount of inhibitor in the reservoir at time $t,$ in minutes. Then, the derivative 

$$
\frac{dQ}{dt}
$$

describes how this amount changes with respect to time $t.$ This is equal to the rate at which inhibitor enters the tank minus the rate at which inhibitor leaves the tank.

$$
\frac{dQ}{dt}={Q}_{\text{in}}^{′}-{Q}_{\text{out}}^{′}
$$

Note that the units of $\frac{dQ}{dt},{Q}_{\text{in}}^{′}$ and ${Q}_{\text{out}}^{′}$ are $\text{kg}/\text{min}.$ Now, let's compute the required rates of change in steps.

**Step 1**: Calculating the rate at which inhibitor enters the reservoir.

Note that a feed solution containing $0.06\,\text{kg/L}$ of the inhibitor enters the reservoir at a rate of $16\,\text{L/min}.$ So, the rate at which the *inhibitor* enters the reservoir is 

$$
\begin{aligned}{Q}_{\text{in}}^{′} & =(0.06\,\frac{\text{kg}}{\text{L}})\cdot (16\,\frac{\text{L}}{\text{min}}) \\  & =(0.06\,\frac{\text{kg}}{\cancel{\text{L}}})\cdot (16\,\frac{\cancel{\text{L}}}{\text{min}}) \\  & =0.96\,\frac{\text{kg}}{\text{min}}.\end{aligned}
$$

**Step 2**: Calculating the rate at which inhibitor exits the reservoir.

To find the rate at which inhibitor leaves the reservoir, we must first determine the volume of liquid in the reservoir at time $t.$

The reservoir initially contains $400\,\text{L}$ of liquid; a solution enters at $16\,\text{L/min}$ and leaves at $12\,\text{L/min}.$
As a result, the volume of liquid in the reservoir after $t$ minutes is 

$$
400+16t-12t=(400+4t)\,\text{L}.
$$

Since $Q$ is the amount of inhibitor in the reservoir, the *concentration* of the mixed solution at time $t$ is

$$
\frac{Q}{400+4t}\,\text{kg/L}.
$$

Therefore, as the completely mixed liquid leaves at a rate of $12\,\text{L/min},$ *inhibitor* leaves at a rate of

$$
\begin{aligned}{Q}_{\text{out}}^{′} & =(12\,\frac{\text{L}}{\text{min}})\cdot (\frac{Q}{400+4t}\,\frac{\text{kg}}{\text{L}}) \\  & =(12\,\frac{\cancel{\text{L}}}{\text{min}})\cdot (\frac{Q}{400+4t}\,\frac{\text{kg}}{\cancel{\text{L}}}) \\  & =\frac{12Q}{400+4t}\,\frac{\text{kg}}{\text{min}} \\  & =\frac{3Q}{100+t}\,\frac{\text{kg}}{\text{min}}.\end{aligned}
$$

**Step 3**: Calculate the overall rate of change.

The rate of change equals the rate of entry minus the rate of exit. Therefore, 

$$
\begin{aligned}\frac{dQ}{dt} & ={Q}_{\text{in}}^{′}-{Q}_{\text{out}}^{′} \\  & =0.96-\frac{3Q}{100+t}\end{aligned}
$$

which gives the equation

$$
\begin{aligned}\frac{dQ}{dt}+\frac{3}{100+t}Q=0.96.\end{aligned}
$$

**Step 4**: Integrate the equation.

This is a first-order linear equation with variable coefficients. So we find the general solution using an integrating factor:

$$
\begin{aligned}I(t) & ={e}^{\int 3/(100+t)\,dt} \\  & ={e}^{3\operatorname{ln}⁡|100+t|} \\  & ={e}^{\operatorname{ln}⁡(100+t)^{3}} \\  & =(100+t)^{3}\end{aligned}
$$

Multiplying both sides of the differential equation by $I(t)=(100+t)^{3}$ yields

$$
\begin{aligned}(100+t)^{3}\cdot (\frac{dQ}{dt}+\frac{3}{100+t}Q) & =(100+t)^{3}\cdot 0.96 \\ (100+t)^{3}\frac{dQ}{dt}+3(100+t)^{2}Q & =0.96(100+t)^{3} \\ \frac{d}{dt}(Q(100+t)^{3}) & =0.96(100+t)^{3}.\end{aligned}
$$

Now, we integrate with respect to $t:$

$$
\begin{aligned}\int \frac{d}{dt}(Q(100+t)^{3})\,dt & =\int 0.96(100+t)^{3}\,dt \\ Q(100+t)^{3} & =0.96\cdot \frac{1}{4}(100+t)^{4}+C \\ Q(t) & =0.24(100+t)+\frac{C}{(100+t)^{3}}\end{aligned}
$$

Note that $C$ is a constant of integration.

We're told that the reservoir initially contains $7.2\,\text{kg}$ of inhibitor. So, we can apply the initial condition $Q(0)=7.2,$ and solve for $C:$

$$
\begin{aligned}Q(0) & =7.2 \\ 0.24(100+0)+\frac{C}{(100+0)^{3}} & =7.2 \\ 24+\frac{C}{{100}^{3}} & =7.2 \\ \frac{C}{{100}^{3}} & =-16.8 \\ C & =-16.8(100)^{3}\end{aligned}
$$

Finally, we obtain the following expression for $Q(t):$

$$
\begin{aligned}Q(t) & =0.24(100+t)-\frac{16.8(100)^{3}}{(100+t)^{3}} \\  & =0.24(100+t)-16.8{(\frac{100}{100+t})}^{3}.\end{aligned}
$$

Finally,  the amount of inhibitor in the reservoir $12$ minutes after pumping begins is

$$
\begin{aligned}Q(12) & =0.24(100+12)-16.8{(\frac{100}{100+12})}^{3} \\  & =26.88-16.8{(\frac{25}{28})}^{3} \\  & ≈14.92\,\text{kg},\end{aligned}
$$

rounded to two decimal places.

---
q-339399 | observed:q-339399 | :question.difficulty/hard | eligible=False

A coolant reservoir initially holds $400\,\text{L}$ of liquid containing $7.5\,\text{kg}$ of dissolved corrosion inhibitor.
A feed solution containing $0.0625\,\text{kg/L}$ of the inhibitor is pumped into the reservoir at a rate of $16\,\text{L/min},$ while the completely mixed liquid is drained out at a rate of $12\,\text{L/min}.$
Find, rounded to two decimal places, the amount of inhibitor in the reservoir $12$ minutes after pumping begins.

- $16.20\,\text{kg}$
- $15.54\,\text{kg}$ [correct]
- $16.50\,\text{kg}$
- $13.59\,\text{kg}$
- $14.89\,\text{kg}$

Let $Q$ be the amount of inhibitor in the reservoir at time $t,$ in minutes. Then, the derivative 

$$
\frac{dQ}{dt}
$$

describes how this amount changes with respect to time $t.$ This is equal to the rate at which inhibitor enters the tank minus the rate at which inhibitor leaves the tank.

$$
\frac{dQ}{dt}={Q}_{\text{in}}^{′}-{Q}_{\text{out}}^{′}
$$

Note that the units of $\frac{dQ}{dt},{Q}_{\text{in}}^{′}$ and ${Q}_{\text{out}}^{′}$ are $\text{kg}/\text{min}.$ Now, let's compute the required rates of change in steps.

**Step 1**: Calculating the rate at which inhibitor enters the reservoir.

Note that a feed solution containing $0.0625\,\text{kg/L}$ of the inhibitor enters the reservoir at a rate of $16\,\text{L/min}.$ So, the rate at which the *inhibitor* enters the reservoir is 

$$
\begin{aligned}{Q}_{\text{in}}^{′} & =(0.0625\,\frac{\text{kg}}{\text{L}})\cdot (16\,\frac{\text{L}}{\text{min}}) \\  & =(0.0625\,\frac{\text{kg}}{\cancel{\text{L}}})\cdot (16\,\frac{\cancel{\text{L}}}{\text{min}}) \\  & =1\,\frac{\text{kg}}{\text{min}}.\end{aligned}
$$

**Step 2**: Calculating the rate at which inhibitor exits the reservoir.

To find the rate at which inhibitor leaves the reservoir, we must first determine the volume of liquid in the reservoir at time $t.$

The reservoir initially contains $400\,\text{L}$ of liquid; a solution enters at $16\,\text{L/min}$ and leaves at $12\,\text{L/min}.$
As a result, the volume of liquid in the reservoir after $t$ minutes is 

$$
400+16t-12t=(400+4t)\,\text{L}.
$$

Since $Q$ is the amount of inhibitor in the reservoir, the *concentration* of the mixed solution at time $t$ is

$$
\frac{Q}{400+4t}\,\text{kg/L}.
$$

Therefore, as the completely mixed liquid leaves at a rate of $12\,\text{L/min},$ *inhibitor* leaves at a rate of

$$
\begin{aligned}{Q}_{\text{out}}^{′} & =(12\,\frac{\text{L}}{\text{min}})\cdot (\frac{Q}{400+4t}\,\frac{\text{kg}}{\text{L}}) \\  & =(12\,\frac{\cancel{\text{L}}}{\text{min}})\cdot (\frac{Q}{400+4t}\,\frac{\text{kg}}{\cancel{\text{L}}}) \\  & =\frac{12Q}{400+4t}\,\frac{\text{kg}}{\text{min}} \\  & =\frac{3Q}{100+t}\,\frac{\text{kg}}{\text{min}}.\end{aligned}
$$

**Step 3**: Calculate the overall rate of change.

The rate of change equals the rate of entry minus the rate of exit. Therefore, 

$$
\begin{aligned}\frac{dQ}{dt} & ={Q}_{\text{in}}^{′}-{Q}_{\text{out}}^{′} \\  & =1-\frac{3Q}{100+t}\end{aligned}
$$

which gives the equation

$$
\begin{aligned}\frac{dQ}{dt}+\frac{3}{100+t}Q=1.\end{aligned}
$$

**Step 4**: Integrate the equation.

This is a first-order linear equation with variable coefficients. So we find the general solution using an integrating factor:

$$
\begin{aligned}I(t) & ={e}^{\int 3/(100+t)\,dt} \\  & ={e}^{3\operatorname{ln}⁡|100+t|} \\  & ={e}^{\operatorname{ln}⁡(100+t)^{3}} \\  & =(100+t)^{3}\end{aligned}
$$

Multiplying both sides of the differential equation by $I(t)=(100+t)^{3}$ yields

$$
\begin{aligned}(100+t)^{3}\cdot (\frac{dQ}{dt}+\frac{3}{100+t}Q) & =(100+t)^{3}\cdot 1 \\ (100+t)^{3}\frac{dQ}{dt}+3(100+t)^{2}Q & =1(100+t)^{3} \\ \frac{d}{dt}(Q(100+t)^{3}) & =1(100+t)^{3}.\end{aligned}
$$

Now, we integrate with respect to $t:$

$$
\begin{aligned}\int \frac{d}{dt}(Q(100+t)^{3})\,dt & =\int 1(100+t)^{3}\,dt \\ Q(100+t)^{3} & =1\cdot \frac{1}{4}(100+t)^{4}+C \\ Q(t) & =0.25(100+t)+\frac{C}{(100+t)^{3}}\end{aligned}
$$

Note that $C$ is a constant of integration.

We're told that the reservoir initially contains $7.5\,\text{kg}$ of inhibitor. So, we can apply the initial condition $Q(0)=7.5,$ and solve for $C:$

$$
\begin{aligned}Q(0) & =7.5 \\ 0.25(100+0)+\frac{C}{(100+0)^{3}} & =7.5 \\ 25+\frac{C}{{100}^{3}} & =7.5 \\ \frac{C}{{100}^{3}} & =-17.5 \\ C & =-17.5(100)^{3}\end{aligned}
$$

Finally, we obtain the following expression for $Q(t):$

$$
\begin{aligned}Q(t) & =0.25(100+t)-\frac{17.5(100)^{3}}{(100+t)^{3}} \\  & =0.25(100+t)-17.5{(\frac{100}{100+t})}^{3}.\end{aligned}
$$

Finally,  the amount of inhibitor in the reservoir $12$ minutes after pumping begins is

$$
\begin{aligned}Q(12) & =0.25(100+12)-17.5{(\frac{100}{100+12})}^{3} \\  & =28-17.5{(\frac{25}{28})}^{3} \\  & ≈15.54\,\text{kg},\end{aligned}
$$

rounded to two decimal places.

---
q-339399 | authored-operations | :question.difficulty/hard | eligible=True

A coolant reservoir initially holds $800\,\text{L}$ of liquid containing $13\,\text{kg}$ of dissolved corrosion inhibitor.
A feed solution containing $0.07\,\text{kg/L}$ of the inhibitor is pumped into the reservoir at a rate of $32\,\text{L/min},$ while the completely mixed liquid is drained out at a rate of $24\,\text{L/min}.$
Find, rounded to two decimal places, the amount of inhibitor in the reservoir $4$ minutes after pumping begins.

- $58.24\,\text{kg}$
- $19.97\,\text{kg}$
- $11.56\,\text{kg}$
- $21.48\,\text{kg}$
- $20.01\,\text{kg}$ [correct]

Let $Q$ be the amount of dissolved substance in the tank at time $t,$ in minutes. The amount entering minus the amount leaving gives
$$\frac{dQ}{dt}=Q'_{\text{in}}-Q'_{\text{out}}.$$
The units of these rates are $\text{kg/min}.$

**Step 1**: Calculating the rate at which substance enters the tank.
$$\begin{aligned}Q'_{\text{in}}&=(0.07\,\frac{\text{kg}}{\text{L}})\cdot(32\,\frac{\text{L}}{\text{min}})\\
&=(0.07\,\frac{\text{kg}}{\cancel{\text{L}}})\cdot(32\,\frac{\cancel{\text{L}}}{\text{min}})\\&=2.24\,\text{kg/min}.\end{aligned}$$

**Step 2**: Calculating the rate at which substance exits the tank.
The volume is
$$V(t)=800+32t-24t=(800+8t)\,\text{L}.$$
The concentration is $\frac{Q}{800+8t}\,\text{kg/L}.$ Hence,
$$\begin{aligned}Q'_{\text{out}}&=(24\,\frac{\text{L}}{\text{min}})\cdot(\frac{Q}{800+8t}\,\frac{\text{kg}}{\text{L}})\\
&=(24\,\frac{\cancel{\text{L}}}{\text{min}})\cdot(\frac{Q}{800+8t}\,\frac{\text{kg}}{\cancel{\text{L}}})\\
&=\frac{24Q}{800+8t}\,\text{kg/min}=\frac{3Q}{100+t}\,\text{kg/min}.\end{aligned}$$

**Step 3**: Calculate the overall rate of change.
$$\begin{aligned}\frac{dQ}{dt}&=Q'_{\text{in}}-Q'_{\text{out}}\\&=2.24-\frac{3Q}{100+t}.\end{aligned}$$
Thus,
$$\frac{dQ}{dt}+\frac{3}{100+t}Q=2.24.$$

**Step 4**: Integrate the equation.
This is a first-order linear equation with variable coefficients. So we find the general solution using an integrating factor:
$$\begin{aligned}I(t)&=e^{\int 3/(100+t)\,dt}\\&=e^{3\ln|100+t|}\\&=e^{\ln (100+t)^{3}}\\&=(100+t)^{3}.\end{aligned}$$
Multiplying both sides by $I(t)=(100+t)^{3}$ yields
$$\begin{aligned}(100+t)^{3}\cdot(\frac{dQ}{dt}+\frac{3}{100+t}Q)&=(100+t)^{3}\cdot 2.24\\
(100+t)^{3}\frac{dQ}{dt}+3(100+t)^{2}Q&=2.24(100+t)^{3}\\\frac{d}{dt}(Q(100+t)^{3})&=2.24(100+t)^{3}.\end{aligned}$$
Now, we integrate with respect to $t:$
$$\begin{aligned}\int\frac{d}{dt}(Q(100+t)^{3})\,dt&=\int 2.24(100+t)^{3}\,dt\\Q(100+t)^{3}&=2.24\cdot\frac{1}{4}(100+t)^{4}+C\\Q(t)&=0.56(100+t)+C(100+t)^{-3}.\end{aligned}$$
Note that $C$ is a constant of integration.
The initial condition is $Q(0)=13.$ Thus,
$$\begin{aligned}0.56(100+0)+C(100+0)^{-3}&=13\\
56+C(100)^{-3}&=13\\C(100)^{-3}&=-43\\C&=-43000000.\end{aligned}$$
Finally, we obtain the following expression for $Q(t):$
$$Q(t)=\frac{14 t}{25} + 56 - \frac{43000000}{\left(t + 100\right)^{3}}.$$
Finally, the amount in the tank $4$ minutes after pumping begins is
$$\begin{aligned}Q(4)&=0.56(100+4)-43(\frac{100}{100+4})^{3}\\&=58.24-43(\frac{25}{26})^{3}\\&\approx 20.01\,\text{kg}.\end{aligned}$$
This is rounded to two decimal places.

---
q-339399 | authored-operations | :question.difficulty/hard | eligible=True

A coolant reservoir initially holds $640\,\text{L}$ of liquid containing $15\,\text{kg}$ of dissolved corrosion inhibitor.
A feed solution containing $0.07\,\text{kg/L}$ of the inhibitor is pumped into the reservoir at a rate of $32\,\text{L/min},$ while the completely mixed liquid is drained out at a rate of $24\,\text{L/min}.$
Find, rounded to two decimal places, the amount of inhibitor in the reservoir $11$ minutes after pumping begins.

- $30.71\,\text{kg}$ [correct]
- $33.16\,\text{kg}$
- $50.96\,\text{kg}$
- $30.12\,\text{kg}$
- $10.19\,\text{kg}$

Let $Q$ be the amount of dissolved substance in the tank at time $t,$ in minutes. The amount entering minus the amount leaving gives
$$\frac{dQ}{dt}=Q'_{\text{in}}-Q'_{\text{out}}.$$
The units of these rates are $\text{kg/min}.$

**Step 1**: Calculating the rate at which substance enters the tank.
$$\begin{aligned}Q'_{\text{in}}&=(0.07\,\frac{\text{kg}}{\text{L}})\cdot(32\,\frac{\text{L}}{\text{min}})\\
&=(0.07\,\frac{\text{kg}}{\cancel{\text{L}}})\cdot(32\,\frac{\cancel{\text{L}}}{\text{min}})\\&=2.24\,\text{kg/min}.\end{aligned}$$

**Step 2**: Calculating the rate at which substance exits the tank.
The volume is
$$V(t)=640+32t-24t=(640+8t)\,\text{L}.$$
The concentration is $\frac{Q}{640+8t}\,\text{kg/L}.$ Hence,
$$\begin{aligned}Q'_{\text{out}}&=(24\,\frac{\text{L}}{\text{min}})\cdot(\frac{Q}{640+8t}\,\frac{\text{kg}}{\text{L}})\\
&=(24\,\frac{\cancel{\text{L}}}{\text{min}})\cdot(\frac{Q}{640+8t}\,\frac{\text{kg}}{\cancel{\text{L}}})\\
&=\frac{24Q}{640+8t}\,\text{kg/min}=\frac{3Q}{80+t}\,\text{kg/min}.\end{aligned}$$

**Step 3**: Calculate the overall rate of change.
$$\begin{aligned}\frac{dQ}{dt}&=Q'_{\text{in}}-Q'_{\text{out}}\\&=2.24-\frac{3Q}{80+t}.\end{aligned}$$
Thus,
$$\frac{dQ}{dt}+\frac{3}{80+t}Q=2.24.$$

**Step 4**: Integrate the equation.
This is a first-order linear equation with variable coefficients. So we find the general solution using an integrating factor:
$$\begin{aligned}I(t)&=e^{\int 3/(80+t)\,dt}\\&=e^{3\ln|80+t|}\\&=e^{\ln (80+t)^{3}}\\&=(80+t)^{3}.\end{aligned}$$
Multiplying both sides by $I(t)=(80+t)^{3}$ yields
$$\begin{aligned}(80+t)^{3}\cdot(\frac{dQ}{dt}+\frac{3}{80+t}Q)&=(80+t)^{3}\cdot 2.24\\
(80+t)^{3}\frac{dQ}{dt}+3(80+t)^{2}Q&=2.24(80+t)^{3}\\\frac{d}{dt}(Q(80+t)^{3})&=2.24(80+t)^{3}.\end{aligned}$$
Now, we integrate with respect to $t:$
$$\begin{aligned}\int\frac{d}{dt}(Q(80+t)^{3})\,dt&=\int 2.24(80+t)^{3}\,dt\\Q(80+t)^{3}&=2.24\cdot\frac{1}{4}(80+t)^{4}+C\\Q(t)&=0.56(80+t)+C(80+t)^{-3}.\end{aligned}$$
Note that $C$ is a constant of integration.
The initial condition is $Q(0)=15.$ Thus,
$$\begin{aligned}0.56(80+0)+C(80+0)^{-3}&=15\\
44.8+C(80)^{-3}&=15\\C(80)^{-3}&=-29.8\\C&=-15257600.\end{aligned}$$
Finally, we obtain the following expression for $Q(t):$
$$Q(t)=\frac{14 t}{25} + \frac{224}{5} - \frac{15257600}{\left(t + 80\right)^{3}}.$$
Finally, the amount in the tank $11$ minutes after pumping begins is
$$\begin{aligned}Q(11)&=0.56(80+11)-29.8(\frac{80}{80+11})^{3}\\&=50.96-29.8(\frac{80}{91})^{3}\\&\approx 30.71\,\text{kg}.\end{aligned}$$
This is rounded to two decimal places.

---
q-339400 | observed:q-339400 | :question.difficulty/hard | eligible=False

A fermentation vat initially holds $500\,\text{L}$ of liquid containing $9.6\,\text{kg}$ of dissolved nutrient.
A feed solution containing $0.072\,\text{kg/L}$ of the nutrient is pumped into the vat at a rate of $10\,\text{L/min},$ while the completely mixed liquid is drained out at a rate of $5\,\text{L/min}.$
Find, rounded to two decimal places, the amount of nutrient in the vat $8$ minutes after pumping begins.

- $14.44\,\text{kg}$ [correct]
- $13.13\,\text{kg}$
- $13.90\,\text{kg}$
- $15.75\,\text{kg}$
- $15.21\,\text{kg}$

Let $Q$ be the amount of nutrient in the vat at time $t,$ in minutes. Then, the derivative 

$$
\frac{dQ}{dt}
$$

describes how this amount changes with respect to time $t.$ This is equal to the rate at which nutrient enters the tank minus the rate at which nutrient leaves the tank.

$$
\frac{dQ}{dt}={Q}_{\text{in}}^{′}-{Q}_{\text{out}}^{′}
$$

Note that the units of $\frac{dQ}{dt},{Q}_{\text{in}}^{′}$ and ${Q}_{\text{out}}^{′}$ are $\text{kg}/\text{min}.$ Now, let's compute the required rates of change in steps.

**Step 1**: Calculating the rate at which nutrient enters the vat.

Note that a feed solution containing $0.072\,\text{kg/L}$ of the nutrient enters the vat at a rate of $10\,\text{L/min}.$ So, the rate at which the *nutrient* enters the vat is 

$$
\begin{aligned}{Q}_{\text{in}}^{′} & =(0.072\,\frac{\text{kg}}{\text{L}})\cdot (10\,\frac{\text{L}}{\text{min}}) \\  & =(0.072\,\frac{\text{kg}}{\cancel{\text{L}}})\cdot (10\,\frac{\cancel{\text{L}}}{\text{min}}) \\  & =0.72\,\frac{\text{kg}}{\text{min}}.\end{aligned}
$$

**Step 2**: Calculating the rate at which nutrient exits the vat.

To find the rate at which nutrient leaves the vat, we must first determine the volume of liquid in the vat at time $t.$

The vat initially contains $500\,\text{L}$ of liquid; a solution enters at $10\,\text{L/min}$ and leaves at $5\,\text{L/min}.$
As a result, the volume of liquid in the vat after $t$ minutes is 

$$
500+10t-5t=(500+5t)\,\text{L}.
$$

Since $Q$ is the amount of nutrient in the vat, the *concentration* of the mixed solution at time $t$ is

$$
\frac{Q}{500+5t}\,\text{kg/L}.
$$

Therefore, as the completely mixed liquid leaves at a rate of $5\,\text{L/min},$ *nutrient* leaves at a rate of

$$
\begin{aligned}{Q}_{\text{out}}^{′} & =(5\,\frac{\text{L}}{\text{min}})\cdot (\frac{Q}{500+5t}\,\frac{\text{kg}}{\text{L}}) \\  & =(5\,\frac{\cancel{\text{L}}}{\text{min}})\cdot (\frac{Q}{500+5t}\,\frac{\text{kg}}{\cancel{\text{L}}}) \\  & =\frac{5Q}{500+5t}\,\frac{\text{kg}}{\text{min}} \\  & =\frac{Q}{100+t}\,\frac{\text{kg}}{\text{min}}.\end{aligned}
$$

**Step 3**: Calculate the overall rate of change.

The rate of change equals the rate of entry minus the rate of exit. Therefore, 

$$
\begin{aligned}\frac{dQ}{dt} & ={Q}_{\text{in}}^{′}-{Q}_{\text{out}}^{′} \\  & =0.72-\frac{Q}{100+t}\end{aligned}
$$

which gives the equation

$$
\begin{aligned}\frac{dQ}{dt}+\frac{1}{100+t}Q=0.72.\end{aligned}
$$

**Step 4**: Integrate the equation.

This is a first-order linear equation with variable coefficients. So we find the general solution using an integrating factor:

$$
\begin{aligned}I(t) & ={e}^{\int 1/(100+t)\,dt} \\  & ={e}^{\operatorname{ln}⁡|100+t|} \\  & =100+t\end{aligned}
$$

Multiplying both sides of the differential equation by $I(t)=100+t$ yields

$$
\begin{aligned}(100+t)\cdot (\frac{dQ}{dt}+\frac{1}{100+t}Q) & =(100+t)\cdot 0.72 \\ (100+t)\frac{dQ}{dt}+Q & =0.72(100+t) \\ \frac{d}{dt}(Q(100+t)) & =0.72(100+t).\end{aligned}
$$

Now, we integrate with respect to $t:$

$$
\begin{aligned}\int \frac{d}{dt}(Q(100+t))\,dt & =\int 0.72(100+t)\,dt \\ Q(100+t) & =0.72\cdot \frac{1}{2}(100+t)^{2}+C \\ Q(t) & =0.36(100+t)+\frac{C}{100+t}\end{aligned}
$$

Note that $C$ is a constant of integration.

We're told that the vat initially contains $9.6\,\text{kg}$ of nutrient. So, we can apply the initial condition $Q(0)=9.6,$ and solve for $C:$

$$
\begin{aligned}Q(0) & =9.6 \\ 0.36(100+0)+\frac{C}{100+0} & =9.6 \\ 36+\frac{C}{100} & =9.6 \\ \frac{C}{100} & =-26.4 \\ C & =-2640\end{aligned}
$$

Finally, we obtain the following expression for $Q(t):$

$$
\begin{aligned}Q(t) & =0.36(100+t)-\frac{2640}{100+t}.\end{aligned}
$$

Finally,  the amount of nutrient in the vat $8$ minutes after pumping begins is

$$
\begin{aligned}Q(8) & =0.36(100+8)-\frac{2640}{100+8} \\  & =38.88-\frac{2640}{108} \\  & ≈14.44\,\text{kg},\end{aligned}
$$

rounded to two decimal places.

---
q-339400 | observed:q-339400 | :question.difficulty/hard | eligible=False

A fermentation vat initially holds $500\,\text{L}$ of liquid containing $10\,\text{kg}$ of dissolved nutrient.
A feed solution containing $0.075\,\text{kg/L}$ of the nutrient is pumped into the vat at a rate of $10\,\text{L/min},$ while the completely mixed liquid is drained out at a rate of $5\,\text{L/min}.$
Find, rounded to two decimal places, the amount of nutrient in the vat $8$ minutes after pumping begins.

- $15.04\,\text{kg}$ [correct]
- $13.68\,\text{kg}$
- $14.48\,\text{kg}$
- $16.40\,\text{kg}$
- $15.84\,\text{kg}$

Let $Q$ be the amount of nutrient in the vat at time $t,$ in minutes. Then, the derivative 

$$
\frac{dQ}{dt}
$$

describes how this amount changes with respect to time $t.$ This is equal to the rate at which nutrient enters the tank minus the rate at which nutrient leaves the tank.

$$
\frac{dQ}{dt}={Q}_{\text{in}}^{′}-{Q}_{\text{out}}^{′}
$$

Note that the units of $\frac{dQ}{dt},{Q}_{\text{in}}^{′}$ and ${Q}_{\text{out}}^{′}$ are $\text{kg}/\text{min}.$ Now, let's compute the required rates of change in steps.

**Step 1**: Calculating the rate at which nutrient enters the vat.

Note that a feed solution containing $0.075\,\text{kg/L}$ of the nutrient enters the vat at a rate of $10\,\text{L/min}.$ So, the rate at which the *nutrient* enters the vat is 

$$
\begin{aligned}{Q}_{\text{in}}^{′} & =(0.075\,\frac{\text{kg}}{\text{L}})\cdot (10\,\frac{\text{L}}{\text{min}}) \\  & =(0.075\,\frac{\text{kg}}{\cancel{\text{L}}})\cdot (10\,\frac{\cancel{\text{L}}}{\text{min}}) \\  & =0.75\,\frac{\text{kg}}{\text{min}}.\end{aligned}
$$

**Step 2**: Calculating the rate at which nutrient exits the vat.

To find the rate at which nutrient leaves the vat, we must first determine the volume of liquid in the vat at time $t.$

The vat initially contains $500\,\text{L}$ of liquid; a solution enters at $10\,\text{L/min}$ and leaves at $5\,\text{L/min}.$
As a result, the volume of liquid in the vat after $t$ minutes is 

$$
500+10t-5t=(500+5t)\,\text{L}.
$$

Since $Q$ is the amount of nutrient in the vat, the *concentration* of the mixed solution at time $t$ is

$$
\frac{Q}{500+5t}\,\text{kg/L}.
$$

Therefore, as the completely mixed liquid leaves at a rate of $5\,\text{L/min},$ *nutrient* leaves at a rate of

$$
\begin{aligned}{Q}_{\text{out}}^{′} & =(5\,\frac{\text{L}}{\text{min}})\cdot (\frac{Q}{500+5t}\,\frac{\text{kg}}{\text{L}}) \\  & =(5\,\frac{\cancel{\text{L}}}{\text{min}})\cdot (\frac{Q}{500+5t}\,\frac{\text{kg}}{\cancel{\text{L}}}) \\  & =\frac{5Q}{500+5t}\,\frac{\text{kg}}{\text{min}} \\  & =\frac{Q}{100+t}\,\frac{\text{kg}}{\text{min}}.\end{aligned}
$$

**Step 3**: Calculate the overall rate of change.

The rate of change equals the rate of entry minus the rate of exit. Therefore, 

$$
\begin{aligned}\frac{dQ}{dt} & ={Q}_{\text{in}}^{′}-{Q}_{\text{out}}^{′} \\  & =0.75-\frac{Q}{100+t}\end{aligned}
$$

which gives the equation

$$
\begin{aligned}\frac{dQ}{dt}+\frac{1}{100+t}Q=0.75.\end{aligned}
$$

**Step 4**: Integrate the equation.

This is a first-order linear equation with variable coefficients. So we find the general solution using an integrating factor:

$$
\begin{aligned}I(t) & ={e}^{\int 1/(100+t)\,dt} \\  & ={e}^{\operatorname{ln}⁡|100+t|} \\  & =100+t\end{aligned}
$$

Multiplying both sides of the differential equation by $I(t)=100+t$ yields

$$
\begin{aligned}(100+t)\cdot (\frac{dQ}{dt}+\frac{1}{100+t}Q) & =(100+t)\cdot 0.75 \\ (100+t)\frac{dQ}{dt}+Q & =0.75(100+t) \\ \frac{d}{dt}(Q(100+t)) & =0.75(100+t).\end{aligned}
$$

Now, we integrate with respect to $t:$

$$
\begin{aligned}\int \frac{d}{dt}(Q(100+t))\,dt & =\int 0.75(100+t)\,dt \\ Q(100+t) & =0.75\cdot \frac{1}{2}(100+t)^{2}+C \\ Q(t) & =0.375(100+t)+\frac{C}{100+t}\end{aligned}
$$

Note that $C$ is a constant of integration.

We're told that the vat initially contains $10\,\text{kg}$ of nutrient. So, we can apply the initial condition $Q(0)=10,$ and solve for $C:$

$$
\begin{aligned}Q(0) & =10 \\ 0.375(100+0)+\frac{C}{100+0} & =10 \\ 37.5+\frac{C}{100} & =10 \\ \frac{C}{100} & =-27.5 \\ C & =-2750\end{aligned}
$$

Finally, we obtain the following expression for $Q(t):$

$$
\begin{aligned}Q(t) & =0.375(100+t)-\frac{2750}{100+t}.\end{aligned}
$$

Finally,  the amount of nutrient in the vat $8$ minutes after pumping begins is

$$
\begin{aligned}Q(8) & =0.375(100+8)-\frac{2750}{100+8} \\  & =40.5-\frac{2750}{108} \\  & ≈15.04\,\text{kg},\end{aligned}
$$

rounded to two decimal places.

---
q-339400 | authored-operations | :question.difficulty/hard | eligible=True

A fermentation vat initially holds $400\,\text{L}$ of liquid containing $16\,\text{kg}$ of dissolved nutrient.
A feed solution containing $0.05\,\text{kg/L}$ of the nutrient is pumped into the vat at a rate of $16\,\text{L/min},$ while the completely mixed liquid is drained out at a rate of $8\,\text{L/min}.$
Find, rounded to two decimal places, the amount of nutrient in the vat $25$ minutes after pumping begins.

- $10.67\,\text{kg}$
- $25.44\,\text{kg}$
- $28.22\,\text{kg}$
- $27.33\,\text{kg}$ [correct]
- $30.00\,\text{kg}$

Let $Q$ be the amount of dissolved substance in the tank at time $t,$ in minutes. The amount entering minus the amount leaving gives
$$\frac{dQ}{dt}=Q'_{\text{in}}-Q'_{\text{out}}.$$
The units of these rates are $\text{kg/min}.$

**Step 1**: Calculating the rate at which substance enters the tank.
$$\begin{aligned}Q'_{\text{in}}&=(0.05\,\frac{\text{kg}}{\text{L}})\cdot(16\,\frac{\text{L}}{\text{min}})\\
&=(0.05\,\frac{\text{kg}}{\cancel{\text{L}}})\cdot(16\,\frac{\cancel{\text{L}}}{\text{min}})\\&=0.8\,\text{kg/min}.\end{aligned}$$

**Step 2**: Calculating the rate at which substance exits the tank.
The volume is
$$V(t)=400+16t-8t=(400+8t)\,\text{L}.$$
The concentration is $\frac{Q}{400+8t}\,\text{kg/L}.$ Hence,
$$\begin{aligned}Q'_{\text{out}}&=(8\,\frac{\text{L}}{\text{min}})\cdot(\frac{Q}{400+8t}\,\frac{\text{kg}}{\text{L}})\\
&=(8\,\frac{\cancel{\text{L}}}{\text{min}})\cdot(\frac{Q}{400+8t}\,\frac{\text{kg}}{\cancel{\text{L}}})\\
&=\frac{8Q}{400+8t}\,\text{kg/min}=\frac{1Q}{50+t}\,\text{kg/min}.\end{aligned}$$

**Step 3**: Calculate the overall rate of change.
$$\begin{aligned}\frac{dQ}{dt}&=Q'_{\text{in}}-Q'_{\text{out}}\\&=0.8-\frac{1Q}{50+t}.\end{aligned}$$
Thus,
$$\frac{dQ}{dt}+\frac{1}{50+t}Q=0.8.$$

**Step 4**: Integrate the equation.
This is a first-order linear equation with variable coefficients. So we find the general solution using an integrating factor:
$$\begin{aligned}I(t)&=e^{\int 1/(50+t)\,dt}\\&=e^{1\ln|50+t|}\\&=e^{\ln (50+t)^{1}}\\&=(50+t)^{1}.\end{aligned}$$
Multiplying both sides by $I(t)=(50+t)^{1}$ yields
$$\begin{aligned}(50+t)^{1}\cdot(\frac{dQ}{dt}+\frac{1}{50+t}Q)&=(50+t)^{1}\cdot 0.8\\
(50+t)^{1}\frac{dQ}{dt}+1(50+t)^{0}Q&=0.8(50+t)^{1}\\\frac{d}{dt}(Q(50+t)^{1})&=0.8(50+t)^{1}.\end{aligned}$$
Now, we integrate with respect to $t:$
$$\begin{aligned}\int\frac{d}{dt}(Q(50+t)^{1})\,dt&=\int 0.8(50+t)^{1}\,dt\\Q(50+t)^{1}&=0.8\cdot\frac{1}{2}(50+t)^{2}+C\\Q(t)&=0.4(50+t)+C(50+t)^{-1}.\end{aligned}$$
Note that $C$ is a constant of integration.
The initial condition is $Q(0)=16.$ Thus,
$$\begin{aligned}0.4(50+0)+C(50+0)^{-1}&=16\\
20+C(50)^{-1}&=16\\C(50)^{-1}&=-4\\C&=-200.\end{aligned}$$
Finally, we obtain the following expression for $Q(t):$
$$Q(t)=\frac{2 t}{5} + 20 - \frac{200}{t + 50}.$$
Finally, the amount in the tank $25$ minutes after pumping begins is
$$\begin{aligned}Q(25)&=0.4(50+25)-4(\frac{50}{50+25})^{1}\\&=30-4(\frac{2}{3})^{1}\\&\approx 27.33\,\text{kg}.\end{aligned}$$
This is rounded to two decimal places.

---
q-339400 | authored-operations | :question.difficulty/hard | eligible=True

A fermentation vat initially holds $640\,\text{L}$ of liquid containing $15\,\text{kg}$ of dissolved nutrient.
A feed solution containing $0.07\,\text{kg/L}$ of the nutrient is pumped into the vat at a rate of $16\,\text{L/min},$ while the completely mixed liquid is drained out at a rate of $8\,\text{L/min}.$
Find, rounded to two decimal places, the amount of nutrient in the vat $11$ minutes after pumping begins.

- $24.76\,\text{kg}$ [correct]
- $27.93\,\text{kg}$
- $50.96\,\text{kg}$
- $24.58\,\text{kg}$
- $13.19\,\text{kg}$

Let $Q$ be the amount of dissolved substance in the tank at time $t,$ in minutes. The amount entering minus the amount leaving gives
$$\frac{dQ}{dt}=Q'_{\text{in}}-Q'_{\text{out}}.$$
The units of these rates are $\text{kg/min}.$

**Step 1**: Calculating the rate at which substance enters the tank.
$$\begin{aligned}Q'_{\text{in}}&=(0.07\,\frac{\text{kg}}{\text{L}})\cdot(16\,\frac{\text{L}}{\text{min}})\\
&=(0.07\,\frac{\text{kg}}{\cancel{\text{L}}})\cdot(16\,\frac{\cancel{\text{L}}}{\text{min}})\\&=1.12\,\text{kg/min}.\end{aligned}$$

**Step 2**: Calculating the rate at which substance exits the tank.
The volume is
$$V(t)=640+16t-8t=(640+8t)\,\text{L}.$$
The concentration is $\frac{Q}{640+8t}\,\text{kg/L}.$ Hence,
$$\begin{aligned}Q'_{\text{out}}&=(8\,\frac{\text{L}}{\text{min}})\cdot(\frac{Q}{640+8t}\,\frac{\text{kg}}{\text{L}})\\
&=(8\,\frac{\cancel{\text{L}}}{\text{min}})\cdot(\frac{Q}{640+8t}\,\frac{\text{kg}}{\cancel{\text{L}}})\\
&=\frac{8Q}{640+8t}\,\text{kg/min}=\frac{1Q}{80+t}\,\text{kg/min}.\end{aligned}$$

**Step 3**: Calculate the overall rate of change.
$$\begin{aligned}\frac{dQ}{dt}&=Q'_{\text{in}}-Q'_{\text{out}}\\&=1.12-\frac{1Q}{80+t}.\end{aligned}$$
Thus,
$$\frac{dQ}{dt}+\frac{1}{80+t}Q=1.12.$$

**Step 4**: Integrate the equation.
This is a first-order linear equation with variable coefficients. So we find the general solution using an integrating factor:
$$\begin{aligned}I(t)&=e^{\int 1/(80+t)\,dt}\\&=e^{1\ln|80+t|}\\&=e^{\ln (80+t)^{1}}\\&=(80+t)^{1}.\end{aligned}$$
Multiplying both sides by $I(t)=(80+t)^{1}$ yields
$$\begin{aligned}(80+t)^{1}\cdot(\frac{dQ}{dt}+\frac{1}{80+t}Q)&=(80+t)^{1}\cdot 1.12\\
(80+t)^{1}\frac{dQ}{dt}+1(80+t)^{0}Q&=1.12(80+t)^{1}\\\frac{d}{dt}(Q(80+t)^{1})&=1.12(80+t)^{1}.\end{aligned}$$
Now, we integrate with respect to $t:$
$$\begin{aligned}\int\frac{d}{dt}(Q(80+t)^{1})\,dt&=\int 1.12(80+t)^{1}\,dt\\Q(80+t)^{1}&=1.12\cdot\frac{1}{2}(80+t)^{2}+C\\Q(t)&=0.56(80+t)+C(80+t)^{-1}.\end{aligned}$$
Note that $C$ is a constant of integration.
The initial condition is $Q(0)=15.$ Thus,
$$\begin{aligned}0.56(80+0)+C(80+0)^{-1}&=15\\
44.8+C(80)^{-1}&=15\\C(80)^{-1}&=-29.8\\C&=-2384.\end{aligned}$$
Finally, we obtain the following expression for $Q(t):$
$$Q(t)=\frac{14 t}{25} + \frac{224}{5} - \frac{2384}{t + 80}.$$
Finally, the amount in the tank $11$ minutes after pumping begins is
$$\begin{aligned}Q(11)&=0.56(80+11)-29.8(\frac{80}{80+11})^{1}\\&=50.96-29.8(\frac{80}{91})^{1}\\&\approx 24.76\,\text{kg}.\end{aligned}$$
This is rounded to two decimal places.

---
q-336439 | authored-operations | :question.difficulty/easy | eligible=True

An aquarium initially holds $640L$ of water containing $22kg$ of dissolved minerals.
A solution containing $0.05kg/L$ of dissolved minerals is pumped into the aquarium at a rate of $16L/min$, while the completely mixed water is drained out at a rate of $24L/min$. If the amount of minerals $Q(t)$, in kilograms, in the tank $t$ minutes after pumping begins is given by
$Q(t) = α(1 - \frac{t}{80}) + β(1 - \frac{t}{80})^{3}$
where $α$ and $β$ are constants, what is the value of $α + β$?

> A scientific calculator is required to answer this question.

- $42$
- $22$ [correct]
- $54$
- $32$
- $10$

At $t=0,$ the supplied model gives $Q(0)=\alpha(1-0/80)+\beta(1-0/80)^{3}=\alpha+\beta.$ The initial amount is $22\,\text{kg},$ so $\alpha+\beta=22.$

---
q-336439 | authored-operations | :question.difficulty/easy | eligible=True

An aquarium initially holds $900L$ of water containing $35kg$ of dissolved minerals.
A solution containing $0.05kg/L$ of dissolved minerals is pumped into the aquarium at a rate of $20L/min$, while the completely mixed water is drained out at a rate of $30L/min$. If the amount of minerals $Q(t)$, in kilograms, in the tank $t$ minutes after pumping begins is given by
$Q(t) = α(1 - \frac{t}{90}) + β(1 - \frac{t}{90})^{3}$
where $α$ and $β$ are constants, what is the value of $α + β$?

> A scientific calculator is required to answer this question.

- $10$
- $55$
- $45$
- $35$ [correct]
- $80$

At $t=0,$ the supplied model gives $Q(0)=\alpha(1-0/90)+\beta(1-0/90)^{3}=\alpha+\beta.$ The initial amount is $35\,\text{kg},$ so $\alpha+\beta=35.$

---
q-336439 | authored-operations | :question.difficulty/easy | eligible=True

An aquarium initially holds $1000L$ of water containing $14kg$ of dissolved minerals.
A solution containing $0.05kg/L$ of dissolved minerals is pumped into the aquarium at a rate of $20L/min$, while the completely mixed water is drained out at a rate of $30L/min$. If the amount of minerals $Q(t)$, in kilograms, in the tank $t$ minutes after pumping begins is given by
$Q(t) = α(1 - \frac{t}{100}) + β(1 - \frac{t}{100})^{3}$
where $α$ and $β$ are constants, what is the value of $α + β$?

> A scientific calculator is required to answer this question.

- $14$ [correct]
- $50$
- $64$
- $36$
- $86$

At $t=0,$ the supplied model gives $Q(0)=\alpha(1-0/100)+\beta(1-0/100)^{3}=\alpha+\beta.$ The initial amount is $14\,\text{kg},$ so $\alpha+\beta=14.$

---
q-336439 | authored-operations | :question.difficulty/easy | eligible=True

An aquarium initially holds $1000L$ of water containing $11kg$ of dissolved minerals.
A solution containing $0.04kg/L$ of dissolved minerals is pumped into the aquarium at a rate of $20L/min$, while the completely mixed water is drained out at a rate of $30L/min$. If the amount of minerals $Q(t)$, in kilograms, in the tank $t$ minutes after pumping begins is given by
$Q(t) = α(1 - \frac{t}{100}) + β(1 - \frac{t}{100})^{3}$
where $α$ and $β$ are constants, what is the value of $α + β$?

> A scientific calculator is required to answer this question.

- $40$
- $11$ [correct]
- $29$
- $69$
- $51$

At $t=0,$ the supplied model gives $Q(0)=\alpha(1-0/100)+\beta(1-0/100)^{3}=\alpha+\beta.$ The initial amount is $11\,\text{kg},$ so $\alpha+\beta=11.$

---
q-336439 | authored-operations | :question.difficulty/easy | eligible=True

An aquarium initially holds $700L$ of water containing $27kg$ of dissolved minerals.
A solution containing $0.06kg/L$ of dissolved minerals is pumped into the aquarium at a rate of $20L/min$, while the completely mixed water is drained out at a rate of $30L/min$. If the amount of minerals $Q(t)$, in kilograms, in the tank $t$ minutes after pumping begins is given by
$Q(t) = α(1 - \frac{t}{70}) + β(1 - \frac{t}{70})^{3}$
where $α$ and $β$ are constants, what is the value of $α + β$?

> A scientific calculator is required to answer this question.

- $15$
- $57$
- $27$ [correct]
- $69$
- $42$

At $t=0,$ the supplied model gives $Q(0)=\alpha(1-0/70)+\beta(1-0/70)^{3}=\alpha+\beta.$ The initial amount is $27\,\text{kg},$ so $\alpha+\beta=27.$

---
q-339396 | authored-operations | :question.difficulty/moderate | eligible=True

A fruit syrup tank initially holds $200\,\text{L}$ of liquid containing $11\,\text{kg}$ of dissolved sweetener.
A solution containing $0.06\,\text{kg/L}$ of dissolved sweetener is pumped into the tank at a rate of $24\,\text{L/min},$ while the completely mixed liquid is drained out at a rate of $32\,\text{L/min}.$ If the amount of sweetener $Q(t),$ in kilograms, in the tank $t$ minutes after pumping begins is given by

$$
Q(t)=\alpha \,(1-\frac{t}{25})+\beta {(1-\frac{t}{25})}^{4}
$$

where $\alpha $ and $\beta $ are constants, what is the value of $\alpha -\beta ?$

- $13$ [correct]
- $12$
- $11$
- $24$
- $23$

Let $Q$ be the amount of dissolved substance in the tank at time $t,$ in minutes. The amount entering minus the amount leaving gives
$$\frac{dQ}{dt}=Q'_{\text{in}}-Q'_{\text{out}}.$$
The units of these rates are $\text{kg/min}.$

**Step 1**: Calculating the rate at which substance enters the tank.
$$\begin{aligned}Q'_{\text{in}}&=(0.06\,\frac{\text{kg}}{\text{L}})\cdot(24\,\frac{\text{L}}{\text{min}})\\
&=(0.06\,\frac{\text{kg}}{\cancel{\text{L}}})\cdot(24\,\frac{\cancel{\text{L}}}{\text{min}})\\&=1.44\,\text{kg/min}.\end{aligned}$$

**Step 2**: Calculating the rate at which substance exits the tank.
The volume is
$$V(t)=200+24t-32t=(200-8t)\,\text{L}.$$
The concentration is $\frac{Q}{200-8t}\,\text{kg/L}.$ Hence,
$$\begin{aligned}Q'_{\text{out}}&=(32\,\frac{\text{L}}{\text{min}})\cdot(\frac{Q}{200-8t}\,\frac{\text{kg}}{\text{L}})\\
&=(32\,\frac{\cancel{\text{L}}}{\text{min}})\cdot(\frac{Q}{200-8t}\,\frac{\text{kg}}{\cancel{\text{L}}})\\
&=\frac{32Q}{200-8t}\,\text{kg/min}=\frac{4Q}{25-t}\,\text{kg/min}.\end{aligned}$$

**Step 3**: Calculate the overall rate of change.
$$\begin{aligned}\frac{dQ}{dt}&=Q'_{\text{in}}-Q'_{\text{out}}\\&=1.44-\frac{4Q}{25-t}.\end{aligned}$$
Thus,
$$\frac{dQ}{dt}+\frac{4}{25-t}Q=1.44.$$

**Step 4**: Integrate the equation.
This is a first-order linear equation with variable coefficients. So we find the general solution using an integrating factor:
$$\begin{aligned}I(t)&=e^{\int 4/(25-t)\,dt}\\&=e^{-4\ln|25-t|}\\&=e^{\ln (25-t)^{-4}}\\&=(25-t)^{-4}.\end{aligned}$$
Multiplying both sides by $I(t)=(25-t)^{-4}$ yields
$$\begin{aligned}(25-t)^{-4}\cdot(\frac{dQ}{dt}+\frac{4}{25-t}Q)&=(25-t)^{-4}\cdot 1.44\\
(25-t)^{-4}\frac{dQ}{dt}+4(25-t)^{-5}Q&=1.44(25-t)^{-4}\\\frac{d}{dt}(Q(25-t)^{-4})&=1.44(25-t)^{-4}.\end{aligned}$$
Now, we integrate with respect to $t:$
$$\begin{aligned}\int\frac{d}{dt}(Q(25-t)^{-4})\,dt&=\int 1.44(25-t)^{-4}\,dt\\Q(25-t)^{-4}&=1.44\cdot\frac{1}{3}(25-t)^{-3}+C\\Q(t)&=0.48(25-t)+C(25-t)^{4}.\end{aligned}$$
Note that $C$ is a constant of integration.
The initial condition is $Q(0)=11.$ Thus,
$$\begin{aligned}0.48(25-0)+C(25-0)^{4}&=11\\
12+C(25)^{4}&=11\\C(25)^{4}&=-1\\C&=- \frac{1}{390625}.\end{aligned}$$
Finally, we obtain the following expression for $Q(t):$
$$Q(t)=- \frac{12 t}{25} - \frac{\left(25 - t\right)^{4}}{390625} + 12.$$
Writing this in the supplied normalized form gives
$$Q(t)=12(1-\frac{t}{25})-1(1-\frac{t}{25})^{4}.$$
Finally, we have $\alpha=12,\beta=-1,$ and
$$\alpha-\beta=12-(-1)=13.$$

---
q-339394 | authored-operations | :question.difficulty/moderate | eligible=True

A juice-processing tank initially holds $600\,\text{L}$ of liquid containing $16\,\text{kg}$ of dissolved sugar.
A solution containing $0.06\,\text{kg/L}$ of dissolved sugar is pumped into the tank at a rate of $12\,\text{L/min},$ while the completely mixed liquid is drained out at a rate of $18\,\text{L/min}.$ If the amount of sugar $Q(t),$ in kilograms, in the tank $t$ minutes after pumping begins is given by

$$
Q(t)=\alpha \,(1-\frac{t}{100})+\beta {(1-\frac{t}{100})}^{3}
$$

where $\alpha $ and $\beta $ are constants, what is the value of $\alpha -\beta ?$

- $56$ [correct]
- $52$
- $72$
- $36$
- $16$

Let $Q$ be the amount of dissolved substance in the tank at time $t,$ in minutes. The amount entering minus the amount leaving gives
$$\frac{dQ}{dt}=Q'_{\text{in}}-Q'_{\text{out}}.$$
The units of these rates are $\text{kg/min}.$

**Step 1**: Calculating the rate at which substance enters the tank.
$$\begin{aligned}Q'_{\text{in}}&=(0.06\,\frac{\text{kg}}{\text{L}})\cdot(12\,\frac{\text{L}}{\text{min}})\\
&=(0.06\,\frac{\text{kg}}{\cancel{\text{L}}})\cdot(12\,\frac{\cancel{\text{L}}}{\text{min}})\\&=0.72\,\text{kg/min}.\end{aligned}$$

**Step 2**: Calculating the rate at which substance exits the tank.
The volume is
$$V(t)=600+12t-18t=(600-6t)\,\text{L}.$$
The concentration is $\frac{Q}{600-6t}\,\text{kg/L}.$ Hence,
$$\begin{aligned}Q'_{\text{out}}&=(18\,\frac{\text{L}}{\text{min}})\cdot(\frac{Q}{600-6t}\,\frac{\text{kg}}{\text{L}})\\
&=(18\,\frac{\cancel{\text{L}}}{\text{min}})\cdot(\frac{Q}{600-6t}\,\frac{\text{kg}}{\cancel{\text{L}}})\\
&=\frac{18Q}{600-6t}\,\text{kg/min}=\frac{3Q}{100-t}\,\text{kg/min}.\end{aligned}$$

**Step 3**: Calculate the overall rate of change.
$$\begin{aligned}\frac{dQ}{dt}&=Q'_{\text{in}}-Q'_{\text{out}}\\&=0.72-\frac{3Q}{100-t}.\end{aligned}$$
Thus,
$$\frac{dQ}{dt}+\frac{3}{100-t}Q=0.72.$$

**Step 4**: Integrate the equation.
This is a first-order linear equation with variable coefficients. So we find the general solution using an integrating factor:
$$\begin{aligned}I(t)&=e^{\int 3/(100-t)\,dt}\\&=e^{-3\ln|100-t|}\\&=e^{\ln (100-t)^{-3}}\\&=(100-t)^{-3}.\end{aligned}$$
Multiplying both sides by $I(t)=(100-t)^{-3}$ yields
$$\begin{aligned}(100-t)^{-3}\cdot(\frac{dQ}{dt}+\frac{3}{100-t}Q)&=(100-t)^{-3}\cdot 0.72\\
(100-t)^{-3}\frac{dQ}{dt}+3(100-t)^{-4}Q&=0.72(100-t)^{-3}\\\frac{d}{dt}(Q(100-t)^{-3})&=0.72(100-t)^{-3}.\end{aligned}$$
Now, we integrate with respect to $t:$
$$\begin{aligned}\int\frac{d}{dt}(Q(100-t)^{-3})\,dt&=\int 0.72(100-t)^{-3}\,dt\\Q(100-t)^{-3}&=0.72\cdot\frac{1}{2}(100-t)^{-2}+C\\Q(t)&=0.36(100-t)+C(100-t)^{3}.\end{aligned}$$
Note that $C$ is a constant of integration.
The initial condition is $Q(0)=16.$ Thus,
$$\begin{aligned}0.36(100-0)+C(100-0)^{3}&=16\\
36+C(100)^{3}&=16\\C(100)^{3}&=-20\\C&=- \frac{1}{50000}.\end{aligned}$$
Finally, we obtain the following expression for $Q(t):$
$$Q(t)=- \frac{9 t}{25} - \frac{\left(100 - t\right)^{3}}{50000} + 36.$$
Writing this in the supplied normalized form gives
$$Q(t)=36(1-\frac{t}{100})-20(1-\frac{t}{100})^{3}.$$
Finally, we have $\alpha=36,\beta=-20,$ and
$$\alpha-\beta=36-(-20)=56.$$

---
q-339394 | authored-operations | :question.difficulty/moderate | eligible=True

A juice-processing tank initially holds $300\,\text{L}$ of liquid containing $11\,\text{kg}$ of dissolved sugar.
A solution containing $0.06\,\text{kg/L}$ of dissolved sugar is pumped into the tank at a rate of $10\,\text{L/min},$ while the completely mixed liquid is drained out at a rate of $15\,\text{L/min}.$ If the amount of sugar $Q(t),$ in kilograms, in the tank $t$ minutes after pumping begins is given by

$$
Q(t)=\alpha \,(1-\frac{t}{60})+\beta {(1-\frac{t}{60})}^{3}
$$

where $\alpha $ and $\beta $ are constants, what is the value of $\alpha -\beta ?$

- $36$
- $29$
- $18$
- $25$ [correct]
- $11$

Let $Q$ be the amount of dissolved substance in the tank at time $t,$ in minutes. The amount entering minus the amount leaving gives
$$\frac{dQ}{dt}=Q'_{\text{in}}-Q'_{\text{out}}.$$
The units of these rates are $\text{kg/min}.$

**Step 1**: Calculating the rate at which substance enters the tank.
$$\begin{aligned}Q'_{\text{in}}&=(0.06\,\frac{\text{kg}}{\text{L}})\cdot(10\,\frac{\text{L}}{\text{min}})\\
&=(0.06\,\frac{\text{kg}}{\cancel{\text{L}}})\cdot(10\,\frac{\cancel{\text{L}}}{\text{min}})\\&=0.6\,\text{kg/min}.\end{aligned}$$

**Step 2**: Calculating the rate at which substance exits the tank.
The volume is
$$V(t)=300+10t-15t=(300-5t)\,\text{L}.$$
The concentration is $\frac{Q}{300-5t}\,\text{kg/L}.$ Hence,
$$\begin{aligned}Q'_{\text{out}}&=(15\,\frac{\text{L}}{\text{min}})\cdot(\frac{Q}{300-5t}\,\frac{\text{kg}}{\text{L}})\\
&=(15\,\frac{\cancel{\text{L}}}{\text{min}})\cdot(\frac{Q}{300-5t}\,\frac{\text{kg}}{\cancel{\text{L}}})\\
&=\frac{15Q}{300-5t}\,\text{kg/min}=\frac{3Q}{60-t}\,\text{kg/min}.\end{aligned}$$

**Step 3**: Calculate the overall rate of change.
$$\begin{aligned}\frac{dQ}{dt}&=Q'_{\text{in}}-Q'_{\text{out}}\\&=0.6-\frac{3Q}{60-t}.\end{aligned}$$
Thus,
$$\frac{dQ}{dt}+\frac{3}{60-t}Q=0.6.$$

**Step 4**: Integrate the equation.
This is a first-order linear equation with variable coefficients. So we find the general solution using an integrating factor:
$$\begin{aligned}I(t)&=e^{\int 3/(60-t)\,dt}\\&=e^{-3\ln|60-t|}\\&=e^{\ln (60-t)^{-3}}\\&=(60-t)^{-3}.\end{aligned}$$
Multiplying both sides by $I(t)=(60-t)^{-3}$ yields
$$\begin{aligned}(60-t)^{-3}\cdot(\frac{dQ}{dt}+\frac{3}{60-t}Q)&=(60-t)^{-3}\cdot 0.6\\
(60-t)^{-3}\frac{dQ}{dt}+3(60-t)^{-4}Q&=0.6(60-t)^{-3}\\\frac{d}{dt}(Q(60-t)^{-3})&=0.6(60-t)^{-3}.\end{aligned}$$
Now, we integrate with respect to $t:$
$$\begin{aligned}\int\frac{d}{dt}(Q(60-t)^{-3})\,dt&=\int 0.6(60-t)^{-3}\,dt\\Q(60-t)^{-3}&=0.6\cdot\frac{1}{2}(60-t)^{-2}+C\\Q(t)&=0.3(60-t)+C(60-t)^{3}.\end{aligned}$$
Note that $C$ is a constant of integration.
The initial condition is $Q(0)=11.$ Thus,
$$\begin{aligned}0.3(60-0)+C(60-0)^{3}&=11\\
18+C(60)^{3}&=11\\C(60)^{3}&=-7\\C&=- \frac{7}{216000}.\end{aligned}$$
Finally, we obtain the following expression for $Q(t):$
$$Q(t)=- \frac{3 t}{10} - \frac{7 \left(60 - t\right)^{3}}{216000} + 18.$$
Writing this in the supplied normalized form gives
$$Q(t)=18(1-\frac{t}{60})-7(1-\frac{t}{60})^{3}.$$
Finally, we have $\alpha=18,\beta=-7,$ and
$$\alpha-\beta=18-(-7)=25.$$

---
q-339394 | authored-operations | :question.difficulty/moderate | eligible=True

A juice-processing tank initially holds $500\,\text{L}$ of liquid containing $15\,\text{kg}$ of dissolved sugar.
A solution containing $0.07\,\text{kg/L}$ of dissolved sugar is pumped into the tank at a rate of $10\,\text{L/min},$ while the completely mixed liquid is drained out at a rate of $15\,\text{L/min}.$ If the amount of sugar $Q(t),$ in kilograms, in the tank $t$ minutes after pumping begins is given by

$$
Q(t)=\alpha \,(1-\frac{t}{100})+\beta {(1-\frac{t}{100})}^{3}
$$

where $\alpha $ and $\beta $ are constants, what is the value of $\alpha -\beta ?$

- $15$
- $35$
- $50$
- $70$
- $55$ [correct]

Let $Q$ be the amount of dissolved substance in the tank at time $t,$ in minutes. The amount entering minus the amount leaving gives
$$\frac{dQ}{dt}=Q'_{\text{in}}-Q'_{\text{out}}.$$
The units of these rates are $\text{kg/min}.$

**Step 1**: Calculating the rate at which substance enters the tank.
$$\begin{aligned}Q'_{\text{in}}&=(0.07\,\frac{\text{kg}}{\text{L}})\cdot(10\,\frac{\text{L}}{\text{min}})\\
&=(0.07\,\frac{\text{kg}}{\cancel{\text{L}}})\cdot(10\,\frac{\cancel{\text{L}}}{\text{min}})\\&=0.7\,\text{kg/min}.\end{aligned}$$

**Step 2**: Calculating the rate at which substance exits the tank.
The volume is
$$V(t)=500+10t-15t=(500-5t)\,\text{L}.$$
The concentration is $\frac{Q}{500-5t}\,\text{kg/L}.$ Hence,
$$\begin{aligned}Q'_{\text{out}}&=(15\,\frac{\text{L}}{\text{min}})\cdot(\frac{Q}{500-5t}\,\frac{\text{kg}}{\text{L}})\\
&=(15\,\frac{\cancel{\text{L}}}{\text{min}})\cdot(\frac{Q}{500-5t}\,\frac{\text{kg}}{\cancel{\text{L}}})\\
&=\frac{15Q}{500-5t}\,\text{kg/min}=\frac{3Q}{100-t}\,\text{kg/min}.\end{aligned}$$

**Step 3**: Calculate the overall rate of change.
$$\begin{aligned}\frac{dQ}{dt}&=Q'_{\text{in}}-Q'_{\text{out}}\\&=0.7-\frac{3Q}{100-t}.\end{aligned}$$
Thus,
$$\frac{dQ}{dt}+\frac{3}{100-t}Q=0.7.$$

**Step 4**: Integrate the equation.
This is a first-order linear equation with variable coefficients. So we find the general solution using an integrating factor:
$$\begin{aligned}I(t)&=e^{\int 3/(100-t)\,dt}\\&=e^{-3\ln|100-t|}\\&=e^{\ln (100-t)^{-3}}\\&=(100-t)^{-3}.\end{aligned}$$
Multiplying both sides by $I(t)=(100-t)^{-3}$ yields
$$\begin{aligned}(100-t)^{-3}\cdot(\frac{dQ}{dt}+\frac{3}{100-t}Q)&=(100-t)^{-3}\cdot 0.7\\
(100-t)^{-3}\frac{dQ}{dt}+3(100-t)^{-4}Q&=0.7(100-t)^{-3}\\\frac{d}{dt}(Q(100-t)^{-3})&=0.7(100-t)^{-3}.\end{aligned}$$
Now, we integrate with respect to $t:$
$$\begin{aligned}\int\frac{d}{dt}(Q(100-t)^{-3})\,dt&=\int 0.7(100-t)^{-3}\,dt\\Q(100-t)^{-3}&=0.7\cdot\frac{1}{2}(100-t)^{-2}+C\\Q(t)&=0.35(100-t)+C(100-t)^{3}.\end{aligned}$$
Note that $C$ is a constant of integration.
The initial condition is $Q(0)=15.$ Thus,
$$\begin{aligned}0.35(100-0)+C(100-0)^{3}&=15\\
35+C(100)^{3}&=15\\C(100)^{3}&=-20\\C&=- \frac{1}{50000}.\end{aligned}$$
Finally, we obtain the following expression for $Q(t):$
$$Q(t)=- \frac{7 t}{20} - \frac{\left(100 - t\right)^{3}}{50000} + 35.$$
Writing this in the supplied normalized form gives
$$Q(t)=35(1-\frac{t}{100})-20(1-\frac{t}{100})^{3}.$$
Finally, we have $\alpha=35,\beta=-20,$ and
$$\alpha-\beta=35-(-20)=55.$$

---
q-339394 | authored-operations | :question.difficulty/moderate | eligible=True

A juice-processing tank initially holds $300\,\text{L}$ of liquid containing $12\,\text{kg}$ of dissolved sugar.
A solution containing $0.07\,\text{kg/L}$ of dissolved sugar is pumped into the tank at a rate of $10\,\text{L/min},$ while the completely mixed liquid is drained out at a rate of $15\,\text{L/min}.$ If the amount of sugar $Q(t),$ in kilograms, in the tank $t$ minutes after pumping begins is given by

$$
Q(t)=\alpha \,(1-\frac{t}{60})+\beta {(1-\frac{t}{60})}^{3}
$$

where $\alpha $ and $\beta $ are constants, what is the value of $\alpha -\beta ?$

- $33$
- $12$
- $42$
- $30$ [correct]
- $21$

Let $Q$ be the amount of dissolved substance in the tank at time $t,$ in minutes. The amount entering minus the amount leaving gives
$$\frac{dQ}{dt}=Q'_{\text{in}}-Q'_{\text{out}}.$$
The units of these rates are $\text{kg/min}.$

**Step 1**: Calculating the rate at which substance enters the tank.
$$\begin{aligned}Q'_{\text{in}}&=(0.07\,\frac{\text{kg}}{\text{L}})\cdot(10\,\frac{\text{L}}{\text{min}})\\
&=(0.07\,\frac{\text{kg}}{\cancel{\text{L}}})\cdot(10\,\frac{\cancel{\text{L}}}{\text{min}})\\&=0.7\,\text{kg/min}.\end{aligned}$$

**Step 2**: Calculating the rate at which substance exits the tank.
The volume is
$$V(t)=300+10t-15t=(300-5t)\,\text{L}.$$
The concentration is $\frac{Q}{300-5t}\,\text{kg/L}.$ Hence,
$$\begin{aligned}Q'_{\text{out}}&=(15\,\frac{\text{L}}{\text{min}})\cdot(\frac{Q}{300-5t}\,\frac{\text{kg}}{\text{L}})\\
&=(15\,\frac{\cancel{\text{L}}}{\text{min}})\cdot(\frac{Q}{300-5t}\,\frac{\text{kg}}{\cancel{\text{L}}})\\
&=\frac{15Q}{300-5t}\,\text{kg/min}=\frac{3Q}{60-t}\,\text{kg/min}.\end{aligned}$$

**Step 3**: Calculate the overall rate of change.
$$\begin{aligned}\frac{dQ}{dt}&=Q'_{\text{in}}-Q'_{\text{out}}\\&=0.7-\frac{3Q}{60-t}.\end{aligned}$$
Thus,
$$\frac{dQ}{dt}+\frac{3}{60-t}Q=0.7.$$

**Step 4**: Integrate the equation.
This is a first-order linear equation with variable coefficients. So we find the general solution using an integrating factor:
$$\begin{aligned}I(t)&=e^{\int 3/(60-t)\,dt}\\&=e^{-3\ln|60-t|}\\&=e^{\ln (60-t)^{-3}}\\&=(60-t)^{-3}.\end{aligned}$$
Multiplying both sides by $I(t)=(60-t)^{-3}$ yields
$$\begin{aligned}(60-t)^{-3}\cdot(\frac{dQ}{dt}+\frac{3}{60-t}Q)&=(60-t)^{-3}\cdot 0.7\\
(60-t)^{-3}\frac{dQ}{dt}+3(60-t)^{-4}Q&=0.7(60-t)^{-3}\\\frac{d}{dt}(Q(60-t)^{-3})&=0.7(60-t)^{-3}.\end{aligned}$$
Now, we integrate with respect to $t:$
$$\begin{aligned}\int\frac{d}{dt}(Q(60-t)^{-3})\,dt&=\int 0.7(60-t)^{-3}\,dt\\Q(60-t)^{-3}&=0.7\cdot\frac{1}{2}(60-t)^{-2}+C\\Q(t)&=0.35(60-t)+C(60-t)^{3}.\end{aligned}$$
Note that $C$ is a constant of integration.
The initial condition is $Q(0)=12.$ Thus,
$$\begin{aligned}0.35(60-0)+C(60-0)^{3}&=12\\
21+C(60)^{3}&=12\\C(60)^{3}&=-9\\C&=- \frac{1}{24000}.\end{aligned}$$
Finally, we obtain the following expression for $Q(t):$
$$Q(t)=- \frac{7 t}{20} - \frac{\left(60 - t\right)^{3}}{24000} + 21.$$
Writing this in the supplied normalized form gives
$$Q(t)=21(1-\frac{t}{60})-9(1-\frac{t}{60})^{3}.$$
Finally, we have $\alpha=21,\beta=-9,$ and
$$\alpha-\beta=21-(-9)=30.$$

---
q-339400 | authored-operations | :question.difficulty/hard | eligible=True

A fermentation vat initially holds $480\,\text{L}$ of liquid containing $18\,\text{kg}$ of dissolved nutrient.
A feed solution containing $0.04\,\text{kg/L}$ of the nutrient is pumped into the vat at a rate of $16\,\text{L/min},$ while the completely mixed liquid is drained out at a rate of $8\,\text{L/min}.$
Find, rounded to two decimal places, the amount of nutrient in the vat $21$ minutes after pumping begins.

- $25.92\,\text{kg}$
- $25.03\,\text{kg}$ [correct]
- $13.33\,\text{kg}$
- $25.26\,\text{kg}$
- $24.02\,\text{kg}$

Let $Q$ be the amount of dissolved substance in the tank at time $t,$ in minutes. The amount entering minus the amount leaving gives
$$\frac{dQ}{dt}=Q'_{\text{in}}-Q'_{\text{out}}.$$
The units of these rates are $\text{kg/min}.$

**Step 1**: Calculating the rate at which substance enters the tank.
$$\begin{aligned}Q'_{\text{in}}&=(0.04\,\frac{\text{kg}}{\text{L}})\cdot(16\,\frac{\text{L}}{\text{min}})\\
&=(0.04\,\frac{\text{kg}}{\cancel{\text{L}}})\cdot(16\,\frac{\cancel{\text{L}}}{\text{min}})\\&=0.64\,\text{kg/min}.\end{aligned}$$

**Step 2**: Calculating the rate at which substance exits the tank.
The volume is
$$V(t)=480+16t-8t=(480+8t)\,\text{L}.$$
The concentration is $\frac{Q}{480+8t}\,\text{kg/L}.$ Hence,
$$\begin{aligned}Q'_{\text{out}}&=(8\,\frac{\text{L}}{\text{min}})\cdot(\frac{Q}{480+8t}\,\frac{\text{kg}}{\text{L}})\\
&=(8\,\frac{\cancel{\text{L}}}{\text{min}})\cdot(\frac{Q}{480+8t}\,\frac{\text{kg}}{\cancel{\text{L}}})\\
&=\frac{8Q}{480+8t}\,\text{kg/min}=\frac{1Q}{60+t}\,\text{kg/min}.\end{aligned}$$

**Step 3**: Calculate the overall rate of change.
$$\begin{aligned}\frac{dQ}{dt}&=Q'_{\text{in}}-Q'_{\text{out}}\\&=0.64-\frac{1Q}{60+t}.\end{aligned}$$
Thus,
$$\frac{dQ}{dt}+\frac{1}{60+t}Q=0.64.$$

**Step 4**: Integrate the equation.
This is a first-order linear equation with variable coefficients. So we find the general solution using an integrating factor:
$$\begin{aligned}I(t)&=e^{\int 1/(60+t)\,dt}\\&=e^{1\ln|60+t|}\\&=e^{\ln (60+t)^{1}}\\&=(60+t)^{1}.\end{aligned}$$
Multiplying both sides by $I(t)=(60+t)^{1}$ yields
$$\begin{aligned}(60+t)^{1}\cdot(\frac{dQ}{dt}+\frac{1}{60+t}Q)&=(60+t)^{1}\cdot 0.64\\
(60+t)^{1}\frac{dQ}{dt}+1(60+t)^{0}Q&=0.64(60+t)^{1}\\\frac{d}{dt}(Q(60+t)^{1})&=0.64(60+t)^{1}.\end{aligned}$$
Now, we integrate with respect to $t:$
$$\begin{aligned}\int\frac{d}{dt}(Q(60+t)^{1})\,dt&=\int 0.64(60+t)^{1}\,dt\\Q(60+t)^{1}&=0.64\cdot\frac{1}{2}(60+t)^{2}+C\\Q(t)&=0.32(60+t)+C(60+t)^{-1}.\end{aligned}$$
Note that $C$ is a constant of integration.
The initial condition is $Q(0)=18.$ Thus,
$$\begin{aligned}0.32(60+0)+C(60+0)^{-1}&=18\\
19.2+C(60)^{-1}&=18\\C(60)^{-1}&=-1.2\\C&=-72.\end{aligned}$$
Finally, we obtain the following expression for $Q(t):$
$$Q(t)=\frac{8 t}{25} + \frac{96}{5} - \frac{72}{t + 60}.$$
Finally, the amount in the tank $21$ minutes after pumping begins is
$$\begin{aligned}Q(21)&=0.32(60+21)-1.2(\frac{60}{60+21})^{1}\\&=25.92-1.2(\frac{20}{27})^{1}\\&\approx 25.03\,\text{kg}.\end{aligned}$$
This is rounded to two decimal places.

---
q-336743 | authored-operations | :question.difficulty/hard | eligible=True

A processing tank initially holds $720\,\text{L}$ of liquid containing $23\,\text{kg}$ of dissolved preservative.
A feed solution containing $0.05\,\text{kg/L}$ of the preservative is pumped into the tank at a rate of $24\,\text{L/min},$ while the completely mixed liquid is drained out at a rate of $16\,\text{L/min}.$
Find, rounded to two decimal places, the amount of preservative in the tank $9$ minutes after pumping begins.

- $39.60\,\text{kg}$
- $28.62\,\text{kg}$
- $29.83\,\text{kg}$
- $19.01\,\text{kg}$
- $28.86\,\text{kg}$ [correct]

Let $Q$ be the amount of dissolved substance in the tank at time $t,$ in minutes. The amount entering minus the amount leaving gives
$$\frac{dQ}{dt}=Q'_{\text{in}}-Q'_{\text{out}}.$$
The units of these rates are $\text{kg/min}.$

**Step 1**: Calculating the rate at which substance enters the tank.
$$\begin{aligned}Q'_{\text{in}}&=(0.05\,\frac{\text{kg}}{\text{L}})\cdot(24\,\frac{\text{L}}{\text{min}})\\
&=(0.05\,\frac{\text{kg}}{\cancel{\text{L}}})\cdot(24\,\frac{\cancel{\text{L}}}{\text{min}})\\&=1.2\,\text{kg/min}.\end{aligned}$$

**Step 2**: Calculating the rate at which substance exits the tank.
The volume is
$$V(t)=720+24t-16t=(720+8t)\,\text{L}.$$
The concentration is $\frac{Q}{720+8t}\,\text{kg/L}.$ Hence,
$$\begin{aligned}Q'_{\text{out}}&=(16\,\frac{\text{L}}{\text{min}})\cdot(\frac{Q}{720+8t}\,\frac{\text{kg}}{\text{L}})\\
&=(16\,\frac{\cancel{\text{L}}}{\text{min}})\cdot(\frac{Q}{720+8t}\,\frac{\text{kg}}{\cancel{\text{L}}})\\
&=\frac{16Q}{720+8t}\,\text{kg/min}=\frac{2Q}{90+t}\,\text{kg/min}.\end{aligned}$$

**Step 3**: Calculate the overall rate of change.
$$\begin{aligned}\frac{dQ}{dt}&=Q'_{\text{in}}-Q'_{\text{out}}\\&=1.2-\frac{2Q}{90+t}.\end{aligned}$$
Thus,
$$\frac{dQ}{dt}+\frac{2}{90+t}Q=1.2.$$

**Step 4**: Integrate the equation.
This is a first-order linear equation with variable coefficients. So we find the general solution using an integrating factor:
$$\begin{aligned}I(t)&=e^{\int 2/(90+t)\,dt}\\&=e^{2\ln|90+t|}\\&=e^{\ln (90+t)^{2}}\\&=(90+t)^{2}.\end{aligned}$$
Multiplying both sides by $I(t)=(90+t)^{2}$ yields
$$\begin{aligned}(90+t)^{2}\cdot(\frac{dQ}{dt}+\frac{2}{90+t}Q)&=(90+t)^{2}\cdot 1.2\\
(90+t)^{2}\frac{dQ}{dt}+2(90+t)^{1}Q&=1.2(90+t)^{2}\\\frac{d}{dt}(Q(90+t)^{2})&=1.2(90+t)^{2}.\end{aligned}$$
Now, we integrate with respect to $t:$
$$\begin{aligned}\int\frac{d}{dt}(Q(90+t)^{2})\,dt&=\int 1.2(90+t)^{2}\,dt\\Q(90+t)^{2}&=1.2\cdot\frac{1}{3}(90+t)^{3}+C\\Q(t)&=0.4(90+t)+C(90+t)^{-2}.\end{aligned}$$
Note that $C$ is a constant of integration.
The initial condition is $Q(0)=23.$ Thus,
$$\begin{aligned}0.4(90+0)+C(90+0)^{-2}&=23\\
36+C(90)^{-2}&=23\\C(90)^{-2}&=-13\\C&=-105300.\end{aligned}$$
Finally, we obtain the following expression for $Q(t):$
$$Q(t)=\frac{2 t}{5} + 36 - \frac{105300}{\left(t + 90\right)^{2}}.$$
Finally, the amount in the tank $9$ minutes after pumping begins is
$$\begin{aligned}Q(9)&=0.4(90+9)-13(\frac{90}{90+9})^{2}\\&=39.6-13(\frac{10}{11})^{2}\\&\approx 28.86\,\text{kg}.\end{aligned}$$
This is rounded to two decimal places.

---
q-336738 | authored-operations | :question.difficulty/hard | eligible=True

A storage tank initially holds $640L$ of liquid containing $19kg$ of dissolved stabilizer.
A feed solution containing $0.04kg/L$ of the stabilizer is pumped into the tank at a rate of $24L/min$, while the completely mixed liquid is drained out at a rate of $16L/min$.
Find, rounded to two decimal places, the amount of stabilizer in the tank $20$ minutes after pumping begins.

> A scientific calculator is required to answer this question.

- $26.63\,\text{kg}$
- $28.62\,\text{kg}$
- $27.78\,\text{kg}$ [correct]
- $32.00\,\text{kg}$
- $12.16\,\text{kg}$

Let $Q$ be the amount of dissolved substance in the tank at time $t,$ in minutes. The amount entering minus the amount leaving gives
$$\frac{dQ}{dt}=Q'_{\text{in}}-Q'_{\text{out}}.$$
The units of these rates are $\text{kg/min}.$

**Step 1**: Calculating the rate at which substance enters the tank.
$$\begin{aligned}Q'_{\text{in}}&=(0.04\,\frac{\text{kg}}{\text{L}})\cdot(24\,\frac{\text{L}}{\text{min}})\\
&=(0.04\,\frac{\text{kg}}{\cancel{\text{L}}})\cdot(24\,\frac{\cancel{\text{L}}}{\text{min}})\\&=0.96\,\text{kg/min}.\end{aligned}$$

**Step 2**: Calculating the rate at which substance exits the tank.
The volume is
$$V(t)=640+24t-16t=(640+8t)\,\text{L}.$$
The concentration is $\frac{Q}{640+8t}\,\text{kg/L}.$ Hence,
$$\begin{aligned}Q'_{\text{out}}&=(16\,\frac{\text{L}}{\text{min}})\cdot(\frac{Q}{640+8t}\,\frac{\text{kg}}{\text{L}})\\
&=(16\,\frac{\cancel{\text{L}}}{\text{min}})\cdot(\frac{Q}{640+8t}\,\frac{\text{kg}}{\cancel{\text{L}}})\\
&=\frac{16Q}{640+8t}\,\text{kg/min}=\frac{2Q}{80+t}\,\text{kg/min}.\end{aligned}$$

**Step 3**: Calculate the overall rate of change.
$$\begin{aligned}\frac{dQ}{dt}&=Q'_{\text{in}}-Q'_{\text{out}}\\&=0.96-\frac{2Q}{80+t}.\end{aligned}$$
Thus,
$$\frac{dQ}{dt}+\frac{2}{80+t}Q=0.96.$$

**Step 4**: Integrate the equation.
This is a first-order linear equation with variable coefficients. So we find the general solution using an integrating factor:
$$\begin{aligned}I(t)&=e^{\int 2/(80+t)\,dt}\\&=e^{2\ln|80+t|}\\&=e^{\ln (80+t)^{2}}\\&=(80+t)^{2}.\end{aligned}$$
Multiplying both sides by $I(t)=(80+t)^{2}$ yields
$$\begin{aligned}(80+t)^{2}\cdot(\frac{dQ}{dt}+\frac{2}{80+t}Q)&=(80+t)^{2}\cdot 0.96\\
(80+t)^{2}\frac{dQ}{dt}+2(80+t)^{1}Q&=0.96(80+t)^{2}\\\frac{d}{dt}(Q(80+t)^{2})&=0.96(80+t)^{2}.\end{aligned}$$
Now, we integrate with respect to $t:$
$$\begin{aligned}\int\frac{d}{dt}(Q(80+t)^{2})\,dt&=\int 0.96(80+t)^{2}\,dt\\Q(80+t)^{2}&=0.96\cdot\frac{1}{3}(80+t)^{3}+C\\Q(t)&=0.32(80+t)+C(80+t)^{-2}.\end{aligned}$$
Note that $C$ is a constant of integration.
The initial condition is $Q(0)=19.$ Thus,
$$\begin{aligned}0.32(80+0)+C(80+0)^{-2}&=19\\
25.6+C(80)^{-2}&=19\\C(80)^{-2}&=-6.6\\C&=-42240.\end{aligned}$$
Finally, we obtain the following expression for $Q(t):$
$$Q(t)=\frac{8 t}{25} + \frac{128}{5} - \frac{42240}{\left(t + 80\right)^{2}}.$$
Finally, the amount in the tank $20$ minutes after pumping begins is
$$\begin{aligned}Q(20)&=0.32(80+20)-6.6(\frac{80}{80+20})^{2}\\&=32-6.6(\frac{4}{5})^{2}\\&\approx 27.78\,\text{kg}.\end{aligned}$$
This is rounded to two decimal places.

---
q-336743 | authored-operations | :question.difficulty/hard | eligible=True

A processing tank initially holds $800\,\text{L}$ of liquid containing $20\,\text{kg}$ of dissolved preservative.
A feed solution containing $0.05\,\text{kg/L}$ of the preservative is pumped into the tank at a rate of $24\,\text{L/min},$ while the completely mixed liquid is drained out at a rate of $16\,\text{L/min}.$
Find, rounded to two decimal places, the amount of preservative in the tank $15$ minutes after pumping begins.

- $15.12\,\text{kg}$
- $30.88\,\text{kg}$ [correct]
- $46.00\,\text{kg}$
- $32.85\,\text{kg}$
- $30.37\,\text{kg}$

Let $Q$ be the amount of dissolved substance in the tank at time $t,$ in minutes. The amount entering minus the amount leaving gives
$$\frac{dQ}{dt}=Q'_{\text{in}}-Q'_{\text{out}}.$$
The units of these rates are $\text{kg/min}.$

**Step 1**: Calculating the rate at which substance enters the tank.
$$\begin{aligned}Q'_{\text{in}}&=(0.05\,\frac{\text{kg}}{\text{L}})\cdot(24\,\frac{\text{L}}{\text{min}})\\
&=(0.05\,\frac{\text{kg}}{\cancel{\text{L}}})\cdot(24\,\frac{\cancel{\text{L}}}{\text{min}})\\&=1.2\,\text{kg/min}.\end{aligned}$$

**Step 2**: Calculating the rate at which substance exits the tank.
The volume is
$$V(t)=800+24t-16t=(800+8t)\,\text{L}.$$
The concentration is $\frac{Q}{800+8t}\,\text{kg/L}.$ Hence,
$$\begin{aligned}Q'_{\text{out}}&=(16\,\frac{\text{L}}{\text{min}})\cdot(\frac{Q}{800+8t}\,\frac{\text{kg}}{\text{L}})\\
&=(16\,\frac{\cancel{\text{L}}}{\text{min}})\cdot(\frac{Q}{800+8t}\,\frac{\text{kg}}{\cancel{\text{L}}})\\
&=\frac{16Q}{800+8t}\,\text{kg/min}=\frac{2Q}{100+t}\,\text{kg/min}.\end{aligned}$$

**Step 3**: Calculate the overall rate of change.
$$\begin{aligned}\frac{dQ}{dt}&=Q'_{\text{in}}-Q'_{\text{out}}\\&=1.2-\frac{2Q}{100+t}.\end{aligned}$$
Thus,
$$\frac{dQ}{dt}+\frac{2}{100+t}Q=1.2.$$

**Step 4**: Integrate the equation.
This is a first-order linear equation with variable coefficients. So we find the general solution using an integrating factor:
$$\begin{aligned}I(t)&=e^{\int 2/(100+t)\,dt}\\&=e^{2\ln|100+t|}\\&=e^{\ln (100+t)^{2}}\\&=(100+t)^{2}.\end{aligned}$$
Multiplying both sides by $I(t)=(100+t)^{2}$ yields
$$\begin{aligned}(100+t)^{2}\cdot(\frac{dQ}{dt}+\frac{2}{100+t}Q)&=(100+t)^{2}\cdot 1.2\\
(100+t)^{2}\frac{dQ}{dt}+2(100+t)^{1}Q&=1.2(100+t)^{2}\\\frac{d}{dt}(Q(100+t)^{2})&=1.2(100+t)^{2}.\end{aligned}$$
Now, we integrate with respect to $t:$
$$\begin{aligned}\int\frac{d}{dt}(Q(100+t)^{2})\,dt&=\int 1.2(100+t)^{2}\,dt\\Q(100+t)^{2}&=1.2\cdot\frac{1}{3}(100+t)^{3}+C\\Q(t)&=0.4(100+t)+C(100+t)^{-2}.\end{aligned}$$
Note that $C$ is a constant of integration.
The initial condition is $Q(0)=20.$ Thus,
$$\begin{aligned}0.4(100+0)+C(100+0)^{-2}&=20\\
40+C(100)^{-2}&=20\\C(100)^{-2}&=-20\\C&=-200000.\end{aligned}$$
Finally, we obtain the following expression for $Q(t):$
$$Q(t)=\frac{2 t}{5} + 40 - \frac{200000}{\left(t + 100\right)^{2}}.$$
Finally, the amount in the tank $15$ minutes after pumping begins is
$$\begin{aligned}Q(15)&=0.4(100+15)-20(\frac{100}{100+15})^{2}\\&=46-20(\frac{20}{23})^{2}\\&\approx 30.88\,\text{kg}.\end{aligned}$$
This is rounded to two decimal places.

---
q-336743 | authored-operations | :question.difficulty/hard | eligible=True

A processing tank initially holds $600\,\text{L}$ of liquid containing $16\,\text{kg}$ of dissolved preservative.
A feed solution containing $0.05\,\text{kg/L}$ of the preservative is pumped into the tank at a rate of $30\,\text{L/min},$ while the completely mixed liquid is drained out at a rate of $20\,\text{L/min}.$
Find, rounded to two decimal places, the amount of preservative in the tank $8$ minutes after pumping begins.

- $12.46\,\text{kg}$
- $23.10\,\text{kg}$ [correct]
- $24.38\,\text{kg}$
- $34.00\,\text{kg}$
- $22.79\,\text{kg}$

Let $Q$ be the amount of dissolved substance in the tank at time $t,$ in minutes. The amount entering minus the amount leaving gives
$$\frac{dQ}{dt}=Q'_{\text{in}}-Q'_{\text{out}}.$$
The units of these rates are $\text{kg/min}.$

**Step 1**: Calculating the rate at which substance enters the tank.
$$\begin{aligned}Q'_{\text{in}}&=(0.05\,\frac{\text{kg}}{\text{L}})\cdot(30\,\frac{\text{L}}{\text{min}})\\
&=(0.05\,\frac{\text{kg}}{\cancel{\text{L}}})\cdot(30\,\frac{\cancel{\text{L}}}{\text{min}})\\&=1.5\,\text{kg/min}.\end{aligned}$$

**Step 2**: Calculating the rate at which substance exits the tank.
The volume is
$$V(t)=600+30t-20t=(600+10t)\,\text{L}.$$
The concentration is $\frac{Q}{600+10t}\,\text{kg/L}.$ Hence,
$$\begin{aligned}Q'_{\text{out}}&=(20\,\frac{\text{L}}{\text{min}})\cdot(\frac{Q}{600+10t}\,\frac{\text{kg}}{\text{L}})\\
&=(20\,\frac{\cancel{\text{L}}}{\text{min}})\cdot(\frac{Q}{600+10t}\,\frac{\text{kg}}{\cancel{\text{L}}})\\
&=\frac{20Q}{600+10t}\,\text{kg/min}=\frac{2Q}{60+t}\,\text{kg/min}.\end{aligned}$$

**Step 3**: Calculate the overall rate of change.
$$\begin{aligned}\frac{dQ}{dt}&=Q'_{\text{in}}-Q'_{\text{out}}\\&=1.5-\frac{2Q}{60+t}.\end{aligned}$$
Thus,
$$\frac{dQ}{dt}+\frac{2}{60+t}Q=1.5.$$

**Step 4**: Integrate the equation.
This is a first-order linear equation with variable coefficients. So we find the general solution using an integrating factor:
$$\begin{aligned}I(t)&=e^{\int 2/(60+t)\,dt}\\&=e^{2\ln|60+t|}\\&=e^{\ln (60+t)^{2}}\\&=(60+t)^{2}.\end{aligned}$$
Multiplying both sides by $I(t)=(60+t)^{2}$ yields
$$\begin{aligned}(60+t)^{2}\cdot(\frac{dQ}{dt}+\frac{2}{60+t}Q)&=(60+t)^{2}\cdot 1.5\\
(60+t)^{2}\frac{dQ}{dt}+2(60+t)^{1}Q&=1.5(60+t)^{2}\\\frac{d}{dt}(Q(60+t)^{2})&=1.5(60+t)^{2}.\end{aligned}$$
Now, we integrate with respect to $t:$
$$\begin{aligned}\int\frac{d}{dt}(Q(60+t)^{2})\,dt&=\int 1.5(60+t)^{2}\,dt\\Q(60+t)^{2}&=1.5\cdot\frac{1}{3}(60+t)^{3}+C\\Q(t)&=0.5(60+t)+C(60+t)^{-2}.\end{aligned}$$
Note that $C$ is a constant of integration.
The initial condition is $Q(0)=16.$ Thus,
$$\begin{aligned}0.5(60+0)+C(60+0)^{-2}&=16\\
30+C(60)^{-2}&=16\\C(60)^{-2}&=-14\\C&=-50400.\end{aligned}$$
Finally, we obtain the following expression for $Q(t):$
$$Q(t)=\frac{t}{2} + 30 - \frac{50400}{\left(t + 60\right)^{2}}.$$
Finally, the amount in the tank $8$ minutes after pumping begins is
$$\begin{aligned}Q(8)&=0.5(60+8)-14(\frac{60}{60+8})^{2}\\&=34-14(\frac{15}{17})^{2}\\&\approx 23.10\,\text{kg}.\end{aligned}$$
This is rounded to two decimal places.
