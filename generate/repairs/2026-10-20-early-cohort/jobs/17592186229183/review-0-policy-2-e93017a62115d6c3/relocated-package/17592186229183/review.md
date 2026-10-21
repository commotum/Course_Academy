# Overflow onset generator review

Source replay retains observed difficulty/omissions. Generated records use explicitly authored workload policies. Raw/opaque records are evidence-only.

## source replay — easy (observed) / q-336451 / observed:q-336451

A de-icing salt reservoir can hold up to $300\,\text{gal}$ of liquid. Initially, it contains $180\,\text{gal}$ of brine with $54\,\text{lb}$ of dissolved salt. A stronger brine with concentration $0.8\,\text{lb/gal}$ flows into the reservoir at a rate of $6\,\text{gal/min},$ while the completely mixed brine drains out at a rate of $4\,\text{gal/min}.$
Find the amount of salt in the reservoir at the moment it begins to overflow.

- $204.3lb$
- $206.2lb$
- $205.4lb$
- $207.6lb$
- $201.0lb$

- $201.0\,\text{lb}$
- $207.6\,\text{lb}$ **supplied key**
- $204.3\,\text{lb}$
- $206.2\,\text{lb}$
- $205.4\,\text{lb}$

Since $Q$ is the amount of salt in the tank at time $t,$ the derivative 

$$
\frac{dQ}{dt}
$$

describes how this amount changes with respect to time $t,$ in minutes. This is equal to the rate at which minerals enter the tank minus the rate at which minerals leave the tank.

$$
\frac{dQ}{dt}={Q}_{\text{in}}^{′}-{Q}_{\text{out}}^{′}
$$

Note that the units of $\frac{dQ}{dt},{Q}_{\text{in}}^{′}$ and ${Q}_{\text{out}}^{′}$ are $\text{kg}/\text{min}.$ Now, let's compute the required rates of change in steps.

**Step 1**: Calculating the rate at which minerals enter the tank.

First, note that a brine solution containing $0.8\,\text{lb/gal}$ of salt enters the reservoir at a rate of $6\,\text{gal/min}.$ So, the rate at which the *salt* enters the reservoir is 

$$
\begin{aligned}{Q}_{\text{in}}^{′} & =(0.8\,\frac{\text{lb}}{\text{gal}})\cdot (6\,\frac{\text{gal}}{\text{min}}) \\  & =(0.8\,\frac{\text{lb}}{\cancel{\text{gal}}})\cdot (6\,\frac{\cancel{\text{gal}}}{\text{min}}) \\  & =4.8\,\frac{\text{lb}}{\text{min}}.\end{aligned}
$$

**Step 2**: Calculating the rate at which minerals exit the tank.

To find the rate at which salt leaves the reservoir, we must first determine the volume of brine in the reservoir at time $t.$

The reservoir initially contains $180\,\text{gal}$ of brine; brine enters at $6\,\text{gal/min}$ and mixed brine leaves at $4\,\text{gal/min}.$
As a result, the amount of brine in the reservoir after $t$ minutes is 

$$
V(t)=180+6t-4t=2(90+t)\,\text{gal}.
$$

Note that $V(t)$ is an increasing function, so the reservoir is filling.

Since $Q$ is the amount of salt in the reservoir, the concentration of the brine at time $t$ is

$$
\frac{Q}{2(90+t)}\,\text{lb/gal}.
$$

Therefore, as the completely mixed brine leaves at a rate of $4\,\text{gal/min},$ *salt* leaves at a rate of

$$
\begin{aligned}{Q}_{\text{out}}^{′} & =(4\,\frac{\text{gal}}{\text{min}})\cdot (\frac{Q}{2(90+t)}\,\frac{\text{lb}}{\text{gal}}) \\  & =(4\,\frac{\cancel{\text{gal}}}{\text{min}})\cdot (\frac{Q}{2(90+t)}\,\frac{\text{lb}}{\cancel{\text{gal}}}) \\  & =\frac{4Q}{2(90+t)}\,\frac{\text{lb}}{\text{min}} \\  & =\frac{2Q}{90+t}\,\frac{\text{lb}}{\text{min}}.\end{aligned}
$$

**Step 3**: Calculate the overall rate of change.

The rate of change equals the rate of entry minus the rate of exit. Therefore, 

$$
\begin{aligned}\frac{dQ}{dt} & ={Q}_{\text{in}}^{′}-{Q}_{\text{out}}^{′} \\  & =4.8-\frac{2Q}{90+t}\end{aligned}
$$

which gives the equation

$$
\frac{dQ}{dt}+\frac{2}{90+t}\,Q=4.8.
$$

**Step 4**: Integrate the equation.

This is a first-order linear equation with variable coefficients. So we find the general solution using an integrating factor:

$$
\begin{aligned}I(t) & ={e}^{\int 2/(90+t)\,dt} \\  & ={e}^{2\operatorname{ln}⁡|90+t|} \\  & ={e}^{\operatorname{ln}⁡(90+t)^{2}} \\  & =(90+t)^{2}\end{aligned}
$$

Multiplying both sides of the differential equation by $I(t)=(90+t)^{2}$ yields

$$
\begin{aligned}(90+t)^{2}\cdot (\frac{dQ}{dt}+\frac{2}{90+t}\,Q) & =(90+t)^{2}\cdot 4.8 \\ (90+t)^{2}\frac{dQ}{dt}+2(90+t)Q & =4.8(90+t)^{2} \\ \frac{d}{dt}(Q(90+t)^{2}) & =4.8(90+t)^{2}.\end{aligned}
$$

Now, we integrate with respect to $t:$

$$
\begin{aligned}\int \frac{d}{dt}(Q(90+t)^{2})\,dt & =\int 4.8(90+t)^{2}\,dt \\ Q(90+t)^{2} & =4.8\cdot \frac{1}{3}(90+t)^{3}+C \\ Q(t) & =1.6(90+t)+\frac{C}{(90+t)^{2}}\end{aligned}
$$

We're told that the reservoir initially contains $54\,\text{lb}$ of salt. So, we can apply the initial condition $Q(0)=54,$ and solve for $C:$

$$
\begin{aligned}Q(0) & =54 \\ 1.6(90+0)+\frac{C}{(90+0)^{2}} & =54 \\ 144+\frac{C}{(90)^{2}} & =54 \\ C & =-90(90)^{2}\end{aligned}
$$

Therefore, we obtain the following expression for $Q(t):$

$$
\begin{aligned}Q(t) & =1.6(90+t)-\frac{90(90)^{2}}{(90+t)^{2}} \\  & =1.6(90+t)-90{(\frac{90}{90+t})}^{2}\end{aligned}
$$

Now, let ${t}_{o}$ be the time when the reservoir begins to overflow. The reservoir has a capacity of $300\,\text{gal},$ so we can use the condition $V({t}_{o})=300$ to solve for ${t}_{o}:$

$$
\begin{aligned}V({t}_{o}) & =300 \\ 2(90+{t}_{o}) & =300 \\ 90+{t}_{o} & =150 \\ {t}_{o} & =60\,\text{min}\end{aligned}
$$

Finally, the amount of salt in the reservoir at the moment it begins to overflow is

$$
\begin{aligned}Q(60) & =1.6(90+60)-90{(\frac{90}{90+60})}^{2} \\  & =240-90{(\frac{9}{15})}^{2} \\  & =207.6\,\text{lb}.\end{aligned}
$$



## generated variant — easy (authored workload policy) / q-336451 / method

A de-icing salt reservoir can hold up to $620\,\text{gal}$ of liquid. Initially, it contains $280\,\text{gal}$ of brine with $84\,\text{lb}$ of dissolved salt. A stronger brine with concentration $0.6\,\text{lb/gal}$ flows into the reservoir at a rate of $30\,\text{gal/min},$ while the completely mixed brine drains out at a rate of $20\,\text{gal/min}.$
Find the amount of salt in the reservoir at the moment it begins to overflow. Round to one decimal place.

- $364.3\,\text{lb}$
- $334.1\,\text{lb}$
- $337.7\,\text{lb}$
- $354.9\,\text{lb}$ **supplied key**
- $372.0\,\text{lb}$

Since $Q$ is the amount of salt in the tank at time $t,$ the derivative 

$$
\frac{dQ}{dt}
$$

describes how this amount changes with respect to time $t,$ in minutes. This is equal to the rate at which salt enter the tank minus the rate at which salt leave the tank.

$$
\frac{dQ}{dt}={Q}_{\text{in}}^{′}-{Q}_{\text{out}}^{′}
$$

Note that the units of $\frac{dQ}{dt},{Q}_{\text{in}}^{′}$ and ${Q}_{\text{out}}^{′}$ are $\text{lb}/\text{min}.$ Now, let's compute the required rates of change in steps.

**Step 1**: Calculating the rate at which salt enter the tank.

First, note that a brine solution containing $0.6\,\text{lb/gal}$ of salt enters the reservoir at a rate of $30\,\text{gal/min}.$ So, the rate at which the *salt* enters the reservoir is 

$$
\begin{aligned}{Q}_{\text{in}}^{′} & =(0.6\,\frac{\text{lb}}{\text{gal}})\cdot (30\,\frac{\text{gal}}{\text{min}}) \\  & =(0.6\,\frac{\text{lb}}{\cancel{\text{gal}}})\cdot (30\,\frac{\cancel{\text{gal}}}{\text{min}}) \\  & =18\,\frac{\text{lb}}{\text{min}}.\end{aligned}
$$

**Step 2**: Calculating the rate at which salt exit the tank.

To find the rate at which salt leaves the reservoir, we must first determine the volume of brine in the reservoir at time $t.$

The reservoir initially contains $280\,\text{gal}$ of brine; brine enters at $30\,\text{gal/min}$ and mixed brine leaves at $20\,\text{gal/min}.$
As a result, the amount of brine in the reservoir after $t$ minutes is 

$$
V(t)=280+30t-20t=10(28+t)\,\text{gal}.
$$

Note that $V(t)$ is an increasing function, so the reservoir is filling.

Since $Q$ is the amount of salt in the reservoir, the concentration of the brine at time $t$ is

$$
\frac{Q}{10(28+t)}\,\text{lb/gal}.
$$

Therefore, as the completely mixed brine leaves at a rate of $20\,\text{gal/min},$ *salt* leaves at a rate of

$$
\begin{aligned}{Q}_{\text{out}}^{′} & =(20\,\frac{\text{gal}}{\text{min}})\cdot (\frac{Q}{10(28+t)}\,\frac{\text{lb}}{\text{gal}}) \\  & =(20\,\frac{\cancel{\text{gal}}}{\text{min}})\cdot (\frac{Q}{10(28+t)}\,\frac{\text{lb}}{\cancel{\text{gal}}}) \\  & =\frac{20Q}{10(28+t)}\,\frac{\text{lb}}{\text{min}} \\  & =\frac{2Q}{28+t}\,\frac{\text{lb}}{\text{min}}.\end{aligned}
$$

**Step 3**: Calculate the overall rate of change.

The rate of change equals the rate of entry minus the rate of exit. Therefore, 

$$
\begin{aligned}\frac{dQ}{dt} & ={Q}_{\text{in}}^{′}-{Q}_{\text{out}}^{′} \\  & =18-\frac{2Q}{28+t}\end{aligned}
$$

which gives the equation

$$
\frac{dQ}{dt}+\frac{2}{28+t}\,Q=18.
$$

**Step 4**: Integrate the equation.

This is a first-order linear equation with variable coefficients. So we find the general solution using an integrating factor:

$$
\begin{aligned}I(t) & ={e}^{\int 2/(28+t)\,dt} \\  & ={e}^{2\operatorname{ln}⁡|28+t|} \\  & ={e}^{\operatorname{ln}⁡(28+t)^{2}} \\  & =(28+t)^{2}\end{aligned}
$$

Multiplying both sides of the differential equation by $I(t)=(28+t)^{2}$ yields

$$
\begin{aligned}(28+t)^{2}\cdot (\frac{dQ}{dt}+\frac{2}{28+t}\,Q) & =(28+t)^{2}\cdot 18 \\ (28+t)^{2}\frac{dQ}{dt}+2(28+t)Q & =18(28+t)^{2} \\ \frac{d}{dt}(Q(28+t)^{2}) & =18(28+t)^{2}.\end{aligned}
$$

Now, we integrate with respect to $t:$

$$
\begin{aligned}\int \frac{d}{dt}(Q(28+t)^{2})\,dt & =\int 18(28+t)^{2}\,dt \\ Q(28+t)^{2} & =18\cdot \frac{1}{3}(28+t)^{3}+C \\ Q(t) & =6(28+t)+\frac{C}{(28+t)^{2}}\end{aligned}
$$

We're told that the reservoir initially contains $84\,\text{lb}$ of salt. So, we can apply the initial condition $Q(0)=84,$ and solve for $C:$

$$
\begin{aligned}Q(0) & =84 \\ 6(28+0)+\frac{C}{(28+0)^{2}} & =84 \\ 168+\frac{C}{(28)^{2}} & =84 \\ C & =-84(28)^{2}\end{aligned}
$$

Therefore, we obtain the following expression for $Q(t):$

$$
\begin{aligned}Q(t) & =6(28+t)-\frac{84(28)^{2}}{(28+t)^{2}} \\  & =6(28+t)-84{(\frac{28}{28+t})}^{2}\end{aligned}
$$

Now, let ${t}_{o}$ be the time when the reservoir begins to overflow. The reservoir has a capacity of $620\,\text{gal},$ so we can use the condition $V({t}_{o})=620$ to solve for ${t}_{o}:$

$$
\begin{aligned}V({t}_{o}) & =620 \\ 10(28+{t}_{o}) & =620 \\ 28+{t}_{o} & =62 \\ {t}_{o} & =34\,\text{min}\end{aligned}
$$

Finally, rounded to one decimal place, the amount of salt in the reservoir at the moment it begins to overflow is

$$
\begin{aligned}Q(34) & =6(28+34)-84{(\frac{28}{28+34})}^{2} \\  & =372-84{(\frac{2.8}{6.2})}^{2} \\  & ≈354.9\,\text{lb}.\end{aligned}
$$



## source replay — easy (observed) / q-336451 / observed:q-336451

A de-icing salt reservoir can hold up to $620\,\text{gal}$ of liquid. Initially, it contains $280\,\text{gal}$ of brine with $84\,\text{lb}$ of dissolved salt. A stronger brine with concentration $0.6\,\text{lb/gal}$ flows into the reservoir at a rate of $30\,\text{gal/min},$ while the completely mixed brine drains out at a rate of $20\,\text{gal/min}.$
Find the amount of salt in the reservoir at the moment it begins to overflow.

- $354.9lb$
- $351.6lb$
- $348.3lb$
- $353.5lb$
- $352.7lb$

- $348.3\,\text{lb}$
- $353.5\,\text{lb}$
- $352.7\,\text{lb}$
- $351.6\,\text{lb}$
- $354.9\,\text{lb}$ **supplied key**

Since $Q$ is the amount of salt in the tank at time $t,$ the derivative 

$$
\frac{dQ}{dt}
$$

describes how this amount changes with respect to time $t,$ in minutes. This is equal to the rate at which minerals enter the tank minus the rate at which minerals leave the tank.

$$
\frac{dQ}{dt}={Q}_{\text{in}}^{′}-{Q}_{\text{out}}^{′}
$$

Note that the units of $\frac{dQ}{dt},{Q}_{\text{in}}^{′}$ and ${Q}_{\text{out}}^{′}$ are $\text{kg}/\text{min}.$ Now, let's compute the required rates of change in steps.

**Step 1**: Calculating the rate at which minerals enter the tank.

First, note that a brine solution containing $0.6\,\text{lb/gal}$ of salt enters the reservoir at a rate of $30\,\text{gal/min}.$ So, the rate at which the *salt* enters the reservoir is 

$$
\begin{aligned}{Q}_{\text{in}}^{′} & =(0.6\,\frac{\text{lb}}{\text{gal}})\cdot (30\,\frac{\text{gal}}{\text{min}}) \\  & =(0.6\,\frac{\text{lb}}{\cancel{\text{gal}}})\cdot (30\,\frac{\cancel{\text{gal}}}{\text{min}}) \\  & =18\,\frac{\text{lb}}{\text{min}}.\end{aligned}
$$

**Step 2**: Calculating the rate at which minerals exit the tank.

To find the rate at which salt leaves the reservoir, we must first determine the volume of brine in the reservoir at time $t.$

The reservoir initially contains $280\,\text{gal}$ of brine; brine enters at $30\,\text{gal/min}$ and mixed brine leaves at $20\,\text{gal/min}.$
As a result, the amount of brine in the reservoir after $t$ minutes is 

$$
V(t)=280+30t-20t=10(28+t)\,\text{gal}.
$$

Note that $V(t)$ is an increasing function, so the reservoir is filling.

Since $Q$ is the amount of salt in the reservoir, the concentration of the brine at time $t$ is

$$
\frac{Q}{10(28+t)}\,\text{lb/gal}.
$$

Therefore, as the completely mixed brine leaves at a rate of $20\,\text{gal/min},$ *salt* leaves at a rate of

$$
\begin{aligned}{Q}_{\text{out}}^{′} & =(20\,\frac{\text{gal}}{\text{min}})\cdot (\frac{Q}{10(28+t)}\,\frac{\text{lb}}{\text{gal}}) \\  & =(20\,\frac{\cancel{\text{gal}}}{\text{min}})\cdot (\frac{Q}{10(28+t)}\,\frac{\text{lb}}{\cancel{\text{gal}}}) \\  & =\frac{20Q}{10(28+t)}\,\frac{\text{lb}}{\text{min}} \\  & =\frac{2Q}{28+t}\,\frac{\text{lb}}{\text{min}}.\end{aligned}
$$

**Step 3**: Calculate the overall rate of change.

The rate of change equals the rate of entry minus the rate of exit. Therefore, 

$$
\begin{aligned}\frac{dQ}{dt} & ={Q}_{\text{in}}^{′}-{Q}_{\text{out}}^{′} \\  & =18-\frac{2Q}{28+t}\end{aligned}
$$

which gives the equation

$$
\frac{dQ}{dt}+\frac{2}{28+t}\,Q=18.
$$

**Step 4**: Integrate the equation.

This is a first-order linear equation with variable coefficients. So we find the general solution using an integrating factor:

$$
\begin{aligned}I(t) & ={e}^{\int 2/(28+t)\,dt} \\  & ={e}^{2\operatorname{ln}⁡|28+t|} \\  & ={e}^{\operatorname{ln}⁡(28+t)^{2}} \\  & =(28+t)^{2}\end{aligned}
$$

Multiplying both sides of the differential equation by $I(t)=(28+t)^{2}$ yields

$$
\begin{aligned}(28+t)^{2}\cdot (\frac{dQ}{dt}+\frac{2}{28+t}\,Q) & =(28+t)^{2}\cdot 18 \\ (28+t)^{2}\frac{dQ}{dt}+2(28+t)Q & =18(28+t)^{2} \\ \frac{d}{dt}(Q(28+t)^{2}) & =18(28+t)^{2}.\end{aligned}
$$

Now, we integrate with respect to $t:$

$$
\begin{aligned}\int \frac{d}{dt}(Q(28+t)^{2})\,dt & =\int 18(28+t)^{2}\,dt \\ Q(28+t)^{2} & =18\cdot \frac{1}{3}(28+t)^{3}+C \\ Q(t) & =6(28+t)+\frac{C}{(28+t)^{2}}\end{aligned}
$$

We're told that the reservoir initially contains $84\,\text{lb}$ of salt. So, we can apply the initial condition $Q(0)=84,$ and solve for $C:$

$$
\begin{aligned}Q(0) & =84 \\ 6(28+0)+\frac{C}{(28+0)^{2}} & =84 \\ 168+\frac{C}{(28)^{2}} & =84 \\ C & =-84(28)^{2}\end{aligned}
$$

Therefore, we obtain the following expression for $Q(t):$

$$
\begin{aligned}Q(t) & =6(28+t)-\frac{84(28)^{2}}{(28+t)^{2}} \\  & =6(28+t)-84{(\frac{28}{28+t})}^{2}\end{aligned}
$$

Now, let ${t}_{o}$ be the time when the reservoir begins to overflow. The reservoir has a capacity of $620\,\text{gal},$ so we can use the condition $V({t}_{o})=620$ to solve for ${t}_{o}:$

$$
\begin{aligned}V({t}_{o}) & =620 \\ 10(28+{t}_{o}) & =620 \\ 28+{t}_{o} & =62 \\ {t}_{o} & =34\,\text{min}\end{aligned}
$$

Finally, the amount of salt in the reservoir at the moment it begins to overflow is

$$
\begin{aligned}Q(34) & =6(28+34)-84{(\frac{28}{28+34})}^{2} \\  & =372-84{(\frac{2.8}{6.2})}^{2} \\  & ≈354.9\,\text{lb}.\end{aligned}
$$



## source replay — easy (omitted in raw source) / q-336499 / observed:q-336499

A nutrient tank for a hydroponic greenhouse can hold up to $210gal$ of solution. Initially, it contains $120gal$ of nutrient solution with $30lb$ of dissolved nutrient. A more concentrated solution with concentration $0.5lb/gal$ flows into the tank at a rate of $9gal/min$, while the completely mixed solution drains out at a rate of $6gal/min$. Rounded to one decimal place, find the amount of nutrient in the tank at the moment it begins to overflow.

> A scientific calculator is required to answer this question.

- $95.0lb$
- $94.7lb$
- $95.2lb$
- $94.2lb$
- $93.5lb$

*Worked solution absent in raw evidence.*



## generated variant — easy (authored workload policy) / q-336499 / method

A nutrient tank for a hydroponic greenhouse can hold up to $620gal$ of solution. Initially, it contains $280gal$ of nutrient solution with $84lb$ of dissolved nutrient. A more concentrated solution with concentration $0.6lb/gal$ flows into the tank at a rate of $30gal/min$, while the completely mixed solution drains out at a rate of $20gal/min$. Rounded to one decimal place, find the amount of nutrient in the tank at the moment it begins to overflow.

