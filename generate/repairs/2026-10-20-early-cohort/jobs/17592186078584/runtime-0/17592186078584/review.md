# Inhibited decay model review

Raw originals retain one documented unit-label anomaly. Generated variants use complete operation banks unless labeled observed profile.


## Original q-107128 — exact raw replay

The temperature $T(t),$ in degrees Fahrenheit, of an exhaust pipe of a motorcycle can be modeled by the differential equation

$$
\frac{dT}{dt}=-0.08(T-74)
$$

where $t>0$ is the time, measured in minutes. If the initial temperature of the exhaust pipe is ${140}^{∘}F,$ calculate its temperature after $3$ minutes. Round your answer to the nearest integer.

- ${112}^{∘}\text{F}$
- ${126}^{∘}\text{F}$ **(correct)**
- ${98}^{∘}\text{F}$
- ${134}^{∘}\text{F}$
- ${92}^{∘}\text{F}$

**Worked solution**

We're told that the temperature of the exhaust pipe of a motorcycle is modeled by the inhibited decay equation

$$
\frac{dT}{dt}=-0.08(T-74).
$$

First, we integrate our differential equation by separating the variables:

$$
\begin{aligned}\frac{dT}{T-74} & =-0.08\,dt \\ \int \frac{dT}{T-74} & =-\int 0.08\,\text{d}t \\ \operatorname{ln}⁡|T-74| & =-0.08t+C\end{aligned}
$$

Since this is the solution to an inhibited decay equation, we have $T-74>0$ for all $t>0.$
Next, we solve for $T(t),$ as follows:

$$
\begin{aligned}T-74 & ={e}^{-0.08t+C} \\ T-74 & ={e}^{C}{e}^{-0.08t} \\ T-74 & =K{e}^{-0.08t} \\ T & =74+K{e}^{-0.08t}\end{aligned}
$$

Note that $K={e}^{C}$ is a constant of integration. 

We're told that the initial temperature of the exhaust pipe was ${140}^{∘}F.$ So, we apply the initial condition $T(0)=140,$ and solve for $K:$

$$
\begin{aligned}140 & =74+K{e}^{0} \\ 140 & =74+K \\ K & =66\end{aligned}
$$

Therefore, the solution to our initial value problem is

$$
T(t)=74+66{e}^{-0.08t}.
$$

Finally, the temperature of the exhaust pipe after $t=3$ minutes is

$$
T(3)=74+66{e}^{-0.08\cdot 3}≈{126}^{∘}\text{F},
$$

rounded to the nearest integer.


## Changed observed profile q-107128 — underdetermined scalar intent

The temperature $T(t),$ in degrees Fahrenheit, of an exhaust pipe of a motorcycle can be modeled by the differential equation

$$
\frac{dT}{dt}=-0.08(T-75)
$$

where $t>0$ is the time, measured in minutes. If the initial temperature of the exhaust pipe is ${141}^{∘}F,$ calculate its temperature after $4$ minutes. Round your answer to the nearest integer.

- ${109}^{∘}\text{F}$
- ${89}^{∘}\text{F}$
- ${131}^{∘}\text{F}$
- ${123}^{∘}\text{F}$ **(correct)**
- ${95}^{∘}\text{F}$

**Worked solution**

We're told that the temperature of the exhaust pipe of a motorcycle is modeled by the inhibited decay equation

$$
\frac{dT}{dt}=-0.08(T-75).
$$

First, we integrate our differential equation by separating the variables:

$$
\begin{aligned}\frac{dT}{T-75} & =-0.08\,dt \\ \int \frac{dT}{T-75} & =-\int 0.08\,\text{d}t \\ \operatorname{ln}⁡|T-75| & =-0.08t+C\end{aligned}
$$

Since this is the solution to an inhibited decay equation, we have $T-75>0$ for all $t>0.$
Next, we solve for $T(t),$ as follows:

$$
\begin{aligned}T-75 & ={e}^{-0.08t+C} \\ T-75 & ={e}^{C}{e}^{-0.08t} \\ T-75 & =K{e}^{-0.08t} \\ T & =75+K{e}^{-0.08t}\end{aligned}
$$

Note that $K={e}^{C}$ is a constant of integration. 

We're told that the initial temperature of the exhaust pipe was ${141}^{∘}F.$ So, we apply the initial condition $T(0)=141,$ and solve for $K:$

$$
\begin{aligned}141 & =75+K{e}^{0} \\ 141 & =75+K \\ K & =66\end{aligned}
$$

Therefore, the solution to our initial value problem is

$$
T(t)=75+66{e}^{-0.08t}.
$$

Finally, the temperature of the exhaust pipe after $t=4$ minutes is

$$
T(4)=75+66{e}^{-0.08\cdot 4}≈{123}^{∘}\text{F},
$$

rounded to the nearest integer.


## Generated default operations exhaust

The temperature $T(t),$ in degrees Fahrenheit, of an exhaust pipe of a motorcycle can be modeled by the differential equation

$$
\frac{dT}{dt}=-0.04(T-64)
$$

where $t>0$ is the time, measured in minutes. If the initial temperature of the exhaust pipe is ${174}^{∘}F,$ calculate its temperature after $12$ minutes. Round your answer to the nearest integer.

- ${132}^{∘}\text{F}$ **(correct)**
- ${68}^{∘}\text{F}$
- ${106}^{∘}\text{F}$
- ${172}^{∘}\text{F}$
- ${151}^{∘}\text{F}$

**Worked solution**

We're told that the temperature of the exhaust pipe of a motorcycle is modeled by the inhibited decay equation

$$
\frac{dT}{dt}=-0.04(T-64).
$$

First, we integrate our differential equation by separating the variables:

$$
\begin{aligned}\frac{dT}{T-64} & =-0.04\,dt \\ \int \frac{dT}{T-64} & =-\int 0.04\,\text{d}t \\ \operatorname{ln}⁡|T-64| & =-0.04t+C\end{aligned}
$$

Since this is the solution to an inhibited decay equation, we have $T-64>0$ for all $t>0.$
Next, we solve for $T(t),$ as follows:

$$
\begin{aligned}T-64 & ={e}^{-0.04t+C} \\ T-64 & ={e}^{C}{e}^{-0.04t} \\ T-64 & =K{e}^{-0.04t} \\ T & =64+K{e}^{-0.04t}\end{aligned}
$$

Note that $K={e}^{C}$ is a constant of integration. 

We're told that the initial temperature of the exhaust pipe was ${174}^{∘}F.$ So, we apply the initial condition $T(0)=174,$ and solve for $K:$

$$
\begin{aligned}174 & =64+K{e}^{0} \\ 174 & =64+K \\ K & =110\end{aligned}
$$

Therefore, the solution to our initial value problem is

$$
T(t)=64+110{e}^{-0.04t}.
$$

Finally, the temperature of the exhaust pipe after $t=12$ minutes is

$$
T(12)=64+110{e}^{-0.04\cdot 12}≈{132}^{∘}\text{F},
$$

rounded to the nearest integer.


## Original q-15595 — exact raw replay

The temperature $T(t),$ in degrees Celsius, of a cup of coffee can be modeled by the differential equation

$$
\frac{dT}{dt}=-0.05(T-25)
$$

where $t>0$ is the time, measured in minutes. If the initial temperature of the coffee is ${100}^{∘}C,$ calculate the temperature of the coffee after $6$ minutes. Round your answer to the nearest integer.

- ${85}^{∘}\text{C}$
- ${79}^{∘}\text{C}$
- ${83}^{∘}\text{C}$
- ${77}^{∘}\text{C}$
- ${81}^{∘}\text{C}$ **(correct)**

**Worked solution**

We're told that the temperature of the cup of coffee is modeled by the inhibited decay equation

$$
\frac{dT}{dt}=-0.05(T-25).
$$

First, we integrate our differential equation by separating the variables:

$$
\begin{aligned}\frac{dT}{T-25} & =-0.05\,dt \\ \int \frac{dT}{T-25} & =-\int 0.05\,\text{d}t \\ \operatorname{ln}⁡|T-25| & =-0.05t+C\end{aligned}
$$

Since this is the solution to an inhibited decay equation, we have $T-25>0$ for all $t>0.$
Next, we solve for $T(t),$ as follows:

$$
\begin{aligned}T-25 & ={e}^{-0.05t+C} \\ T-25 & ={e}^{C}{e}^{-0.05t} \\ T-25 & =K{e}^{-0.05t} \\ T & =25+K{e}^{-0.05t}\end{aligned}
$$

Note that $K={e}^{C}$ is a constant of integration. 

We're told that the initial temperature of the coffee was ${100}^{∘}C.$ So, we apply the initial condition $T(0)=100,$ and solve for $K:$

$$
\begin{aligned}100 & =25+K{e}^{0} \\ 100 & =25+K \\ K & =75\end{aligned}
$$

Therefore, the solution to our initial value problem is

$$
T(t)=25+75{e}^{-0.05t}.
$$

Finally, the temperature of the coffee after $t=6$ minutes is

$$
T(6)=25+75{e}^{-0.05\cdot 6}≈{81}^{∘}\text{C},
$$

rounded to the nearest integer.


## Changed observed profile q-15595 — underdetermined scalar intent

The temperature $T(t),$ in degrees Celsius, of a cup of coffee can be modeled by the differential equation

$$
\frac{dT}{dt}=-0.05(T-26)
$$

where $t>0$ is the time, measured in minutes. If the initial temperature of the coffee is ${99}^{∘}C,$ calculate the temperature of the coffee after $7$ minutes. Round your answer to the nearest integer.

- ${81}^{∘}\text{C}$
- ${77}^{∘}\text{C}$ **(correct)**
- ${73}^{∘}\text{C}$
- ${75}^{∘}\text{C}$
- ${79}^{∘}\text{C}$

**Worked solution**

We're told that the temperature of the cup of coffee is modeled by the inhibited decay equation

$$
\frac{dT}{dt}=-0.05(T-26).
$$

First, we integrate our differential equation by separating the variables:

$$
\begin{aligned}\frac{dT}{T-26} & =-0.05\,dt \\ \int \frac{dT}{T-26} & =-\int 0.05\,\text{d}t \\ \operatorname{ln}⁡|T-26| & =-0.05t+C\end{aligned}
$$

Since this is the solution to an inhibited decay equation, we have $T-26>0$ for all $t>0.$
Next, we solve for $T(t),$ as follows:

$$
\begin{aligned}T-26 & ={e}^{-0.05t+C} \\ T-26 & ={e}^{C}{e}^{-0.05t} \\ T-26 & =K{e}^{-0.05t} \\ T & =26+K{e}^{-0.05t}\end{aligned}
$$

Note that $K={e}^{C}$ is a constant of integration. 

We're told that the initial temperature of the coffee was ${99}^{∘}C.$ So, we apply the initial condition $T(0)=99,$ and solve for $K:$

$$
\begin{aligned}99 & =26+K{e}^{0} \\ 99 & =26+K \\ K & =73\end{aligned}
$$

Therefore, the solution to our initial value problem is

$$
T(t)=26+73{e}^{-0.05t}.
$$

Finally, the temperature of the coffee after $t=7$ minutes is

$$
T(7)=26+73{e}^{-0.05\cdot 7}≈{77}^{∘}\text{C},
$$

rounded to the nearest integer.


## Generated default operations coffee

The temperature $T(t),$ in degrees Celsius, of a cup of coffee can be modeled by the differential equation

$$
\frac{dT}{dt}=-0.18(T-23)
$$

where $t>0$ is the time, measured in minutes. If the initial temperature of the coffee is ${81}^{∘}C,$ calculate the temperature of the coffee after $5$ minutes. Round your answer to the nearest integer.

- ${60}^{∘}\text{C}$
- ${24}^{∘}\text{C}$
- ${56}^{∘}\text{C}$
- ${47}^{∘}\text{C}$ **(correct)**
- ${33}^{∘}\text{C}$

**Worked solution**

We're told that the temperature of the cup of coffee is modeled by the inhibited decay equation

$$
\frac{dT}{dt}=-0.18(T-23).
$$

First, we integrate our differential equation by separating the variables:

$$
\begin{aligned}\frac{dT}{T-23} & =-0.18\,dt \\ \int \frac{dT}{T-23} & =-\int 0.18\,\text{d}t \\ \operatorname{ln}⁡|T-23| & =-0.18t+C\end{aligned}
$$

Since this is the solution to an inhibited decay equation, we have $T-23>0$ for all $t>0.$
Next, we solve for $T(t),$ as follows:

$$
\begin{aligned}T-23 & ={e}^{-0.18t+C} \\ T-23 & ={e}^{C}{e}^{-0.18t} \\ T-23 & =K{e}^{-0.18t} \\ T & =23+K{e}^{-0.18t}\end{aligned}
$$

Note that $K={e}^{C}$ is a constant of integration. 

We're told that the initial temperature of the coffee was ${81}^{∘}C.$ So, we apply the initial condition $T(0)=81,$ and solve for $K:$

$$
\begin{aligned}81 & =23+K{e}^{0} \\ 81 & =23+K \\ K & =58\end{aligned}
$$