> A scientific calculator is required to answer this question.

- $364.3\,\text{lb}$
- $334.1\,\text{lb}$
- $337.7\,\text{lb}$
- $354.9\,\text{lb}$ **supplied key**
- $372.0\,\text{lb}$

Since $Q$ is the amount of nutrient in the tank at time $t,$ the derivative 

$$
\frac{dQ}{dt}
$$

describes how this amount changes with respect to time $t,$ in minutes. This is equal to the rate at which nutrient enters the tank minus the rate at which nutrient leaves the tank.

$$
\frac{dQ}{dt}={Q}_{\text{in}}^{′}-{Q}_{\text{out}}^{′}
$$

Note that the units of $\frac{dQ}{dt},{Q}_{\text{in}}^{′}$ and ${Q}_{\text{out}}^{′}$ are $\text{lb}/\text{min}.$ Now, let's compute the required rates of change in steps.

**Step 1**: Calculating the rate at which nutrient enters the tank.

First, note that a solution containing $0.6\,\text{lb/gal}$ of nutrient enters the tank at a rate of $30\,\text{gal/min}.$ So, the rate at which the *nutrient* enters the tank is 

$$
\begin{aligned}{Q}_{\text{in}}^{′} & =(0.6\,\frac{\text{lb}}{\text{gal}})\cdot (30\,\frac{\text{gal}}{\text{min}}) \\  & =(0.6\,\frac{\text{lb}}{\cancel{\text{gal}}})\cdot (30\,\frac{\cancel{\text{gal}}}{\text{min}}) \\  & =18\,\frac{\text{lb}}{\text{min}}.\end{aligned}
$$

**Step 2**: Calculating the rate at which nutrient exits the tank.

To find the rate at which nutrient leaves the tank, we must first determine the volume of solution in the tank at time $t.$

The tank initially contains $280\,\text{gal}$ of solution; solution enters at $30\,\text{gal/min}$ and mixed solution leaves at $20\,\text{gal/min}.$
As a result, the amount of solution in the tank after $t$ minutes is 

$$
V(t)=280+30t-20t=10(28+t)\,\text{gal}.
$$

Note that $V(t)$ is an increasing function, so the tank is filling.

Since $Q$ is the amount of nutrient in the tank, the concentration of the solution at time $t$ is

$$
\frac{Q}{10(28+t)}\,\text{lb/gal}.
$$

Therefore, as the completely mixed solution leaves at a rate of $20\,\text{gal/min},$ *nutrient* leaves at a rate of

$$
\begin{aligned}{Q}_{\text{out}}^{′} & =(20\,\frac{\text{gal}}{\text{min}})\cdot (\frac{Q}{10(28+t)}\,\frac{\text{lb}}{\text{gal}}) \\  & =(20\,\frac{\cancel{\text{gal}}}{\text{min}})\cdot (\frac{Q}{10(28+t)}\,\frac{\text{lb}}{\cancel{\text{gal}}}) \\  & =\frac{20Q}{10(28+t)}\,\frac{\text{lb}}{\text{min}} \\  & =\frac{2Q}{28+t}\,\frac{\text{lb}}{\text{min}}.\end{aligned}
$$

**Step 3**: Calculate the overall rate of change.

The rate of change equals the rate of entry minus the rate of exit. Therefore, 

$$
\begin{aligned}\frac{dQ}{dt} & ={Q}_{\text{in}}^{′}-{Q}_{\text{out}}^{′} \\  & =18-\frac{2Q}{28+t}\end{aligned}
$$

which gives the equation

$$
\frac{dQ}{dt}+\frac{2}{28+t}\,Q=18.
$$

**Step 4**: Integrate the equation.

This is a first-order linear equation with variable coefficients. So we find the general solution using an integrating factor:

$$
\begin{aligned}I(t) & ={e}^{\int 2/(28+t)\,dt} \\  & ={e}^{2\operatorname{ln}⁡|28+t|} \\  & ={e}^{\operatorname{ln}⁡(28+t)^{2}} \\  & =(28+t)^{2}.\end{aligned}
$$

Multiplying both sides of the differential equation by $I(t)=(28+t)^{2}$ yields

$$
\begin{aligned}(28+t)^{2}\cdot (\frac{dQ}{dt}+\frac{2}{28+t}\,Q) & =(28+t)^{2}\cdot 18 \\ (28+t)^{2}\frac{dQ}{dt}+2(28+t)Q & =18(28+t)^{2} \\ \frac{d}{dt}(Q(28+t)^{2}) & =18(28+t)^{2}.\end{aligned}
$$

Now, we integrate with respect to $t:$

$$
\begin{aligned}\int \frac{d}{dt}(Q(28+t)^{2})\,dt & =\int 18(28+t)^{2}\,dt \\ Q(28+t)^{2} & =18\cdot \frac{1}{3}(28+t)^{3}+C \\ Q(t) & =6(28+t)+\frac{C}{(28+t)^{2}}.\end{aligned}
$$

We're told that the tank initially contains $84\,\text{lb}$ of nutrient. So, we can apply the initial condition $Q(0)=84,$ and solve for $C:$

$$
\begin{aligned}Q(0) & =84 \\ 6(28+0)+\frac{C}{(28+0)^{2}} & =84 \\ 168+\frac{C}{(28)^{2}} & =84 \\ \frac{C}{(28)^{2}} & =-84 \\ C & =-84(28)^{2}.\end{aligned}
$$

Therefore, we obtain the following expression for $Q(t):$

$$
\begin{aligned}Q(t) & =6(28+t)-\frac{84(28)^{2}}{(28+t)^{2}} \\  & =6(28+t)-84{(\frac{28}{28+t})}^{2}.\end{aligned}
$$

Now, let ${t}_{o}$ be the time when the tank begins to overflow. The tank has a capacity of $620\,\text{gal},$ so we can use the condition $V({t}_{o})=620$ to solve for ${t}_{o}:$

$$
\begin{aligned}V({t}_{o}) & =620 \\ 280+30{t}_{o}-20{t}_{o} & =620 \\ 280+10{t}_{o} & =620 \\ 10{t}_{o} & =340 \\ {t}_{o} & =34\,\text{min}.\end{aligned}
$$

Finally, rounded to one decimal place, the amount of nutrient in the tank at the moment it begins to overflow is

$$
\begin{aligned}Q(34) & =6(28+34)-84{(\frac{28}{28+34})}^{2} \\  & =372-84{(\frac{28}{62})}^{2} \\  & ≈354.9\,\text{lb}.\end{aligned}
$$



## source replay — easy (omitted in raw source) / q-336499 / observed:q-336499

A nutrient tank for a hydroponic greenhouse can hold up to $620gal$ of solution. Initially, it contains $280gal$ of nutrient solution with $84lb$ of dissolved nutrient. A more concentrated solution with concentration $0.6lb/gal$ flows into the tank at a rate of $30gal/min$, while the completely mixed solution drains out at a rate of $20gal/min$. Rounded to one decimal place, find the amount of nutrient in the tank at the moment it begins to overflow.

> A scientific calculator is required to answer this question.

- $353.9lb$
- $354.7lb$
- $353.2lb$
- $354.4lb$
- $354.9lb$

*Worked solution absent in raw evidence.*



## source replay — easy (observed) / q-336506 / observed:q-336506

A coolant reservoir in a manufacturing plant can hold up to $210\,\text{gal}$ of liquid. Initially, it contains $70\,\text{gal}$ of coolant solution with $20\,\text{lb}$ of dissolved corrosion inhibitor. A more concentrated coolant solution with concentration $0.5\,\text{lb/gal}$ flows into the reservoir at a rate of $21\,\text{gal/min},$ while the completely mixed solution drains out at a rate of $14\,\text{gal/min}.$ Rounded to one decimal place, find the amount of inhibitor in the reservoir at the moment it begins to overflow.

- $103.7\,\text{lb}$
- $103.3\,\text{lb}$ **supplied key**
- $102.5\,\text{lb}$
- $103.9\,\text{lb}$
- $102.9\,\text{lb}$

Since $Q$ is the amount of inhibitor in the reservoir at time $t,$ the derivative 

$$
\frac{dQ}{dt}
$$

describes how this amount changes with respect to time $t,$ in minutes. This is equal to the rate at which inhibitor enters the reservoir minus the rate at which inhibitor leaves the reservoir.

$$
\frac{dQ}{dt}={Q}_{\text{in}}^{′}-{Q}_{\text{out}}^{′}
$$

Note that the units of $\frac{dQ}{dt},{Q}_{\text{in}}^{′}$ and ${Q}_{\text{out}}^{′}$ are $\text{lb}/\text{min}.$ Now, let's compute the required rates of change in steps.

**Step 1**: Calculating the rate at which inhibitor enters the reservoir.

First, note that a solution containing $0.5\,\text{lb/gal}$ of inhibitor enters the reservoir at a rate of $21\,\text{gal/min}.$ So, the rate at which the *inhibitor* enters the reservoir is 

$$
\begin{aligned}{Q}_{\text{in}}^{′} & =(0.5\,\frac{\text{lb}}{\text{gal}})\cdot (21\,\frac{\text{gal}}{\text{min}}) \\  & =(0.5\,\frac{\text{lb}}{\cancel{\text{gal}}})\cdot (21\,\frac{\cancel{\text{gal}}}{\text{min}}) \\  & =10.5\,\frac{\text{lb}}{\text{min}}.\end{aligned}
$$

**Step 2**: Calculating the rate at which inhibitor exits the reservoir.

To find the rate at which inhibitor leaves the reservoir, we must first determine the volume of solution in the reservoir at time $t.$

The reservoir initially contains $70\,\text{gal}$ of solution; solution enters at $21\,\text{gal/min}$ and mixed solution leaves at $14\,\text{gal/min}.$
As a result, the amount of solution in the reservoir after $t$ minutes is 

$$
V(t)=70+21t-14t=7(10+t)\,\text{gal}.
$$

Note that $V(t)$ is an increasing function, so the reservoir is filling.

Since $Q$ is the amount of inhibitor in the reservoir, the concentration of the solution at time $t$ is

$$
\frac{Q}{7(10+t)}\,\text{lb/gal}.
$$

Therefore, as the completely mixed solution leaves at a rate of $14\,\text{gal/min},$ *inhibitor* leaves at a rate of

$$
\begin{aligned}{Q}_{\text{out}}^{′} & =(14\,\frac{\text{gal}}{\text{min}})\cdot (\frac{Q}{7(10+t)}\,\frac{\text{lb}}{\text{gal}}) \\  & =(14\,\frac{\cancel{\text{gal}}}{\text{min}})\cdot (\frac{Q}{7(10+t)}\,\frac{\text{lb}}{\cancel{\text{gal}}}) \\  & =\frac{14Q}{7(10+t)}\,\frac{\text{lb}}{\text{min}} \\  & =\frac{2Q}{10+t}\,\frac{\text{lb}}{\text{min}}.\end{aligned}
$$

**Step 3**: Calculate the overall rate of change.

The rate of change equals the rate of entry minus the rate of exit. Therefore, 

$$
\begin{aligned}\frac{dQ}{dt} & ={Q}_{\text{in}}^{′}-{Q}_{\text{out}}^{′} \\  & =10.5-\frac{2Q}{10+t}\end{aligned}
$$

which gives the equation

$$
\frac{dQ}{dt}+\frac{2}{10+t}\,Q=10.5.
$$

**Step 4**: Integrate the equation.

This is a first-order linear equation with variable coefficients. So we find the general solution using an integrating factor:

$$
\begin{aligned}I(t) & ={e}^{\int 2/(10+t)\,dt} \\  & ={e}^{2\operatorname{ln}⁡|10+t|} \\  & ={e}^{\operatorname{ln}⁡(10+t)^{2}} \\  & =(10+t)^{2}.\end{aligned}
$$

Multiplying both sides of the differential equation by $I(t)=(10+t)^{2}$ yields

$$
\begin{aligned}(10+t)^{2}\cdot (\frac{dQ}{dt}+\frac{2}{10+t}\,Q) & =(10+t)^{2}\cdot 10.5 \\ (10+t)^{2}\frac{dQ}{dt}+2(10+t)Q & =10.5(10+t)^{2} \\ \frac{d}{dt}(Q(10+t)^{2}) & =10.5(10+t)^{2}.\end{aligned}
$$

Now, we integrate with respect to $t:$

$$
\begin{aligned}\int \frac{d}{dt}(Q(10+t)^{2})\,dt & =\int 10.5(10+t)^{2}\,dt \\ Q(10+t)^{2} & =10.5\cdot \frac{1}{3}(10+t)^{3}+C \\ Q(t) & =3.5(10+t)+\frac{C}{(10+t)^{2}}.\end{aligned}
$$

We're told that the reservoir initially contains $20\,\text{lb}$ of inhibitor. So, we can apply the initial condition $Q(0)=20,$ and solve for $C:$

$$
\begin{aligned}Q(0) & =20 \\ 3.5(10+0)+\frac{C}{(10+0)^{2}} & =20 \\ 35+\frac{C}{(10)^{2}} & =20 \\ \frac{C}{{10}^{2}} & =-15 \\ C & =-15(10)^{2}.\end{aligned}
$$

Therefore, we obtain the following expression for $Q(t):$

$$
\begin{aligned}Q(t) & =3.5(10+t)-\frac{15(10)^{2}}{(10+t)^{2}} \\  & =3.5(10+t)-15{(\frac{10}{10+t})}^{2}.\end{aligned}
$$

Now, let ${t}_{o}$ be the time when the reservoir begins to overflow. The reservoir has a capacity of $210\,\text{gal},$ so we can use the condition $V({t}_{o})=210$ to solve for ${t}_{o}:$

$$
\begin{aligned}V({t}_{o}) & =210 \\ 70+21{t}_{o}-14{t}_{o} & =210 \\ 70+7{t}_{o} & =210 \\ 7{t}_{o} & =140 \\ {t}_{o} & =20\,\text{min}.\end{aligned}
$$

Finally, rounded to one decimal place, the amount of inhibitor in the reservoir at the moment it begins to overflow is

$$
\begin{aligned}Q(20) & =3.5(10+20)-15{(\frac{10}{10+20})}^{2} \\  & =105-15{(\frac{10}{30})}^{2} \\  & ≈103.3\,\text{lb}.\end{aligned}
$$



## generated variant — easy (authored workload policy) / q-336506 / method

A coolant reservoir in a manufacturing plant can hold up to $620\,\text{gal}$ of liquid. Initially, it contains $280\,\text{gal}$ of coolant solution with $84\,\text{lb}$ of dissolved corrosion inhibitor. A more concentrated coolant solution with concentration $0.6\,\text{lb/gal}$ flows into the reservoir at a rate of $30\,\text{gal/min},$ while the completely mixed solution drains out at a rate of $20\,\text{gal/min}.$ Rounded to one decimal place, find the amount of inhibitor in the reservoir at the moment it begins to overflow.

- $364.3\,\text{lb}$
- $334.1\,\text{lb}$
- $337.7\,\text{lb}$
- $354.9\,\text{lb}$ **supplied key**
- $372.0\,\text{lb}$

Since $Q$ is the amount of inhibitor in the reservoir at time $t,$ the derivative 

$$
\frac{dQ}{dt}
$$

describes how this amount changes with respect to time $t,$ in minutes. This is equal to the rate at which inhibitor enters the reservoir minus the rate at which inhibitor leaves the reservoir.

$$
\frac{dQ}{dt}={Q}_{\text{in}}^{′}-{Q}_{\text{out}}^{′}
$$

Note that the units of $\frac{dQ}{dt},{Q}_{\text{in}}^{′}$ and ${Q}_{\text{out}}^{′}$ are $\text{lb}/\text{min}.$ Now, let's compute the required rates of change in steps.

**Step 1**: Calculating the rate at which inhibitor enters the reservoir.

First, note that a solution containing $0.6\,\text{lb/gal}$ of inhibitor enters the reservoir at a rate of $30\,\text{gal/min}.$ So, the rate at which the *inhibitor* enters the reservoir is 

$$
\begin{aligned}{Q}_{\text{in}}^{′} & =(0.6\,\frac{\text{lb}}{\text{gal}})\cdot (30\,\frac{\text{gal}}{\text{min}}) \\  & =(0.6\,\frac{\text{lb}}{\cancel{\text{gal}}})\cdot (30\,\frac{\cancel{\text{gal}}}{\text{min}}) \\  & =18\,\frac{\text{lb}}{\text{min}}.\end{aligned}
$$

**Step 2**: Calculating the rate at which inhibitor exits the reservoir.

To find the rate at which inhibitor leaves the reservoir, we must first determine the volume of solution in the reservoir at time $t.$

The reservoir initially contains $280\,\text{gal}$ of solution; solution enters at $30\,\text{gal/min}$ and mixed solution leaves at $20\,\text{gal/min}.$
As a result, the amount of solution in the reservoir after $t$ minutes is 

$$
V(t)=280+30t-20t=10(28+t)\,\text{gal}.
$$

Note that $V(t)$ is an increasing function, so the reservoir is filling.

Since $Q$ is the amount of inhibitor in the reservoir, the concentration of the solution at time $t$ is

$$
\frac{Q}{10(28+t)}\,\text{lb/gal}.
$$

Therefore, as the completely mixed solution leaves at a rate of $20\,\text{gal/min},$ *inhibitor* leaves at a rate of

$$
\begin{aligned}{Q}_{\text{out}}^{′} & =(20\,\frac{\text{gal}}{\text{min}})\cdot (\frac{Q}{10(28+t)}\,\frac{\text{lb}}{\text{gal}}) \\  & =(20\,\frac{\cancel{\text{gal}}}{\text{min}})\cdot (\frac{Q}{10(28+t)}\,\frac{\text{lb}}{\cancel{\text{gal}}}) \\  & =\frac{20Q}{10(28+t)}\,\frac{\text{lb}}{\text{min}} \\  & =\frac{2Q}{28+t}\,\frac{\text{lb}}{\text{min}}.\end{aligned}
$$

**Step 3**: Calculate the overall rate of change.

The rate of change equals the rate of entry minus the rate of exit. Therefore, 

$$
\begin{aligned}\frac{dQ}{dt} & ={Q}_{\text{in}}^{′}-{Q}_{\text{out}}^{′} \\  & =18-\frac{2Q}{28+t}\end{aligned}
$$

which gives the equation

$$
\frac{dQ}{dt}+\frac{2}{28+t}\,Q=18.
$$

**Step 4**: Integrate the equation.

This is a first-order linear equation with variable coefficients. So we find the general solution using an integrating factor:

$$
\begin{aligned}I(t) & ={e}^{\int 2/(28+t)\,dt} \\  & ={e}^{2\operatorname{ln}⁡|28+t|} \\  & ={e}^{\operatorname{ln}⁡(28+t)^{2}} \\  & =(28+t)^{2}.\end{aligned}
$$

Multiplying both sides of the differential equation by $I(t)=(28+t)^{2}$ yields

$$
\begin{aligned}(28+t)^{2}\cdot (\frac{dQ}{dt}+\frac{2}{28+t}\,Q) & =(28+t)^{2}\cdot 18 \\ (28+t)^{2}\frac{dQ}{dt}+2(28+t)Q & =18(28+t)^{2} \\ \frac{d}{dt}(Q(28+t)^{2}) & =18(28+t)^{2}.\end{aligned}
$$

Now, we integrate with respect to $t:$

$$
\begin{aligned}\int \frac{d}{dt}(Q(28+t)^{2})\,dt & =\int 18(28+t)^{2}\,dt \\ Q(28+t)^{2} & =18\cdot \frac{1}{3}(28+t)^{3}+C \\ Q(t) & =6(28+t)+\frac{C}{(28+t)^{2}}.\end{aligned}
$$

We're told that the reservoir initially contains $84\,\text{lb}$ of inhibitor. So, we can apply the initial condition $Q(0)=84,$ and solve for $C:$

$$
\begin{aligned}Q(0) & =84 \\ 6(28+0)+\frac{C}{(28+0)^{2}} & =84 \\ 168+\frac{C}{(28)^{2}} & =84 \\ \frac{C}{{28}^{2}} & =-84 \\ C & =-84(28)^{2}.\end{aligned}
$$

Therefore, we obtain the following expression for $Q(t):$

$$
\begin{aligned}Q(t) & =6(28+t)-\frac{84(28)^{2}}{(28+t)^{2}} \\  & =6(28+t)-84{(\frac{28}{28+t})}^{2}.\end{aligned}
$$

Now, let ${t}_{o}$ be the time when the reservoir begins to overflow. The reservoir has a capacity of $620\,\text{gal},$ so we can use the condition $V({t}_{o})=620$ to solve for ${t}_{o}:$

$$
\begin{aligned}V({t}_{o}) & =620 \\ 280+30{t}_{o}-20{t}_{o} & =620 \\ 280+10{t}_{o} & =620 \\ 10{t}_{o} & =340 \\ {t}_{o} & =34\,\text{min}.\end{aligned}
$$

Finally, rounded to one decimal place, the amount of inhibitor in the reservoir at the moment it begins to overflow is

$$
\begin{aligned}Q(34) & =6(28+34)-84{(\frac{28}{28+34})}^{2} \\  & =372-84{(\frac{28}{62})}^{2} \\  & ≈354.9\,\text{lb}.\end{aligned}
$$



## source replay — easy (observed) / q-336506 / observed:q-336506

A coolant reservoir in a manufacturing plant can hold up to $620\,\text{gal}$ of liquid. Initially, it contains $280\,\text{gal}$ of coolant solution with $84\,\text{lb}$ of dissolved corrosion inhibitor. A more concentrated coolant solution with concentration $0.6\,\text{lb/gal}$ flows into the reservoir at a rate of $30\,\text{gal/min},$ while the completely mixed solution drains out at a rate of $20\,\text{gal/min}.$ Rounded to one decimal place, find the amount of inhibitor in the reservoir at the moment it begins to overflow.

- $355.5\,\text{lb}$
- $355.3\,\text{lb}$
- $354.5\,\text{lb}$
- $354.9\,\text{lb}$ **supplied key**
- $354.1\,\text{lb}$

Since $Q$ is the amount of inhibitor in the reservoir at time $t,$ the derivative 

$$
\frac{dQ}{dt}
$$

describes how this amount changes with respect to time $t,$ in minutes. This is equal to the rate at which inhibitor enters the reservoir minus the rate at which inhibitor leaves the reservoir.

$$
\frac{dQ}{dt}={Q}_{\text{in}}^{′}-{Q}_{\text{out}}^{′}
$$

Note that the units of $\frac{dQ}{dt},{Q}_{\text{in}}^{′}$ and ${Q}_{\text{out}}^{′}$ are $\text{lb}/\text{min}.$ Now, let's compute the required rates of change in steps.

**Step 1**: Calculating the rate at which inhibitor enters the reservoir.

First, note that a solution containing $0.6\,\text{lb/gal}$ of inhibitor enters the reservoir at a rate of $30\,\text{gal/min}.$ So, the rate at which the *inhibitor* enters the reservoir is 

$$
\begin{aligned}{Q}_{\text{in}}^{′} & =(0.6\,\frac{\text{lb}}{\text{gal}})\cdot (30\,\frac{\text{gal}}{\text{min}}) \\  & =(0.6\,\frac{\text{lb}}{\cancel{\text{gal}}})\cdot (30\,\frac{\cancel{\text{gal}}}{\text{min}}) \\  & =18\,\frac{\text{lb}}{\text{min}}.\end{aligned}
$$

**Step 2**: Calculating the rate at which inhibitor exits the reservoir.

To find the rate at which inhibitor leaves the reservoir, we must first determine the volume of solution in the reservoir at time $t.$

The reservoir initially contains $280\,\text{gal}$ of solution; solution enters at $30\,\text{gal/min}$ and mixed solution leaves at $20\,\text{gal/min}.$
As a result, the amount of solution in the reservoir after $t$ minutes is 

$$
V(t)=280+30t-20t=10(28+t)\,\text{gal}.
$$

Note that $V(t)$ is an increasing function, so the reservoir is filling.

Since $Q$ is the amount of inhibitor in the reservoir, the concentration of the solution at time $t$ is

$$
\frac{Q}{10(28+t)}\,\text{lb/gal}.
$$

Therefore, as the completely mixed solution leaves at a rate of $20\,\text{gal/min},$ *inhibitor* leaves at a rate of

$$
\begin{aligned}{Q}_{\text{out}}^{′} & =(20\,\frac{\text{gal}}{\text{min}})\cdot (\frac{Q}{10(28+t)}\,\frac{\text{lb}}{\text{gal}}) \\  & =(20\,\frac{\cancel{\text{gal}}}{\text{min}})\cdot (\frac{Q}{10(28+t)}\,\frac{\text{lb}}{\cancel{\text{gal}}}) \\  & =\frac{20Q}{10(28+t)}\,\frac{\text{lb}}{\text{min}} \\  & =\frac{2Q}{28+t}\,\frac{\text{lb}}{\text{min}}.\end{aligned}
$$

**Step 3**: Calculate the overall rate of change.

The rate of change equals the rate of entry minus the rate of exit. Therefore, 

$$
\begin{aligned}\frac{dQ}{dt} & ={Q}_{\text{in}}^{′}-{Q}_{\text{out}}^{′} \\  & =18-\frac{2Q}{28+t}\end{aligned}
$$

which gives the equation

$$
\frac{dQ}{dt}+\frac{2}{28+t}\,Q=18.
$$

**Step 4**: Integrate the equation.

This is a first-order linear equation with variable coefficients. So we find the general solution using an integrating factor:

$$
\begin{aligned}I(t) & ={e}^{\int 2/(28+t)\,dt} \\  & ={e}^{2\operatorname{ln}⁡|28+t|} \\  & ={e}^{\operatorname{ln}⁡(28+t)^{2}} \\  & =(28+t)^{2}.\end{aligned}
$$

Multiplying both sides of the differential equation by $I(t)=(28+t)^{2}$ yields

$$
\begin{aligned}(28+t)^{2}\cdot (\frac{dQ}{dt}+\frac{2}{28+t}\,Q) & =(28+t)^{2}\cdot 18 \\ (28+t)^{2}\frac{dQ}{dt}+2(28+t)Q & =18(28+t)^{2} \\ \frac{d}{dt}(Q(28+t)^{2}) & =18(28+t)^{2}.\end{aligned}
$$

Now, we integrate with respect to $t:$

$$
\begin{aligned}\int \frac{d}{dt}(Q(28+t)^{2})\,dt & =\int 18(28+t)^{2}\,dt \\ Q(28+t)^{2} & =18\cdot \frac{1}{3}(28+t)^{3}+C \\ Q(t) & =6(28+t)+\frac{C}{(28+t)^{2}}.\end{aligned}
$$

We're told that the reservoir initially contains $84\,\text{lb}$ of inhibitor. So, we can apply the initial condition $Q(0)=84,$ and solve for $C:$

$$
\begin{aligned}Q(0) & =84 \\ 6(28+0)+\frac{C}{(28+0)^{2}} & =84 \\ 168+\frac{C}{(28)^{2}} & =84 \\ \frac{C}{{28}^{2}} & =-84 \\ C & =-84(28)^{2}.\end{aligned}
$$

Therefore, we obtain the following expression for $Q(t):$

$$
\begin{aligned}Q(t) & =6(28+t)-\frac{84(28)^{2}}{(28+t)^{2}} \\  & =6(28+t)-84{(\frac{28}{28+t})}^{2}.\end{aligned}
$$

Now, let ${t}_{o}$ be the time when the reservoir begins to overflow. The reservoir has a capacity of $620\,\text{gal},$ so we can use the condition $V({t}_{o})=620$ to solve for ${t}_{o}:$

$$
\begin{aligned}V({t}_{o}) & =620 \\ 280+30{t}_{o}-20{t}_{o} & =620 \\ 280+10{t}_{o} & =620 \\ 10{t}_{o} & =340 \\ {t}_{o} & =34\,\text{min}.\end{aligned}
$$

Finally, rounded to one decimal place, the amount of inhibitor in the reservoir at the moment it begins to overflow is

$$
\begin{aligned}Q(34) & =6(28+34)-84{(\frac{28}{28+34})}^{2} \\  & =372-84{(\frac{28}{62})}^{2} \\  & ≈354.9\,\text{lb}.\end{aligned}
$$



## source replay — easy (observed) / q-336513 / observed:q-336513

A flavoring tank at a beverage factory can hold up to $150\,\text{gal}$ of liquid. Initially, it contains $75\,\text{gal}$ of flavoring solution with $25\,\text{lb}$ of dissolved flavoring. A more concentrated solution with concentration $\frac{2}{3}\,\text{lb/gal}$ flows into the tank at a rate of $9\,\text{gal/min},$ while the completely mixed solution drains out at a rate of $6\,\text{gal/min}.$ Rounded to one decimal place, find the amount of flavoring in the tank at the moment it begins to overflow.

- $93.8\,\text{lb}$ **supplied key**
- $92.9\,\text{lb}$
- $93.3\,\text{lb}$
- $94.1\,\text{lb}$
- $94.5\,\text{lb}$

Since $Q$ is the amount of flavoring in the tank at time $t,$ the derivative 

$$
\frac{dQ}{dt}
$$

describes how this amount changes with respect to time $t,$ in minutes. This is equal to the rate at which flavoring enters the tank minus the rate at which flavoring leaves the tank.

$$
\frac{dQ}{dt}={Q}_{\text{in}}^{′}-{Q}_{\text{out}}^{′}
$$

Note that the units of $\frac{dQ}{dt},{Q}_{\text{in}}^{′}$ and ${Q}_{\text{out}}^{′}$ are $\text{lb}/\text{min}.$ Now, let's compute the required rates of change in steps.

**Step 1**: Calculating the rate at which flavoring enters the tank.

First, note that a solution containing $\frac{2}{3}\,\text{lb/gal}$ of flavoring enters the tank at a rate of $9\,\text{gal/min}.$ So, the rate at which the *flavoring* enters the tank is 

$$
\begin{aligned}{Q}_{\text{in}}^{′} & =(\frac{2}{3}\,\frac{\text{lb}}{\text{gal}})\cdot (9\,\frac{\text{gal}}{\text{min}}) \\  & =(\frac{2}{3}\,\frac{\text{lb}}{\cancel{\text{gal}}})\cdot (9\,\frac{\cancel{\text{gal}}}{\text{min}}) \\  & =6\,\frac{\text{lb}}{\text{min}}.\end{aligned}
$$

**Step 2**: Calculating the rate at which flavoring exits the tank.

To find the rate at which flavoring leaves the tank, we must first determine the volume of solution in the tank at time $t.$

The tank initially contains $75\,\text{gal}$ of solution; solution enters at $9\,\text{gal/min}$ and mixed solution leaves at $6\,\text{gal/min}.$
As a result, the amount of solution in the tank after $t$ minutes is 

$$
V(t)=75+9t-6t=3(25+t)\,\text{gal}.
$$

Note that $V(t)$ is an increasing function, so the tank is filling.

Since $Q$ is the amount of flavoring in the tank, the concentration of the solution at time $t$ is

$$
\frac{Q}{3(25+t)}\,\text{lb/gal}.
$$

Therefore, as the completely mixed solution leaves at a rate of $6\,\text{gal/min},$ *flavoring* leaves at a rate of

$$
\begin{aligned}{Q}_{\text{out}}^{′} & =(6\,\frac{\text{gal}}{\text{min}})\cdot (\frac{Q}{3(25+t)}\,\frac{\text{lb}}{\text{gal}}) \\  & =(6\,\frac{\cancel{\text{gal}}}{\text{min}})\cdot (\frac{Q}{3(25+t)}\,\frac{\text{lb}}{\cancel{\text{gal}}}) \\  & =\frac{6Q}{3(25+t)}\,\frac{\text{lb}}{\text{min}} \\  & =\frac{2Q}{25+t}\,\frac{\text{lb}}{\text{min}}.\end{aligned}
$$

**Step 3**: Calculate the overall rate of change.

The rate of change equals the rate of entry minus the rate of exit. Therefore, 

$$
\begin{aligned}\frac{dQ}{dt} & ={Q}_{\text{in}}^{′}-{Q}_{\text{out}}^{′} \\  & =6-\frac{2Q}{25+t}\end{aligned}
$$

which gives the equation

$$
\frac{dQ}{dt}+\frac{2}{25+t}\,Q=6.
$$

**Step 4**: Integrate the equation.

This is a first-order linear equation with variable coefficients. So we find the general solution using an integrating factor:

$$
\begin{aligned}I(t) & ={e}^{\int 2/(25+t)\,dt} \\  & ={e}^{2\operatorname{ln}⁡|25+t|} \\  & ={e}^{\operatorname{ln}⁡(25+t)^{2}} \\  & =(25+t)^{2}.\end{aligned}
$$

Multiplying both sides of the differential equation by $I(t)=(25+t)^{2}$ yields

$$
\begin{aligned}(25+t)^{2}\cdot (\frac{dQ}{dt}+\frac{2}{25+t}\,Q) & =(25+t)^{2}\cdot 6 \\ (25+t)^{2}\frac{dQ}{dt}+2(25+t)Q & =6(25+t)^{2} \\ \frac{d}{dt}(Q(25+t)^{2}) & =6(25+t)^{2}.\end{aligned}
$$

Now, we integrate with respect to $t:$

$$
\begin{aligned}\int \frac{d}{dt}(Q(25+t)^{2})\,dt & =\int 6(25+t)^{2}\,dt \\ Q(25+t)^{2} & =6\cdot \frac{1}{3}(25+t)^{3}+C \\ Q(t) & =2(25+t)+\frac{C}{(25+t)^{2}}.\end{aligned}
$$

We're told that the tank initially contains $25\,\text{lb}$ of flavoring. So, we can apply the initial condition $Q(0)=25,$ and solve for $C:$

$$
\begin{aligned}Q(0) & =25 \\ 2(25+0)+\frac{C}{(25+0)^{2}} & =25 \\ 50+\frac{C}{(25)^{2}} & =25 \\ \frac{C}{{25}^{2}} & =-25 \\ C & =-25(25)^{2}.\end{aligned}
$$

Therefore, we obtain the following expression for $Q(t):$

$$
\begin{aligned}Q(t) & =2(25+t)-\frac{25(25)^{2}}{(25+t)^{2}} \\  & =2(25+t)-25{(\frac{25}{25+t})}^{2}.\end{aligned}
$$

Now, let ${t}_{o}$ be the time when the tank begins to overflow. The tank has a capacity of $150\,\text{gal},$ so we can use the condition $V({t}_{o})=150$ to solve for ${t}_{o}:$

$$
\begin{aligned}V({t}_{o}) & =150 \\ 75+9{t}_{o}-6{t}_{o} & =150 \\ 75+3{t}_{o} & =150 \\ 3{t}_{o} & =75 \\ {t}_{o} & =25\,\text{min}.\end{aligned}
$$

Finally, rounded to one decimal place, the amount of flavoring in the tank at the moment it begins to overflow is

$$
\begin{aligned}Q(25) & =2(25+25)-25{(\frac{25}{25+25})}^{2} \\  & =100-25{(\frac{25}{50})}^{2} \\  & ≈93.8\,\text{lb}.\end{aligned}
$$



## generated variant — easy (authored workload policy) / q-336513 / method

A flavoring tank at a beverage factory can hold up to $620\,\text{gal}$ of liquid. Initially, it contains $280\,\text{gal}$ of flavoring solution with $84\,\text{lb}$ of dissolved flavoring. A more concentrated solution with concentration $0.6\,\text{lb/gal}$ flows into the tank at a rate of $30\,\text{gal/min},$ while the completely mixed solution drains out at a rate of $20\,\text{gal/min}.$ Rounded to one decimal place, find the amount of flavoring in the tank at the moment it begins to overflow.

- $364.3\,\text{lb}$
- $334.1\,\text{lb}$
- $337.7\,\text{lb}$
- $354.9\,\text{lb}$ **supplied key**
- $372.0\,\text{lb}$

Since $Q$ is the amount of flavoring in the tank at time $t,$ the derivative 

$$
\frac{dQ}{dt}
$$

describes how this amount changes with respect to time $t,$ in minutes. This is equal to the rate at which flavoring enters the tank minus the rate at which flavoring leaves the tank.

$$
\frac{dQ}{dt}={Q}_{\text{in}}^{′}-{Q}_{\text{out}}^{′}
$$

Note that the units of $\frac{dQ}{dt},{Q}_{\text{in}}^{′}$ and ${Q}_{\text{out}}^{′}$ are $\text{lb}/\text{min}.$ Now, let's compute the required rates of change in steps.

**Step 1**: Calculating the rate at which flavoring enters the tank.

First, note that a solution containing $0.6\,\text{lb/gal}$ of flavoring enters the tank at a rate of $30\,\text{gal/min}.$ So, the rate at which the *flavoring* enters the tank is 

$$
\begin{aligned}{Q}_{\text{in}}^{′} & =(0.6\,\frac{\text{lb}}{\text{gal}})\cdot (30\,\frac{\text{gal}}{\text{min}}) \\  & =(0.6\,\frac{\text{lb}}{\cancel{\text{gal}}})\cdot (30\,\frac{\cancel{\text{gal}}}{\text{min}}) \\  & =18\,\frac{\text{lb}}{\text{min}}.\end{aligned}
$$

**Step 2**: Calculating the rate at which flavoring exits the tank.

To find the rate at which flavoring leaves the tank, we must first determine the volume of solution in the tank at time $t.$

The tank initially contains $280\,\text{gal}$ of solution; solution enters at $30\,\text{gal/min}$ and mixed solution leaves at $20\,\text{gal/min}.$
As a result, the amount of solution in the tank after $t$ minutes is 

$$
V(t)=280+30t-20t=10(28+t)\,\text{gal}.
$$

Note that $V(t)$ is an increasing function, so the tank is filling.

Since $Q$ is the amount of flavoring in the tank, the concentration of the solution at time $t$ is

$$
\frac{Q}{10(28+t)}\,\text{lb/gal}.
$$

Therefore, as the completely mixed solution leaves at a rate of $20\,\text{gal/min},$ *flavoring* leaves at a rate of

$$
\begin{aligned}{Q}_{\text{out}}^{′} & =(20\,\frac{\text{gal}}{\text{min}})\cdot (\frac{Q}{10(28+t)}\,\frac{\text{lb}}{\text{gal}}) \\  & =(20\,\frac{\cancel{\text{gal}}}{\text{min}})\cdot (\frac{Q}{10(28+t)}\,\frac{\text{lb}}{\cancel{\text{gal}}}) \\  & =\frac{20Q}{10(28+t)}\,\frac{\text{lb}}{\text{min}} \\  & =\frac{2Q}{28+t}\,\frac{\text{lb}}{\text{min}}.\end{aligned}
$$

**Step 3**: Calculate the overall rate of change.

The rate of change equals the rate of entry minus the rate of exit. Therefore, 

$$
\begin{aligned}\frac{dQ}{dt} & ={Q}_{\text{in}}^{′}-{Q}_{\text{out}}^{′} \\  & =18-\frac{2Q}{28+t}\end{aligned}
$$

which gives the equation

$$
\frac{dQ}{dt}+\frac{2}{28+t}\,Q=18.
$$

**Step 4**: Integrate the equation.

This is a first-order linear equation with variable coefficients. So we find the general solution using an integrating factor:

$$
\begin{aligned}I(t) & ={e}^{\int 2/(28+t)\,dt} \\  & ={e}^{2\operatorname{ln}⁡|28+t|} \\  & ={e}^{\operatorname{ln}⁡(28+t)^{2}} \\  & =(28+t)^{2}.\end{aligned}
$$

Multiplying both sides of the differential equation by $I(t)=(28+t)^{2}$ yields

$$
\begin{aligned}(28+t)^{2}\cdot (\frac{dQ}{dt}+\frac{2}{28+t}\,Q) & =(28+t)^{2}\cdot 18 \\ (28+t)^{2}\frac{dQ}{dt}+2(28+t)Q & =18(28+t)^{2} \\ \frac{d}{dt}(Q(28+t)^{2}) & =18(28+t)^{2}.\end{aligned}
$$

Now, we integrate with respect to $t:$

$$
\begin{aligned}\int \frac{d}{dt}(Q(28+t)^{2})\,dt & =\int 18(28+t)^{2}\,dt \\ Q(28+t)^{2} & =18\cdot \frac{1}{3}(28+t)^{3}+C \\ Q(t) & =6(28+t)+\frac{C}{(28+t)^{2}}.\end{aligned}
$$

We're told that the tank initially contains $84\,\text{lb}$ of flavoring. So, we can apply the initial condition $Q(0)=84,$ and solve for $C:$

$$
\begin{aligned}Q(0) & =84 \\ 6(28+0)+\frac{C}{(28+0)^{2}} & =84 \\ 168+\frac{C}{(28)^{2}} & =84 \\ \frac{C}{{28}^{2}} & =-84 \\ C & =-84(28)^{2}.\end{aligned}
$$

Therefore, we obtain the following expression for $Q(t):$

$$
\begin{aligned}Q(t) & =6(28+t)-\frac{84(28)^{2}}{(28+t)^{2}} \\  & =6(28+t)-84{(\frac{28}{28+t})}^{2}.\end{aligned}
$$

Now, let ${t}_{o}$ be the time when the tank begins to overflow. The tank has a capacity of $620\,\text{gal},$ so we can use the condition $V({t}_{o})=620$ to solve for ${t}_{o}:$

$$
\begin{aligned}V({t}_{o}) & =620 \\ 280+30{t}_{o}-20{t}_{o} & =620 \\ 280+10{t}_{o} & =620 \\ 10{t}_{o} & =340 \\ {t}_{o} & =34\,\text{min}.\end{aligned}
$$

Finally, rounded to one decimal place, the amount of flavoring in the tank at the moment it begins to overflow is

$$
\begin{aligned}Q(34) & =6(28+34)-84{(\frac{28}{28+34})}^{2} \\  & =372-84{(\frac{28}{62})}^{2} \\  & ≈354.9\,\text{lb}.\end{aligned}
$$



## source replay — easy (observed) / q-336513 / observed:q-336513

A flavoring tank at a beverage factory can hold up to $620\,\text{gal}$ of liquid. Initially, it contains $280\,\text{gal}$ of flavoring solution with $84\,\text{lb}$ of dissolved flavoring. A more concentrated solution with concentration $0.6\,\text{lb/gal}$ flows into the tank at a rate of $30\,\text{gal/min},$ while the completely mixed solution drains out at a rate of $20\,\text{gal/min}.$ Rounded to one decimal place, find the amount of flavoring in the tank at the moment it begins to overflow.

- $355.2\,\text{lb}$
- $354.9\,\text{lb}$ **supplied key**
- $355.6\,\text{lb}$
- $354.0\,\text{lb}$
- $354.4\,\text{lb}$

Since $Q$ is the amount of flavoring in the tank at time $t,$ the derivative 

$$
\frac{dQ}{dt}
$$

describes how this amount changes with respect to time $t,$ in minutes. This is equal to the rate at which flavoring enters the tank minus the rate at which flavoring leaves the tank.

$$
\frac{dQ}{dt}={Q}_{\text{in}}^{′}-{Q}_{\text{out}}^{′}
$$

Note that the units of $\frac{dQ}{dt},{Q}_{\text{in}}^{′}$ and ${Q}_{\text{out}}^{′}$ are $\text{lb}/\text{min}.$ Now, let's compute the required rates of change in steps.

**Step 1**: Calculating the rate at which flavoring enters the tank.

First, note that a solution containing $0.6\,\text{lb/gal}$ of flavoring enters the tank at a rate of $30\,\text{gal/min}.$ So, the rate at which the *flavoring* enters the tank is 

$$
\begin{aligned}{Q}_{\text{in}}^{′} & =(0.6\,\frac{\text{lb}}{\text{gal}})\cdot (30\,\frac{\text{gal}}{\text{min}}) \\  & =(0.6\,\frac{\text{lb}}{\cancel{\text{gal}}})\cdot (30\,\frac{\cancel{\text{gal}}}{\text{min}}) \\  & =18\,\frac{\text{lb}}{\text{min}}.\end{aligned}
$$