Therefore, the solution to our initial value problem is

$$
T(t)=23+58{e}^{-0.18t}.
$$

Finally, the temperature of the coffee after $t=5$ minutes is

$$
T(5)=23+58{e}^{-0.18\cdot 5}≈{47}^{∘}\text{C},
$$

rounded to the nearest integer.


## Original q-107118 — exact raw replay

The temperature $T(t),$ in degrees Celsius, of a cooling iron can be modeled by the differential equation

$$
\frac{dT}{dt}=-0.1(T-28)
$$

where $t>0$ is the time, measured in minutes. If the initial temperature of the iron is ${140}^{∘}C,$ calculate its temperature after $5$ minutes. Round your answer to the nearest integer.

- ${79}^{∘}\text{C}$
- ${92}^{∘}\text{C}$
- ${96}^{∘}\text{C}$ **(correct)**
- ${81}^{∘}\text{C}$
- ${76}^{∘}\text{C}$

**Worked solution**

We're told that the temperature of the cooling iron is modeled by the inhibited decay equation

$$
\frac{dT}{dt}=-0.1(T-28).
$$

First, we integrate our differential equation by separating the variables:

$$
\begin{aligned}\frac{dT}{T-28} & =-0.1\,dt \\ \int \frac{dT}{T-28} & =-\int 0.1\,\text{d}t \\ \operatorname{ln}⁡|T-28| & =-0.1t+C\end{aligned}
$$

Since this is the solution to an inhibited decay equation, we have $T-28>0$ for all $t>0.$
Next, we solve for $T(t),$ as follows:

$$
\begin{aligned}T-28 & ={e}^{-0.1t+C} \\ T-28 & ={e}^{C}{e}^{-0.1t} \\ T-28 & =K{e}^{-0.1t} \\ T & =28+K{e}^{-0.1t}\end{aligned}
$$

Note that $K={e}^{C}$ is a constant of integration. 

We're told that the initial temperature of the iron was ${140}^{∘}C.$ So, we apply the initial condition $T(0)=140,$ and solve for $K:$

$$
\begin{aligned}140 & =28+K{e}^{0} \\ 140 & =28+K \\ K & =112\end{aligned}
$$

Therefore, the solution to our initial value problem is

$$
T(t)=28+112{e}^{-0.1t}.
$$

Finally, the temperature of the iron after $t=5$ minutes is

$$
T(5)=28+112{e}^{-0.1\cdot 5}≈{96}^{∘}\text{C},
$$

rounded to the nearest integer.


## Changed observed profile q-107118 — underdetermined scalar intent

The temperature $T(t),$ in degrees Celsius, of a cooling iron can be modeled by the differential equation

$$
\frac{dT}{dt}=-0.1(T-29)
$$

where $t>0$ is the time, measured in minutes. If the initial temperature of the iron is ${141}^{∘}C,$ calculate its temperature after $6$ minutes. Round your answer to the nearest integer.

- ${73}^{∘}\text{C}$
- ${70}^{∘}\text{C}$
- ${75}^{∘}\text{C}$
- ${86}^{∘}\text{C}$
- ${90}^{∘}\text{C}$ **(correct)**

**Worked solution**

We're told that the temperature of the cooling iron is modeled by the inhibited decay equation

$$
\frac{dT}{dt}=-0.1(T-29).
$$

First, we integrate our differential equation by separating the variables:

$$
\begin{aligned}\frac{dT}{T-29} & =-0.1\,dt \\ \int \frac{dT}{T-29} & =-\int 0.1\,\text{d}t \\ \operatorname{ln}⁡|T-29| & =-0.1t+C\end{aligned}
$$

Since this is the solution to an inhibited decay equation, we have $T-29>0$ for all $t>0.$
Next, we solve for $T(t),$ as follows:

$$
\begin{aligned}T-29 & ={e}^{-0.1t+C} \\ T-29 & ={e}^{C}{e}^{-0.1t} \\ T-29 & =K{e}^{-0.1t} \\ T & =29+K{e}^{-0.1t}\end{aligned}
$$

Note that $K={e}^{C}$ is a constant of integration. 

We're told that the initial temperature of the iron was ${141}^{∘}C.$ So, we apply the initial condition $T(0)=141,$ and solve for $K:$

$$
\begin{aligned}141 & =29+K{e}^{0} \\ 141 & =29+K \\ K & =112\end{aligned}
$$

Therefore, the solution to our initial value problem is

$$
T(t)=29+112{e}^{-0.1t}.
$$

Finally, the temperature of the iron after $t=6$ minutes is

$$
T(6)=29+112{e}^{-0.1\cdot 6}≈{90}^{∘}\text{C},
$$

rounded to the nearest integer.


## Generated default operations iron

The temperature $T(t),$ in degrees Celsius, of a cooling iron can be modeled by the differential equation

$$
\frac{dT}{dt}=-0.06(T-23)
$$

where $t>0$ is the time, measured in minutes. If the initial temperature of the iron is ${131}^{∘}C,$ calculate its temperature after $7$ minutes. Round your answer to the nearest integer.

- ${111}^{∘}\text{C}$
- ${70}^{∘}\text{C}$
- ${109}^{∘}\text{C}$
- ${94}^{∘}\text{C}$ **(correct)**
- ${71}^{∘}\text{C}$

**Worked solution**

We're told that the temperature of the cooling iron is modeled by the inhibited decay equation

$$
\frac{dT}{dt}=-0.06(T-23).
$$

First, we integrate our differential equation by separating the variables:

$$
\begin{aligned}\frac{dT}{T-23} & =-0.06\,dt \\ \int \frac{dT}{T-23} & =-\int 0.06\,\text{d}t \\ \operatorname{ln}⁡|T-23| & =-0.06t+C\end{aligned}
$$

Since this is the solution to an inhibited decay equation, we have $T-23>0$ for all $t>0.$
Next, we solve for $T(t),$ as follows:

$$
\begin{aligned}T-23 & ={e}^{-0.06t+C} \\ T-23 & ={e}^{C}{e}^{-0.06t} \\ T-23 & =K{e}^{-0.06t} \\ T & =23+K{e}^{-0.06t}\end{aligned}
$$

Note that $K={e}^{C}$ is a constant of integration. 

We're told that the initial temperature of the iron was ${131}^{∘}C.$ So, we apply the initial condition $T(0)=131,$ and solve for $K:$

$$
\begin{aligned}131 & =23+K{e}^{0} \\ 131 & =23+K \\ K & =108\end{aligned}
$$

Therefore, the solution to our initial value problem is

$$
T(t)=23+108{e}^{-0.06t}.
$$

Finally, the temperature of the iron after $t=7$ minutes is

$$
T(7)=23+108{e}^{-0.06\cdot 7}≈{94}^{∘}\text{C},
$$

rounded to the nearest integer.


## Original q-107120 — exact raw replay

The temperature $T(t),$ in degrees Fahrenheit, of a fresh-baked cake can be modeled by the differential equation

$$
\frac{dT}{dt}=-0.09(T-70)
$$

where $t>0$ is the time, measured in minutes. If the initial temperature of the cake is ${340}^{∘}F,$ calculate the temperature of the cake after $8$ minutes. Round your answer to the nearest integer.

- ${194}^{∘}\text{F}$
- ${223}^{∘}\text{F}$
- ${198}^{∘}\text{F}$
- ${189}^{∘}\text{F}$
- ${201}^{∘}\text{F}$ **(correct)**

**Worked solution**

We're told that the temperature of the fresh-baked cake is modeled by the inhibited decay equation

$$
\frac{dT}{dt}=-0.09(T-70).
$$

First, we integrate our differential equation by separating the variables:

$$
\begin{aligned}\frac{dT}{T-70} & =-0.09\,dt \\ \int \frac{dT}{T-70} & =-\int 0.09\,\text{d}t \\ \operatorname{ln}⁡|T-70| & =-0.09t+C\end{aligned}
$$

Since this is the solution to an inhibited decay equation, we have $T-70>0$ for all $t>0.$
Next, we solve for $T(t),$ as follows:

$$
\begin{aligned}T-70 & ={e}^{-0.09t+C} \\ T-70 & ={e}^{C}{e}^{-0.09t} \\ T-70 & =K{e}^{-0.09t} \\ T & =70+K{e}^{-0.09t}\end{aligned}
$$

Note that $K={e}^{C}$ is a constant of integration. 

We're told that the initial temperature of the cake was ${340}^{∘}F.$ So, we apply the initial condition $T(0)=340,$ and solve for $K:$

$$
\begin{aligned}340 & =70+K{e}^{0} \\ 340 & =70+K \\ K & =270\end{aligned}
$$

Therefore, the solution to our initial value problem is

$$
T(t)=70+270{e}^{-0.09t}.
$$

Finally, the temperature of the cake after $t=8$ minutes is

$$
T(8)=70+270{e}^{-0.09\cdot 8}≈{201}^{∘}\text{F},
$$

rounded to the nearest integer.


## Changed observed profile q-107120 — underdetermined scalar intent

The temperature $T(t),$ in degrees Fahrenheit, of a fresh-baked cake can be modeled by the differential equation

$$
\frac{dT}{dt}=-0.09(T-71)
$$

where $t>0$ is the time, measured in minutes. If the initial temperature of the cake is ${341}^{∘}F,$ calculate the temperature of the cake after $9$ minutes. Round your answer to the nearest integer.

- ${184}^{∘}\text{F}$
- ${191}^{∘}\text{F}$ **(correct)**
- ${179}^{∘}\text{F}$
- ${213}^{∘}\text{F}$
- ${188}^{∘}\text{F}$

**Worked solution**

We're told that the temperature of the fresh-baked cake is modeled by the inhibited decay equation

$$
\frac{dT}{dt}=-0.09(T-71).
$$

First, we integrate our differential equation by separating the variables:

$$
\begin{aligned}\frac{dT}{T-71} & =-0.09\,dt \\ \int \frac{dT}{T-71} & =-\int 0.09\,\text{d}t \\ \operatorname{ln}⁡|T-71| & =-0.09t+C\end{aligned}
$$

Since this is the solution to an inhibited decay equation, we have $T-71>0$ for all $t>0.$
Next, we solve for $T(t),$ as follows:

$$
\begin{aligned}T-71 & ={e}^{-0.09t+C} \\ T-71 & ={e}^{C}{e}^{-0.09t} \\ T-71 & =K{e}^{-0.09t} \\ T & =71+K{e}^{-0.09t}\end{aligned}
$$

Note that $K={e}^{C}$ is a constant of integration. 

We're told that the initial temperature of the cake was ${341}^{∘}F.$ So, we apply the initial condition $T(0)=341,$ and solve for $K:$

$$
\begin{aligned}341 & =71+K{e}^{0} \\ 341 & =71+K \\ K & =270\end{aligned}
$$

Therefore, the solution to our initial value problem is

$$
T(t)=71+270{e}^{-0.09t}.
$$

Finally, the temperature of the cake after $t=9$ minutes is

$$
T(9)=71+270{e}^{-0.09\cdot 9}≈{191}^{∘}\text{F},
$$

rounded to the nearest integer.


## Generated default operations cake

The temperature $T(t),$ in degrees Fahrenheit, of a fresh-baked cake can be modeled by the differential equation

$$
\frac{dT}{dt}=-0.07(T-61)
$$

where $t>0$ is the time, measured in minutes. If the initial temperature of the cake is ${325}^{∘}F,$ calculate the temperature of the cake after $10$ minutes. Round your answer to the nearest integer.

- ${131}^{∘}\text{F}$
- ${126}^{∘}\text{F}$
- ${247}^{∘}\text{F}$
- ${192}^{∘}\text{F}$ **(correct)**
- ${222}^{∘}\text{F}$

**Worked solution**

We're told that the temperature of the fresh-baked cake is modeled by the inhibited decay equation

$$
\frac{dT}{dt}=-0.07(T-61).
$$

First, we integrate our differential equation by separating the variables:

$$
\begin{aligned}\frac{dT}{T-61} & =-0.07\,dt \\ \int \frac{dT}{T-61} & =-\int 0.07\,\text{d}t \\ \operatorname{ln}⁡|T-61| & =-0.07t+C\end{aligned}
$$

Since this is the solution to an inhibited decay equation, we have $T-61>0$ for all $t>0.$
Next, we solve for $T(t),$ as follows:

$$
\begin{aligned}T-61 & ={e}^{-0.07t+C} \\ T-61 & ={e}^{C}{e}^{-0.07t} \\ T-61 & =K{e}^{-0.07t} \\ T & =61+K{e}^{-0.07t}\end{aligned}
$$

Note that $K={e}^{C}$ is a constant of integration. 

We're told that the initial temperature of the cake was ${325}^{∘}F.$ So, we apply the initial condition $T(0)=325,$ and solve for $K:$

$$
\begin{aligned}325 & =61+K{e}^{0} \\ 325 & =61+K \\ K & =264\end{aligned}
$$

Therefore, the solution to our initial value problem is

$$
T(t)=61+264{e}^{-0.07t}.
$$

Finally, the temperature of the cake after $t=10$ minutes is