**Step 2**: Calculating the rate at which flavoring exits the tank.

To find the rate at which flavoring leaves the tank, we must first determine the volume of solution in the tank at time $t.$

The tank initially contains $280\,\text{gal}$ of solution; solution enters at $30\,\text{gal/min}$ and mixed solution leaves at $20\,\text{gal/min}.$
As a result, the amount of solution in the tank after $t$ minutes is 

$$
V(t)=280+30t-20t=10(28+t)\,\text{gal}.
$$

Note that $V(t)$ is an increasing function, so the tank is filling.

Since $Q$ is the amount of flavoring in the tank, the concentration of the solution at time $t$ is

$$
\frac{Q}{10(28+t)}\,\text{lb/gal}.
$$

Therefore, as the completely mixed solution leaves at a rate of $20\,\text{gal/min},$ *flavoring* leaves at a rate of

$$
\begin{aligned}{Q}_{\text{out}}^{′} & =(20\,\frac{\text{gal}}{\text{min}})\cdot (\frac{Q}{10(28+t)}\,\frac{\text{lb}}{\text{gal}}) \\  & =(20\,\frac{\cancel{\text{gal}}}{\text{min}})\cdot (\frac{Q}{10(28+t)}\,\frac{\text{lb}}{\cancel{\text{gal}}}) \\  & =\frac{20Q}{10(28+t)}\,\frac{\text{lb}}{\text{min}} \\  & =\frac{2Q}{28+t}\,\frac{\text{lb}}{\text{min}}.\end{aligned}
$$

**Step 3**: Calculate the overall rate of change.

The rate of change equals the rate of entry minus the rate of exit. Therefore, 

$$
\begin{aligned}\frac{dQ}{dt} & ={Q}_{\text{in}}^{′}-{Q}_{\text{out}}^{′} \\  & =18-\frac{2Q}{28+t}\end{aligned}
$$

which gives the equation

$$
\frac{dQ}{dt}+\frac{2}{28+t}\,Q=18.
$$

**Step 4**: Integrate the equation.

This is a first-order linear equation with variable coefficients. So we find the general solution using an integrating factor:

$$
\begin{aligned}I(t) & ={e}^{\int 2/(28+t)\,dt} \\  & ={e}^{2\operatorname{ln}⁡|28+t|} \\  & ={e}^{\operatorname{ln}⁡(28+t)^{2}} \\  & =(28+t)^{2}.\end{aligned}
$$

Multiplying both sides of the differential equation by $I(t)=(28+t)^{2}$ yields

$$
\begin{aligned}(28+t)^{2}\cdot (\frac{dQ}{dt}+\frac{2}{28+t}\,Q) & =(28+t)^{2}\cdot 18 \\ (28+t)^{2}\frac{dQ}{dt}+2(28+t)Q & =18(28+t)^{2} \\ \frac{d}{dt}(Q(28+t)^{2}) & =18(28+t)^{2}.\end{aligned}
$$

Now, we integrate with respect to $t:$

$$
\begin{aligned}\int \frac{d}{dt}(Q(28+t)^{2})\,dt & =\int 18(28+t)^{2}\,dt \\ Q(28+t)^{2} & =18\cdot \frac{1}{3}(28+t)^{3}+C \\ Q(t) & =6(28+t)+\frac{C}{(28+t)^{2}}.\end{aligned}
$$

We're told that the tank initially contains $84\,\text{lb}$ of flavoring. So, we can apply the initial condition $Q(0)=84,$ and solve for $C:$

$$
\begin{aligned}Q(0) & =84 \\ 6(28+0)+\frac{C}{(28+0)^{2}} & =84 \\ 168+\frac{C}{(28)^{2}} & =84 \\ \frac{C}{{28}^{2}} & =-84 \\ C & =-84(28)^{2}.\end{aligned}
$$

Therefore, we obtain the following expression for $Q(t):$

$$
\begin{aligned}Q(t) & =6(28+t)-\frac{84(28)^{2}}{(28+t)^{2}} \\  & =6(28+t)-84{(\frac{28}{28+t})}^{2}.\end{aligned}
$$

Now, let ${t}_{o}$ be the time when the tank begins to overflow. The tank has a capacity of $620\,\text{gal},$ so we can use the condition $V({t}_{o})=620$ to solve for ${t}_{o}:$

$$
\begin{aligned}V({t}_{o}) & =620 \\ 280+30{t}_{o}-20{t}_{o} & =620 \\ 280+10{t}_{o} & =620 \\ 10{t}_{o} & =340 \\ {t}_{o} & =34\,\text{min}.\end{aligned}
$$

Finally, rounded to one decimal place, the amount of flavoring in the tank at the moment it begins to overflow is

$$
\begin{aligned}Q(34) & =6(28+34)-84{(\frac{28}{28+34})}^{2} \\  & =372-84{(\frac{28}{62})}^{2} \\  & ≈354.9\,\text{lb}.\end{aligned}
$$



## source replay — easy (observed) / q-336516 / observed:q-336516

A disinfectant reservoir in a water treatment facility can hold up to $200\,\text{gal}$ of liquid. Initially, it contains $50\,\text{gal}$ of disinfectant solution with $10\,\text{lb}$ of dissolved disinfectant. A more concentrated solution with concentration $0.8\,\text{lb/gal}$ flows into the reservoir at a rate of $15\,\text{gal/min},$ while the completely mixed solution drains out at a rate of $10\,\text{gal/min}.$ Rounded to one decimal place, find the amount of disinfectant in the reservoir at the moment it begins to overflow.

- $158.1\,\text{lb}$ **supplied key**
- $157.2\,\text{lb}$
- $158.5\,\text{lb}$
- $159.0\,\text{lb}$
- $157.6\,\text{lb}$

Since $Q$ is the amount of disinfectant in the reservoir at time $t,$ the derivative 

$$
\frac{dQ}{dt}
$$

describes how this amount changes with respect to time $t,$ in minutes. This is equal to the rate at which disinfectant enters the reservoir minus the rate at which disinfectant leaves the reservoir.

$$
\frac{dQ}{dt}={Q}_{\text{in}}^{′}-{Q}_{\text{out}}^{′}
$$

Note that the units of $\frac{dQ}{dt},{Q}_{\text{in}}^{′}$ and ${Q}_{\text{out}}^{′}$ are $\text{lb}/\text{min}.$ Now, let's compute the required rates of change in steps.

**Step 1**: Calculating the rate at which disinfectant enters the reservoir.

First, note that a solution containing $0.8\,\text{lb/gal}$ of disinfectant enters the reservoir at a rate of $15\,\text{gal/min}.$ So, the rate at which the *disinfectant* enters the reservoir is 

$$
\begin{aligned}{Q}_{\text{in}}^{′} & =(0.8\,\frac{\text{lb}}{\text{gal}})\cdot (15\,\frac{\text{gal}}{\text{min}}) \\  & =(0.8\,\frac{\text{lb}}{\cancel{\text{gal}}})\cdot (15\,\frac{\cancel{\text{gal}}}{\text{min}}) \\  & =12\,\frac{\text{lb}}{\text{min}}.\end{aligned}
$$

**Step 2**: Calculating the rate at which disinfectant exits the reservoir.

To find the rate at which disinfectant leaves the reservoir, we must first determine the volume of solution in the reservoir at time $t.$

The reservoir initially contains $50\,\text{gal}$ of solution; solution enters at $15\,\text{gal/min}$ and mixed solution leaves at $10\,\text{gal/min}.$
As a result, the amount of solution in the reservoir after $t$ minutes is 

$$
V(t)=50+15t-10t=5(10+t)\,\text{gal}.
$$

Note that $V(t)$ is an increasing function, so the reservoir is filling.

Since $Q$ is the amount of disinfectant in the reservoir, the concentration of the solution at time $t$ is

$$
\frac{Q}{5(10+t)}\,\text{lb/gal}.
$$

Therefore, as the completely mixed solution leaves at a rate of $10\,\text{gal/min},$ *disinfectant* leaves at a rate of

$$
\begin{aligned}{Q}_{\text{out}}^{′} & =(10\,\frac{\text{gal}}{\text{min}})\cdot (\frac{Q}{5(10+t)}\,\frac{\text{lb}}{\text{gal}}) \\  & =(10\,\frac{\cancel{\text{gal}}}{\text{min}})\cdot (\frac{Q}{5(10+t)}\,\frac{\text{lb}}{\cancel{\text{gal}}}) \\  & =\frac{10Q}{5(10+t)}\,\frac{\text{lb}}{\text{min}} \\  & =\frac{2Q}{10+t}\,\frac{\text{lb}}{\text{min}}.\end{aligned}
$$

**Step 3**: Calculate the overall rate of change.

The rate of change equals the rate of entry minus the rate of exit. Therefore, 

$$
\begin{aligned}\frac{dQ}{dt} & ={Q}_{\text{in}}^{′}-{Q}_{\text{out}}^{′} \\  & =12-\frac{2Q}{10+t}\end{aligned}
$$

which gives the equation

$$
\frac{dQ}{dt}+\frac{2}{10+t}\,Q=12.
$$

**Step 4**: Integrate the equation.

This is a first-order linear equation with variable coefficients. So we find the general solution using an integrating factor:

$$
\begin{aligned}I(t) & ={e}^{\int 2/(10+t)\,dt} \\  & ={e}^{2\operatorname{ln}⁡|10+t|} \\  & ={e}^{\operatorname{ln}⁡(10+t)^{2}} \\  & =(10+t)^{2}.\end{aligned}
$$

Multiplying both sides of the differential equation by $I(t)=(10+t)^{2}$ yields

$$
\begin{aligned}(10+t)^{2}\cdot (\frac{dQ}{dt}+\frac{2}{10+t}\,Q) & =(10+t)^{2}\cdot 12 \\ (10+t)^{2}\frac{dQ}{dt}+2(10+t)Q & =12(10+t)^{2} \\ \frac{d}{dt}(Q(10+t)^{2}) & =12(10+t)^{2}.\end{aligned}
$$

Now, we integrate with respect to $t:$

$$
\begin{aligned}\int \frac{d}{dt}(Q(10+t)^{2})\,dt & =\int 12(10+t)^{2}\,dt \\ Q(10+t)^{2} & =12\cdot \frac{1}{3}(10+t)^{3}+C \\ Q(t) & =4(10+t)+\frac{C}{(10+t)^{2}}.\end{aligned}
$$

We're told that the reservoir initially contains $10\,\text{lb}$ of disinfectant. So, we can apply the initial condition $Q(0)=10,$ and solve for $C:$

$$
\begin{aligned}Q(0) & =10 \\ 4(10+0)+\frac{C}{(10+0)^{2}} & =10 \\ 40+\frac{C}{(10)^{2}} & =10 \\ \frac{C}{{10}^{2}} & =-30 \\ C & =-30(10)^{2}.\end{aligned}
$$

Therefore, we obtain the following expression for $Q(t):$

$$
\begin{aligned}Q(t) & =4(10+t)-\frac{30(10)^{2}}{(10+t)^{2}} \\  & =4(10+t)-30{(\frac{10}{10+t})}^{2}.\end{aligned}
$$

Now, let ${t}_{o}$ be the time when the reservoir begins to overflow. The reservoir has a capacity of $200\,\text{gal},$ so we can use the condition $V({t}_{o})=200$ to solve for ${t}_{o}:$

$$
\begin{aligned}V({t}_{o}) & =200 \\ 50+15{t}_{o}-10{t}_{o} & =200 \\ 50+5{t}_{o} & =200 \\ 5{t}_{o} & =150 \\ {t}_{o} & =30\,\text{min}.\end{aligned}
$$

Finally, rounded to one decimal place, the amount of disinfectant in the reservoir at the moment it begins to overflow is

$$
\begin{aligned}Q(30) & =4(10+30)-30{(\frac{10}{10+30})}^{2} \\  & =160-30{(\frac{10}{40})}^{2} \\  & ≈158.1\,\text{lb}.\end{aligned}
$$



## generated variant — easy (authored workload policy) / q-336516 / method

A disinfectant reservoir in a water treatment facility can hold up to $620\,\text{gal}$ of liquid. Initially, it contains $280\,\text{gal}$ of disinfectant solution with $84\,\text{lb}$ of dissolved disinfectant. A more concentrated solution with concentration $0.6\,\text{lb/gal}$ flows into the reservoir at a rate of $30\,\text{gal/min},$ while the completely mixed solution drains out at a rate of $20\,\text{gal/min}.$ Rounded to one decimal place, find the amount of disinfectant in the reservoir at the moment it begins to overflow.

- $364.3\,\text{lb}$
- $334.1\,\text{lb}$
- $337.7\,\text{lb}$
- $354.9\,\text{lb}$ **supplied key**
- $372.0\,\text{lb}$

Since $Q$ is the amount of disinfectant in the reservoir at time $t,$ the derivative 

$$
\frac{dQ}{dt}
$$

describes how this amount changes with respect to time $t,$ in minutes. This is equal to the rate at which disinfectant enters the reservoir minus the rate at which disinfectant leaves the reservoir.

$$
\frac{dQ}{dt}={Q}_{\text{in}}^{′}-{Q}_{\text{out}}^{′}
$$

Note that the units of $\frac{dQ}{dt},{Q}_{\text{in}}^{′}$ and ${Q}_{\text{out}}^{′}$ are $\text{lb}/\text{min}.$ Now, let's compute the required rates of change in steps.

**Step 1**: Calculating the rate at which disinfectant enters the reservoir.

First, note that a solution containing $0.6\,\text{lb/gal}$ of disinfectant enters the reservoir at a rate of $30\,\text{gal/min}.$ So, the rate at which the *disinfectant* enters the reservoir is 

$$
\begin{aligned}{Q}_{\text{in}}^{′} & =(0.6\,\frac{\text{lb}}{\text{gal}})\cdot (30\,\frac{\text{gal}}{\text{min}}) \\  & =(0.6\,\frac{\text{lb}}{\cancel{\text{gal}}})\cdot (30\,\frac{\cancel{\text{gal}}}{\text{min}}) \\  & =18\,\frac{\text{lb}}{\text{min}}.\end{aligned}
$$

**Step 2**: Calculating the rate at which disinfectant exits the reservoir.

To find the rate at which disinfectant leaves the reservoir, we must first determine the volume of solution in the reservoir at time $t.$

The reservoir initially contains $280\,\text{gal}$ of solution; solution enters at $30\,\text{gal/min}$ and mixed solution leaves at $20\,\text{gal/min}.$
As a result, the amount of solution in the reservoir after $t$ minutes is 

$$
V(t)=280+30t-20t=10(28+t)\,\text{gal}.
$$

Note that $V(t)$ is an increasing function, so the reservoir is filling.

Since $Q$ is the amount of disinfectant in the reservoir, the concentration of the solution at time $t$ is

$$
\frac{Q}{10(28+t)}\,\text{lb/gal}.
$$

Therefore, as the completely mixed solution leaves at a rate of $20\,\text{gal/min},$ *disinfectant* leaves at a rate of

$$
\begin{aligned}{Q}_{\text{out}}^{′} & =(20\,\frac{\text{gal}}{\text{min}})\cdot (\frac{Q}{10(28+t)}\,\frac{\text{lb}}{\text{gal}}) \\  & =(20\,\frac{\cancel{\text{gal}}}{\text{min}})\cdot (\frac{Q}{10(28+t)}\,\frac{\text{lb}}{\cancel{\text{gal}}}) \\  & =\frac{20Q}{10(28+t)}\,\frac{\text{lb}}{\text{min}} \\  & =\frac{2Q}{28+t}\,\frac{\text{lb}}{\text{min}}.\end{aligned}
$$

**Step 3**: Calculate the overall rate of change.

The rate of change equals the rate of entry minus the rate of exit. Therefore, 

$$
\begin{aligned}\frac{dQ}{dt} & ={Q}_{\text{in}}^{′}-{Q}_{\text{out}}^{′} \\  & =18-\frac{2Q}{28+t}\end{aligned}
$$

which gives the equation

$$
\frac{dQ}{dt}+\frac{2}{28+t}\,Q=18.
$$

**Step 4**: Integrate the equation.

This is a first-order linear equation with variable coefficients. So we find the general solution using an integrating factor:

$$
\begin{aligned}I(t) & ={e}^{\int 2/(28+t)\,dt} \\  & ={e}^{2\operatorname{ln}⁡|28+t|} \\  & ={e}^{\operatorname{ln}⁡(28+t)^{2}} \\  & =(28+t)^{2}.\end{aligned}
$$

Multiplying both sides of the differential equation by $I(t)=(28+t)^{2}$ yields

$$
\begin{aligned}(28+t)^{2}\cdot (\frac{dQ}{dt}+\frac{2}{28+t}\,Q) & =(28+t)^{2}\cdot 18 \\ (28+t)^{2}\frac{dQ}{dt}+2(28+t)Q & =18(28+t)^{2} \\ \frac{d}{dt}(Q(28+t)^{2}) & =18(28+t)^{2}.\end{aligned}
$$

Now, we integrate with respect to $t:$

$$
\begin{aligned}\int \frac{d}{dt}(Q(28+t)^{2})\,dt & =\int 18(28+t)^{2}\,dt \\ Q(28+t)^{2} & =18\cdot \frac{1}{3}(28+t)^{3}+C \\ Q(t) & =6(28+t)+\frac{C}{(28+t)^{2}}.\end{aligned}
$$

We're told that the reservoir initially contains $84\,\text{lb}$ of disinfectant. So, we can apply the initial condition $Q(0)=84,$ and solve for $C:$

$$
\begin{aligned}Q(0) & =84 \\ 6(28+0)+\frac{C}{(28+0)^{2}} & =84 \\ 168+\frac{C}{(28)^{2}} & =84 \\ \frac{C}{{28}^{2}} & =-84 \\ C & =-84(28)^{2}.\end{aligned}
$$

Therefore, we obtain the following expression for $Q(t):$

$$
\begin{aligned}Q(t) & =6(28+t)-\frac{84(28)^{2}}{(28+t)^{2}} \\  & =6(28+t)-84{(\frac{28}{28+t})}^{2}.\end{aligned}
$$

Now, let ${t}_{o}$ be the time when the reservoir begins to overflow. The reservoir has a capacity of $620\,\text{gal},$ so we can use the condition $V({t}_{o})=620$ to solve for ${t}_{o}:$

$$
\begin{aligned}V({t}_{o}) & =620 \\ 280+30{t}_{o}-20{t}_{o} & =620 \\ 280+10{t}_{o} & =620 \\ 10{t}_{o} & =340 \\ {t}_{o} & =34\,\text{min}.\end{aligned}
$$

Finally, rounded to one decimal place, the amount of disinfectant in the reservoir at the moment it begins to overflow is

$$
\begin{aligned}Q(34) & =6(28+34)-84{(\frac{28}{28+34})}^{2} \\  & =372-84{(\frac{28}{62})}^{2} \\  & ≈354.9\,\text{lb}.\end{aligned}
$$



## source replay — easy (observed) / q-336516 / observed:q-336516

A disinfectant reservoir in a water treatment facility can hold up to $620\,\text{gal}$ of liquid. Initially, it contains $280\,\text{gal}$ of disinfectant solution with $84\,\text{lb}$ of dissolved disinfectant. A more concentrated solution with concentration $0.6\,\text{lb/gal}$ flows into the reservoir at a rate of $30\,\text{gal/min},$ while the completely mixed solution drains out at a rate of $20\,\text{gal/min}.$ Rounded to one decimal place, find the amount of disinfectant in the reservoir at the moment it begins to overflow.

- $355.8\,\text{lb}$
- $354.9\,\text{lb}$ **supplied key**
- $354.4\,\text{lb}$
- $354.0\,\text{lb}$
- $355.3\,\text{lb}$

Since $Q$ is the amount of disinfectant in the reservoir at time $t,$ the derivative 

$$
\frac{dQ}{dt}
$$

describes how this amount changes with respect to time $t,$ in minutes. This is equal to the rate at which disinfectant enters the reservoir minus the rate at which disinfectant leaves the reservoir.

$$
\frac{dQ}{dt}={Q}_{\text{in}}^{′}-{Q}_{\text{out}}^{′}
$$

Note that the units of $\frac{dQ}{dt},{Q}_{\text{in}}^{′}$ and ${Q}_{\text{out}}^{′}$ are $\text{lb}/\text{min}.$ Now, let's compute the required rates of change in steps.

**Step 1**: Calculating the rate at which disinfectant enters the reservoir.

First, note that a solution containing $0.6\,\text{lb/gal}$ of disinfectant enters the reservoir at a rate of $30\,\text{gal/min}.$ So, the rate at which the *disinfectant* enters the reservoir is 

$$
\begin{aligned}{Q}_{\text{in}}^{′} & =(0.6\,\frac{\text{lb}}{\text{gal}})\cdot (30\,\frac{\text{gal}}{\text{min}}) \\  & =(0.6\,\frac{\text{lb}}{\cancel{\text{gal}}})\cdot (30\,\frac{\cancel{\text{gal}}}{\text{min}}) \\  & =18\,\frac{\text{lb}}{\text{min}}.\end{aligned}
$$

**Step 2**: Calculating the rate at which disinfectant exits the reservoir.

To find the rate at which disinfectant leaves the reservoir, we must first determine the volume of solution in the reservoir at time $t.$

The reservoir initially contains $280\,\text{gal}$ of solution; solution enters at $30\,\text{gal/min}$ and mixed solution leaves at $20\,\text{gal/min}.$
As a result, the amount of solution in the reservoir after $t$ minutes is 

$$
V(t)=280+30t-20t=10(28+t)\,\text{gal}.
$$

Note that $V(t)$ is an increasing function, so the reservoir is filling.

Since $Q$ is the amount of disinfectant in the reservoir, the concentration of the solution at time $t$ is

$$
\frac{Q}{10(28+t)}\,\text{lb/gal}.
$$

Therefore, as the completely mixed solution leaves at a rate of $20\,\text{gal/min},$ *disinfectant* leaves at a rate of

$$
\begin{aligned}{Q}_{\text{out}}^{′} & =(20\,\frac{\text{gal}}{\text{min}})\cdot (\frac{Q}{10(28+t)}\,\frac{\text{lb}}{\text{gal}}) \\  & =(20\,\frac{\cancel{\text{gal}}}{\text{min}})\cdot (\frac{Q}{10(28+t)}\,\frac{\text{lb}}{\cancel{\text{gal}}}) \\  & =\frac{20Q}{10(28+t)}\,\frac{\text{lb}}{\text{min}} \\  & =\frac{2Q}{28+t}\,\frac{\text{lb}}{\text{min}}.\end{aligned}
$$

**Step 3**: Calculate the overall rate of change.

The rate of change equals the rate of entry minus the rate of exit. Therefore, 

$$
\begin{aligned}\frac{dQ}{dt} & ={Q}_{\text{in}}^{′}-{Q}_{\text{out}}^{′} \\  & =18-\frac{2Q}{28+t}\end{aligned}
$$

which gives the equation

$$
\frac{dQ}{dt}+\frac{2}{28+t}\,Q=18.
$$

**Step 4**: Integrate the equation.

This is a first-order linear equation with variable coefficients. So we find the general solution using an integrating factor:

$$
\begin{aligned}I(t) & ={e}^{\int 2/(28+t)\,dt} \\  & ={e}^{2\operatorname{ln}⁡|28+t|} \\  & ={e}^{\operatorname{ln}⁡(28+t)^{2}} \\  & =(28+t)^{2}.\end{aligned}
$$

Multiplying both sides of the differential equation by $I(t)=(28+t)^{2}$ yields

$$
\begin{aligned}(28+t)^{2}\cdot (\frac{dQ}{dt}+\frac{2}{28+t}\,Q) & =(28+t)^{2}\cdot 18 \\ (28+t)^{2}\frac{dQ}{dt}+2(28+t)Q & =18(28+t)^{2} \\ \frac{d}{dt}(Q(28+t)^{2}) & =18(28+t)^{2}.\end{aligned}
$$

Now, we integrate with respect to $t:$

$$
\begin{aligned}\int \frac{d}{dt}(Q(28+t)^{2})\,dt & =\int 18(28+t)^{2}\,dt \\ Q(28+t)^{2} & =18\cdot \frac{1}{3}(28+t)^{3}+C \\ Q(t) & =6(28+t)+\frac{C}{(28+t)^{2}}.\end{aligned}
$$

We're told that the reservoir initially contains $84\,\text{lb}$ of disinfectant. So, we can apply the initial condition $Q(0)=84,$ and solve for $C:$

$$
\begin{aligned}Q(0) & =84 \\ 6(28+0)+\frac{C}{(28+0)^{2}} & =84 \\ 168+\frac{C}{(28)^{2}} & =84 \\ \frac{C}{{28}^{2}} & =-84 \\ C & =-84(28)^{2}.\end{aligned}
$$

Therefore, we obtain the following expression for $Q(t):$

$$
\begin{aligned}Q(t) & =6(28+t)-\frac{84(28)^{2}}{(28+t)^{2}} \\  & =6(28+t)-84{(\frac{28}{28+t})}^{2}.\end{aligned}
$$

Now, let ${t}_{o}$ be the time when the reservoir begins to overflow. The reservoir has a capacity of $620\,\text{gal},$ so we can use the condition $V({t}_{o})=620$ to solve for ${t}_{o}:$

$$
\begin{aligned}V({t}_{o}) & =620 \\ 280+30{t}_{o}-20{t}_{o} & =620 \\ 280+10{t}_{o} & =620 \\ 10{t}_{o} & =340 \\ {t}_{o} & =34\,\text{min}.\end{aligned}
$$

Finally, rounded to one decimal place, the amount of disinfectant in the reservoir at the moment it begins to overflow is

$$
\begin{aligned}Q(34) & =6(28+34)-84{(\frac{28}{28+34})}^{2} \\  & =372-84{(\frac{28}{62})}^{2} \\  & ≈354.9\,\text{lb}.\end{aligned}
$$



## source replay — easy (observed) / q-336501 / observed:q-336501

A dye mixing tank at a textile factory can hold up to $180\,\text{gal}$ of liquid. Initially, it contains $100\,\text{gal}$ of solution with $20\,\text{lb}$ of dissolved dye. A more concentrated dye solution with concentration $0.6\,\text{lb/gal}$ flows into the tank at a rate of $15\,\text{gal/min},$ while the completely mixed solution drains out at a rate of $10\,\text{gal/min}.$ Rounded to one decimal place, find the amount of dye in the tank at the moment it begins to overflow.

- $95.7\,\text{lb}$ **supplied key**
- $96.1\,\text{lb}$
- $95.2\,\text{lb}$
- $94.9\,\text{lb}$
- $96.4\,\text{lb}$

Since $Q$ is the amount of dye in the tank at time $t,$ the derivative 

$$
\frac{dQ}{dt}
$$

describes how this amount changes with respect to time $t,$ in minutes. This is equal to the rate at which dye enters the tank minus the rate at which dye leaves the tank.

$$
\frac{dQ}{dt}={Q}_{\text{in}}^{′}-{Q}_{\text{out}}^{′}
$$

Note that the units of $\frac{dQ}{dt},{Q}_{\text{in}}^{′}$ and ${Q}_{\text{out}}^{′}$ are $\text{lb}/\text{min}.$ Now, let's compute the required rates of change in steps.

**Step 1**: Calculating the rate at which dye enters the tank.

First, note that a solution containing $0.6\,\text{lb/gal}$ of dye enters the tank at a rate of $15\,\text{gal/min}.$ So, the rate at which the *dye* enters the tank is 

$$
\begin{aligned}{Q}_{\text{in}}^{′} & =(0.6\,\frac{\text{lb}}{\text{gal}})\cdot (15\,\frac{\text{gal}}{\text{min}}) \\  & =(0.6\,\frac{\text{lb}}{\cancel{\text{gal}}})\cdot (15\,\frac{\cancel{\text{gal}}}{\text{min}}) \\  & =9\,\frac{\text{lb}}{\text{min}}.\end{aligned}
$$

**Step 2**: Calculating the rate at which dye exits the tank.

To find the rate at which dye leaves the tank, we must first determine the volume of liquid in the tank at time $t.$

The tank initially contains $100\,\text{gal}$ of liquid; solution enters at $15\,\text{gal/min}$ and mixed solution leaves at $10\,\text{gal/min}.$
As a result, the amount of liquid in the tank after $t$ minutes is 

$$
V(t)=100+15t-10t=5(20+t)\,\text{gal}.
$$

Note that $V(t)$ is an increasing function, so the tank is filling.

Since $Q$ is the amount of dye in the tank, the concentration of the solution at time $t$ is

$$
\frac{Q}{5(20+t)}\,\text{lb/gal}.
$$

Therefore, as the completely mixed solution leaves at a rate of $10\,\text{gal/min},$ *dye* leaves at a rate of

$$
\begin{aligned}{Q}_{\text{out}}^{′} & =(10\,\frac{\text{gal}}{\text{min}})\cdot (\frac{Q}{5(20+t)}\,\frac{\text{lb}}{\text{gal}}) \\  & =(10\,\frac{\cancel{\text{gal}}}{\text{min}})\cdot (\frac{Q}{5(20+t)}\,\frac{\text{lb}}{\cancel{\text{gal}}}) \\  & =\frac{10Q}{5(20+t)}\,\frac{\text{lb}}{\text{min}} \\  & =\frac{2Q}{20+t}\,\frac{\text{lb}}{\text{min}}.\end{aligned}
$$

**Step 3**: Calculate the overall rate of change.

The rate of change equals the rate of entry minus the rate of exit. Therefore, 

$$
\begin{aligned}\frac{dQ}{dt} & ={Q}_{\text{in}}^{′}-{Q}_{\text{out}}^{′} \\  & =9-\frac{2Q}{20+t}\end{aligned}
$$

which gives the equation

$$
\frac{dQ}{dt}+\frac{2}{20+t}\,Q=9.
$$

**Step 4**: Integrate the equation.

This is a first-order linear equation with variable coefficients. So we find the general solution using an integrating factor:

$$
\begin{aligned}I(t) & ={e}^{\int 2/(20+t)\,dt} \\  & ={e}^{2\operatorname{ln}⁡|20+t|} \\  & ={e}^{\operatorname{ln}⁡(20+t)^{2}} \\  & =(20+t)^{2}.\end{aligned}
$$

Multiplying both sides of the differential equation by $I(t)=(20+t)^{2}$ yields

$$
\begin{aligned}(20+t)^{2}\cdot (\frac{dQ}{dt}+\frac{2}{20+t}\,Q) & =(20+t)^{2}\cdot 9 \\ (20+t)^{2}\frac{dQ}{dt}+2(20+t)Q & =9(20+t)^{2} \\ \frac{d}{dt}(Q(20+t)^{2}) & =9(20+t)^{2}.\end{aligned}
$$

Now, we integrate with respect to $t:$

$$
\begin{aligned}\int \frac{d}{dt}(Q(20+t)^{2})\,dt & =\int 9(20+t)^{2}\,dt \\ Q(20+t)^{2} & =9\cdot \frac{1}{3}(20+t)^{3}+C \\ Q(t) & =3(20+t)+\frac{C}{(20+t)^{2}}.\end{aligned}
$$

We're told that the tank initially contains $20\,\text{lb}$ of dye. So, we can apply the initial condition $Q(0)=20,$ and solve for $C:$

$$
\begin{aligned}Q(0) & =20 \\ 3(20+0)+\frac{C}{(20+0)^{2}} & =20 \\ 60+\frac{C}{(20)^{2}} & =20 \\ \frac{C}{(20)^{2}} & =-40 \\ C & =-40(20)^{2}.\end{aligned}
$$

Therefore, we obtain the following expression for $Q(t):$

$$
\begin{aligned}Q(t) & =3(20+t)-\frac{40(20)^{2}}{(20+t)^{2}} \\  & =3(20+t)-40{(\frac{20}{20+t})}^{2}.\end{aligned}
$$

Now, let ${t}_{o}$ be the time when the tank begins to overflow. The tank has a capacity of $180\,\text{gal},$ so we can use the condition $V({t}_{o})=180$ to solve for ${t}_{o}:$

$$
\begin{aligned}V({t}_{o}) & =180 \\ 100+15{t}_{o}-10{t}_{o} & =180 \\ 100+5{t}_{o} & =180 \\ 5{t}_{o} & =80 \\ {t}_{o} & =16\,\text{min}.\end{aligned}
$$

Finally, rounded to one decimal place, the amount of dye in the tank at the moment it begins to overflow is

$$
\begin{aligned}Q(16) & =3(20+16)-40{(\frac{20}{20+16})}^{2} \\  & =108-40{(\frac{20}{36})}^{2} \\  & ≈95.7\,\text{lb}.\end{aligned}
$$



## generated variant — easy (authored workload policy) / q-336501 / method

A dye mixing tank at a textile factory can hold up to $620\,\text{gal}$ of liquid. Initially, it contains $280\,\text{gal}$ of solution with $84\,\text{lb}$ of dissolved dye. A more concentrated dye solution with concentration $0.6\,\text{lb/gal}$ flows into the tank at a rate of $30\,\text{gal/min},$ while the completely mixed solution drains out at a rate of $20\,\text{gal/min}.$ Rounded to one decimal place, find the amount of dye in the tank at the moment it begins to overflow.

- $364.3\,\text{lb}$
- $334.1\,\text{lb}$
- $337.7\,\text{lb}$
- $354.9\,\text{lb}$ **supplied key**
- $372.0\,\text{lb}$

Since $Q$ is the amount of dye in the tank at time $t,$ the derivative 

$$
\frac{dQ}{dt}
$$

describes how this amount changes with respect to time $t,$ in minutes. This is equal to the rate at which dye enters the tank minus the rate at which dye leaves the tank.

$$
\frac{dQ}{dt}={Q}_{\text{in}}^{′}-{Q}_{\text{out}}^{′}
$$

Note that the units of $\frac{dQ}{dt},{Q}_{\text{in}}^{′}$ and ${Q}_{\text{out}}^{′}$ are $\text{lb}/\text{min}.$ Now, let's compute the required rates of change in steps.

**Step 1**: Calculating the rate at which dye enters the tank.

First, note that a solution containing $0.6\,\text{lb/gal}$ of dye enters the tank at a rate of $30\,\text{gal/min}.$ So, the rate at which the *dye* enters the tank is 

$$
\begin{aligned}{Q}_{\text{in}}^{′} & =(0.6\,\frac{\text{lb}}{\text{gal}})\cdot (30\,\frac{\text{gal}}{\text{min}}) \\  & =(0.6\,\frac{\text{lb}}{\cancel{\text{gal}}})\cdot (30\,\frac{\cancel{\text{gal}}}{\text{min}}) \\  & =18\,\frac{\text{lb}}{\text{min}}.\end{aligned}
$$

**Step 2**: Calculating the rate at which dye exits the tank.

To find the rate at which dye leaves the tank, we must first determine the volume of liquid in the tank at time $t.$

The tank initially contains $280\,\text{gal}$ of liquid; solution enters at $30\,\text{gal/min}$ and mixed solution leaves at $20\,\text{gal/min}.$
As a result, the amount of liquid in the tank after $t$ minutes is 

$$
V(t)=280+30t-20t=10(28+t)\,\text{gal}.
$$

Note that $V(t)$ is an increasing function, so the tank is filling.

Since $Q$ is the amount of dye in the tank, the concentration of the solution at time $t$ is

$$
\frac{Q}{10(28+t)}\,\text{lb/gal}.
$$

Therefore, as the completely mixed solution leaves at a rate of $20\,\text{gal/min},$ *dye* leaves at a rate of

$$
\begin{aligned}{Q}_{\text{out}}^{′} & =(20\,\frac{\text{gal}}{\text{min}})\cdot (\frac{Q}{10(28+t)}\,\frac{\text{lb}}{\text{gal}}) \\  & =(20\,\frac{\cancel{\text{gal}}}{\text{min}})\cdot (\frac{Q}{10(28+t)}\,\frac{\text{lb}}{\cancel{\text{gal}}}) \\  & =\frac{20Q}{10(28+t)}\,\frac{\text{lb}}{\text{min}} \\  & =\frac{2Q}{28+t}\,\frac{\text{lb}}{\text{min}}.\end{aligned}
$$

**Step 3**: Calculate the overall rate of change.

The rate of change equals the rate of entry minus the rate of exit. Therefore, 

$$
\begin{aligned}\frac{dQ}{dt} & ={Q}_{\text{in}}^{′}-{Q}_{\text{out}}^{′} \\  & =18-\frac{2Q}{28+t}\end{aligned}
$$

which gives the equation

$$
\frac{dQ}{dt}+\frac{2}{28+t}\,Q=18.
$$

**Step 4**: Integrate the equation.

This is a first-order linear equation with variable coefficients. So we find the general solution using an integrating factor:

$$
\begin{aligned}I(t) & ={e}^{\int 2/(28+t)\,dt} \\  & ={e}^{2\operatorname{ln}⁡|28+t|} \\  & ={e}^{\operatorname{ln}⁡(28+t)^{2}} \\  & =(28+t)^{2}.\end{aligned}
$$

Multiplying both sides of the differential equation by $I(t)=(28+t)^{2}$ yields

$$
\begin{aligned}(28+t)^{2}\cdot (\frac{dQ}{dt}+\frac{2}{28+t}\,Q) & =(28+t)^{2}\cdot 18 \\ (28+t)^{2}\frac{dQ}{dt}+2(28+t)Q & =18(28+t)^{2} \\ \frac{d}{dt}(Q(28+t)^{2}) & =18(28+t)^{2}.\end{aligned}
$$

Now, we integrate with respect to $t:$

$$
\begin{aligned}\int \frac{d}{dt}(Q(28+t)^{2})\,dt & =\int 18(28+t)^{2}\,dt \\ Q(28+t)^{2} & =18\cdot \frac{1}{3}(28+t)^{3}+C \\ Q(t) & =6(28+t)+\frac{C}{(28+t)^{2}}.\end{aligned}
$$

We're told that the tank initially contains $84\,\text{lb}$ of dye. So, we can apply the initial condition $Q(0)=84,$ and solve for $C:$

$$
\begin{aligned}Q(0) & =84 \\ 6(28+0)+\frac{C}{(28+0)^{2}} & =84 \\ 168+\frac{C}{(28)^{2}} & =84 \\ \frac{C}{(28)^{2}} & =-84 \\ C & =-84(28)^{2}.\end{aligned}
$$

Therefore, we obtain the following expression for $Q(t):$

$$
\begin{aligned}Q(t) & =6(28+t)-\frac{84(28)^{2}}{(28+t)^{2}} \\  & =6(28+t)-84{(\frac{28}{28+t})}^{2}.\end{aligned}
$$

Now, let ${t}_{o}$ be the time when the tank begins to overflow. The tank has a capacity of $620\,\text{gal},$ so we can use the condition $V({t}_{o})=620$ to solve for ${t}_{o}:$

$$
\begin{aligned}V({t}_{o}) & =620 \\ 280+30{t}_{o}-20{t}_{o} & =620 \\ 280+10{t}_{o} & =620 \\ 10{t}_{o} & =340 \\ {t}_{o} & =34\,\text{min}.\end{aligned}
$$

Finally, rounded to one decimal place, the amount of dye in the tank at the moment it begins to overflow is

$$
\begin{aligned}Q(34) & =6(28+34)-84{(\frac{28}{28+34})}^{2} \\  & =372-84{(\frac{28}{62})}^{2} \\  & ≈354.9\,\text{lb}.\end{aligned}
$$



## source replay — easy (observed) / q-336501 / observed:q-336501

A dye mixing tank at a textile factory can hold up to $620\,\text{gal}$ of liquid. Initially, it contains $280\,\text{gal}$ of solution with $84\,\text{lb}$ of dissolved dye. A more concentrated dye solution with concentration $0.6\,\text{lb/gal}$ flows into the tank at a rate of $30\,\text{gal/min},$ while the completely mixed solution drains out at a rate of $20\,\text{gal/min}.$ Rounded to one decimal place, find the amount of dye in the tank at the moment it begins to overflow.

- $354.1\,\text{lb}$
- $354.9\,\text{lb}$ **supplied key**
- $355.6\,\text{lb}$
- $355.3\,\text{lb}$
- $354.4\,\text{lb}$

Since $Q$ is the amount of dye in the tank at time $t,$ the derivative 

$$
\frac{dQ}{dt}
$$

describes how this amount changes with respect to time $t,$ in minutes. This is equal to the rate at which dye enters the tank minus the rate at which dye leaves the tank.

$$
\frac{dQ}{dt}={Q}_{\text{in}}^{′}-{Q}_{\text{out}}^{′}
$$

Note that the units of $\frac{dQ}{dt},{Q}_{\text{in}}^{′}$ and ${Q}_{\text{out}}^{′}$ are $\text{lb}/\text{min}.$ Now, let's compute the required rates of change in steps.

**Step 1**: Calculating the rate at which dye enters the tank.

First, note that a solution containing $0.6\,\text{lb/gal}$ of dye enters the tank at a rate of $30\,\text{gal/min}.$ So, the rate at which the *dye* enters the tank is 

$$
\begin{aligned}{Q}_{\text{in}}^{′} & =(0.6\,\frac{\text{lb}}{\text{gal}})\cdot (30\,\frac{\text{gal}}{\text{min}}) \\  & =(0.6\,\frac{\text{lb}}{\cancel{\text{gal}}})\cdot (30\,\frac{\cancel{\text{gal}}}{\text{min}}) \\  & =18\,\frac{\text{lb}}{\text{min}}.\end{aligned}
$$

**Step 2**: Calculating the rate at which dye exits the tank.

To find the rate at which dye leaves the tank, we must first determine the volume of liquid in the tank at time $t.$

The tank initially contains $280\,\text{gal}$ of liquid; solution enters at $30\,\text{gal/min}$ and mixed solution leaves at $20\,\text{gal/min}.$
As a result, the amount of liquid in the tank after $t$ minutes is 

$$
V(t)=280+30t-20t=10(28+t)\,\text{gal}.
$$

Note that $V(t)$ is an increasing function, so the tank is filling.

Since $Q$ is the amount of dye in the tank, the concentration of the solution at time $t$ is

$$
\frac{Q}{10(28+t)}\,\text{lb/gal}.
$$

Therefore, as the completely mixed solution leaves at a rate of $20\,\text{gal/min},$ *dye* leaves at a rate of

$$
\begin{aligned}{Q}_{\text{out}}^{′} & =(20\,\frac{\text{gal}}{\text{min}})\cdot (\frac{Q}{10(28+t)}\,\frac{\text{lb}}{\text{gal}}) \\  & =(20\,\frac{\cancel{\text{gal}}}{\text{min}})\cdot (\frac{Q}{10(28+t)}\,\frac{\text{lb}}{\cancel{\text{gal}}}) \\  & =\frac{20Q}{10(28+t)}\,\frac{\text{lb}}{\text{min}} \\  & =\frac{2Q}{28+t}\,\frac{\text{lb}}{\text{min}}.\end{aligned}
$$

**Step 3**: Calculate the overall rate of change.

The rate of change equals the rate of entry minus the rate of exit. Therefore, 

$$
\begin{aligned}\frac{dQ}{dt} & ={Q}_{\text{in}}^{′}-{Q}_{\text{out}}^{′} \\  & =18-\frac{2Q}{28+t}\end{aligned}
$$

which gives the equation

$$
\frac{dQ}{dt}+\frac{2}{28+t}\,Q=18.
$$

**Step 4**: Integrate the equation.

This is a first-order linear equation with variable coefficients. So we find the general solution using an integrating factor:

$$
\begin{aligned}I(t) & ={e}^{\int 2/(28+t)\,dt} \\  & ={e}^{2\operatorname{ln}⁡|28+t|} \\  & ={e}^{\operatorname{ln}⁡(28+t)^{2}} \\  & =(28+t)^{2}.\end{aligned}
$$