$$
T(10)=61+264{e}^{-0.07\cdot 10}≈{192}^{∘}\text{F},
$$

rounded to the nearest integer.


## Original q-107129 — exact raw replay

The temperature $T(t),$ in degrees Celsius, of a compressor of a refrigerator can be modeled by the differential equation

$$
\frac{dT}{dt}=-0.12(T-21)
$$

where $t>0$ is the time, measured in minutes. If the initial temperature of the compressor is ${65}^{∘}C,$ calculate the temperature of the compressor after $8$ minutes. Round your answer to the nearest integer.

- ${43}^{∘}\text{C}$
- ${38}^{∘}\text{C}$ **(correct)**
- ${31}^{∘}\text{C}$
- ${58}^{∘}\text{C}$
- ${29}^{∘}\text{C}$

**Worked solution**

We're told that the temperature of the compressor of a refrigerator is modeled by the inhibited decay equation

$$
\frac{dT}{dt}=-0.12(T-21).
$$

First, we integrate our differential equation by separating the variables:

$$
\begin{aligned}\frac{dT}{T-21} & =-0.12\,dt \\ \int \frac{dT}{T-21} & =-\int 0.12\,\text{d}t \\ \operatorname{ln}⁡|T-21| & =-0.12t+C\end{aligned}
$$

Since this is the solution to an inhibited decay equation, we have $T-21>0$ for all $t>0.$
Next, we solve for $T(t),$ as follows:

$$
\begin{aligned}T-21 & ={e}^{-0.12t+C} \\ T-21 & ={e}^{C}{e}^{-0.12t} \\ T-21 & =K{e}^{-0.12t} \\ T & =21+K{e}^{-0.12t}\end{aligned}
$$

Note that $K={e}^{C}$ is a constant of integration. 

We're told that the initial temperature of the compressor was ${65}^{∘}C.$ So, we apply the initial condition $T(0)=65,$ and solve for $K:$

$$
\begin{aligned}65 & =21+K{e}^{0} \\ 65 & =21+K \\ K & =44\end{aligned}
$$

Therefore, the solution to our initial value problem is

$$
T(t)=21+44{e}^{-0.12t}.
$$

Finally, the temperature of the compressor after $t=8$ minutes is

$$
T(8)=21+44{e}^{-0.12\cdot 8}≈{38}^{∘}\text{C},
$$

rounded to the nearest integer.


## Changed observed profile q-107129 — underdetermined scalar intent

The temperature $T(t),$ in degrees Celsius, of a compressor of a refrigerator can be modeled by the differential equation

$$
\frac{dT}{dt}=-0.12(T-22)
$$

where $t>0$ is the time, measured in minutes. If the initial temperature of the compressor is ${66}^{∘}C,$ calculate the temperature of the compressor after $9$ minutes. Round your answer to the nearest integer.

- ${42}^{∘}\text{C}$
- ${28}^{∘}\text{C}$
- ${57}^{∘}\text{C}$
- ${37}^{∘}\text{C}$ **(correct)**
- ${30}^{∘}\text{C}$

**Worked solution**

We're told that the temperature of the compressor of a refrigerator is modeled by the inhibited decay equation

$$
\frac{dT}{dt}=-0.12(T-22).
$$

First, we integrate our differential equation by separating the variables:

$$
\begin{aligned}\frac{dT}{T-22} & =-0.12\,dt \\ \int \frac{dT}{T-22} & =-\int 0.12\,\text{d}t \\ \operatorname{ln}⁡|T-22| & =-0.12t+C\end{aligned}
$$

Since this is the solution to an inhibited decay equation, we have $T-22>0$ for all $t>0.$
Next, we solve for $T(t),$ as follows:

$$
\begin{aligned}T-22 & ={e}^{-0.12t+C} \\ T-22 & ={e}^{C}{e}^{-0.12t} \\ T-22 & =K{e}^{-0.12t} \\ T & =22+K{e}^{-0.12t}\end{aligned}
$$

Note that $K={e}^{C}$ is a constant of integration. 

We're told that the initial temperature of the compressor was ${66}^{∘}C.$ So, we apply the initial condition $T(0)=66,$ and solve for $K:$

$$
\begin{aligned}66 & =22+K{e}^{0} \\ 66 & =22+K \\ K & =44\end{aligned}
$$

Therefore, the solution to our initial value problem is

$$
T(t)=22+44{e}^{-0.12t}.
$$

Finally, the temperature of the compressor after $t=9$ minutes is

$$
T(9)=22+44{e}^{-0.12\cdot 9}≈{37}^{∘}\text{C},
$$

rounded to the nearest integer.


## Generated default operations compressor

The temperature $T(t),$ in degrees Celsius, of a compressor of a refrigerator can be modeled by the differential equation

$$
\frac{dT}{dt}=-0.13(T-24)
$$

where $t>0$ is the time, measured in minutes. If the initial temperature of the compressor is ${99}^{∘}C,$ calculate the temperature of the compressor after $7$ minutes. Round your answer to the nearest integer.

- ${54}^{∘}\text{C}$ **(correct)**
- ${36}^{∘}\text{C}$
- ${64}^{∘}\text{C}$
- ${30}^{∘}\text{C}$
- ${72}^{∘}\text{C}$

**Worked solution**

We're told that the temperature of the compressor of a refrigerator is modeled by the inhibited decay equation

$$
\frac{dT}{dt}=-0.13(T-24).
$$

First, we integrate our differential equation by separating the variables:

$$
\begin{aligned}\frac{dT}{T-24} & =-0.13\,dt \\ \int \frac{dT}{T-24} & =-\int 0.13\,\text{d}t \\ \operatorname{ln}⁡|T-24| & =-0.13t+C\end{aligned}
$$

Since this is the solution to an inhibited decay equation, we have $T-24>0$ for all $t>0.$
Next, we solve for $T(t),$ as follows:

$$
\begin{aligned}T-24 & ={e}^{-0.13t+C} \\ T-24 & ={e}^{C}{e}^{-0.13t} \\ T-24 & =K{e}^{-0.13t} \\ T & =24+K{e}^{-0.13t}\end{aligned}
$$

Note that $K={e}^{C}$ is a constant of integration. 

We're told that the initial temperature of the compressor was ${99}^{∘}C.$ So, we apply the initial condition $T(0)=99,$ and solve for $K:$

$$
\begin{aligned}99 & =24+K{e}^{0} \\ 99 & =24+K \\ K & =75\end{aligned}
$$

Therefore, the solution to our initial value problem is

$$
T(t)=24+75{e}^{-0.13t}.
$$

Finally, the temperature of the compressor after $t=7$ minutes is

$$
T(7)=24+75{e}^{-0.13\cdot 7}≈{54}^{∘}\text{C},
$$

rounded to the nearest integer.


## Original q-15384 — exact raw replay

A thermometer is placed into a water bath and displays a reading of ${50}^{∘}C.$ The thermometer is then transferred to a ${10}^{∘}C$ water bath, and its reading begins to decrease. After $5$ minutes, the thermometer reading is ${40}^{∘}C.$ To the nearest minute, how long does it take for the thermometer to register a reading of ${30}^{∘}C?$ 

*Hint: You may assume that the temperature reading $T(t)$ of the thermometer decreases at a rate that obeys Newton's law of cooling, where $T$ is measured in degrees Celsius and $t>0$ is the time, in minutes, since the thermometer was transferred into the ${10}^{∘}C$ water bath.*

- $13\,\text{min}$
- $15\,\text{min}$
- $12\,\text{min}$ **(correct)**
- $10\,\text{min}$
- $14\,\text{min}$

**Worked solution**

Newton's law of cooling states that the rate at which the temperature $T(t)$ of a body changes is proportional to the difference between its temperature and its surroundings. Therefore, we have the inhibited decay equation

$$
\frac{\text{d}T}{\text{d}t}=-k(T-{T}_{S}),
$$

where ${T}_{S}$ is the temperature of the surroundings, and $k>0$ is a constant of proportionality.

In our case, ${T}_{S}={10}^{∘}\text{C},$ and we have

$$
\frac{\text{d}T}{\text{d}t}=-k(T-10).
$$

First, we integrate our differential equation by separating the variables:

$$
\begin{aligned}\frac{dT}{T-10} & =-k\,dt \\ \int \frac{dT}{T-10} & =-k\int dt \\ \operatorname{ln}⁡|T-10| & =-kt+C\end{aligned}
$$

Since this is the solution to an inhibited decay equation, we have $T-10>0$ for all $t>0.$
Next, we solve for $T(t),$ as follows:

$$
\begin{aligned}T-10 & ={e}^{-kt+C} \\ T-10 & ={e}^{C}{e}^{-kt} \\ T-10 & =K{e}^{-kt} \\ T & =10+K{e}^{-kt}\end{aligned}
$$

Note that $K={e}^{C}$ is a constant of integration. 

We're told that the initial temperature reading was ${50}^{∘}C.$ So, we apply the initial condition $T(0)=50,$ and solve for $K:$

$$
\begin{aligned}50 & =10+K{e}^{0} \\ 50 & =10+K \\ K & =40\end{aligned}
$$

Therefore, we have the following expression for $T(t):$

$$
T(t)=10+40{e}^{-kt}
$$

We're also told that, after $5$ minutes, the thermometer reading is ${40}^{∘}C.$ So, applying the condition $T(5)=40,$ we can solve for $k:$

$$
\begin{aligned}40 & =10+40{e}^{-5k} \\ 30 & =40{e}^{-5k} \\ \frac{3}{4} & ={e}^{-5k} \\ \operatorname{ln}⁡(\frac{3}{4}) & =-5k \\ k & =-\frac{1}{5}\operatorname{ln}⁡(\frac{3}{4})\end{aligned}
$$

Finally, let ${t}_{1}$ be the time when the thermometer reads ${30}^{∘}C.$ Then, we have

$$
\begin{aligned}T({t}_{1}) & =30 \\ 10+40{e}^{-k{t}_{1}} & =30 \\ 40{e}^{-k{t}_{1}} & =20 \\ {e}^{-k{t}_{1}} & =\frac{1}{2} \\ -k{t}_{1} & =\operatorname{ln}⁡(\frac{1}{2}) \\ {t}_{1} & =-\frac{1}{k}\operatorname{ln}⁡(\frac{1}{2}).\end{aligned}
$$

Substituting in our value for $k,$ we conclude that the thermometer will read ${30}^{∘}C$ after

$$
{t}_{1}=\frac{-\operatorname{ln}⁡(\frac{1}{2})}{-\frac{1}{5}\operatorname{ln}⁡(\frac{3}{4})}≈12\,\text{min},
$$

rounded to the nearest minute.


## Changed observed profile q-15384 — underdetermined scalar intent

A thermometer is placed into a water bath and displays a reading of ${51}^{∘}C.$ The thermometer is then transferred to a ${11}^{∘}C$ water bath, and its reading begins to decrease. After $6$ minutes, the thermometer reading is ${41}^{∘}C.$ To the nearest minute, how long does it take for the thermometer to register a reading of ${31}^{∘}C?$ 

*Hint: You may assume that the temperature reading $T(t)$ of the thermometer decreases at a rate that obeys Newton's law of cooling, where $T$ is measured in degrees Celsius and $t>0$ is the time, in minutes, since the thermometer was transferred into the ${11}^{∘}C$ water bath.*

- $15\,\text{min}$
- $16\,\text{min}$
- $12\,\text{min}$
- $17\,\text{min}$
- $14\,\text{min}$ **(correct)**

**Worked solution**

Newton's law of cooling states that the rate at which the temperature $T(t)$ of a body changes is proportional to the difference between its temperature and its surroundings. Therefore, we have the inhibited decay equation

$$
\frac{\text{d}T}{\text{d}t}=-k(T-{T}_{S}),
$$

where ${T}_{S}$ is the temperature of the surroundings, and $k>0$ is a constant of proportionality.

In our case, ${T}_{S}={11}^{∘}\text{C},$ and we have

$$
\frac{\text{d}T}{\text{d}t}=-k(T-11).
$$

First, we integrate our differential equation by separating the variables:

$$
\begin{aligned}\frac{dT}{T-11} & =-k\,dt \\ \int \frac{dT}{T-11} & =-k\int dt \\ \operatorname{ln}⁡|T-11| & =-kt+C\end{aligned}
$$

Since this is the solution to an inhibited decay equation, we have $T-11>0$ for all $t>0.$
Next, we solve for $T(t),$ as follows:

$$
\begin{aligned}T-11 & ={e}^{-kt+C} \\ T-11 & ={e}^{C}{e}^{-kt} \\ T-11 & =K{e}^{-kt} \\ T & =11+K{e}^{-kt}\end{aligned}
$$

Note that $K={e}^{C}$ is a constant of integration. 

We're told that the initial temperature reading was ${51}^{∘}C.$ So, we apply the initial condition $T(0)=51,$ and solve for $K:$

$$
\begin{aligned}51 & =11+K{e}^{0} \\ 51 & =11+K \\ K & =40\end{aligned}
$$

Therefore, we have the following expression for $T(t):$

$$
T(t)=11+40{e}^{-kt}
$$

We're also told that, after $6$ minutes, the thermometer reading is ${41}^{∘}C.$ So, applying the condition $T(6)=41,$ we can solve for $k:$

$$
\begin{aligned}41 & =11+40{e}^{-6k} \\ 30 & =40{e}^{-6k} \\ \frac{3}{4} & ={e}^{-6k} \\ \operatorname{ln}⁡(\frac{3}{4}) & =-6k \\ k & =-\frac{1}{6}\operatorname{ln}⁡(\frac{3}{4})\end{aligned}
$$

Finally, let ${t}_{1}$ be the time when the thermometer reads ${31}^{∘}C.$ Then, we have

$$
\begin{aligned}T({t}_{1}) & =31 \\ 11+40{e}^{-k{t}_{1}} & =31 \\ 40{e}^{-k{t}_{1}} & =20 \\ {e}^{-k{t}_{1}} & =\frac{1}{2} \\ -k{t}_{1} & =\operatorname{ln}⁡(\frac{1}{2}) \\ {t}_{1} & =-\frac{1}{k}\operatorname{ln}⁡(\frac{1}{2}).\end{aligned}
$$

Substituting in our value for $k,$ we conclude that the thermometer will read ${31}^{∘}C$ after

$$
{t}_{1}=\frac{-\operatorname{ln}⁡(\frac{1}{2})}{-\frac{1}{6}\operatorname{ln}⁡(\frac{3}{4})}≈14\,\text{min},
$$

rounded to the nearest minute.


## Generated default operations bath

A thermometer is placed into a water bath and displays a reading of ${100}^{∘}C.$ The thermometer is then transferred to a ${24}^{∘}C$ water bath, and its reading begins to decrease. After $2$ minutes, the thermometer reading is ${95}^{∘}C.$ To the nearest minute, how long does it take for the thermometer to register a reading of ${48}^{∘}C?$ 

*Hint: You may assume that the temperature reading $T(t)$ of the thermometer decreases at a rate that obeys Newton's law of cooling, where $T$ is measured in degrees Celsius and $t>0$ is the time, in minutes, since the thermometer was transferred into the ${24}^{∘}C$ water bath.*

- $17\,\text{min}$
- $34\,\text{min}$ **(correct)**
- $22\,\text{min}$
- $68\,\text{min}$
- $29\,\text{min}$

**Worked solution**

Newton's law of cooling states that the rate at which the temperature $T(t)$ of a body changes is proportional to the difference between its temperature and its surroundings. Therefore, we have the inhibited decay equation

$$
\frac{\text{d}T}{\text{d}t}=-k(T-{T}_{S}),
$$

where ${T}_{S}$ is the temperature of the surroundings, and $k>0$ is a constant of proportionality.

In our case, ${T}_{S}={24}^{∘}\text{C},$ and we have

$$
\frac{\text{d}T}{\text{d}t}=-k(T-24).
$$

First, we integrate our differential equation by separating the variables:

$$
\begin{aligned}\frac{dT}{T-24} & =-k\,dt \\ \int \frac{dT}{T-24} & =-k\int dt \\ \operatorname{ln}⁡|T-24| & =-kt+C\end{aligned}
$$

Since this is the solution to an inhibited decay equation, we have $T-24>0$ for all $t>0.$
Next, we solve for $T(t),$ as follows:

$$
\begin{aligned}T-24 & ={e}^{-kt+C} \\ T-24 & ={e}^{C}{e}^{-kt} \\ T-24 & =K{e}^{-kt} \\ T & =24+K{e}^{-kt}\end{aligned}
$$

Note that $K={e}^{C}$ is a constant of integration. 

We're told that the initial temperature reading was ${100}^{∘}C.$ So, we apply the initial condition $T(0)=100,$ and solve for $K:$

$$
\begin{aligned}100 & =24+K{e}^{0} \\ 100 & =24+K \\ K & =76\end{aligned}
$$

Therefore, we have the following expression for $T(t):$

$$
T(t)=24+76{e}^{-kt}
$$

We're also told that, after $2$ minutes, the thermometer reading is ${95}^{∘}C.$ So, applying the condition $T(2)=95,$ we can solve for $k:$

$$
\begin{aligned}95 & =24+76{e}^{-2k} \\ 71 & =76{e}^{-2k} \\ \frac{71}{76} & ={e}^{-2k} \\ \operatorname{ln}⁡(\frac{71}{76}) & =-2k \\ k & =-\frac{1}{2}\operatorname{ln}⁡(\frac{71}{76})\end{aligned}
$$

Finally, let ${t}_{1}$ be the time when the thermometer reads ${48}^{∘}C.$ Then, we have

$$
\begin{aligned}T({t}_{1}) & =48 \\ 24+76{e}^{-k{t}_{1}} & =48 \\ 76{e}^{-k{t}_{1}} & =24 \\ {e}^{-k{t}_{1}} & =\frac{6}{19} \\ -k{t}_{1} & =\operatorname{ln}⁡(\frac{6}{19}) \\ {t}_{1} & =-\frac{1}{k}\operatorname{ln}⁡(\frac{6}{19}).\end{aligned}
$$

Substituting in our value for $k,$ we conclude that the thermometer will read ${48}^{∘}C$ after

$$
{t}_{1}=\frac{-\operatorname{ln}⁡(\frac{6}{19})}{-\frac{1}{2}\operatorname{ln}⁡(\frac{71}{76})}≈34\,\text{min},
$$

rounded to the nearest minute.


## Original q-107122 — exact raw replay

A thermometer is taken out of a room where the air temperature is ${72}^{∘}F$  and brought outside where the temperature is ${15}^{∘}F,$ and its reading begins to decrease. After $2$ minutes, the thermometer reading is ${54}^{∘}F.$ To the nearest minute, how long does it take for the thermometer to register a reading of ${25}^{∘}F?$ 

*Hint: You may assume that the temperature reading $T(t)$ of the thermometer decreases at a rate that obeys Newton's law of cooling, where $T$ is measured in degrees Fahrenheit and $t>0$ is the time, in minutes, since the thermometer was transferred outside to ${15}^{∘}F.$*

- $9\,\text{min}$ **(correct)**
- $15\,\text{min}$
- $11\,\text{min}$
- $13\,\text{min}$
- $8\,\text{min}$

**Worked solution**

Newton's law of cooling states that the rate at which the temperature $T(t)$ of a body changes is proportional to the difference between its temperature and its surroundings. Therefore, we have the inhibited decay equation

$$
\frac{\text{d}T}{\text{d}t}=-k(T-{T}_{S}),
$$

where ${T}_{S}$ is the temperature of the surroundings, and $k>0$ is a constant of proportionality.

In our case, ${T}_{S}={15}^{∘}\text{C},$ and we have

$$
\frac{\text{d}T}{\text{d}t}=-k(T-15).
$$

First, we integrate our differential equation by separating the variables:

$$
\begin{aligned}\frac{dT}{T-15} & =-k\,dt \\ \int \frac{dT}{T-15} & =-k\int dt \\ \operatorname{ln}⁡|T-15| & =-kt+C\end{aligned}
$$

Since this is the solution to an inhibited decay equation, we have $T-15>0$ for all $t>0.$
Next, we solve for $T(t),$ as follows:

$$
\begin{aligned}T-15 & ={e}^{-kt+C} \\ T-15 & ={e}^{C}{e}^{-kt} \\ T-15 & =K{e}^{-kt} \\ T & =15+K{e}^{-kt}\end{aligned}
$$

Note that $K={e}^{C}$ is a constant of integration. 

We're told that the initial temperature reading was ${72}^{∘}F.$ So, we apply the initial condition $T(0)=72,$ and solve for $K:$

$$
\begin{aligned}72 & =15+K{e}^{0} \\ 72 & =15+K \\ K & =57\end{aligned}
$$

Therefore, we have the following expression for $T(t):$

$$
T(t)=15+57{e}^{-kt}
$$

We're also told that, after $2$ minutes, the thermometer reading is ${54}^{∘}C.$ So, applying the condition $T(2)=54,$ we can solve for $k:$

$$
\begin{aligned}54 & =15+57{e}^{-2k} \\ 39 & =57{e}^{-2k} \\ \frac{39}{57} & ={e}^{-2k} \\ \operatorname{ln}⁡(\frac{39}{57}) & =-2k \\ k & =-\frac{1}{2}\operatorname{ln}⁡(\frac{39}{57})\end{aligned}
$$

Finally, let ${t}_{1}$ be the time when the thermometer reads ${25}^{∘}F.$ Then, we have

$$
\begin{aligned}T({t}_{1}) & =25 \\ 15+57{e}^{-k{t}_{1}} & =25 \\ 57{e}^{-k{t}_{1}} & =10 \\ {e}^{-k{t}_{1}} & =\frac{10}{57} \\ -k{t}_{1} & =\operatorname{ln}⁡(\frac{10}{57}) \\ {t}_{1} & =-\frac{1}{k}\operatorname{ln}⁡(\frac{10}{57}).\end{aligned}
$$

Substituting in our value for $k,$ we conclude that the thermometer will read ${25}^{∘}C$ after

$$
{t}_{1}=\frac{-\operatorname{ln}⁡(\frac{10}{57})}{-\frac{1}{2}\operatorname{ln}⁡(\frac{39}{57})}≈9\,\text{min},
$$

rounded to the nearest minute.


## Changed observed profile q-107122 — underdetermined scalar intent

A thermometer is taken out of a room where the air temperature is ${73}^{∘}F$  and brought outside where the temperature is ${16}^{∘}F,$ and its reading begins to decrease. After $3$ minutes, the thermometer reading is ${55}^{∘}F.$ To the nearest minute, how long does it take for the thermometer to register a reading of ${26}^{∘}F?$ 

*Hint: You may assume that the temperature reading $T(t)$ of the thermometer decreases at a rate that obeys Newton's law of cooling, where $T$ is measured in degrees Fahrenheit and $t>0$ is the time, in minutes, since the thermometer was transferred outside to ${16}^{∘}F.$*

- $14\,\text{min}$ **(correct)**
- $13\,\text{min}$
- $18\,\text{min}$
- $20\,\text{min}$
- $16\,\text{min}$

**Worked solution**

Newton's law of cooling states that the rate at which the temperature $T(t)$ of a body changes is proportional to the difference between its temperature and its surroundings. Therefore, we have the inhibited decay equation

$$
\frac{\text{d}T}{\text{d}t}=-k(T-{T}_{S}),
$$

where ${T}_{S}$ is the temperature of the surroundings, and $k>0$ is a constant of proportionality.

In our case, ${T}_{S}={16}^{∘}\text{C},$ and we have

$$
\frac{\text{d}T}{\text{d}t}=-k(T-16).
$$

First, we integrate our differential equation by separating the variables:

$$
\begin{aligned}\frac{dT}{T-16} & =-k\,dt \\ \int \frac{dT}{T-16} & =-k\int dt \\ \operatorname{ln}⁡|T-16| & =-kt+C\end{aligned}
$$

Since this is the solution to an inhibited decay equation, we have $T-16>0$ for all $t>0.$
Next, we solve for $T(t),$ as follows:

$$
\begin{aligned}T-16 & ={e}^{-kt+C} \\ T-16 & ={e}^{C}{e}^{-kt} \\ T-16 & =K{e}^{-kt} \\ T & =16+K{e}^{-kt}\end{aligned}
$$

Note that $K={e}^{C}$ is a constant of integration. 

We're told that the initial temperature reading was ${73}^{∘}F.$ So, we apply the initial condition $T(0)=73,$ and solve for $K:$

$$
\begin{aligned}73 & =16+K{e}^{0} \\ 73 & =16+K \\ K & =57\end{aligned}
$$

Therefore, we have the following expression for $T(t):$

$$
T(t)=16+57{e}^{-kt}
$$

We're also told that, after $3$ minutes, the thermometer reading is ${55}^{∘}C.$ So, applying the condition $T(3)=55,$ we can solve for $k:$

$$
\begin{aligned}55 & =16+57{e}^{-3k} \\ 39 & =57{e}^{-3k} \\ \frac{39}{57} & ={e}^{-3k} \\ \operatorname{ln}⁡(\frac{39}{57}) & =-3k \\ k & =-\frac{1}{3}\operatorname{ln}⁡(\frac{39}{57})\end{aligned}
$$

Finally, let ${t}_{1}$ be the time when the thermometer reads ${26}^{∘}F.$ Then, we have

$$
\begin{aligned}T({t}_{1}) & =26 \\ 16+57{e}^{-k{t}_{1}} & =26 \\ 57{e}^{-k{t}_{1}} & =10 \\ {e}^{-k{t}_{1}} & =\frac{10}{57} \\ -k{t}_{1} & =\operatorname{ln}⁡(\frac{10}{57}) \\ {t}_{1} & =-\frac{1}{k}\operatorname{ln}⁡(\frac{10}{57}).\end{aligned}
$$

Substituting in our value for $k,$ we conclude that the thermometer will read ${26}^{∘}C$ after

$$
{t}_{1}=\frac{-\operatorname{ln}⁡(\frac{10}{57})}{-\frac{1}{3}\operatorname{ln}⁡(\frac{39}{57})}≈14\,\text{min},
$$