Multiplying both sides of the differential equation by $I(t)=(28+t)^{2}$ yields

$$
\begin{aligned}(28+t)^{2}\cdot (\frac{dQ}{dt}+\frac{2}{28+t}\,Q) & =(28+t)^{2}\cdot 18 \\ (28+t)^{2}\frac{dQ}{dt}+2(28+t)Q & =18(28+t)^{2} \\ \frac{d}{dt}(Q(28+t)^{2}) & =18(28+t)^{2}.\end{aligned}
$$

Now, we integrate with respect to $t:$

$$
\begin{aligned}\int \frac{d}{dt}(Q(28+t)^{2})\,dt & =\int 18(28+t)^{2}\,dt \\ Q(28+t)^{2} & =18\cdot \frac{1}{3}(28+t)^{3}+C \\ Q(t) & =6(28+t)+\frac{C}{(28+t)^{2}}.\end{aligned}
$$

We're told that the tank initially contains $84\,\text{lb}$ of dye. So, we can apply the initial condition $Q(0)=84,$ and solve for $C:$

$$
\begin{aligned}Q(0) & =84 \\ 6(28+0)+\frac{C}{(28+0)^{2}} & =84 \\ 168+\frac{C}{(28)^{2}} & =84 \\ \frac{C}{(28)^{2}} & =-84 \\ C & =-84(28)^{2}.\end{aligned}
$$

Therefore, we obtain the following expression for $Q(t):$

$$
\begin{aligned}Q(t) & =6(28+t)-\frac{84(28)^{2}}{(28+t)^{2}} \\  & =6(28+t)-84{(\frac{28}{28+t})}^{2}.\end{aligned}
$$

Now, let ${t}_{o}$ be the time when the tank begins to overflow. The tank has a capacity of $620\,\text{gal},$ so we can use the condition $V({t}_{o})=620$ to solve for ${t}_{o}:$

$$
\begin{aligned}V({t}_{o}) & =620 \\ 280+30{t}_{o}-20{t}_{o} & =620 \\ 280+10{t}_{o} & =620 \\ 10{t}_{o} & =340 \\ {t}_{o} & =34\,\text{min}.\end{aligned}
$$

Finally, rounded to one decimal place, the amount of dye in the tank at the moment it begins to overflow is

$$
\begin{aligned}Q(34) & =6(28+34)-84{(\frac{28}{28+34})}^{2} \\  & =372-84{(\frac{28}{62})}^{2} \\  & ≈354.9\,\text{lb}.\end{aligned}
$$



## source replay — easy (observed) / q-336502 / observed:q-336502

A saline reservoir for a medical research lab can hold up to $160\,\text{gal}$ of solution. Initially, it contains $100\,\text{gal}$ of saline solution with $25\,\text{lb}$ of dissolved salt. A more concentrated saline solution with concentration $1.0\,\text{lb/gal}$ flows into the reservoir at a rate of $6\,\text{gal/min},$ while the completely mixed solution drains out at a rate of $4\,\text{gal/min}.$ Rounded to one decimal place, find the amount of salt in the reservoir at the moment it begins to overflow.

- $129.9\,\text{lb}$
- $130.2\,\text{lb}$
- $130.7\,\text{lb}$ **supplied key**
- $131.0\,\text{lb}$
- $131.4\,\text{lb}$

Since $Q$ is the amount of salt in the reservoir at time $t,$ the derivative 

$$
\frac{dQ}{dt}
$$

describes how this amount changes with respect to time $t,$ in minutes. This is equal to the rate at which salt enters the reservoir minus the rate at which salt leaves the reservoir.

$$
\frac{dQ}{dt}={Q}_{\text{in}}^{′}-{Q}_{\text{out}}^{′}
$$

Note that the units of $\frac{dQ}{dt},{Q}_{\text{in}}^{′}$ and ${Q}_{\text{out}}^{′}$ are $\text{lb}/\text{min}.$ Now, let's compute the required rates of change in steps.

**Step 1**: Calculating the rate at which salt enters the reservoir.

First, note that a solution containing $1.0\,\text{lb/gal}$ of salt enters the reservoir at a rate of $6\,\text{gal/min}.$ So, the rate at which the *salt* enters the reservoir is 

$$
\begin{aligned}{Q}_{\text{in}}^{′} & =(1.0\,\frac{\text{lb}}{\text{gal}})\cdot (6\,\frac{\text{gal}}{\text{min}}) \\  & =(1.0\,\frac{\text{lb}}{\cancel{\text{gal}}})\cdot (6\,\frac{\cancel{\text{gal}}}{\text{min}}) \\  & =6\,\frac{\text{lb}}{\text{min}}.\end{aligned}
$$

**Step 2**: Calculating the rate at which salt exits the reservoir.

To find the rate at which salt leaves the reservoir, we must first determine the volume of solution in the reservoir at time $t.$

The reservoir initially contains $100\,\text{gal}$ of solution; solution enters at $6\,\text{gal/min}$ and mixed solution leaves at $4\,\text{gal/min}.$
As a result, the amount of solution in the reservoir after $t$ minutes is 

$$
V(t)=100+6t-4t=2(50+t)\,\text{gal}.
$$

Note that $V(t)$ is an increasing function, so the reservoir is filling.

Since $Q$ is the amount of salt in the reservoir, the concentration of the solution at time $t$ is

$$
\frac{Q}{2(50+t)}\,\text{lb/gal}.
$$

Therefore, as the completely mixed solution leaves at a rate of $4\,\text{gal/min},$ *salt* leaves at a rate of

$$
\begin{aligned}{Q}_{\text{out}}^{′} & =(4\,\frac{\text{gal}}{\text{min}})\cdot (\frac{Q}{2(50+t)}\,\frac{\text{lb}}{\text{gal}}) \\  & =(4\,\frac{\cancel{\text{gal}}}{\text{min}})\cdot (\frac{Q}{2(50+t)}\,\frac{\text{lb}}{\cancel{\text{gal}}}) \\  & =\frac{4Q}{2(50+t)}\,\frac{\text{lb}}{\text{min}} \\  & =\frac{2Q}{50+t}\,\frac{\text{lb}}{\text{min}}.\end{aligned}
$$

**Step 3**: Calculate the overall rate of change.

The rate of change equals the rate of entry minus the rate of exit. Therefore, 

$$
\begin{aligned}\frac{dQ}{dt} & ={Q}_{\text{in}}^{′}-{Q}_{\text{out}}^{′} \\  & =6-\frac{2Q}{50+t}\end{aligned}
$$

which gives the equation

$$
\frac{dQ}{dt}+\frac{2}{50+t}\,Q=6.
$$

**Step 4**: Integrate the equation.

This is a first-order linear equation with variable coefficients. So we find the general solution using an integrating factor:

$$
\begin{aligned}I(t) & ={e}^{\int 2/(50+t)\,dt} \\  & ={e}^{2\operatorname{ln}⁡|50+t|} \\  & ={e}^{\operatorname{ln}⁡(50+t)^{2}} \\  & =(50+t)^{2}.\end{aligned}
$$

Multiplying both sides of the differential equation by $I(t)=(50+t)^{2}$ yields

$$
\begin{aligned}(50+t)^{2}\cdot (\frac{dQ}{dt}+\frac{2}{50+t}\,Q) & =(50+t)^{2}\cdot 6 \\ (50+t)^{2}\frac{dQ}{dt}+2(50+t)Q & =6(50+t)^{2} \\ \frac{d}{dt}(Q(50+t)^{2}) & =6(50+t)^{2}.\end{aligned}
$$

Now, we integrate with respect to $t:$

$$
\begin{aligned}\int \frac{d}{dt}(Q(50+t)^{2})\,dt & =\int 6(50+t)^{2}\,dt \\ Q(50+t)^{2} & =6\cdot \frac{1}{3}(50+t)^{3}+C \\ Q(t) & =2(50+t)+\frac{C}{(50+t)^{2}}.\end{aligned}
$$

We're told that the reservoir initially contains $25\,\text{lb}$ of salt. So, we can apply the initial condition $Q(0)=25,$ and solve for $C:$

$$
\begin{aligned}Q(0) & =25 \\ 2(50+0)+\frac{C}{(50+0)^{2}} & =25 \\ 100+\frac{C}{(50)^{2}} & =25 \\ \frac{C}{(50)^{2}} & =-75 \\ C & =-75(50)^{2}.\end{aligned}
$$

Therefore, we obtain the following expression for $Q(t):$

$$
\begin{aligned}Q(t) & =2(50+t)-\frac{75(50)^{2}}{(50+t)^{2}} \\  & =2(50+t)-75{(\frac{50}{50+t})}^{2}.\end{aligned}
$$

Now, let ${t}_{o}$ be the time when the reservoir begins to overflow. The reservoir has a capacity of $160\,\text{gal},$ so we can use the condition $V({t}_{o})=160$ to solve for ${t}_{o}:$

$$
\begin{aligned}V({t}_{o}) & =160 \\ 100+6{t}_{o}-4{t}_{o} & =160 \\ 100+2{t}_{o} & =160 \\ 2{t}_{o} & =60 \\ {t}_{o} & =30\,\text{min}.\end{aligned}
$$

Finally, rounded to one decimal place, the amount of salt in the reservoir at the moment it begins to overflow is

$$
\begin{aligned}Q(30) & =2(50+30)-75{(\frac{50}{50+30})}^{2} \\  & =160-75{(\frac{50}{80})}^{2} \\  & ≈130.7\,\text{lb}.\end{aligned}
$$



## generated variant — easy (authored workload policy) / q-336502 / method

A saline reservoir for a medical research lab can hold up to $620\,\text{gal}$ of solution. Initially, it contains $280\,\text{gal}$ of saline solution with $84\,\text{lb}$ of dissolved salt. A more concentrated saline solution with concentration $0.6\,\text{lb/gal}$ flows into the reservoir at a rate of $30\,\text{gal/min},$ while the completely mixed solution drains out at a rate of $20\,\text{gal/min}.$ Rounded to one decimal place, find the amount of salt in the reservoir at the moment it begins to overflow.

- $364.3\,\text{lb}$
- $334.1\,\text{lb}$
- $337.7\,\text{lb}$
- $354.9\,\text{lb}$ **supplied key**
- $372.0\,\text{lb}$

Since $Q$ is the amount of salt in the reservoir at time $t,$ the derivative 

$$
\frac{dQ}{dt}
$$

describes how this amount changes with respect to time $t,$ in minutes. This is equal to the rate at which salt enters the reservoir minus the rate at which salt leaves the reservoir.

$$
\frac{dQ}{dt}={Q}_{\text{in}}^{′}-{Q}_{\text{out}}^{′}
$$

Note that the units of $\frac{dQ}{dt},{Q}_{\text{in}}^{′}$ and ${Q}_{\text{out}}^{′}$ are $\text{lb}/\text{min}.$ Now, let's compute the required rates of change in steps.

**Step 1**: Calculating the rate at which salt enters the reservoir.

First, note that a solution containing $0.6\,\text{lb/gal}$ of salt enters the reservoir at a rate of $30\,\text{gal/min}.$ So, the rate at which the *salt* enters the reservoir is 

$$
\begin{aligned}{Q}_{\text{in}}^{′} & =(0.6\,\frac{\text{lb}}{\text{gal}})\cdot (30\,\frac{\text{gal}}{\text{min}}) \\  & =(0.6\,\frac{\text{lb}}{\cancel{\text{gal}}})\cdot (30\,\frac{\cancel{\text{gal}}}{\text{min}}) \\  & =18\,\frac{\text{lb}}{\text{min}}.\end{aligned}
$$

**Step 2**: Calculating the rate at which salt exits the reservoir.

To find the rate at which salt leaves the reservoir, we must first determine the volume of solution in the reservoir at time $t.$

The reservoir initially contains $280\,\text{gal}$ of solution; solution enters at $30\,\text{gal/min}$ and mixed solution leaves at $20\,\text{gal/min}.$
As a result, the amount of solution in the reservoir after $t$ minutes is 

$$
V(t)=280+30t-20t=10(28+t)\,\text{gal}.
$$

Note that $V(t)$ is an increasing function, so the reservoir is filling.

Since $Q$ is the amount of salt in the reservoir, the concentration of the solution at time $t$ is

$$
\frac{Q}{10(28+t)}\,\text{lb/gal}.
$$

Therefore, as the completely mixed solution leaves at a rate of $20\,\text{gal/min},$ *salt* leaves at a rate of

$$
\begin{aligned}{Q}_{\text{out}}^{′} & =(20\,\frac{\text{gal}}{\text{min}})\cdot (\frac{Q}{10(28+t)}\,\frac{\text{lb}}{\text{gal}}) \\  & =(20\,\frac{\cancel{\text{gal}}}{\text{min}})\cdot (\frac{Q}{10(28+t)}\,\frac{\text{lb}}{\cancel{\text{gal}}}) \\  & =\frac{20Q}{10(28+t)}\,\frac{\text{lb}}{\text{min}} \\  & =\frac{2Q}{28+t}\,\frac{\text{lb}}{\text{min}}.\end{aligned}
$$

**Step 3**: Calculate the overall rate of change.

The rate of change equals the rate of entry minus the rate of exit. Therefore, 

$$
\begin{aligned}\frac{dQ}{dt} & ={Q}_{\text{in}}^{′}-{Q}_{\text{out}}^{′} \\  & =18-\frac{2Q}{28+t}\end{aligned}
$$

which gives the equation

$$
\frac{dQ}{dt}+\frac{2}{28+t}\,Q=18.
$$

**Step 4**: Integrate the equation.

This is a first-order linear equation with variable coefficients. So we find the general solution using an integrating factor:

$$
\begin{aligned}I(t) & ={e}^{\int 2/(28+t)\,dt} \\  & ={e}^{2\operatorname{ln}⁡|28+t|} \\  & ={e}^{\operatorname{ln}⁡(28+t)^{2}} \\  & =(28+t)^{2}.\end{aligned}
$$

Multiplying both sides of the differential equation by $I(t)=(28+t)^{2}$ yields

$$
\begin{aligned}(28+t)^{2}\cdot (\frac{dQ}{dt}+\frac{2}{28+t}\,Q) & =(28+t)^{2}\cdot 18 \\ (28+t)^{2}\frac{dQ}{dt}+2(28+t)Q & =18(28+t)^{2} \\ \frac{d}{dt}(Q(28+t)^{2}) & =18(28+t)^{2}.\end{aligned}
$$

Now, we integrate with respect to $t:$

$$
\begin{aligned}\int \frac{d}{dt}(Q(28+t)^{2})\,dt & =\int 18(28+t)^{2}\,dt \\ Q(28+t)^{2} & =18\cdot \frac{1}{3}(28+t)^{3}+C \\ Q(t) & =6(28+t)+\frac{C}{(28+t)^{2}}.\end{aligned}
$$

We're told that the reservoir initially contains $84\,\text{lb}$ of salt. So, we can apply the initial condition $Q(0)=84,$ and solve for $C:$

$$
\begin{aligned}Q(0) & =84 \\ 6(28+0)+\frac{C}{(28+0)^{2}} & =84 \\ 168+\frac{C}{(28)^{2}} & =84 \\ \frac{C}{(28)^{2}} & =-84 \\ C & =-84(28)^{2}.\end{aligned}
$$

Therefore, we obtain the following expression for $Q(t):$

$$
\begin{aligned}Q(t) & =6(28+t)-\frac{84(28)^{2}}{(28+t)^{2}} \\  & =6(28+t)-84{(\frac{28}{28+t})}^{2}.\end{aligned}
$$

Now, let ${t}_{o}$ be the time when the reservoir begins to overflow. The reservoir has a capacity of $620\,\text{gal},$ so we can use the condition $V({t}_{o})=620$ to solve for ${t}_{o}:$

$$
\begin{aligned}V({t}_{o}) & =620 \\ 280+30{t}_{o}-20{t}_{o} & =620 \\ 280+10{t}_{o} & =620 \\ 10{t}_{o} & =340 \\ {t}_{o} & =34\,\text{min}.\end{aligned}
$$

Finally, rounded to one decimal place, the amount of salt in the reservoir at the moment it begins to overflow is

$$
\begin{aligned}Q(34) & =6(28+34)-84{(\frac{28}{28+34})}^{2} \\  & =372-84{(\frac{28}{62})}^{2} \\  & ≈354.9\,\text{lb}.\end{aligned}
$$



## source replay — easy (observed) / q-336502 / observed:q-336502

A saline reservoir for a medical research lab can hold up to $620\,\text{gal}$ of solution. Initially, it contains $280\,\text{gal}$ of saline solution with $84\,\text{lb}$ of dissolved salt. A more concentrated saline solution with concentration $0.6\,\text{lb/gal}$ flows into the reservoir at a rate of $30\,\text{gal/min},$ while the completely mixed solution drains out at a rate of $20\,\text{gal/min}.$ Rounded to one decimal place, find the amount of salt in the reservoir at the moment it begins to overflow.

- $355.2\,\text{lb}$
- $354.1\,\text{lb}$
- $355.6\,\text{lb}$
- $354.4\,\text{lb}$
- $354.9\,\text{lb}$ **supplied key**

Since $Q$ is the amount of salt in the reservoir at time $t,$ the derivative 

$$
\frac{dQ}{dt}
$$

describes how this amount changes with respect to time $t,$ in minutes. This is equal to the rate at which salt enters the reservoir minus the rate at which salt leaves the reservoir.

$$
\frac{dQ}{dt}={Q}_{\text{in}}^{′}-{Q}_{\text{out}}^{′}
$$

Note that the units of $\frac{dQ}{dt},{Q}_{\text{in}}^{′}$ and ${Q}_{\text{out}}^{′}$ are $\text{lb}/\text{min}.$ Now, let's compute the required rates of change in steps.

**Step 1**: Calculating the rate at which salt enters the reservoir.

First, note that a solution containing $0.6\,\text{lb/gal}$ of salt enters the reservoir at a rate of $30\,\text{gal/min}.$ So, the rate at which the *salt* enters the reservoir is 

$$
\begin{aligned}{Q}_{\text{in}}^{′} & =(0.6\,\frac{\text{lb}}{\text{gal}})\cdot (30\,\frac{\text{gal}}{\text{min}}) \\  & =(0.6\,\frac{\text{lb}}{\cancel{\text{gal}}})\cdot (30\,\frac{\cancel{\text{gal}}}{\text{min}}) \\  & =18\,\frac{\text{lb}}{\text{min}}.\end{aligned}
$$

**Step 2**: Calculating the rate at which salt exits the reservoir.

To find the rate at which salt leaves the reservoir, we must first determine the volume of solution in the reservoir at time $t.$

The reservoir initially contains $280\,\text{gal}$ of solution; solution enters at $30\,\text{gal/min}$ and mixed solution leaves at $20\,\text{gal/min}.$
As a result, the amount of solution in the reservoir after $t$ minutes is 

$$
V(t)=280+30t-20t=10(28+t)\,\text{gal}.
$$

Note that $V(t)$ is an increasing function, so the reservoir is filling.

Since $Q$ is the amount of salt in the reservoir, the concentration of the solution at time $t$ is

$$
\frac{Q}{10(28+t)}\,\text{lb/gal}.
$$

Therefore, as the completely mixed solution leaves at a rate of $20\,\text{gal/min},$ *salt* leaves at a rate of

$$
\begin{aligned}{Q}_{\text{out}}^{′} & =(20\,\frac{\text{gal}}{\text{min}})\cdot (\frac{Q}{10(28+t)}\,\frac{\text{lb}}{\text{gal}}) \\  & =(20\,\frac{\cancel{\text{gal}}}{\text{min}})\cdot (\frac{Q}{10(28+t)}\,\frac{\text{lb}}{\cancel{\text{gal}}}) \\  & =\frac{20Q}{10(28+t)}\,\frac{\text{lb}}{\text{min}} \\  & =\frac{2Q}{28+t}\,\frac{\text{lb}}{\text{min}}.\end{aligned}
$$

**Step 3**: Calculate the overall rate of change.

The rate of change equals the rate of entry minus the rate of exit. Therefore, 

$$
\begin{aligned}\frac{dQ}{dt} & ={Q}_{\text{in}}^{′}-{Q}_{\text{out}}^{′} \\  & =18-\frac{2Q}{28+t}\end{aligned}
$$

which gives the equation

$$
\frac{dQ}{dt}+\frac{2}{28+t}\,Q=18.
$$

**Step 4**: Integrate the equation.

This is a first-order linear equation with variable coefficients. So we find the general solution using an integrating factor:

$$
\begin{aligned}I(t) & ={e}^{\int 2/(28+t)\,dt} \\  & ={e}^{2\operatorname{ln}⁡|28+t|} \\  & ={e}^{\operatorname{ln}⁡(28+t)^{2}} \\  & =(28+t)^{2}.\end{aligned}
$$

Multiplying both sides of the differential equation by $I(t)=(28+t)^{2}$ yields

$$
\begin{aligned}(28+t)^{2}\cdot (\frac{dQ}{dt}+\frac{2}{28+t}\,Q) & =(28+t)^{2}\cdot 18 \\ (28+t)^{2}\frac{dQ}{dt}+2(28+t)Q & =18(28+t)^{2} \\ \frac{d}{dt}(Q(28+t)^{2}) & =18(28+t)^{2}.\end{aligned}
$$

Now, we integrate with respect to $t:$

$$
\begin{aligned}\int \frac{d}{dt}(Q(28+t)^{2})\,dt & =\int 18(28+t)^{2}\,dt \\ Q(28+t)^{2} & =18\cdot \frac{1}{3}(28+t)^{3}+C \\ Q(t) & =6(28+t)+\frac{C}{(28+t)^{2}}.\end{aligned}
$$

We're told that the reservoir initially contains $84\,\text{lb}$ of salt. So, we can apply the initial condition $Q(0)=84,$ and solve for $C:$

$$
\begin{aligned}Q(0) & =84 \\ 6(28+0)+\frac{C}{(28+0)^{2}} & =84 \\ 168+\frac{C}{(28)^{2}} & =84 \\ \frac{C}{(28)^{2}} & =-84 \\ C & =-84(28)^{2}.\end{aligned}
$$