rounded to the nearest minute.


## Generated default operations outside

A thermometer is taken out of a room where the air temperature is ${63}^{∘}F$  and brought outside where the temperature is ${13}^{∘}F,$ and its reading begins to decrease. After $10$ minutes, the thermometer reading is ${50}^{∘}F.$ To the nearest minute, how long does it take for the thermometer to register a reading of ${38}^{∘}F?$ 

*Hint: You may assume that the temperature reading $T(t)$ of the thermometer decreases at a rate that obeys Newton's law of cooling, where $T$ is measured in degrees Fahrenheit and $t>0$ is the time, in minutes, since the thermometer was transferred outside to ${13}^{∘}F.$*

- $17\,\text{min}$
- $12\,\text{min}$
- $23\,\text{min}$ **(correct)**
- $22\,\text{min}$
- $46\,\text{min}$

**Worked solution**

Newton's law of cooling states that the rate at which the temperature $T(t)$ of a body changes is proportional to the difference between its temperature and its surroundings. Therefore, we have the inhibited decay equation

$$
\frac{\text{d}T}{\text{d}t}=-k(T-{T}_{S}),
$$

where ${T}_{S}$ is the temperature of the surroundings, and $k>0$ is a constant of proportionality.

In our case, ${T}_{S}={13}^{∘}\text{F},$ and we have

$$
\frac{\text{d}T}{\text{d}t}=-k(T-13).
$$

First, we integrate our differential equation by separating the variables:

$$
\begin{aligned}\frac{dT}{T-13} & =-k\,dt \\ \int \frac{dT}{T-13} & =-k\int dt \\ \operatorname{ln}⁡|T-13| & =-kt+C\end{aligned}
$$

Since this is the solution to an inhibited decay equation, we have $T-13>0$ for all $t>0.$
Next, we solve for $T(t),$ as follows:

$$
\begin{aligned}T-13 & ={e}^{-kt+C} \\ T-13 & ={e}^{C}{e}^{-kt} \\ T-13 & =K{e}^{-kt} \\ T & =13+K{e}^{-kt}\end{aligned}
$$

Note that $K={e}^{C}$ is a constant of integration. 

We're told that the initial temperature reading was ${63}^{∘}F.$ So, we apply the initial condition $T(0)=63,$ and solve for $K:$

$$
\begin{aligned}63 & =13+K{e}^{0} \\ 63 & =13+K \\ K & =50\end{aligned}
$$

Therefore, we have the following expression for $T(t):$

$$
T(t)=13+50{e}^{-kt}
$$

We're also told that, after $10$ minutes, the thermometer reading is ${50}^{∘}F.$ So, applying the condition $T(10)=50,$ we can solve for $k:$

$$
\begin{aligned}50 & =13+50{e}^{-10k} \\ 37 & =50{e}^{-10k} \\ \frac{37}{50} & ={e}^{-10k} \\ \operatorname{ln}⁡(\frac{37}{50}) & =-10k \\ k & =-\frac{1}{10}\operatorname{ln}⁡(\frac{37}{50})\end{aligned}
$$

Finally, let ${t}_{1}$ be the time when the thermometer reads ${38}^{∘}F.$ Then, we have

$$
\begin{aligned}T({t}_{1}) & =38 \\ 13+50{e}^{-k{t}_{1}} & =38 \\ 50{e}^{-k{t}_{1}} & =25 \\ {e}^{-k{t}_{1}} & =\frac{25}{50} \\ -k{t}_{1} & =\operatorname{ln}⁡(\frac{25}{50}) \\ {t}_{1} & =-\frac{1}{k}\operatorname{ln}⁡(\frac{25}{50}).\end{aligned}
$$

Substituting in our value for $k,$ we conclude that the thermometer will read ${38}^{∘}F$ after

$$
{t}_{1}=\frac{-\operatorname{ln}⁡(\frac{25}{50})}{-\frac{1}{10}\operatorname{ln}⁡(\frac{37}{50})}≈23\,\text{min},
$$

rounded to the nearest minute.


## Original q-15589 — exact raw replay

The water boils in a pan at a temperature of ${100}^{∘}C.$ The pan with water is then placed to a room with a temperature of ${25}^{∘}C,$ and the temperature of water decreases. After $5$ minutes, it cools to ${90}^{∘}C.$ To the nearest minute, how long does it take for the water to have a temperature of ${30}^{∘}C?$ 

*Hint: You may assume that the temperature reading $T(t)$ of the water in the pan decreases at a rate that obeys Newton's law of cooling, where $T$ is measured in degrees Celsius and $t>0$ is the time, in minutes, since the water starts cooling.*

- $98\,\text{min}$
- $95\,\text{min}$ **(correct)**
- $87\,\text{min}$
- $67\,\text{min}$
- $89\,\text{min}$

**Worked solution**

Newton's law of cooling states that the rate at which the temperature $T(t)$ of a body changes is proportional to the difference between its temperature and its surroundings. Therefore, we have the inhibited decay equation

$$
\frac{\text{d}T}{\text{d}t}=-k(T-{T}_{S}),
$$

where ${T}_{S}$ is the temperature of the surroundings, and $k>0$ is a constant of proportionality.

In our case, ${T}_{S}={25}^{∘}\text{C},$ and we have

$$
\frac{\text{d}T}{\text{d}t}=-k(T-25).
$$

First, we integrate our differential equation by separating the variables:

$$
\begin{aligned}\frac{dT}{T-25} & =-k\,dt \\ \int \frac{dT}{T-25} & =-k\int dt \\ \operatorname{ln}⁡|T-25| & =-kt+C\end{aligned}
$$

Since this is the solution to an inhibited decay equation, we have $T-25>0$ for all $t>0.$
Next, we solve for $T(t),$ as follows:

$$
\begin{aligned}T-25 & ={e}^{-kt+C} \\ T-25 & ={e}^{C}{e}^{-kt} \\ T-25 & =K{e}^{-kt} \\ T & =25+K{e}^{-kt}\end{aligned}
$$

Note that $K={e}^{C}$ is a constant of integration. 

We're told that the initial temperature was ${100}^{∘}C.$ So, we apply the initial condition $T(0)=100,$ and solve for $K:$

$$
\begin{aligned}100 & =25+K{e}^{0} \\ 100 & =25+K \\ K & =75\end{aligned}
$$

Therefore, we have the following expression for $T(t):$

$$
T(t)=25+75{e}^{-kt}
$$

We're also told that, after $5$ minutes, it cools to ${90}^{∘}C.$ So, applying the condition $T(5)=90,$ we can solve for $k:$

$$
\begin{aligned}90 & =25+75{e}^{-5k} \\ 65 & =75{e}^{-5k} \\ \frac{13}{15} & ={e}^{-5k} \\ \operatorname{ln}⁡(\frac{13}{15}) & =-5k \\ k & =-\frac{1}{5}\operatorname{ln}⁡(\frac{13}{15})\end{aligned}
$$

Finally, let ${t}_{1}$ be the time when the water has a temperature of ${30}^{∘}C.$ Then, we have

$$
\begin{aligned}T({t}_{1}) & =30 \\ 25+75{e}^{-k{t}_{1}} & =30 \\ 75{e}^{-k{t}_{1}} & =5 \\ {e}^{-k{t}_{1}} & =\frac{1}{15} \\ -k{t}_{1} & =\operatorname{ln}⁡(\frac{1}{15}) \\ {t}_{1} & =-\frac{1}{k}\operatorname{ln}⁡(\frac{1}{15}).\end{aligned}
$$

Substituting in our value for $k,$ we conclude that the temperature of water will be ${30}^{∘}C$ after

$$
{t}_{1}=\frac{-\operatorname{ln}⁡(\frac{1}{15})}{-\frac{1}{5}\operatorname{ln}⁡(\frac{13}{15})}≈95\,\text{min},
$$

rounded to the nearest minute.


## Changed observed profile q-15589 — underdetermined scalar intent

The water boils in a pan at a temperature of ${100}^{∘}C.$ The pan with water is then placed to a room with a temperature of ${26}^{∘}C,$ and the temperature of water decreases. After $6$ minutes, it cools to ${91}^{∘}C.$ To the nearest minute, how long does it take for the water to have a temperature of ${31}^{∘}C?$ 

*Hint: You may assume that the temperature reading $T(t)$ of the water in the pan decreases at a rate that obeys Newton's law of cooling, where $T$ is measured in degrees Celsius and $t>0$ is the time, in minutes, since the water starts cooling.*

- $128\,\text{min}$
- $119\,\text{min}$
- $97\,\text{min}$
- $125\,\text{min}$ **(correct)**
- $117\,\text{min}$

**Worked solution**

Newton's law of cooling states that the rate at which the temperature $T(t)$ of a body changes is proportional to the difference between its temperature and its surroundings. Therefore, we have the inhibited decay equation

$$
\frac{\text{d}T}{\text{d}t}=-k(T-{T}_{S}),
$$

where ${T}_{S}$ is the temperature of the surroundings, and $k>0$ is a constant of proportionality.

In our case, ${T}_{S}={26}^{∘}\text{C},$ and we have

$$
\frac{\text{d}T}{\text{d}t}=-k(T-26).
$$

First, we integrate our differential equation by separating the variables:

$$
\begin{aligned}\frac{dT}{T-26} & =-k\,dt \\ \int \frac{dT}{T-26} & =-k\int dt \\ \operatorname{ln}⁡|T-26| & =-kt+C\end{aligned}
$$

Since this is the solution to an inhibited decay equation, we have $T-26>0$ for all $t>0.$
Next, we solve for $T(t),$ as follows:

$$
\begin{aligned}T-26 & ={e}^{-kt+C} \\ T-26 & ={e}^{C}{e}^{-kt} \\ T-26 & =K{e}^{-kt} \\ T & =26+K{e}^{-kt}\end{aligned}
$$

Note that $K={e}^{C}$ is a constant of integration. 

We're told that the initial temperature was ${100}^{∘}C.$ So, we apply the initial condition $T(0)=100,$ and solve for $K:$

$$
\begin{aligned}100 & =26+K{e}^{0} \\ 100 & =26+K \\ K & =74\end{aligned}
$$

Therefore, we have the following expression for $T(t):$

$$
T(t)=26+74{e}^{-kt}
$$

We're also told that, after $6$ minutes, it cools to ${91}^{∘}C.$ So, applying the condition $T(6)=91,$ we can solve for $k:$

$$
\begin{aligned}91 & =26+74{e}^{-6k} \\ 65 & =74{e}^{-6k} \\ \frac{65}{74} & ={e}^{-6k} \\ \operatorname{ln}⁡(\frac{65}{74}) & =-6k \\ k & =-\frac{1}{6}\operatorname{ln}⁡(\frac{65}{74})\end{aligned}
$$

Finally, let ${t}_{1}$ be the time when the water has a temperature of ${31}^{∘}C.$ Then, we have

$$
\begin{aligned}T({t}_{1}) & =31 \\ 26+74{e}^{-k{t}_{1}} & =31 \\ 74{e}^{-k{t}_{1}} & =5 \\ {e}^{-k{t}_{1}} & =\frac{5}{74} \\ -k{t}_{1} & =\operatorname{ln}⁡(\frac{5}{74}) \\ {t}_{1} & =-\frac{1}{k}\operatorname{ln}⁡(\frac{5}{74}).\end{aligned}
$$

Substituting in our value for $k,$ we conclude that the temperature of water will be ${31}^{∘}C$ after

$$
{t}_{1}=\frac{-\operatorname{ln}⁡(\frac{5}{74})}{-\frac{1}{6}\operatorname{ln}⁡(\frac{65}{74})}≈125\,\text{min},
$$

rounded to the nearest minute.


## Generated default operations water

The water boils in a pan at a temperature of ${100}^{∘}C.$ The pan with water is then placed to a room with a temperature of ${16}^{∘}C,$ and the temperature of water decreases. After $10$ minutes, it cools to ${86}^{∘}C.$ To the nearest minute, how long does it take for the water to have a temperature of ${49}^{∘}C?$ 

*Hint: You may assume that the temperature reading $T(t)$ of the water in the pan decreases at a rate that obeys Newton's law of cooling, where $T$ is measured in degrees Celsius and $t>0$ is the time, in minutes, since the water starts cooling.*

- $26\,\text{min}$
- $102\,\text{min}$
- $39\,\text{min}$
- $47\,\text{min}$
- $51\,\text{min}$ **(correct)**

**Worked solution**

Newton's law of cooling states that the rate at which the temperature $T(t)$ of a body changes is proportional to the difference between its temperature and its surroundings. Therefore, we have the inhibited decay equation

$$
\frac{\text{d}T}{\text{d}t}=-k(T-{T}_{S}),
$$

where ${T}_{S}$ is the temperature of the surroundings, and $k>0$ is a constant of proportionality.

In our case, ${T}_{S}={16}^{∘}\text{C},$ and we have

$$
\frac{\text{d}T}{\text{d}t}=-k(T-16).
$$

First, we integrate our differential equation by separating the variables:

$$
\begin{aligned}\frac{dT}{T-16} & =-k\,dt \\ \int \frac{dT}{T-16} & =-k\int dt \\ \operatorname{ln}⁡|T-16| & =-kt+C\end{aligned}
$$

Since this is the solution to an inhibited decay equation, we have $T-16>0$ for all $t>0.$
Next, we solve for $T(t),$ as follows:

$$
\begin{aligned}T-16 & ={e}^{-kt+C} \\ T-16 & ={e}^{C}{e}^{-kt} \\ T-16 & =K{e}^{-kt} \\ T & =16+K{e}^{-kt}\end{aligned}
$$

Note that $K={e}^{C}$ is a constant of integration. 

We're told that the initial temperature was ${100}^{∘}C.$ So, we apply the initial condition $T(0)=100,$ and solve for $K:$

$$
\begin{aligned}100 & =16+K{e}^{0} \\ 100 & =16+K \\ K & =84\end{aligned}
$$

Therefore, we have the following expression for $T(t):$

$$
T(t)=16+84{e}^{-kt}
$$

We're also told that, after $10$ minutes, it cools to ${86}^{∘}C.$ So, applying the condition $T(10)=86,$ we can solve for $k:$

$$
\begin{aligned}86 & =16+84{e}^{-10k} \\ 70 & =84{e}^{-10k} \\ \frac{5}{6} & ={e}^{-10k} \\ \operatorname{ln}⁡(\frac{5}{6}) & =-10k \\ k & =-\frac{1}{10}\operatorname{ln}⁡(\frac{5}{6})\end{aligned}
$$

Finally, let ${t}_{1}$ be the time when the water has a temperature of ${49}^{∘}C.$ Then, we have

$$
\begin{aligned}T({t}_{1}) & =49 \\ 16+84{e}^{-k{t}_{1}} & =49 \\ 84{e}^{-k{t}_{1}} & =33 \\ {e}^{-k{t}_{1}} & =\frac{11}{28} \\ -k{t}_{1} & =\operatorname{ln}⁡(\frac{11}{28}) \\ {t}_{1} & =-\frac{1}{k}\operatorname{ln}⁡(\frac{11}{28}).\end{aligned}
$$

Substituting in our value for $k,$ we conclude that the temperature of water will be ${49}^{∘}C$ after

$$
{t}_{1}=\frac{-\operatorname{ln}⁡(\frac{11}{28})}{-\frac{1}{10}\operatorname{ln}⁡(\frac{5}{6})}≈51\,\text{min},
$$

rounded to the nearest minute.


## Original q-107125 — exact raw replay

Simon measures the temperature of the tea in his cup, and the thermometer displays a reading of ${60}^{∘}C.$ After $10$ minutes, Simon repeats the measurement and the thermometer displays a reading of  ${52}^{∘}C.$ To the nearest minute, how long does it take for the tea to decrease its temperature to ${40}^{∘}C$ if the temperature in the room is ${28}^{∘}C?$ 

*Hint: You may assume that the temperature $T(t)$ of the tea in Simon's cup decreases at a rate that obeys Newton's law of cooling, where $T$ is measured in degrees Celsius and $t>0$ is the time, in minutes, since the first measurement.*

- $45\,\text{min}$
- $31\,\text{min}$
- $23\,\text{min}$
- $28\,\text{min}$
- $34\,\text{min}$ **(correct)**

**Worked solution**

Newton's law of cooling states that the rate at which the temperature $T(t)$ of a body changes is proportional to the difference between its temperature and its surroundings. Therefore, we have the inhibited decay equation

$$
\frac{\text{d}T}{\text{d}t}=-k(T-{T}_{S}),
$$

where ${T}_{S}$ is the temperature of the surroundings, and $k>0$ is a constant of proportionality.

In our case, ${T}_{S}={28}^{∘}\text{C},$ and we have

$$
\frac{\text{d}T}{\text{d}t}=-k(T-28).
$$

First, we integrate our differential equation by separating the variables:

$$
\begin{aligned}\frac{dT}{T-28} & =-k\,dt \\ \int \frac{dT}{T-28} & =-k\int dt \\ \operatorname{ln}⁡|T-28| & =-kt+C\end{aligned}
$$

Since this is the solution to an inhibited decay equation, we have $T-28>0$ for all $t>0.$
Next, we solve for $T(t),$ as follows:

$$
\begin{aligned}T-28 & ={e}^{-kt+C} \\ T-28 & ={e}^{C}{e}^{-kt} \\ T-28 & =K{e}^{-kt} \\ T & =28+K{e}^{-kt}\end{aligned}
$$

Note that $K={e}^{C}$ is a constant of integration. 

We're told that the initial temperature reading was ${60}^{∘}C.$ So, we apply the initial condition $T(0)=60,$ and solve for $K:$

$$
\begin{aligned}60 & =28+K{e}^{0} \\ 60 & =28+K \\ K & =32\end{aligned}
$$

Therefore, we have the following expression for $T(t):$

$$
T(t)=28+32{e}^{-kt}
$$

We're also told that, after $10$ minutes, the thermometer reading is ${52}^{∘}C.$ So, applying the condition $T(10)=52,$ we can solve for $k:$

$$
\begin{aligned}52 & =28+32{e}^{-10k} \\ 24 & =32{e}^{-10k} \\ \frac{3}{4} & ={e}^{-10k} \\ \operatorname{ln}⁡(\frac{3}{4}) & =-10k \\ k & =-\frac{1}{10}\operatorname{ln}⁡(\frac{3}{4})\end{aligned}
$$

Finally, let ${t}_{1}$ be the time when the temperature of the tea is ${40}^{∘}C.$ Then, we have

$$
\begin{aligned}T({t}_{1}) & =40 \\ 28+32{e}^{-k{t}_{1}} & =40 \\ 32{e}^{-k{t}_{1}} & =12 \\ {e}^{-k{t}_{1}} & =\frac{3}{8} \\ -k{t}_{1} & =\operatorname{ln}⁡(\frac{3}{8}) \\ {t}_{1} & =-\frac{1}{k}\operatorname{ln}⁡(\frac{3}{8}).\end{aligned}
$$

Substituting in our value for $k,$ we conclude that the tea will have a temperature of ${40}^{∘}C$ after

$$
{t}_{1}=\frac{-\operatorname{ln}⁡(\frac{3}{8})}{-\frac{1}{10}\operatorname{ln}⁡(\frac{3}{4})}≈34\,\text{min},
$$

rounded to the nearest minute.


## Changed observed profile q-107125 — underdetermined scalar intent

Simon measures the temperature of the tea in his cup, and the thermometer displays a reading of ${61}^{∘}C.$ After $11$ minutes, Simon repeats the measurement and the thermometer displays a reading of  ${53}^{∘}C.$ To the nearest minute, how long does it take for the tea to decrease its temperature to ${41}^{∘}C$ if the temperature in the room is ${29}^{∘}C?$ 

*Hint: You may assume that the temperature $T(t)$ of the tea in Simon's cup decreases at a rate that obeys Newton's law of cooling, where $T$ is measured in degrees Celsius and $t>0$ is the time, in minutes, since the first measurement.*

- $49\,\text{min}$
- $38\,\text{min}$ **(correct)**
- $32\,\text{min}$
- $35\,\text{min}$
- $27\,\text{min}$

**Worked solution**

Newton's law of cooling states that the rate at which the temperature $T(t)$ of a body changes is proportional to the difference between its temperature and its surroundings. Therefore, we have the inhibited decay equation

$$
\frac{\text{d}T}{\text{d}t}=-k(T-{T}_{S}),
$$

where ${T}_{S}$ is the temperature of the surroundings, and $k>0$ is a constant of proportionality.

In our case, ${T}_{S}={29}^{∘}\text{C},$ and we have

$$
\frac{\text{d}T}{\text{d}t}=-k(T-29).
$$

First, we integrate our differential equation by separating the variables:

$$
\begin{aligned}\frac{dT}{T-29} & =-k\,dt \\ \int \frac{dT}{T-29} & =-k\int dt \\ \operatorname{ln}⁡|T-29| & =-kt+C\end{aligned}
$$

Since this is the solution to an inhibited decay equation, we have $T-29>0$ for all $t>0.$
Next, we solve for $T(t),$ as follows:

$$
\begin{aligned}T-29 & ={e}^{-kt+C} \\ T-29 & ={e}^{C}{e}^{-kt} \\ T-29 & =K{e}^{-kt} \\ T & =29+K{e}^{-kt}\end{aligned}
$$

Note that $K={e}^{C}$ is a constant of integration. 

We're told that the initial temperature reading was ${61}^{∘}C.$ So, we apply the initial condition $T(0)=61,$ and solve for $K:$

$$
\begin{aligned}61 & =29+K{e}^{0} \\ 61 & =29+K \\ K & =32\end{aligned}
$$

Therefore, we have the following expression for $T(t):$

$$
T(t)=29+32{e}^{-kt}
$$

We're also told that, after $11$ minutes, the thermometer reading is ${53}^{∘}C.$ So, applying the condition $T(11)=53,$ we can solve for $k:$

$$
\begin{aligned}53 & =29+32{e}^{-11k} \\ 24 & =32{e}^{-11k} \\ \frac{3}{4} & ={e}^{-11k} \\ \operatorname{ln}⁡(\frac{3}{4}) & =-11k \\ k & =-\frac{1}{11}\operatorname{ln}⁡(\frac{3}{4})\end{aligned}
$$

Finally, let ${t}_{1}$ be the time when the temperature of the tea is ${41}^{∘}C.$ Then, we have

$$
\begin{aligned}T({t}_{1}) & =41 \\ 29+32{e}^{-k{t}_{1}} & =41 \\ 32{e}^{-k{t}_{1}} & =12 \\ {e}^{-k{t}_{1}} & =\frac{3}{8} \\ -k{t}_{1} & =\operatorname{ln}⁡(\frac{3}{8}) \\ {t}_{1} & =-\frac{1}{k}\operatorname{ln}⁡(\frac{3}{8}).\end{aligned}
$$

Substituting in our value for $k,$ we conclude that the tea will have a temperature of ${41}^{∘}C$ after

$$
{t}_{1}=\frac{-\operatorname{ln}⁡(\frac{3}{8})}{-\frac{1}{11}\operatorname{ln}⁡(\frac{3}{4})}≈38\,\text{min},
$$

rounded to the nearest minute.


## Generated default operations tea

Simon measures the temperature of the tea in his cup, and the thermometer displays a reading of ${53}^{∘}C.$ After $4$ minutes, Simon repeats the measurement and the thermometer displays a reading of  ${40}^{∘}C.$ To the nearest minute, how long does it take for the tea to decrease its temperature to ${20}^{∘}C$ if the temperature in the room is ${11}^{∘}C?$ 

*Hint: You may assume that the temperature $T(t)$ of the tea in Simon's cup decreases at a rate that obeys Newton's law of cooling, where $T$ is measured in degrees Celsius and $t>0$ is the time, in minutes, since the first measurement.*

- $17\,\text{min}$ **(correct)**
- $8\,\text{min}$
- $11\,\text{min}$
- $33\,\text{min}$
- $14\,\text{min}$

**Worked solution**

Newton's law of cooling states that the rate at which the temperature $T(t)$ of a body changes is proportional to the difference between its temperature and its surroundings. Therefore, we have the inhibited decay equation

$$
\frac{\text{d}T}{\text{d}t}=-k(T-{T}_{S}),
$$

where ${T}_{S}$ is the temperature of the surroundings, and $k>0$ is a constant of proportionality.

In our case, ${T}_{S}={11}^{∘}\text{C},$ and we have

$$
\frac{\text{d}T}{\text{d}t}=-k(T-11).
$$

First, we integrate our differential equation by separating the variables:

$$
\begin{aligned}\frac{dT}{T-11} & =-k\,dt \\ \int \frac{dT}{T-11} & =-k\int dt \\ \operatorname{ln}⁡|T-11| & =-kt+C\end{aligned}
$$

Since this is the solution to an inhibited decay equation, we have $T-11>0$ for all $t>0.$
Next, we solve for $T(t),$ as follows:

$$
\begin{aligned}T-11 & ={e}^{-kt+C} \\ T-11 & ={e}^{C}{e}^{-kt} \\ T-11 & =K{e}^{-kt} \\ T & =11+K{e}^{-kt}\end{aligned}
$$

Note that $K={e}^{C}$ is a constant of integration. 

We're told that the initial temperature reading was ${53}^{∘}C.$ So, we apply the initial condition $T(0)=53,$ and solve for $K:$

$$
\begin{aligned}53 & =11+K{e}^{0} \\ 53 & =11+K \\ K & =42\end{aligned}
$$

Therefore, we have the following expression for $T(t):$

$$
T(t)=11+42{e}^{-kt}
$$

We're also told that, after $4$ minutes, the thermometer reading is ${40}^{∘}C.$ So, applying the condition $T(4)=40,$ we can solve for $k:$

$$
\begin{aligned}40 & =11+42{e}^{-4k} \\ 29 & =42{e}^{-4k} \\ \frac{29}{42} & ={e}^{-4k} \\ \operatorname{ln}⁡(\frac{29}{42}) & =-4k \\ k & =-\frac{1}{4}\operatorname{ln}⁡(\frac{29}{42})\end{aligned}
$$