Therefore, we obtain the following expression for $Q(t):$

$$
\begin{aligned}Q(t) & =6(28+t)-\frac{84(28)^{2}}{(28+t)^{2}} \\  & =6(28+t)-84{(\frac{28}{28+t})}^{2}.\end{aligned}
$$

Now, let ${t}_{o}$ be the time when the reservoir begins to overflow. The reservoir has a capacity of $620\,\text{gal},$ so we can use the condition $V({t}_{o})=620$ to solve for ${t}_{o}:$

$$
\begin{aligned}V({t}_{o}) & =620 \\ 280+30{t}_{o}-20{t}_{o} & =620 \\ 280+10{t}_{o} & =620 \\ 10{t}_{o} & =340 \\ {t}_{o} & =34\,\text{min}.\end{aligned}
$$

Finally, rounded to one decimal place, the amount of salt in the reservoir at the moment it begins to overflow is

$$
\begin{aligned}Q(34) & =6(28+34)-84{(\frac{28}{28+34})}^{2} \\  & =372-84{(\frac{28}{62})}^{2} \\  & ≈354.9\,\text{lb}.\end{aligned}
$$



## generated variant — easy (authored workload policy) / q-336502 / method

A saline reservoir for a medical research lab can hold up to $610\,\text{gal}$ of solution. Initially, it contains $180\,\text{gal}$ of saline solution with $120\,\text{lb}$ of dissolved salt. A more concentrated saline solution with concentration $1.0\,\text{lb/gal}$ flows into the reservoir at a rate of $30\,\text{gal/min},$ while the completely mixed solution drains out at a rate of $20\,\text{gal/min}.$ Rounded to one decimal place, find the amount of salt in the reservoir at the moment it begins to overflow.

- $608.5\,\text{lb}$
- $594.3\,\text{lb}$
- $610.0\,\text{lb}$
- $592.3\,\text{lb}$
- $604.8\,\text{lb}$ **supplied key**

Since $Q$ is the amount of salt in the reservoir at time $t,$ the derivative 

$$
\frac{dQ}{dt}
$$

describes how this amount changes with respect to time $t,$ in minutes. This is equal to the rate at which salt enters the reservoir minus the rate at which salt leaves the reservoir.

$$
\frac{dQ}{dt}={Q}_{\text{in}}^{′}-{Q}_{\text{out}}^{′}
$$

Note that the units of $\frac{dQ}{dt},{Q}_{\text{in}}^{′}$ and ${Q}_{\text{out}}^{′}$ are $\text{lb}/\text{min}.$ Now, let's compute the required rates of change in steps.

**Step 1**: Calculating the rate at which salt enters the reservoir.

First, note that a solution containing $1.0\,\text{lb/gal}$ of salt enters the reservoir at a rate of $30\,\text{gal/min}.$ So, the rate at which the *salt* enters the reservoir is 

$$
\begin{aligned}{Q}_{\text{in}}^{′} & =(1.0\,\frac{\text{lb}}{\text{gal}})\cdot (30\,\frac{\text{gal}}{\text{min}}) \\  & =(1.0\,\frac{\text{lb}}{\cancel{\text{gal}}})\cdot (30\,\frac{\cancel{\text{gal}}}{\text{min}}) \\  & =30\,\frac{\text{lb}}{\text{min}}.\end{aligned}
$$

**Step 2**: Calculating the rate at which salt exits the reservoir.

To find the rate at which salt leaves the reservoir, we must first determine the volume of solution in the reservoir at time $t.$

The reservoir initially contains $180\,\text{gal}$ of solution; solution enters at $30\,\text{gal/min}$ and mixed solution leaves at $20\,\text{gal/min}.$
As a result, the amount of solution in the reservoir after $t$ minutes is 

$$
V(t)=180+30t-20t=10(18+t)\,\text{gal}.
$$

Note that $V(t)$ is an increasing function, so the reservoir is filling.

Since $Q$ is the amount of salt in the reservoir, the concentration of the solution at time $t$ is

$$
\frac{Q}{10(18+t)}\,\text{lb/gal}.
$$

Therefore, as the completely mixed solution leaves at a rate of $20\,\text{gal/min},$ *salt* leaves at a rate of

$$
\begin{aligned}{Q}_{\text{out}}^{′} & =(20\,\frac{\text{gal}}{\text{min}})\cdot (\frac{Q}{10(18+t)}\,\frac{\text{lb}}{\text{gal}}) \\  & =(20\,\frac{\cancel{\text{gal}}}{\text{min}})\cdot (\frac{Q}{10(18+t)}\,\frac{\text{lb}}{\cancel{\text{gal}}}) \\  & =\frac{20Q}{10(18+t)}\,\frac{\text{lb}}{\text{min}} \\  & =\frac{2Q}{18+t}\,\frac{\text{lb}}{\text{min}}.\end{aligned}
$$

**Step 3**: Calculate the overall rate of change.

The rate of change equals the rate of entry minus the rate of exit. Therefore, 

$$
\begin{aligned}\frac{dQ}{dt} & ={Q}_{\text{in}}^{′}-{Q}_{\text{out}}^{′} \\  & =30-\frac{2Q}{18+t}\end{aligned}
$$

which gives the equation

$$
\frac{dQ}{dt}+\frac{2}{18+t}\,Q=30.
$$

**Step 4**: Integrate the equation.

This is a first-order linear equation with variable coefficients. So we find the general solution using an integrating factor:

$$
\begin{aligned}I(t) & ={e}^{\int 2/(18+t)\,dt} \\  & ={e}^{2\operatorname{ln}⁡|18+t|} \\  & ={e}^{\operatorname{ln}⁡(18+t)^{2}} \\  & =(18+t)^{2}.\end{aligned}
$$

Multiplying both sides of the differential equation by $I(t)=(18+t)^{2}$ yields

$$
\begin{aligned}(18+t)^{2}\cdot (\frac{dQ}{dt}+\frac{2}{18+t}\,Q) & =(18+t)^{2}\cdot 30 \\ (18+t)^{2}\frac{dQ}{dt}+2(18+t)Q & =30(18+t)^{2} \\ \frac{d}{dt}(Q(18+t)^{2}) & =30(18+t)^{2}.\end{aligned}
$$

Now, we integrate with respect to $t:$

$$
\begin{aligned}\int \frac{d}{dt}(Q(18+t)^{2})\,dt & =\int 30(18+t)^{2}\,dt \\ Q(18+t)^{2} & =30\cdot \frac{1}{3}(18+t)^{3}+C \\ Q(t) & =10(18+t)+\frac{C}{(18+t)^{2}}.\end{aligned}
$$

We're told that the reservoir initially contains $120\,\text{lb}$ of salt. So, we can apply the initial condition $Q(0)=120,$ and solve for $C:$

$$
\begin{aligned}Q(0) & =120 \\ 10(18+0)+\frac{C}{(18+0)^{2}} & =120 \\ 180+\frac{C}{(18)^{2}} & =120 \\ \frac{C}{(18)^{2}} & =-60 \\ C & =-60(18)^{2}.\end{aligned}
$$

Therefore, we obtain the following expression for $Q(t):$

$$
\begin{aligned}Q(t) & =10(18+t)-\frac{60(18)^{2}}{(18+t)^{2}} \\  & =10(18+t)-60{(\frac{18}{18+t})}^{2}.\end{aligned}
$$

Now, let ${t}_{o}$ be the time when the reservoir begins to overflow. The reservoir has a capacity of $610\,\text{gal},$ so we can use the condition $V({t}_{o})=610$ to solve for ${t}_{o}:$

$$
\begin{aligned}V({t}_{o}) & =610 \\ 180+30{t}_{o}-20{t}_{o} & =610 \\ 180+10{t}_{o} & =610 \\ 10{t}_{o} & =430 \\ {t}_{o} & =43\,\text{min}.\end{aligned}
$$

Finally, rounded to one decimal place, the amount of salt in the reservoir at the moment it begins to overflow is

$$
\begin{aligned}Q(43) & =10(18+43)-60{(\frac{18}{18+43})}^{2} \\  & =610-60{(\frac{18}{61})}^{2} \\  & ≈604.8\,\text{lb}.\end{aligned}
$$



## generated variant — easy (authored workload policy) / q-336499 / method

A nutrient tank for a hydroponic greenhouse can hold up to $99gal$ of solution. Initially, it contains $63gal$ of nutrient solution with $28lb$ of dissolved nutrient. A more concentrated solution with concentration $\frac{2}{3}lb/gal$ flows into the tank at a rate of $9gal/min$, while the completely mixed solution drains out at a rate of $6gal/min$. Rounded to one decimal place, find the amount of nutrient in the tank at the moment it begins to overflow.

> A scientific calculator is required to answer this question.

- $66.0\,\text{lb}$
- $62.4\,\text{lb}$
- $60.3\,\text{lb}$ **supplied key**
- $49.0\,\text{lb}$
- $57.1\,\text{lb}$

Since $Q$ is the amount of nutrient in the tank at time $t,$ the derivative 

$$
\frac{dQ}{dt}
$$

describes how this amount changes with respect to time $t,$ in minutes. This is equal to the rate at which nutrient enters the tank minus the rate at which nutrient leaves the tank.

$$
\frac{dQ}{dt}={Q}_{\text{in}}^{′}-{Q}_{\text{out}}^{′}
$$

Note that the units of $\frac{dQ}{dt},{Q}_{\text{in}}^{′}$ and ${Q}_{\text{out}}^{′}$ are $\text{lb}/\text{min}.$ Now, let's compute the required rates of change in steps.

**Step 1**: Calculating the rate at which nutrient enters the tank.

First, note that a solution containing $\frac{2}{3}\,\text{lb/gal}$ of nutrient enters the tank at a rate of $9\,\text{gal/min}.$ So, the rate at which the *nutrient* enters the tank is 

$$
\begin{aligned}{Q}_{\text{in}}^{′} & =(\frac{2}{3}\,\frac{\text{lb}}{\text{gal}})\cdot (9\,\frac{\text{gal}}{\text{min}}) \\  & =(\frac{2}{3}\,\frac{\text{lb}}{\cancel{\text{gal}}})\cdot (9\,\frac{\cancel{\text{gal}}}{\text{min}}) \\  & =6\,\frac{\text{lb}}{\text{min}}.\end{aligned}
$$

**Step 2**: Calculating the rate at which nutrient exits the tank.

To find the rate at which nutrient leaves the tank, we must first determine the volume of solution in the tank at time $t.$

The tank initially contains $63\,\text{gal}$ of solution; solution enters at $9\,\text{gal/min}$ and mixed solution leaves at $6\,\text{gal/min}.$
As a result, the amount of solution in the tank after $t$ minutes is 

$$
V(t)=63+9t-6t=3(21+t)\,\text{gal}.
$$

Note that $V(t)$ is an increasing function, so the tank is filling.

Since $Q$ is the amount of nutrient in the tank, the concentration of the solution at time $t$ is

$$
\frac{Q}{3(21+t)}\,\text{lb/gal}.
$$

Therefore, as the completely mixed solution leaves at a rate of $6\,\text{gal/min},$ *nutrient* leaves at a rate of

$$
\begin{aligned}{Q}_{\text{out}}^{′} & =(6\,\frac{\text{gal}}{\text{min}})\cdot (\frac{Q}{3(21+t)}\,\frac{\text{lb}}{\text{gal}}) \\  & =(6\,\frac{\cancel{\text{gal}}}{\text{min}})\cdot (\frac{Q}{3(21+t)}\,\frac{\text{lb}}{\cancel{\text{gal}}}) \\  & =\frac{6Q}{3(21+t)}\,\frac{\text{lb}}{\text{min}} \\  & =\frac{2Q}{21+t}\,\frac{\text{lb}}{\text{min}}.\end{aligned}
$$

**Step 3**: Calculate the overall rate of change.

The rate of change equals the rate of entry minus the rate of exit. Therefore, 

$$
\begin{aligned}\frac{dQ}{dt} & ={Q}_{\text{in}}^{′}-{Q}_{\text{out}}^{′} \\  & =6-\frac{2Q}{21+t}\end{aligned}
$$

which gives the equation

$$
\frac{dQ}{dt}+\frac{2}{21+t}\,Q=6.
$$

**Step 4**: Integrate the equation.

This is a first-order linear equation with variable coefficients. So we find the general solution using an integrating factor:

$$
\begin{aligned}I(t) & ={e}^{\int 2/(21+t)\,dt} \\  & ={e}^{2\operatorname{ln}⁡|21+t|} \\  & ={e}^{\operatorname{ln}⁡(21+t)^{2}} \\  & =(21+t)^{2}.\end{aligned}
$$

Multiplying both sides of the differential equation by $I(t)=(21+t)^{2}$ yields

$$
\begin{aligned}(21+t)^{2}\cdot (\frac{dQ}{dt}+\frac{2}{21+t}\,Q) & =(21+t)^{2}\cdot 6 \\ (21+t)^{2}\frac{dQ}{dt}+2(21+t)Q & =6(21+t)^{2} \\ \frac{d}{dt}(Q(21+t)^{2}) & =6(21+t)^{2}.\end{aligned}
$$

Now, we integrate with respect to $t:$

$$
\begin{aligned}\int \frac{d}{dt}(Q(21+t)^{2})\,dt & =\int 6(21+t)^{2}\,dt \\ Q(21+t)^{2} & =6\cdot \frac{1}{3}(21+t)^{3}+C \\ Q(t) & =2(21+t)+\frac{C}{(21+t)^{2}}.\end{aligned}
$$

We're told that the tank initially contains $28\,\text{lb}$ of nutrient. So, we can apply the initial condition $Q(0)=28,$ and solve for $C:$

$$
\begin{aligned}Q(0) & =28 \\ 2(21+0)+\frac{C}{(21+0)^{2}} & =28 \\ 42+\frac{C}{(21)^{2}} & =28 \\ \frac{C}{(21)^{2}} & =-14 \\ C & =-14(21)^{2}.\end{aligned}
$$

Therefore, we obtain the following expression for $Q(t):$

$$
\begin{aligned}Q(t) & =2(21+t)-\frac{14(21)^{2}}{(21+t)^{2}} \\  & =2(21+t)-14{(\frac{21}{21+t})}^{2}.\end{aligned}
$$

Now, let ${t}_{o}$ be the time when the tank begins to overflow. The tank has a capacity of $99\,\text{gal},$ so we can use the condition $V({t}_{o})=99$ to solve for ${t}_{o}:$

$$
\begin{aligned}V({t}_{o}) & =99 \\ 63+9{t}_{o}-6{t}_{o} & =99 \\ 63+3{t}_{o} & =99 \\ 3{t}_{o} & =36 \\ {t}_{o} & =12\,\text{min}.\end{aligned}
$$

Finally, rounded to one decimal place, the amount of nutrient in the tank at the moment it begins to overflow is

$$
\begin{aligned}Q(12) & =2(21+12)-14{(\frac{21}{21+12})}^{2} \\  & =66-14{(\frac{21}{33})}^{2} \\  & ≈60.3\,\text{lb}.\end{aligned}
$$



## generated variant — moderate (authored workload policy) / q-336502 / method

A saline reservoir for a medical research lab can hold up to $590\,\text{gal}$ of solution. Initially, it contains $270\,\text{gal}$ of saline solution with $108\,\text{lb}$ of dissolved salt. A more concentrated saline solution with concentration $1.2\,\text{lb/gal}$ flows into the reservoir at a rate of $40\,\text{gal/min},$ while the completely mixed solution drains out at a rate of $30\,\text{gal/min}.$ Rounded to one decimal place, find the amount of salt in the reservoir at the moment it begins to overflow.

- $687.3\,\text{lb}$ **supplied key**
- $698.5\,\text{lb}$
- $708.0\,\text{lb}$
- $662.8\,\text{lb}$
- $676.9\,\text{lb}$

Since $Q$ is the amount of salt in the reservoir at time $t,$ the derivative 

$$
\frac{dQ}{dt}
$$

describes how this amount changes with respect to time $t,$ in minutes. This is equal to the rate at which salt enters the reservoir minus the rate at which salt leaves the reservoir.

$$
\frac{dQ}{dt}={Q}_{\text{in}}^{′}-{Q}_{\text{out}}^{′}
$$

Note that the units of $\frac{dQ}{dt},{Q}_{\text{in}}^{′}$ and ${Q}_{\text{out}}^{′}$ are $\text{lb}/\text{min}.$ Now, let's compute the required rates of change in steps.

**Step 1**: Calculating the rate at which salt enters the reservoir.

First, note that a solution containing $1.2\,\text{lb/gal}$ of salt enters the reservoir at a rate of $40\,\text{gal/min}.$ So, the rate at which the *salt* enters the reservoir is 

$$
\begin{aligned}{Q}_{\text{in}}^{′} & =(1.2\,\frac{\text{lb}}{\text{gal}})\cdot (40\,\frac{\text{gal}}{\text{min}}) \\  & =(1.2\,\frac{\text{lb}}{\cancel{\text{gal}}})\cdot (40\,\frac{\cancel{\text{gal}}}{\text{min}}) \\  & =48\,\frac{\text{lb}}{\text{min}}.\end{aligned}
$$

**Step 2**: Calculating the rate at which salt exits the reservoir.

To find the rate at which salt leaves the reservoir, we must first determine the volume of solution in the reservoir at time $t.$

The reservoir initially contains $270\,\text{gal}$ of solution; solution enters at $40\,\text{gal/min}$ and mixed solution leaves at $30\,\text{gal/min}.$
As a result, the amount of solution in the reservoir after $t$ minutes is 

$$
V(t)=270+40t-30t=10(27+t)\,\text{gal}.
$$

Note that $V(t)$ is an increasing function, so the reservoir is filling.

Since $Q$ is the amount of salt in the reservoir, the concentration of the solution at time $t$ is

$$
\frac{Q}{10(27+t)}\,\text{lb/gal}.
$$

Therefore, as the completely mixed solution leaves at a rate of $30\,\text{gal/min},$ *salt* leaves at a rate of

$$
\begin{aligned}{Q}_{\text{out}}^{′} & =(30\,\frac{\text{gal}}{\text{min}})\cdot (\frac{Q}{10(27+t)}\,\frac{\text{lb}}{\text{gal}}) \\  & =(30\,\frac{\cancel{\text{gal}}}{\text{min}})\cdot (\frac{Q}{10(27+t)}\,\frac{\text{lb}}{\cancel{\text{gal}}}) \\  & =\frac{30Q}{10(27+t)}\,\frac{\text{lb}}{\text{min}} \\  & =\frac{3Q}{27+t}\,\frac{\text{lb}}{\text{min}}.\end{aligned}
$$

**Step 3**: Calculate the overall rate of change.

The rate of change equals the rate of entry minus the rate of exit. Therefore, 

$$
\begin{aligned}\frac{dQ}{dt} & ={Q}_{\text{in}}^{′}-{Q}_{\text{out}}^{′} \\  & =48-\frac{3Q}{27+t}\end{aligned}
$$

which gives the equation

$$
\frac{dQ}{dt}+\frac{3}{27+t}\,Q=48.
$$

**Step 4**: Integrate the equation.

This is a first-order linear equation with variable coefficients. So we find the general solution using an integrating factor:

$$
\begin{aligned}I(t) & ={e}^{\int 3/(27+t)\,dt} \\  & ={e}^{3\operatorname{ln}⁡|27+t|} \\  & ={e}^{\operatorname{ln}⁡(27+t)^{3}} \\  & =(27+t)^{3}.\end{aligned}
$$

Multiplying both sides of the differential equation by $I(t)=(27+t)^{3}$ yields

$$
\begin{aligned}(27+t)^{3}\cdot (\frac{dQ}{dt}+\frac{3}{27+t}\,Q) & =(27+t)^{3}\cdot 48 \\ (27+t)^{3}\frac{dQ}{dt}+3(27+t)^{2}Q & =48(27+t)^{3} \\ \frac{d}{dt}(Q(27+t)^{3}) & =48(27+t)^{3}.\end{aligned}
$$

Now, we integrate with respect to $t:$

$$
\begin{aligned}\int \frac{d}{dt}(Q(27+t)^{3})\,dt & =\int 48(27+t)^{3}\,dt \\ Q(27+t)^{3} & =48\cdot \frac{1}{4}(27+t)^{4}+C \\ Q(t) & =12(27+t)+\frac{C}{(27+t)^{3}}.\end{aligned}
$$

We're told that the reservoir initially contains $108\,\text{lb}$ of salt. So, we can apply the initial condition $Q(0)=108,$ and solve for $C:$

$$
\begin{aligned}Q(0) & =108 \\ 12(27+0)+\frac{C}{(27+0)^{3}} & =108 \\ 324+\frac{C}{(27)^{3}} & =108 \\ \frac{C}{(27)^{3}} & =-216 \\ C & =-216(27)^{3}.\end{aligned}
$$

Therefore, we obtain the following expression for $Q(t):$

$$
\begin{aligned}Q(t) & =12(27+t)-\frac{216(27)^{3}}{(27+t)^{3}} \\  & =12(27+t)-216{(\frac{27}{27+t})}^{3}.\end{aligned}
$$

Now, let ${t}_{o}$ be the time when the reservoir begins to overflow. The reservoir has a capacity of $590\,\text{gal},$ so we can use the condition $V({t}_{o})=590$ to solve for ${t}_{o}:$

$$
\begin{aligned}V({t}_{o}) & =590 \\ 270+40{t}_{o}-30{t}_{o} & =590 \\ 270+10{t}_{o} & =590 \\ 10{t}_{o} & =320 \\ {t}_{o} & =32\,\text{min}.\end{aligned}
$$

Finally, rounded to one decimal place, the amount of salt in the reservoir at the moment it begins to overflow is

$$
\begin{aligned}Q(32) & =12(27+32)-216{(\frac{27}{27+32})}^{3} \\  & =708-216{(\frac{27}{59})}^{3} \\  & ≈687.3\,\text{lb}.\end{aligned}
$$



## generated variant — moderate (authored workload policy) / q-336499 / method

A nutrient tank for a hydroponic greenhouse can hold up to $426gal$ of solution. Initially, it contains $186gal$ of nutrient solution with $31lb$ of dissolved nutrient. A more concentrated solution with concentration $0.5lb/gal$ flows into the tank at a rate of $24gal/min$, while the completely mixed solution drains out at a rate of $18gal/min$. Rounded to one decimal place, find the amount of nutrient in the tank at the moment it begins to overflow.

> A scientific calculator is required to answer this question.

- $201.2\,\text{lb}$
- $213.0\,\text{lb}$
- $205.3\,\text{lb}$
- $207.8\,\text{lb}$ **supplied key**
- $210.7\,\text{lb}$

Since $Q$ is the amount of nutrient in the tank at time $t,$ the derivative 

$$
\frac{dQ}{dt}
$$

describes how this amount changes with respect to time $t,$ in minutes. This is equal to the rate at which nutrient enters the tank minus the rate at which nutrient leaves the tank.

$$
\frac{dQ}{dt}={Q}_{\text{in}}^{′}-{Q}_{\text{out}}^{′}
$$

Note that the units of $\frac{dQ}{dt},{Q}_{\text{in}}^{′}$ and ${Q}_{\text{out}}^{′}$ are $\text{lb}/\text{min}.$ Now, let's compute the required rates of change in steps.

**Step 1**: Calculating the rate at which nutrient enters the tank.

First, note that a solution containing $0.5\,\text{lb/gal}$ of nutrient enters the tank at a rate of $24\,\text{gal/min}.$ So, the rate at which the *nutrient* enters the tank is 

$$
\begin{aligned}{Q}_{\text{in}}^{′} & =(0.5\,\frac{\text{lb}}{\text{gal}})\cdot (24\,\frac{\text{gal}}{\text{min}}) \\  & =(0.5\,\frac{\text{lb}}{\cancel{\text{gal}}})\cdot (24\,\frac{\cancel{\text{gal}}}{\text{min}}) \\  & =12\,\frac{\text{lb}}{\text{min}}.\end{aligned}
$$

**Step 2**: Calculating the rate at which nutrient exits the tank.

To find the rate at which nutrient leaves the tank, we must first determine the volume of solution in the tank at time $t.$

The tank initially contains $186\,\text{gal}$ of solution; solution enters at $24\,\text{gal/min}$ and mixed solution leaves at $18\,\text{gal/min}.$
As a result, the amount of solution in the tank after $t$ minutes is 

$$
V(t)=186+24t-18t=6(31+t)\,\text{gal}.
$$

Note that $V(t)$ is an increasing function, so the tank is filling.

Since $Q$ is the amount of nutrient in the tank, the concentration of the solution at time $t$ is

$$
\frac{Q}{6(31+t)}\,\text{lb/gal}.
$$

Therefore, as the completely mixed solution leaves at a rate of $18\,\text{gal/min},$ *nutrient* leaves at a rate of

$$
\begin{aligned}{Q}_{\text{out}}^{′} & =(18\,\frac{\text{gal}}{\text{min}})\cdot (\frac{Q}{6(31+t)}\,\frac{\text{lb}}{\text{gal}}) \\  & =(18\,\frac{\cancel{\text{gal}}}{\text{min}})\cdot (\frac{Q}{6(31+t)}\,\frac{\text{lb}}{\cancel{\text{gal}}}) \\  & =\frac{18Q}{6(31+t)}\,\frac{\text{lb}}{\text{min}} \\  & =\frac{3Q}{31+t}\,\frac{\text{lb}}{\text{min}}.\end{aligned}
$$

**Step 3**: Calculate the overall rate of change.

The rate of change equals the rate of entry minus the rate of exit. Therefore, 

$$
\begin{aligned}\frac{dQ}{dt} & ={Q}_{\text{in}}^{′}-{Q}_{\text{out}}^{′} \\  & =12-\frac{3Q}{31+t}\end{aligned}
$$

which gives the equation

$$
\frac{dQ}{dt}+\frac{3}{31+t}\,Q=12.
$$

**Step 4**: Integrate the equation.

This is a first-order linear equation with variable coefficients. So we find the general solution using an integrating factor:

$$
\begin{aligned}I(t) & ={e}^{\int 3/(31+t)\,dt} \\  & ={e}^{3\operatorname{ln}⁡|31+t|} \\  & ={e}^{\operatorname{ln}⁡(31+t)^{3}} \\  & =(31+t)^{3}.\end{aligned}
$$

Multiplying both sides of the differential equation by $I(t)=(31+t)^{3}$ yields

$$
\begin{aligned}(31+t)^{3}\cdot (\frac{dQ}{dt}+\frac{3}{31+t}\,Q) & =(31+t)^{3}\cdot 12 \\ (31+t)^{3}\frac{dQ}{dt}+3(31+t)^{2}Q & =12(31+t)^{3} \\ \frac{d}{dt}(Q(31+t)^{3}) & =12(31+t)^{3}.\end{aligned}
$$

Now, we integrate with respect to $t:$

$$
\begin{aligned}\int \frac{d}{dt}(Q(31+t)^{3})\,dt & =\int 12(31+t)^{3}\,dt \\ Q(31+t)^{3} & =12\cdot \frac{1}{4}(31+t)^{4}+C \\ Q(t) & =3(31+t)+\frac{C}{(31+t)^{3}}.\end{aligned}
$$

We're told that the tank initially contains $31\,\text{lb}$ of nutrient. So, we can apply the initial condition $Q(0)=31,$ and solve for $C:$

$$
\begin{aligned}Q(0) & =31 \\ 3(31+0)+\frac{C}{(31+0)^{3}} & =31 \\ 93+\frac{C}{(31)^{3}} & =31 \\ \frac{C}{(31)^{3}} & =-62 \\ C & =-62(31)^{3}.\end{aligned}
$$

Therefore, we obtain the following expression for $Q(t):$

$$
\begin{aligned}Q(t) & =3(31+t)-\frac{62(31)^{3}}{(31+t)^{3}} \\  & =3(31+t)-62{(\frac{31}{31+t})}^{3}.\end{aligned}
$$

Now, let ${t}_{o}$ be the time when the tank begins to overflow. The tank has a capacity of $426\,\text{gal},$ so we can use the condition $V({t}_{o})=426$ to solve for ${t}_{o}:$

$$
\begin{aligned}V({t}_{o}) & =426 \\ 186+24{t}_{o}-18{t}_{o} & =426 \\ 186+6{t}_{o} & =426 \\ 6{t}_{o} & =240 \\ {t}_{o} & =40\,\text{min}.\end{aligned}
$$

Finally, rounded to one decimal place, the amount of nutrient in the tank at the moment it begins to overflow is

$$
\begin{aligned}Q(40) & =3(31+40)-62{(\frac{31}{31+40})}^{3} \\  & =213-62{(\frac{31}{71})}^{3} \\  & ≈207.8\,\text{lb}.\end{aligned}
$$



## generated variant — hard (authored workload policy) / q-336502 / method

A saline reservoir for a medical research lab can hold up to $232\,\text{gal}$ of solution. Initially, it contains $60\,\text{gal}$ of saline solution with $\frac{80}{3}\,\text{lb}$ of dissolved salt. A more concentrated saline solution with concentration $\frac{2}{3}\,\text{lb/gal}$ flows into the reservoir at a rate of $20\,\text{gal/min},$ while the completely mixed solution drains out at a rate of $12\,\text{gal/min}.$ Rounded to one decimal place, find the amount of salt in the reservoir at the moment it begins to overflow.

- $149.4\,\text{lb}$
- $152.9\,\text{lb}$ **supplied key**
- $154.7\,\text{lb}$
- $147.9\,\text{lb}$
- $154.2\,\text{lb}$

Since $Q$ is the amount of salt in the reservoir at time $t,$ the derivative 

$$
\frac{dQ}{dt}
$$

describes how this amount changes with respect to time $t,$ in minutes. This is equal to the rate at which salt enters the reservoir minus the rate at which salt leaves the reservoir.

$$
\frac{dQ}{dt}={Q}_{\text{in}}^{′}-{Q}_{\text{out}}^{′}
$$

Note that the units of $\frac{dQ}{dt},{Q}_{\text{in}}^{′}$ and ${Q}_{\text{out}}^{′}$ are $\text{lb}/\text{min}.$ Now, let's compute the required rates of change in steps.

**Step 1**: Calculating the rate at which salt enters the reservoir.

First, note that a solution containing $\frac{2}{3}\,\text{lb/gal}$ of salt enters the reservoir at a rate of $20\,\text{gal/min}.$ So, the rate at which the *salt* enters the reservoir is 

$$
\begin{aligned}{Q}_{\text{in}}^{′} & =(\frac{2}{3}\,\frac{\text{lb}}{\text{gal}})\cdot (20\,\frac{\text{gal}}{\text{min}}) \\  & =(\frac{2}{3}\,\frac{\text{lb}}{\cancel{\text{gal}}})\cdot (20\,\frac{\cancel{\text{gal}}}{\text{min}}) \\  & =\frac{40}{3}\,\frac{\text{lb}}{\text{min}}.\end{aligned}
$$

**Step 2**: Calculating the rate at which salt exits the reservoir.

To find the rate at which salt leaves the reservoir, we must first determine the volume of solution in the reservoir at time $t.$

The reservoir initially contains $60\,\text{gal}$ of solution; solution enters at $20\,\text{gal/min}$ and mixed solution leaves at $12\,\text{gal/min}.$
As a result, the amount of solution in the reservoir after $t$ minutes is 

$$
V(t)=60+20t-12t=8(7.5+t)\,\text{gal}.
$$

Note that $V(t)$ is an increasing function, so the reservoir is filling.

Since $Q$ is the amount of salt in the reservoir, the concentration of the solution at time $t$ is

$$
\frac{Q}{8(7.5+t)}\,\text{lb/gal}.
$$

Therefore, as the completely mixed solution leaves at a rate of $12\,\text{gal/min},$ *salt* leaves at a rate of

$$
\begin{aligned}{Q}_{\text{out}}^{′} & =(12\,\frac{\text{gal}}{\text{min}})\cdot (\frac{Q}{8(7.5+t)}\,\frac{\text{lb}}{\text{gal}}) \\  & =(12\,\frac{\cancel{\text{gal}}}{\text{min}})\cdot (\frac{Q}{8(7.5+t)}\,\frac{\text{lb}}{\cancel{\text{gal}}}) \\  & =\frac{12Q}{8(7.5+t)}\,\frac{\text{lb}}{\text{min}} \\  & =\frac{1.5Q}{7.5+t}\,\frac{\text{lb}}{\text{min}}.\end{aligned}
$$

**Step 3**: Calculate the overall rate of change.

The rate of change equals the rate of entry minus the rate of exit. Therefore, 

$$
\begin{aligned}\frac{dQ}{dt} & ={Q}_{\text{in}}^{′}-{Q}_{\text{out}}^{′} \\  & =\frac{40}{3}-\frac{1.5Q}{7.5+t}\end{aligned}
$$

which gives the equation

$$
\frac{dQ}{dt}+\frac{1.5}{7.5+t}\,Q=\frac{40}{3}.
$$

**Step 4**: Integrate the equation.

This is a first-order linear equation with variable coefficients. So we find the general solution using an integrating factor:

$$
\begin{aligned}I(t) & ={e}^{\int 1.5/(7.5+t)\,dt} \\  & ={e}^{1.5\operatorname{ln}⁡|7.5+t|} \\  & ={e}^{\operatorname{ln}⁡(7.5+t)^{1.5}} \\  & =(7.5+t)^{1.5}.\end{aligned}
$$

Multiplying both sides of the differential equation by $I(t)=(7.5+t)^{1.5}$ yields

$$
\begin{aligned}(7.5+t)^{1.5}\cdot (\frac{dQ}{dt}+\frac{1.5}{7.5+t}\,Q) & =(7.5+t)^{1.5}\cdot \frac{40}{3} \\ (7.5+t)^{1.5}\frac{dQ}{dt}+1.5(7.5+t)^{0.5}Q & =\frac{40}{3}(7.5+t)^{1.5} \\ \frac{d}{dt}(Q(7.5+t)^{1.5}) & =\frac{40}{3}(7.5+t)^{1.5}.\end{aligned}
$$

Now, we integrate with respect to $t:$

$$
\begin{aligned}\int \frac{d}{dt}(Q(7.5+t)^{1.5})\,dt & =\int \frac{40}{3}(7.5+t)^{1.5}\,dt \\ Q(7.5+t)^{1.5} & =\frac{40}{3}\cdot \frac{1}{2.5}(7.5+t)^{2.5}+C \\ Q(t) & =\frac{16}{3}(7.5+t)+\frac{C}{(7.5+t)^{1.5}}.\end{aligned}
$$

We're told that the reservoir initially contains $\frac{80}{3}\,\text{lb}$ of salt. So, we can apply the initial condition $Q(0)=\frac{80}{3},$ and solve for $C:$

$$
\begin{aligned}Q(0) & =\frac{80}{3} \\ \frac{16}{3}(7.5+0)+\frac{C}{(7.5+0)^{1.5}} & =\frac{80}{3} \\ 40+\frac{C}{(7.5)^{1.5}} & =\frac{80}{3} \\ \frac{C}{(7.5)^{1.5}} & =-\frac{40}{3} \\ C & =-\frac{40}{3}(7.5)^{1.5}.\end{aligned}
$$

Therefore, we obtain the following expression for $Q(t):$

$$
\begin{aligned}Q(t) & =\frac{16}{3}(7.5+t)-\frac{\frac{40}{3}(7.5)^{1.5}}{(7.5+t)^{1.5}} \\  & =\frac{16}{3}(7.5+t)-\frac{40}{3}{(\frac{7.5}{7.5+t})}^{1.5}.\end{aligned}
$$

Now, let ${t}_{o}$ be the time when the reservoir begins to overflow. The reservoir has a capacity of $232\,\text{gal},$ so we can use the condition $V({t}_{o})=232$ to solve for ${t}_{o}:$

$$
\begin{aligned}V({t}_{o}) & =232 \\ 60+20{t}_{o}-12{t}_{o} & =232 \\ 60+8{t}_{o} & =232 \\ 8{t}_{o} & =172 \\ {t}_{o} & =21.5\,\text{min}.\end{aligned}
$$

Finally, rounded to one decimal place, the amount of salt in the reservoir at the moment it begins to overflow is

$$
\begin{aligned}Q(21.5) & =\frac{16}{3}(7.5+21.5)-\frac{40}{3}{(\frac{7.5}{7.5+21.5})}^{1.5} \\  & =\frac{464}{3}-\frac{40}{3}{(\frac{7.5}{29})}^{1.5} \\  & ≈152.9\,\text{lb}.\end{aligned}
$$



## generated variant — hard (authored workload policy) / q-336499 / method

A nutrient tank for a hydroponic greenhouse can hold up to $448gal$ of solution. Initially, it contains $268gal$ of nutrient solution with $53.6lb$ of dissolved nutrient. A more concentrated solution with concentration $0.8lb/gal$ flows into the tank at a rate of $12gal/min$, while the completely mixed solution drains out at a rate of $4gal/min$. Rounded to one decimal place, find the amount of nutrient in the tank at the moment it begins to overflow.

> A scientific calculator is required to answer this question.

- $358.4\,\text{lb}$
- $192.6\,\text{lb}$
- $150.5\,\text{lb}$
- $234.0\,\text{lb}$ **supplied key**
- $284.0\,\text{lb}$

Since $Q$ is the amount of nutrient in the tank at time $t,$ the derivative 

$$
\frac{dQ}{dt}
$$

describes how this amount changes with respect to time $t,$ in minutes. This is equal to the rate at which nutrient enters the tank minus the rate at which nutrient leaves the tank.

$$
\frac{dQ}{dt}={Q}_{\text{in}}^{′}-{Q}_{\text{out}}^{′}
$$

Note that the units of $\frac{dQ}{dt},{Q}_{\text{in}}^{′}$ and ${Q}_{\text{out}}^{′}$ are $\text{lb}/\text{min}.$ Now, let's compute the required rates of change in steps.

**Step 1**: Calculating the rate at which nutrient enters the tank.

First, note that a solution containing $0.8\,\text{lb/gal}$ of nutrient enters the tank at a rate of $12\,\text{gal/min}.$ So, the rate at which the *nutrient* enters the tank is 

$$
\begin{aligned}{Q}_{\text{in}}^{′} & =(0.8\,\frac{\text{lb}}{\text{gal}})\cdot (12\,\frac{\text{gal}}{\text{min}}) \\  & =(0.8\,\frac{\text{lb}}{\cancel{\text{gal}}})\cdot (12\,\frac{\cancel{\text{gal}}}{\text{min}}) \\  & =9.6\,\frac{\text{lb}}{\text{min}}.\end{aligned}
$$

**Step 2**: Calculating the rate at which nutrient exits the tank.

To find the rate at which nutrient leaves the tank, we must first determine the volume of solution in the tank at time $t.$

The tank initially contains $268\,\text{gal}$ of solution; solution enters at $12\,\text{gal/min}$ and mixed solution leaves at $4\,\text{gal/min}.$
As a result, the amount of solution in the tank after $t$ minutes is 

$$
V(t)=268+12t-4t=8(33.5+t)\,\text{gal}.
$$

Note that $V(t)$ is an increasing function, so the tank is filling.

Since $Q$ is the amount of nutrient in the tank, the concentration of the solution at time $t$ is

$$
\frac{Q}{8(33.5+t)}\,\text{lb/gal}.
$$

Therefore, as the completely mixed solution leaves at a rate of $4\,\text{gal/min},$ *nutrient* leaves at a rate of

$$
\begin{aligned}{Q}_{\text{out}}^{′} & =(4\,\frac{\text{gal}}{\text{min}})\cdot (\frac{Q}{8(33.5+t)}\,\frac{\text{lb}}{\text{gal}}) \\  & =(4\,\frac{\cancel{\text{gal}}}{\text{min}})\cdot (\frac{Q}{8(33.5+t)}\,\frac{\text{lb}}{\cancel{\text{gal}}}) \\  & =\frac{4Q}{8(33.5+t)}\,\frac{\text{lb}}{\text{min}} \\  & =\frac{0.5Q}{33.5+t}\,\frac{\text{lb}}{\text{min}}.\end{aligned}
$$

**Step 3**: Calculate the overall rate of change.

The rate of change equals the rate of entry minus the rate of exit. Therefore, 

$$
\begin{aligned}\frac{dQ}{dt} & ={Q}_{\text{in}}^{′}-{Q}_{\text{out}}^{′} \\  & =9.6-\frac{0.5Q}{33.5+t}\end{aligned}
$$

which gives the equation

$$
\frac{dQ}{dt}+\frac{0.5}{33.5+t}\,Q=9.6.
$$

**Step 4**: Integrate the equation.

This is a first-order linear equation with variable coefficients. So we find the general solution using an integrating factor:

$$
\begin{aligned}I(t) & ={e}^{\int 0.5/(33.5+t)\,dt} \\  & ={e}^{0.5\operatorname{ln}⁡|33.5+t|} \\  & ={e}^{\operatorname{ln}⁡(33.5+t)^{0.5}} \\  & =(33.5+t)^{0.5}.\end{aligned}
$$

Multiplying both sides of the differential equation by $I(t)=(33.5+t)^{0.5}$ yields

$$
\begin{aligned}(33.5+t)^{0.5}\cdot (\frac{dQ}{dt}+\frac{0.5}{33.5+t}\,Q) & =(33.5+t)^{0.5}\cdot 9.6 \\ (33.5+t)^{0.5}\frac{dQ}{dt}+0.5(33.5+t)^{-0.5}Q & =9.6(33.5+t)^{0.5} \\ \frac{d}{dt}(Q(33.5+t)^{0.5}) & =9.6(33.5+t)^{0.5}.\end{aligned}
$$

Now, we integrate with respect to $t:$

$$
\begin{aligned}\int \frac{d}{dt}(Q(33.5+t)^{0.5})\,dt & =\int 9.6(33.5+t)^{0.5}\,dt \\ Q(33.5+t)^{0.5} & =9.6\cdot \frac{1}{1.5}(33.5+t)^{1.5}+C \\ Q(t) & =6.4(33.5+t)+\frac{C}{(33.5+t)^{0.5}}.\end{aligned}
$$

We're told that the tank initially contains $53.6\,\text{lb}$ of nutrient. So, we can apply the initial condition $Q(0)=53.6,$ and solve for $C:$

$$
\begin{aligned}Q(0) & =53.6 \\ 6.4(33.5+0)+\frac{C}{(33.5+0)^{0.5}} & =53.6 \\ 214.4+\frac{C}{(33.5)^{0.5}} & =53.6 \\ \frac{C}{(33.5)^{0.5}} & =-160.8 \\ C & =-160.8(33.5)^{0.5}.\end{aligned}
$$

Therefore, we obtain the following expression for $Q(t):$

$$
\begin{aligned}Q(t) & =6.4(33.5+t)-\frac{160.8(33.5)^{0.5}}{(33.5+t)^{0.5}} \\  & =6.4(33.5+t)-160.8{(\frac{33.5}{33.5+t})}^{0.5}.\end{aligned}
$$

Now, let ${t}_{o}$ be the time when the tank begins to overflow. The tank has a capacity of $448\,\text{gal},$ so we can use the condition $V({t}_{o})=448$ to solve for ${t}_{o}:$

$$
\begin{aligned}V({t}_{o}) & =448 \\ 268+12{t}_{o}-4{t}_{o} & =448 \\ 268+8{t}_{o} & =448 \\ 8{t}_{o} & =180 \\ {t}_{o} & =22.5\,\text{min}.\end{aligned}
$$

Finally, rounded to one decimal place, the amount of nutrient in the tank at the moment it begins to overflow is

$$
\begin{aligned}Q(22.5) & =6.4(33.5+22.5)-160.8{(\frac{33.5}{33.5+22.5})}^{0.5} \\  & =358.4-160.8{(\frac{33.5}{56})}^{0.5} \\  & ≈234.0\,\text{lb}.\end{aligned}
$$