Finally, let ${t}_{1}$ be the time when the temperature of the tea is ${20}^{∘}C.$ Then, we have

$$
\begin{aligned}T({t}_{1}) & =20 \\ 11+42{e}^{-k{t}_{1}} & =20 \\ 42{e}^{-k{t}_{1}} & =9 \\ {e}^{-k{t}_{1}} & =\frac{3}{14} \\ -k{t}_{1} & =\operatorname{ln}⁡(\frac{3}{14}) \\ {t}_{1} & =-\frac{1}{k}\operatorname{ln}⁡(\frac{3}{14}).\end{aligned}
$$

Substituting in our value for $k,$ we conclude that the tea will have a temperature of ${20}^{∘}C$ after

$$
{t}_{1}=\frac{-\operatorname{ln}⁡(\frac{3}{14})}{-\frac{1}{4}\operatorname{ln}⁡(\frac{29}{42})}≈17\,\text{min},
$$

rounded to the nearest minute.


## Generated easy seed 121

The temperature $T(t),$ in degrees Fahrenheit, of an exhaust pipe of a motorcycle can be modeled by the differential equation

$$
\frac{dT}{dt}=-0.06(T-65)
$$

where $t>0$ is the time, measured in minutes. If the initial temperature of the exhaust pipe is ${175}^{∘}F,$ calculate its temperature after $8$ minutes. Round your answer to the nearest integer.

- ${133}^{∘}\text{F}$ **(correct)**
- ${107}^{∘}\text{F}$
- ${173}^{∘}\text{F}$
- ${152}^{∘}\text{F}$
- ${68}^{∘}\text{F}$

**Worked solution**

We're told that the temperature of the exhaust pipe of a motorcycle is modeled by the inhibited decay equation

$$
\frac{dT}{dt}=-0.06(T-65).
$$

First, we integrate our differential equation by separating the variables:

$$
\begin{aligned}\frac{dT}{T-65} & =-0.06\,dt \\ \int \frac{dT}{T-65} & =-\int 0.06\,\text{d}t \\ \operatorname{ln}⁡|T-65| & =-0.06t+C\end{aligned}
$$

Since this is the solution to an inhibited decay equation, we have $T-65>0$ for all $t>0.$
Next, we solve for $T(t),$ as follows:

$$
\begin{aligned}T-65 & ={e}^{-0.06t+C} \\ T-65 & ={e}^{C}{e}^{-0.06t} \\ T-65 & =K{e}^{-0.06t} \\ T & =65+K{e}^{-0.06t}\end{aligned}
$$

Note that $K={e}^{C}$ is a constant of integration. 

We're told that the initial temperature of the exhaust pipe was ${175}^{∘}F.$ So, we apply the initial condition $T(0)=175,$ and solve for $K:$

$$
\begin{aligned}175 & =65+K{e}^{0} \\ 175 & =65+K \\ K & =110\end{aligned}
$$

Therefore, the solution to our initial value problem is

$$
T(t)=65+110{e}^{-0.06t}.
$$

Finally, the temperature of the exhaust pipe after $t=8$ minutes is

$$
T(8)=65+110{e}^{-0.06\cdot 8}≈{133}^{∘}\text{F},
$$

rounded to the nearest integer.


## Generated easy seed 722

The temperature $T(t),$ in degrees Celsius, of a compressor of a refrigerator can be modeled by the differential equation

$$
\frac{dT}{dt}=-0.07(T-28)
$$

where $t>0$ is the time, measured in minutes. If the initial temperature of the compressor is ${82}^{∘}C,$ calculate the temperature of the compressor after $7$ minutes. Round your answer to the nearest integer.

- ${48}^{∘}\text{C}$
- ${70}^{∘}\text{C}$
- ${61}^{∘}\text{C}$ **(correct)**
- ${78}^{∘}\text{C}$
- ${33}^{∘}\text{C}$

**Worked solution**

We're told that the temperature of the compressor of a refrigerator is modeled by the inhibited decay equation

$$
\frac{dT}{dt}=-0.07(T-28).
$$

First, we integrate our differential equation by separating the variables:

$$
\begin{aligned}\frac{dT}{T-28} & =-0.07\,dt \\ \int \frac{dT}{T-28} & =-\int 0.07\,\text{d}t \\ \operatorname{ln}⁡|T-28| & =-0.07t+C\end{aligned}
$$

Since this is the solution to an inhibited decay equation, we have $T-28>0$ for all $t>0.$
Next, we solve for $T(t),$ as follows:

$$
\begin{aligned}T-28 & ={e}^{-0.07t+C} \\ T-28 & ={e}^{C}{e}^{-0.07t} \\ T-28 & =K{e}^{-0.07t} \\ T & =28+K{e}^{-0.07t}\end{aligned}
$$

Note that $K={e}^{C}$ is a constant of integration. 

We're told that the initial temperature of the compressor was ${82}^{∘}C.$ So, we apply the initial condition $T(0)=82,$ and solve for $K:$

$$
\begin{aligned}82 & =28+K{e}^{0} \\ 82 & =28+K \\ K & =54\end{aligned}
$$

Therefore, the solution to our initial value problem is

$$
T(t)=28+54{e}^{-0.07t}.
$$

Finally, the temperature of the compressor after $t=7$ minutes is

$$
T(7)=28+54{e}^{-0.07\cdot 7}≈{61}^{∘}\text{C},
$$

rounded to the nearest integer.


## Generated moderate seed 121

A thermometer is placed into a water bath and displays a reading of ${88}^{∘}C.$ The thermometer is then transferred to a ${16}^{∘}C$ water bath, and its reading begins to decrease. After $11$ minutes, the thermometer reading is ${61}^{∘}C.$ To the nearest minute, how long does it take for the thermometer to register a reading of ${30}^{∘}C?$ 

*Hint: You may assume that the temperature reading $T(t)$ of the thermometer decreases at a rate that obeys Newton's law of cooling, where $T$ is measured in degrees Celsius and $t>0$ is the time, in minutes, since the thermometer was transferred into the ${16}^{∘}C$ water bath.*

- $38\,\text{min}$ **(correct)**
- $25\,\text{min}$
- $19\,\text{min}$
- $32\,\text{min}$
- $77\,\text{min}$

**Worked solution**

Newton's law of cooling states that the rate at which the temperature $T(t)$ of a body changes is proportional to the difference between its temperature and its surroundings. Therefore, we have the inhibited decay equation

$$
\frac{\text{d}T}{\text{d}t}=-k(T-{T}_{S}),
$$

where ${T}_{S}$ is the temperature of the surroundings, and $k>0$ is a constant of proportionality.

In our case, ${T}_{S}={16}^{∘}\text{C},$ and we have

$$
\frac{\text{d}T}{\text{d}t}=-k(T-16).
$$

First, we integrate our differential equation by separating the variables:

$$
\begin{aligned}\frac{dT}{T-16} & =-k\,dt \\ \int \frac{dT}{T-16} & =-k\int dt \\ \operatorname{ln}⁡|T-16| & =-kt+C\end{aligned}
$$

Since this is the solution to an inhibited decay equation, we have $T-16>0$ for all $t>0.$
Next, we solve for $T(t),$ as follows:

$$
\begin{aligned}T-16 & ={e}^{-kt+C} \\ T-16 & ={e}^{C}{e}^{-kt} \\ T-16 & =K{e}^{-kt} \\ T & =16+K{e}^{-kt}\end{aligned}
$$

Note that $K={e}^{C}$ is a constant of integration. 

We're told that the initial temperature reading was ${88}^{∘}C.$ So, we apply the initial condition $T(0)=88,$ and solve for $K:$

$$
\begin{aligned}88 & =16+K{e}^{0} \\ 88 & =16+K \\ K & =72\end{aligned}
$$

Therefore, we have the following expression for $T(t):$

$$
T(t)=16+72{e}^{-kt}
$$

We're also told that, after $11$ minutes, the thermometer reading is ${61}^{∘}C.$ So, applying the condition $T(11)=61,$ we can solve for $k:$

$$
\begin{aligned}61 & =16+72{e}^{-11k} \\ 45 & =72{e}^{-11k} \\ \frac{5}{8} & ={e}^{-11k} \\ \operatorname{ln}⁡(\frac{5}{8}) & =-11k \\ k & =-\frac{1}{11}\operatorname{ln}⁡(\frac{5}{8})\end{aligned}
$$

Finally, let ${t}_{1}$ be the time when the thermometer reads ${30}^{∘}C.$ Then, we have

$$
\begin{aligned}T({t}_{1}) & =30 \\ 16+72{e}^{-k{t}_{1}} & =30 \\ 72{e}^{-k{t}_{1}} & =14 \\ {e}^{-k{t}_{1}} & =\frac{7}{36} \\ -k{t}_{1} & =\operatorname{ln}⁡(\frac{7}{36}) \\ {t}_{1} & =-\frac{1}{k}\operatorname{ln}⁡(\frac{7}{36}).\end{aligned}
$$

Substituting in our value for $k,$ we conclude that the thermometer will read ${30}^{∘}C$ after

$$
{t}_{1}=\frac{-\operatorname{ln}⁡(\frac{7}{36})}{-\frac{1}{11}\operatorname{ln}⁡(\frac{5}{8})}≈38\,\text{min},
$$

rounded to the nearest minute.


## Generated moderate seed 722

A thermometer is taken out of a room where the air temperature is ${69}^{∘}F$  and brought outside where the temperature is ${15}^{∘}F,$ and its reading begins to decrease. After $8$ minutes, the thermometer reading is ${63}^{∘}F.$ To the nearest minute, how long does it take for the thermometer to register a reading of ${52}^{∘}F?$ 

*Hint: You may assume that the temperature reading $T(t)$ of the thermometer decreases at a rate that obeys Newton's law of cooling, where $T$ is measured in degrees Fahrenheit and $t>0$ is the time, in minutes, since the thermometer was transferred outside to ${15}^{∘}F.$*

- $51\,\text{min}$
- $26\,\text{min}$ **(correct)**
- $13\,\text{min}$
- $25\,\text{min}$
- $19\,\text{min}$

**Worked solution**

Newton's law of cooling states that the rate at which the temperature $T(t)$ of a body changes is proportional to the difference between its temperature and its surroundings. Therefore, we have the inhibited decay equation

$$
\frac{\text{d}T}{\text{d}t}=-k(T-{T}_{S}),
$$

where ${T}_{S}$ is the temperature of the surroundings, and $k>0$ is a constant of proportionality.

In our case, ${T}_{S}={15}^{∘}\text{F},$ and we have

$$
\frac{\text{d}T}{\text{d}t}=-k(T-15).
$$

First, we integrate our differential equation by separating the variables:

$$
\begin{aligned}\frac{dT}{T-15} & =-k\,dt \\ \int \frac{dT}{T-15} & =-k\int dt \\ \operatorname{ln}⁡|T-15| & =-kt+C\end{aligned}
$$

Since this is the solution to an inhibited decay equation, we have $T-15>0$ for all $t>0.$
Next, we solve for $T(t),$ as follows:

$$
\begin{aligned}T-15 & ={e}^{-kt+C} \\ T-15 & ={e}^{C}{e}^{-kt} \\ T-15 & =K{e}^{-kt} \\ T & =15+K{e}^{-kt}\end{aligned}
$$

Note that $K={e}^{C}$ is a constant of integration. 

We're told that the initial temperature reading was ${69}^{∘}F.$ So, we apply the initial condition $T(0)=69,$ and solve for $K:$

$$
\begin{aligned}69 & =15+K{e}^{0} \\ 69 & =15+K \\ K & =54\end{aligned}
$$

Therefore, we have the following expression for $T(t):$

$$
T(t)=15+54{e}^{-kt}
$$

We're also told that, after $8$ minutes, the thermometer reading is ${63}^{∘}F.$ So, applying the condition $T(8)=63,$ we can solve for $k:$

$$
\begin{aligned}63 & =15+54{e}^{-8k} \\ 48 & =54{e}^{-8k} \\ \frac{48}{54} & ={e}^{-8k} \\ \operatorname{ln}⁡(\frac{48}{54}) & =-8k \\ k & =-\frac{1}{8}\operatorname{ln}⁡(\frac{48}{54})\end{aligned}
$$

Finally, let ${t}_{1}$ be the time when the thermometer reads ${52}^{∘}F.$ Then, we have

$$
\begin{aligned}T({t}_{1}) & =52 \\ 15+54{e}^{-k{t}_{1}} & =52 \\ 54{e}^{-k{t}_{1}} & =37 \\ {e}^{-k{t}_{1}} & =\frac{37}{54} \\ -k{t}_{1} & =\operatorname{ln}⁡(\frac{37}{54}) \\ {t}_{1} & =-\frac{1}{k}\operatorname{ln}⁡(\frac{37}{54}).\end{aligned}
$$

Substituting in our value for $k,$ we conclude that the thermometer will read ${52}^{∘}F$ after

$$
{t}_{1}=\frac{-\operatorname{ln}⁡(\frac{37}{54})}{-\frac{1}{8}\operatorname{ln}⁡(\frac{48}{54})}≈26\,\text{min},
$$

rounded to the nearest minute.


## Generated hard seed 121

A heated metal body cools in a room at ${16}^{∘}\text{C}.$ Its temperature is ${93}^{∘}\text{C}$ after $5$ minutes and ${67}^{∘}\text{C}$ after $11$ minutes. The temperature $T(t)$, in degrees Celsius, obeys Newton's law of cooling, with $t$ measured in minutes since cooling began. To the nearest minute, how long after cooling began does the body reach ${23}^{∘}\text{C}$?

- $75\,\text{min}$
- $40\,\text{min}$ **(correct)**
- $31\,\text{min}$
- $22\,\text{min}$
- $35\,\text{min}$

**Worked solution**

Newton's law of cooling states that the rate at which the temperature $T(t)$ of a body changes is proportional to the difference between its temperature and its surroundings. Therefore, we have the inhibited decay equation

$$
\frac{dT}{dt}=-k(T-16),\qquad k>0.
$$

First, we integrate our differential equation by separating the variables:

$$
\begin{aligned}\frac{dT}{T-16} & =-k\,dt \\ \int \frac{dT}{T-16} & =-k\int dt \\ \operatorname{ln}⁡|T-16| & =-kt+C\end{aligned}
$$

Since this is the solution to an inhibited decay equation, we have $T-16>0$ for all $t>0.$
Next, we solve for $T(t),$ as follows:

$$
\begin{aligned}T-16 & ={e}^{-kt+C} \\ T-16 & ={e}^{C}{e}^{-kt} \\ T-16 & =K{e}^{-kt} \\ T & =16+K{e}^{-kt}\end{aligned}
$$

Note that $K={e}^{C}$ is a constant of integration. 

Apply the two observed conditions $T(5)=93$ and $T(11)=67$:

$$
\begin{aligned}93 & =16+Ke^{-5k} \\ 77 & =Ke^{-5k} \\ 67 & =16+Ke^{-11k} \\ 51 & =Ke^{-11k}\end{aligned}
$$

Divide the excess temperatures to eliminate $K$, then take natural logarithms:

$$
\begin{aligned}\frac{51}{77} & =\frac{Ke^{-11k}}{Ke^{-5k}} \\ \frac{51}{77} & =e^{-6k} \\ \ln(\frac{51}{77}) & =-6k \\ k & =- \frac{\ln{\left(\frac{51}{77} \right)}}{6}\end{aligned}
$$

Now substitute this rate into $T(5)=93$ to determine the constant:

$$
\begin{aligned}77 & =Ke^{-5(- \frac{\ln{\left(\frac{51}{77} \right)}}{6})} \\ K & =77e^{5(- \frac{\ln{\left(\frac{51}{77} \right)}}{6})} \\ K & =77\left(\frac{77}{51}\right)^{\frac{5}{6}}\end{aligned}
$$

Therefore, the solution satisfying both observations is

$$
T(t)=16+77\left(\frac{77}{51}\right)^{\frac{5}{6}}e^{-(- \frac{\ln{\left(\frac{51}{77} \right)}}{6})t}.
$$

Substituting the two observation times confirms the model:

$$
\begin{aligned}T(5) & =16+(77\left(\frac{77}{51}\right)^{\frac{5}{6}})e^{-(- \frac{\ln{\left(\frac{51}{77} \right)}}{6})\cdot 5}=93 \\ T(11) & =16+(77\left(\frac{77}{51}\right)^{\frac{5}{6}})e^{-(- \frac{\ln{\left(\frac{51}{77} \right)}}{6})\cdot 11}=67\end{aligned}
$$

Finally, let ${t}_{1}$ be the time when the body reaches ${23}^{∘}\text{C}.$ Then, we have

$$
\begin{aligned}T({t}_{1}) & =23 \\ 16+Ke^{-k{t}_{1}} & =23 \\ Ke^{-k{t}_{1}} & =7 \\ e^{-k{t}_{1}} & =\frac{7}{K} \\ -k{t}_{1} & =\ln\left(\frac{7}{K}\right) \\ {t}_{1} & =-\frac{1}{k}\ln\left(\frac{7}{K}\right)\end{aligned}
$$

Substitute the values of $K$ and $k$ to obtain the time measured since cooling began:

$$
\begin{aligned}{t}_{1} & =-\frac{1}{- \frac{\ln{\left(\frac{51}{77} \right)}}{6}}\ln\left(\frac{7}{77\left(\frac{77}{51}\right)^{\frac{5}{6}}}\right) \\ {t}_{1} & =5+6\frac{\ln(\frac{1}{11})}{\ln(\frac{51}{77})}≈40\,\text{min}.\end{aligned}
$$


## Generated hard seed 722

A heated metal body cools in a room at ${18}^{∘}\text{C}.$ Its temperature is ${72}^{∘}\text{C}$ after $5$ minutes and ${59}^{∘}\text{C}$ after $11$ minutes. The temperature $T(t)$, in degrees Celsius, obeys Newton's law of cooling, with $t$ measured in minutes since cooling began. To the nearest minute, how long after cooling began does the body reach ${31}^{∘}\text{C}$?

- $30\,\text{min}$
- $67\,\text{min}$
- $36\,\text{min}$ **(correct)**
- $31\,\text{min}$
- $21\,\text{min}$

**Worked solution**

Newton's law of cooling states that the rate at which the temperature $T(t)$ of a body changes is proportional to the difference between its temperature and its surroundings. Therefore, we have the inhibited decay equation

$$
\frac{dT}{dt}=-k(T-18),\qquad k>0.
$$

First, we integrate our differential equation by separating the variables:

$$
\begin{aligned}\frac{dT}{T-18} & =-k\,dt \\ \int \frac{dT}{T-18} & =-k\int dt \\ \operatorname{ln}⁡|T-18| & =-kt+C\end{aligned}
$$

Since this is the solution to an inhibited decay equation, we have $T-18>0$ for all $t>0.$
Next, we solve for $T(t),$ as follows:

$$
\begin{aligned}T-18 & ={e}^{-kt+C} \\ T-18 & ={e}^{C}{e}^{-kt} \\ T-18 & =K{e}^{-kt} \\ T & =18+K{e}^{-kt}\end{aligned}
$$

Note that $K={e}^{C}$ is a constant of integration. 

Apply the two observed conditions $T(5)=72$ and $T(11)=59$:

$$
\begin{aligned}72 & =18+Ke^{-5k} \\ 54 & =Ke^{-5k} \\ 59 & =18+Ke^{-11k} \\ 41 & =Ke^{-11k}\end{aligned}
$$

Divide the excess temperatures to eliminate $K$, then take natural logarithms:

$$
\begin{aligned}\frac{41}{54} & =\frac{Ke^{-11k}}{Ke^{-5k}} \\ \frac{41}{54} & =e^{-6k} \\ \ln(\frac{41}{54}) & =-6k \\ k & =- \frac{\ln{\left(\frac{41}{54} \right)}}{6}\end{aligned}
$$

Now substitute this rate into $T(5)=72$ to determine the constant:

$$
\begin{aligned}54 & =Ke^{-5(- \frac{\ln{\left(\frac{41}{54} \right)}}{6})} \\ K & =54e^{5(- \frac{\ln{\left(\frac{41}{54} \right)}}{6})} \\ K & =54\left(\frac{54}{41}\right)^{\frac{5}{6}}\end{aligned}
$$

Therefore, the solution satisfying both observations is

$$
T(t)=18+54\left(\frac{54}{41}\right)^{\frac{5}{6}}e^{-(- \frac{\ln{\left(\frac{41}{54} \right)}}{6})t}.
$$

Substituting the two observation times confirms the model:

$$
\begin{aligned}T(5) & =18+(54\left(\frac{54}{41}\right)^{\frac{5}{6}})e^{-(- \frac{\ln{\left(\frac{41}{54} \right)}}{6})\cdot 5}=72 \\ T(11) & =18+(54\left(\frac{54}{41}\right)^{\frac{5}{6}})e^{-(- \frac{\ln{\left(\frac{41}{54} \right)}}{6})\cdot 11}=59\end{aligned}
$$

Finally, let ${t}_{1}$ be the time when the body reaches ${31}^{∘}\text{C}.$ Then, we have

$$
\begin{aligned}T({t}_{1}) & =31 \\ 18+Ke^{-k{t}_{1}} & =31 \\ Ke^{-k{t}_{1}} & =13 \\ e^{-k{t}_{1}} & =\frac{13}{K} \\ -k{t}_{1} & =\ln\left(\frac{13}{K}\right) \\ {t}_{1} & =-\frac{1}{k}\ln\left(\frac{13}{K}\right)\end{aligned}
$$

Substitute the values of $K$ and $k$ to obtain the time measured since cooling began:

$$
\begin{aligned}{t}_{1} & =-\frac{1}{- \frac{\ln{\left(\frac{41}{54} \right)}}{6}}\ln\left(\frac{13}{54\left(\frac{54}{41}\right)^{\frac{5}{6}}}\right) \\ {t}_{1} & =5+6\frac{\ln(\frac{13}{54})}{\ln(\frac{41}{54})}≈36\,\text{min}.\end{aligned}
$$


## Fahrenheit source unit repair — authored default bank

A thermometer is taken out of a room where the air temperature is ${72}^{∘}F$  and brought outside where the temperature is ${15}^{∘}F,$ and its reading begins to decrease. After $2$ minutes, the thermometer reading is ${54}^{∘}F.$ To the nearest minute, how long does it take for the thermometer to register a reading of ${25}^{∘}F?$ 

*Hint: You may assume that the temperature reading $T(t)$ of the thermometer decreases at a rate that obeys Newton's law of cooling, where $T$ is measured in degrees Fahrenheit and $t>0$ is the time, in minutes, since the thermometer was transferred outside to ${15}^{∘}F.$*

- $6\,\text{min}$
- $7\,\text{min}$
- $9\,\text{min}$ **(correct)**
- $18\,\text{min}$
- $5\,\text{min}$

**Worked solution**

Newton's law of cooling states that the rate at which the temperature $T(t)$ of a body changes is proportional to the difference between its temperature and its surroundings. Therefore, we have the inhibited decay equation

$$
\frac{\text{d}T}{\text{d}t}=-k(T-{T}_{S}),
$$

where ${T}_{S}$ is the temperature of the surroundings, and $k>0$ is a constant of proportionality.

In our case, ${T}_{S}={15}^{∘}\text{F},$ and we have

$$
\frac{\text{d}T}{\text{d}t}=-k(T-15).
$$

First, we integrate our differential equation by separating the variables:

$$
\begin{aligned}\frac{dT}{T-15} & =-k\,dt \\ \int \frac{dT}{T-15} & =-k\int dt \\ \operatorname{ln}⁡|T-15| & =-kt+C\end{aligned}
$$

Since this is the solution to an inhibited decay equation, we have $T-15>0$ for all $t>0.$
Next, we solve for $T(t),$ as follows:

$$
\begin{aligned}T-15 & ={e}^{-kt+C} \\ T-15 & ={e}^{C}{e}^{-kt} \\ T-15 & =K{e}^{-kt} \\ T & =15+K{e}^{-kt}\end{aligned}
$$

Note that $K={e}^{C}$ is a constant of integration. 

We're told that the initial temperature reading was ${72}^{∘}F.$ So, we apply the initial condition $T(0)=72,$ and solve for $K:$

$$
\begin{aligned}72 & =15+K{e}^{0} \\ 72 & =15+K \\ K & =57\end{aligned}
$$

Therefore, we have the following expression for $T(t):$

$$
T(t)=15+57{e}^{-kt}
$$

We're also told that, after $2$ minutes, the thermometer reading is ${54}^{∘}F.$ So, applying the condition $T(2)=54,$ we can solve for $k:$

$$
\begin{aligned}54 & =15+57{e}^{-2k} \\ 39 & =57{e}^{-2k} \\ \frac{39}{57} & ={e}^{-2k} \\ \operatorname{ln}⁡(\frac{39}{57}) & =-2k \\ k & =-\frac{1}{2}\operatorname{ln}⁡(\frac{39}{57})\end{aligned}
$$

Finally, let ${t}_{1}$ be the time when the thermometer reads ${25}^{∘}F.$ Then, we have

$$
\begin{aligned}T({t}_{1}) & =25 \\ 15+57{e}^{-k{t}_{1}} & =25 \\ 57{e}^{-k{t}_{1}} & =10 \\ {e}^{-k{t}_{1}} & =\frac{10}{57} \\ -k{t}_{1} & =\operatorname{ln}⁡(\frac{10}{57}) \\ {t}_{1} & =-\frac{1}{k}\operatorname{ln}⁡(\frac{10}{57}).\end{aligned}
$$

Substituting in our value for $k,$ we conclude that the thermometer will read ${25}^{∘}F$ after

$$
{t}_{1}=\frac{-\operatorname{ln}⁡(\frac{10}{57})}{-\frac{1}{2}\operatorname{ln}⁡(\frac{39}{57})}≈9\,\text{min},
$$

rounded to the nearest minute.
