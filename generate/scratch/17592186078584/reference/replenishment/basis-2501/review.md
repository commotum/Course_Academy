Simon measures the temperature of the tea in his cup, and the thermometer displays a reading of ${59}^{∘}C.$ After $2$ minutes, Simon repeats the measurement and the thermometer displays a reading of  ${51}^{∘}C.$ To the nearest minute, how long does it take for the tea to decrease its temperature to ${26}^{∘}C$ if the temperature in the room is ${12}^{∘}C?$ 

*Hint: You may assume that the temperature $T(t)$ of the tea in Simon's cup decreases at a rate that obeys Newton's law of cooling, where $T$ is measured in degrees Celsius and $t>0$ is the time, in minutes, since the first measurement.*

- $9\,\text{min}$
- $13\,\text{min}$ **(correct)**
- $6\,\text{min}$
- $26\,\text{min}$
- $11\,\text{min}$

**Worked solution**

Newton's law of cooling states that the rate at which the temperature $T(t)$ of a body changes is proportional to the difference between its temperature and its surroundings. Therefore, we have the inhibited decay equation

$$
\frac{\text{d}T}{\text{d}t}=-k(T-{T}_{S}),
$$

where ${T}_{S}$ is the temperature of the surroundings, and $k>0$ is a constant of proportionality.

In our case, ${T}_{S}={12}^{∘}\text{C},$ and we have

$$
\frac{\text{d}T}{\text{d}t}=-k(T-12).
$$

First, we integrate our differential equation by separating the variables:

$$
\begin{aligned}\frac{dT}{T-12} & =-k\,dt \\ \int \frac{dT}{T-12} & =-k\int dt \\ \operatorname{ln}⁡|T-12| & =-kt+C\end{aligned}
$$

Since this is the solution to an inhibited decay equation, we have $T-12>0$ for all $t>0.$
Next, we solve for $T(t),$ as follows:

$$
\begin{aligned}T-12 & ={e}^{-kt+C} \\ T-12 & ={e}^{C}{e}^{-kt} \\ T-12 & =K{e}^{-kt} \\ T & =12+K{e}^{-kt}\end{aligned}
$$

Note that $K={e}^{C}$ is a constant of integration. 

We're told that the initial temperature reading was ${59}^{∘}C.$ So, we apply the initial condition $T(0)=59,$ and solve for $K:$

$$
\begin{aligned}59 & =12+K{e}^{0} \\ 59 & =12+K \\ K & =47\end{aligned}
$$

Therefore, we have the following expression for $T(t):$

$$
T(t)=12+47{e}^{-kt}
$$

We're also told that, after $2$ minutes, the thermometer reading is ${51}^{∘}C.$ So, applying the condition $T(2)=51,$ we can solve for $k:$

$$
\begin{aligned}51 & =12+47{e}^{-2k} \\ 39 & =47{e}^{-2k} \\ \frac{39}{47} & ={e}^{-2k} \\ \operatorname{ln}⁡(\frac{39}{47}) & =-2k \\ k & =-\frac{1}{2}\operatorname{ln}⁡(\frac{39}{47})\end{aligned}
$$

Finally, let ${t}_{1}$ be the time when the temperature of the tea is ${26}^{∘}C.$ Then, we have

$$
\begin{aligned}T({t}_{1}) & =26 \\ 12+47{e}^{-k{t}_{1}} & =26 \\ 47{e}^{-k{t}_{1}} & =14 \\ {e}^{-k{t}_{1}} & =\frac{14}{47} \\ -k{t}_{1} & =\operatorname{ln}⁡(\frac{14}{47}) \\ {t}_{1} & =-\frac{1}{k}\operatorname{ln}⁡(\frac{14}{47}).\end{aligned}
$$

Substituting in our value for $k,$ we conclude that the tea will have a temperature of ${26}^{∘}C$ after

$$
{t}_{1}=\frac{-\operatorname{ln}⁡(\frac{14}{47})}{-\frac{1}{2}\operatorname{ln}⁡(\frac{39}{47})}≈13\,\text{min},
$$

rounded to the nearest minute.

---

The water boils in a pan at a temperature of ${100}^{∘}C.$ The pan with water is then placed to a room with a temperature of ${17}^{∘}C,$ and the temperature of water decreases. After $3$ minutes, it cools to ${83}^{∘}C.$ To the nearest minute, how long does it take for the water to have a temperature of ${43}^{∘}C?$ 

*Hint: You may assume that the temperature reading $T(t)$ of the water in the pan decreases at a rate that obeys Newton's law of cooling, where $T$ is measured in degrees Celsius and $t>0$ is the time, in minutes, since the water starts cooling.*

- $8\,\text{min}$
- $14\,\text{min}$
- $11\,\text{min}$
- $15\,\text{min}$ **(correct)**
- $30\,\text{min}$

**Worked solution**

Newton's law of cooling states that the rate at which the temperature $T(t)$ of a body changes is proportional to the difference between its temperature and its surroundings. Therefore, we have the inhibited decay equation

$$
\frac{\text{d}T}{\text{d}t}=-k(T-{T}_{S}),
$$

where ${T}_{S}$ is the temperature of the surroundings, and $k>0$ is a constant of proportionality.

In our case, ${T}_{S}={17}^{∘}\text{C},$ and we have

$$
\frac{\text{d}T}{\text{d}t}=-k(T-17).
$$

First, we integrate our differential equation by separating the variables:

$$
\begin{aligned}\frac{dT}{T-17} & =-k\,dt \\ \int \frac{dT}{T-17} & =-k\int dt \\ \operatorname{ln}⁡|T-17| & =-kt+C\end{aligned}
$$

Since this is the solution to an inhibited decay equation, we have $T-17>0$ for all $t>0.$
Next, we solve for $T(t),$ as follows:

$$
\begin{aligned}T-17 & ={e}^{-kt+C} \\ T-17 & ={e}^{C}{e}^{-kt} \\ T-17 & =K{e}^{-kt} \\ T & =17+K{e}^{-kt}\end{aligned}
$$

Note that $K={e}^{C}$ is a constant of integration. 

We're told that the initial temperature was ${100}^{∘}C.$ So, we apply the initial condition $T(0)=100,$ and solve for $K:$

$$
\begin{aligned}100 & =17+K{e}^{0} \\ 100 & =17+K \\ K & =83\end{aligned}
$$

Therefore, we have the following expression for $T(t):$

$$
T(t)=17+83{e}^{-kt}
$$

We're also told that, after $3$ minutes, it cools to ${83}^{∘}C.$ So, applying the condition $T(3)=83,$ we can solve for $k:$

$$
\begin{aligned}83 & =17+83{e}^{-3k} \\ 66 & =83{e}^{-3k} \\ \frac{66}{83} & ={e}^{-3k} \\ \operatorname{ln}⁡(\frac{66}{83}) & =-3k \\ k & =-\frac{1}{3}\operatorname{ln}⁡(\frac{66}{83})\end{aligned}
$$

Finally, let ${t}_{1}$ be the time when the water has a temperature of ${43}^{∘}C.$ Then, we have

$$
\begin{aligned}T({t}_{1}) & =43 \\ 17+83{e}^{-k{t}_{1}} & =43 \\ 83{e}^{-k{t}_{1}} & =26 \\ {e}^{-k{t}_{1}} & =\frac{26}{83} \\ -k{t}_{1} & =\operatorname{ln}⁡(\frac{26}{83}) \\ {t}_{1} & =-\frac{1}{k}\operatorname{ln}⁡(\frac{26}{83}).\end{aligned}
$$

Substituting in our value for $k,$ we conclude that the temperature of water will be ${43}^{∘}C$ after

$$
{t}_{1}=\frac{-\operatorname{ln}⁡(\frac{26}{83})}{-\frac{1}{3}\operatorname{ln}⁡(\frac{66}{83})}≈15\,\text{min},
$$

rounded to the nearest minute.

---

A heated metal body cools in a room at ${12}^{∘}\text{C}.$ Its temperature is ${64}^{∘}\text{C}$ after $1$ minute and ${49}^{∘}\text{C}$ after $4$ minutes. The temperature $T(t)$, in degrees Celsius, obeys Newton's law of cooling, with $t$ measured in minutes since cooling began. To the nearest minute, how long after cooling began does the body reach ${19}^{∘}\text{C}$?

- $15\,\text{min}$
- $10\,\text{min}$
- $19\,\text{min}$ **(correct)**
- $36\,\text{min}$
- $18\,\text{min}$

**Worked solution**

Newton's law of cooling states that the rate at which the temperature $T(t)$ of a body changes is proportional to the difference between its temperature and its surroundings. Therefore, we have the inhibited decay equation

$$
\frac{dT}{dt}=-k(T-12),\qquad k>0.
$$

First, we integrate our differential equation by separating the variables:

$$
\begin{aligned}\frac{dT}{T-12} & =-k\,dt \\ \int \frac{dT}{T-12} & =-k\int dt \\ \operatorname{ln}⁡|T-12| & =-kt+C\end{aligned}
$$

Since this is the solution to an inhibited decay equation, we have $T-12>0$ for all $t>0.$
Next, we solve for $T(t),$ as follows:

$$
\begin{aligned}T-12 & ={e}^{-kt+C} \\ T-12 & ={e}^{C}{e}^{-kt} \\ T-12 & =K{e}^{-kt} \\ T & =12+K{e}^{-kt}\end{aligned}
$$

Note that $K={e}^{C}$ is a constant of integration. 

Apply the two observed conditions $T(1)=64$ and $T(4)=49$:

$$
\begin{aligned}64 & =12+Ke^{-1k} \\ 52 & =Ke^{-1k} \\ 49 & =12+Ke^{-4k} \\ 37 & =Ke^{-4k}\end{aligned}
$$

Divide the excess temperatures to eliminate $K$, then take natural logarithms:

$$
\begin{aligned}\frac{37}{52} & =\frac{Ke^{-4k}}{Ke^{-1k}} \\ \frac{37}{52} & =e^{-3k} \\ \ln(\frac{37}{52}) & =-3k \\ k & =- \frac{\ln{\left(\frac{37}{52} \right)}}{3}\end{aligned}
$$

Now substitute this rate into $T(1)=64$ to determine the constant:

$$
\begin{aligned}52 & =Ke^{-1(- \frac{\ln{\left(\frac{37}{52} \right)}}{3})} \\ K & =52e^{1(- \frac{\ln{\left(\frac{37}{52} \right)}}{3})} \\ K & =52\left(\frac{52}{37}\right)^{\frac{1}{3}}\end{aligned}
$$

Therefore, the solution satisfying both observations is

$$
T(t)=12+52\left(\frac{52}{37}\right)^{\frac{1}{3}}e^{-(- \frac{\ln{\left(\frac{37}{52} \right)}}{3})t}.
$$

Substituting the two observation times confirms the model:

$$
\begin{aligned}T(1) & =12+(52\left(\frac{52}{37}\right)^{\frac{1}{3}})e^{-(- \frac{\ln{\left(\frac{37}{52} \right)}}{3})\cdot 1}=64 \\ T(4) & =12+(52\left(\frac{52}{37}\right)^{\frac{1}{3}})e^{-(- \frac{\ln{\left(\frac{37}{52} \right)}}{3})\cdot 4}=49\end{aligned}
$$

Finally, let ${t}_{1}$ be the time when the body reaches ${19}^{∘}\text{C}.$ Then, we have

$$
\begin{aligned}T({t}_{1}) & =19 \\ 12+Ke^{-k{t}_{1}} & =19 \\ Ke^{-k{t}_{1}} & =7 \\ e^{-k{t}_{1}} & =\frac{7}{K} \\ -k{t}_{1} & =\ln\left(\frac{7}{K}\right) \\ {t}_{1} & =-\frac{1}{k}\ln\left(\frac{7}{K}\right)\end{aligned}
$$

Substitute the values of $K$ and $k$ to obtain the time measured since cooling began:

$$
\begin{aligned}{t}_{1} & =-\frac{1}{- \frac{\ln{\left(\frac{37}{52} \right)}}{3}}\ln\left(\frac{7}{52\left(\frac{52}{37}\right)^{\frac{1}{3}}}\right) \\ {t}_{1} & =1+3\frac{\ln(\frac{7}{52})}{\ln(\frac{37}{52})}≈19\,\text{min}.\end{aligned}
$$

---

A heated metal body cools in a room at ${14}^{∘}\text{C}.$ Its temperature is ${114}^{∘}\text{C}$ after $2$ minutes and ${79}^{∘}\text{C}$ after $7$ minutes. The temperature $T(t)$, in degrees Celsius, obeys Newton's law of cooling, with $t$ measured in minutes since cooling began. To the nearest minute, how long after cooling began does the body reach ${32}^{∘}\text{C}$?

- $19\,\text{min}$
- $42\,\text{min}$
- $12\,\text{min}$
- $22\,\text{min}$ **(correct)**
- $20\,\text{min}$

**Worked solution**

Newton's law of cooling states that the rate at which the temperature $T(t)$ of a body changes is proportional to the difference between its temperature and its surroundings. Therefore, we have the inhibited decay equation

$$
\frac{dT}{dt}=-k(T-14),\qquad k>0.
$$

First, we integrate our differential equation by separating the variables:

$$
\begin{aligned}\frac{dT}{T-14} & =-k\,dt \\ \int \frac{dT}{T-14} & =-k\int dt \\ \operatorname{ln}⁡|T-14| & =-kt+C\end{aligned}
$$

Since this is the solution to an inhibited decay equation, we have $T-14>0$ for all $t>0.$
Next, we solve for $T(t),$ as follows:

$$
\begin{aligned}T-14 & ={e}^{-kt+C} \\ T-14 & ={e}^{C}{e}^{-kt} \\ T-14 & =K{e}^{-kt} \\ T & =14+K{e}^{-kt}\end{aligned}
$$

Note that $K={e}^{C}$ is a constant of integration. 

Apply the two observed conditions $T(2)=114$ and $T(7)=79$:

$$
\begin{aligned}114 & =14+Ke^{-2k} \\ 100 & =Ke^{-2k} \\ 79 & =14+Ke^{-7k} \\ 65 & =Ke^{-7k}\end{aligned}
$$

Divide the excess temperatures to eliminate $K$, then take natural logarithms:

$$
\begin{aligned}\frac{65}{100} & =\frac{Ke^{-7k}}{Ke^{-2k}} \\ \frac{13}{20} & =e^{-5k} \\ \ln(\frac{13}{20}) & =-5k \\ k & =- \frac{\ln{\left(\frac{13}{20} \right)}}{5}\end{aligned}
$$

Now substitute this rate into $T(2)=114$ to determine the constant:

$$
\begin{aligned}100 & =Ke^{-2(- \frac{\ln{\left(\frac{13}{20} \right)}}{5})} \\ K & =100e^{2(- \frac{\ln{\left(\frac{13}{20} \right)}}{5})} \\ K & =100\left(\frac{100}{65}\right)^{\frac{2}{5}}\end{aligned}
$$

Therefore, the solution satisfying both observations is

$$
T(t)=14+100\left(\frac{100}{65}\right)^{\frac{2}{5}}e^{-(- \frac{\ln{\left(\frac{13}{20} \right)}}{5})t}.
$$

Substituting the two observation times confirms the model:

$$
\begin{aligned}T(2) & =14+(100\left(\frac{100}{65}\right)^{\frac{2}{5}})e^{-(- \frac{\ln{\left(\frac{13}{20} \right)}}{5})\cdot 2}=114 \\ T(7) & =14+(100\left(\frac{100}{65}\right)^{\frac{2}{5}})e^{-(- \frac{\ln{\left(\frac{13}{20} \right)}}{5})\cdot 7}=79\end{aligned}
$$

Finally, let ${t}_{1}$ be the time when the body reaches ${32}^{∘}\text{C}.$ Then, we have

$$
\begin{aligned}T({t}_{1}) & =32 \\ 14+Ke^{-k{t}_{1}} & =32 \\ Ke^{-k{t}_{1}} & =18 \\ e^{-k{t}_{1}} & =\frac{18}{K} \\ -k{t}_{1} & =\ln\left(\frac{18}{K}\right) \\ {t}_{1} & =-\frac{1}{k}\ln\left(\frac{18}{K}\right)\end{aligned}
$$

Substitute the values of $K$ and $k$ to obtain the time measured since cooling began:

$$
\begin{aligned}{t}_{1} & =-\frac{1}{- \frac{\ln{\left(\frac{13}{20} \right)}}{5}}\ln\left(\frac{18}{100\left(\frac{100}{65}\right)^{\frac{2}{5}}}\right) \\ {t}_{1} & =2+5\frac{\ln(\frac{9}{50})}{\ln(\frac{13}{20})}≈22\,\text{min}.\end{aligned}
$$

---

A heated metal body cools in a room at ${22}^{∘}\text{C}.$ Its temperature is ${82}^{∘}\text{C}$ after $2$ minutes and ${54}^{∘}\text{C}$ after $7$ minutes. The temperature $T(t)$, in degrees Celsius, obeys Newton's law of cooling, with $t$ measured in minutes since cooling began. To the nearest minute, how long after cooling began does the body reach ${31}^{∘}\text{C}$?

- $15\,\text{min}$
- $32\,\text{min}$
- $17\,\text{min}$ **(correct)**
- $14\,\text{min}$
- $10\,\text{min}$

**Worked solution**

Newton's law of cooling states that the rate at which the temperature $T(t)$ of a body changes is proportional to the difference between its temperature and its surroundings. Therefore, we have the inhibited decay equation

$$
\frac{dT}{dt}=-k(T-22),\qquad k>0.
$$

First, we integrate our differential equation by separating the variables:

$$
\begin{aligned}\frac{dT}{T-22} & =-k\,dt \\ \int \frac{dT}{T-22} & =-k\int dt \\ \operatorname{ln}⁡|T-22| & =-kt+C\end{aligned}
$$

Since this is the solution to an inhibited decay equation, we have $T-22>0$ for all $t>0.$
Next, we solve for $T(t),$ as follows:

$$
\begin{aligned}T-22 & ={e}^{-kt+C} \\ T-22 & ={e}^{C}{e}^{-kt} \\ T-22 & =K{e}^{-kt} \\ T & =22+K{e}^{-kt}\end{aligned}
$$

Note that $K={e}^{C}$ is a constant of integration. 

Apply the two observed conditions $T(2)=82$ and $T(7)=54$:

$$
\begin{aligned}82 & =22+Ke^{-2k} \\ 60 & =Ke^{-2k} \\ 54 & =22+Ke^{-7k} \\ 32 & =Ke^{-7k}\end{aligned}
$$

Divide the excess temperatures to eliminate $K$, then take natural logarithms:

$$
\begin{aligned}\frac{32}{60} & =\frac{Ke^{-7k}}{Ke^{-2k}} \\ \frac{8}{15} & =e^{-5k} \\ \ln(\frac{8}{15}) & =-5k \\ k & =- \frac{\ln{\left(\frac{8}{15} \right)}}{5}\end{aligned}
$$

Now substitute this rate into $T(2)=82$ to determine the constant:

$$
\begin{aligned}60 & =Ke^{-2(- \frac{\ln{\left(\frac{8}{15} \right)}}{5})} \\ K & =60e^{2(- \frac{\ln{\left(\frac{8}{15} \right)}}{5})} \\ K & =60\left(\frac{60}{32}\right)^{\frac{2}{5}}\end{aligned}
$$

Therefore, the solution satisfying both observations is

$$
T(t)=22+60\left(\frac{60}{32}\right)^{\frac{2}{5}}e^{-(- \frac{\ln{\left(\frac{8}{15} \right)}}{5})t}.
$$

Substituting the two observation times confirms the model:

$$
\begin{aligned}T(2) & =22+(60\left(\frac{60}{32}\right)^{\frac{2}{5}})e^{-(- \frac{\ln{\left(\frac{8}{15} \right)}}{5})\cdot 2}=82 \\ T(7) & =22+(60\left(\frac{60}{32}\right)^{\frac{2}{5}})e^{-(- \frac{\ln{\left(\frac{8}{15} \right)}}{5})\cdot 7}=54\end{aligned}
$$

Finally, let ${t}_{1}$ be the time when the body reaches ${31}^{∘}\text{C}.$ Then, we have

$$
\begin{aligned}T({t}_{1}) & =31 \\ 22+Ke^{-k{t}_{1}} & =31 \\ Ke^{-k{t}_{1}} & =9 \\ e^{-k{t}_{1}} & =\frac{9}{K} \\ -k{t}_{1} & =\ln\left(\frac{9}{K}\right) \\ {t}_{1} & =-\frac{1}{k}\ln\left(\frac{9}{K}\right)\end{aligned}
$$

Substitute the values of $K$ and $k$ to obtain the time measured since cooling began:

$$
\begin{aligned}{t}_{1} & =-\frac{1}{- \frac{\ln{\left(\frac{8}{15} \right)}}{5}}\ln\left(\frac{9}{60\left(\frac{60}{32}\right)^{\frac{2}{5}}}\right) \\ {t}_{1} & =2+5\frac{\ln(\frac{3}{20})}{\ln(\frac{8}{15})}≈17\,\text{min}.\end{aligned}
$$

---

A heated metal body cools in a room at ${23}^{∘}\text{C}.$ Its temperature is ${110}^{∘}\text{C}$ after $2$ minutes and ${62}^{∘}\text{C}$ after $8$ minutes. The temperature $T(t)$, in degrees Celsius, obeys Newton's law of cooling, with $t$ measured in minutes since cooling began. To the nearest minute, how long after cooling began does the body reach ${25}^{∘}\text{C}$?

- $18\,\text{min}$
- $28\,\text{min}$
- $30\,\text{min}$ **(correct)**
- $58\,\text{min}$
- $16\,\text{min}$

**Worked solution**

Newton's law of cooling states that the rate at which the temperature $T(t)$ of a body changes is proportional to the difference between its temperature and its surroundings. Therefore, we have the inhibited decay equation

$$
\frac{dT}{dt}=-k(T-23),\qquad k>0.
$$

First, we integrate our differential equation by separating the variables:

$$
\begin{aligned}\frac{dT}{T-23} & =-k\,dt \\ \int \frac{dT}{T-23} & =-k\int dt \\ \operatorname{ln}⁡|T-23| & =-kt+C\end{aligned}
$$

Since this is the solution to an inhibited decay equation, we have $T-23>0$ for all $t>0.$
Next, we solve for $T(t),$ as follows:

$$
\begin{aligned}T-23 & ={e}^{-kt+C} \\ T-23 & ={e}^{C}{e}^{-kt} \\ T-23 & =K{e}^{-kt} \\ T & =23+K{e}^{-kt}\end{aligned}
$$

Note that $K={e}^{C}$ is a constant of integration. 

Apply the two observed conditions $T(2)=110$ and $T(8)=62$:

$$
\begin{aligned}110 & =23+Ke^{-2k} \\ 87 & =Ke^{-2k} \\ 62 & =23+Ke^{-8k} \\ 39 & =Ke^{-8k}\end{aligned}
$$

Divide the excess temperatures to eliminate $K$, then take natural logarithms:

$$
\begin{aligned}\frac{39}{87} & =\frac{Ke^{-8k}}{Ke^{-2k}} \\ \frac{13}{29} & =e^{-6k} \\ \ln(\frac{13}{29}) & =-6k \\ k & =- \frac{\ln{\left(\frac{13}{29} \right)}}{6}\end{aligned}
$$

Now substitute this rate into $T(2)=110$ to determine the constant:

$$
\begin{aligned}87 & =Ke^{-2(- \frac{\ln{\left(\frac{13}{29} \right)}}{6})} \\ K & =87e^{2(- \frac{\ln{\left(\frac{13}{29} \right)}}{6})} \\ K & =87\left(\frac{87}{39}\right)^{\frac{1}{3}}\end{aligned}
$$

Therefore, the solution satisfying both observations is

$$
T(t)=23+87\left(\frac{87}{39}\right)^{\frac{1}{3}}e^{-(- \frac{\ln{\left(\frac{13}{29} \right)}}{6})t}.
$$

Substituting the two observation times confirms the model:

$$
\begin{aligned}T(2) & =23+(87\left(\frac{87}{39}\right)^{\frac{1}{3}})e^{-(- \frac{\ln{\left(\frac{13}{29} \right)}}{6})\cdot 2}=110 \\ T(8) & =23+(87\left(\frac{87}{39}\right)^{\frac{1}{3}})e^{-(- \frac{\ln{\left(\frac{13}{29} \right)}}{6})\cdot 8}=62\end{aligned}
$$

Finally, let ${t}_{1}$ be the time when the body reaches ${25}^{∘}\text{C}.$ Then, we have

$$
\begin{aligned}T({t}_{1}) & =25 \\ 23+Ke^{-k{t}_{1}} & =25 \\ Ke^{-k{t}_{1}} & =2 \\ e^{-k{t}_{1}} & =\frac{2}{K} \\ -k{t}_{1} & =\ln\left(\frac{2}{K}\right) \\ {t}_{1} & =-\frac{1}{k}\ln\left(\frac{2}{K}\right)\end{aligned}
$$

Substitute the values of $K$ and $k$ to obtain the time measured since cooling began:

$$
\begin{aligned}{t}_{1} & =-\frac{1}{- \frac{\ln{\left(\frac{13}{29} \right)}}{6}}\ln\left(\frac{2}{87\left(\frac{87}{39}\right)^{\frac{1}{3}}}\right) \\ {t}_{1} & =2+6\frac{\ln(\frac{2}{87})}{\ln(\frac{13}{29})}≈30\,\text{min}.\end{aligned}
$$

---

A heated metal body cools in a room at ${18}^{∘}\text{C}.$ Its temperature is ${60}^{∘}\text{C}$ after $3$ minutes and ${39}^{∘}\text{C}$ after $7$ minutes. The temperature $T(t)$, in degrees Celsius, obeys Newton's law of cooling, with $t$ measured in minutes since cooling began. To the nearest minute, how long after cooling began does the body reach ${25}^{∘}\text{C}$?

- $10\,\text{min}$
- $8\,\text{min}$
- $24\,\text{min}$
- $13\,\text{min}$ **(correct)**
- $11\,\text{min}$

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

Apply the two observed conditions $T(3)=60$ and $T(7)=39$:

$$
\begin{aligned}60 & =18+Ke^{-3k} \\ 42 & =Ke^{-3k} \\ 39 & =18+Ke^{-7k} \\ 21 & =Ke^{-7k}\end{aligned}
$$

Divide the excess temperatures to eliminate $K$, then take natural logarithms:

$$
\begin{aligned}\frac{21}{42} & =\frac{Ke^{-7k}}{Ke^{-3k}} \\ \frac{1}{2} & =e^{-4k} \\ \ln(\frac{1}{2}) & =-4k \\ k & =\frac{\ln{\left(2 \right)}}{4}\end{aligned}
$$

Now substitute this rate into $T(3)=60$ to determine the constant:

$$
\begin{aligned}42 & =Ke^{-3(\frac{\ln{\left(2 \right)}}{4})} \\ K & =42e^{3(\frac{\ln{\left(2 \right)}}{4})} \\ K & =42\left(\frac{42}{21}\right)^{\frac{3}{4}}\end{aligned}
$$

Therefore, the solution satisfying both observations is

$$
T(t)=18+42\left(\frac{42}{21}\right)^{\frac{3}{4}}e^{-(\frac{\ln{\left(2 \right)}}{4})t}.
$$

Substituting the two observation times confirms the model:

$$
\begin{aligned}T(3) & =18+(42\left(\frac{42}{21}\right)^{\frac{3}{4}})e^{-(\frac{\ln{\left(2 \right)}}{4})\cdot 3}=60 \\ T(7) & =18+(42\left(\frac{42}{21}\right)^{\frac{3}{4}})e^{-(\frac{\ln{\left(2 \right)}}{4})\cdot 7}=39\end{aligned}
$$

Finally, let ${t}_{1}$ be the time when the body reaches ${25}^{∘}\text{C}.$ Then, we have

$$
\begin{aligned}T({t}_{1}) & =25 \\ 18+Ke^{-k{t}_{1}} & =25 \\ Ke^{-k{t}_{1}} & =7 \\ e^{-k{t}_{1}} & =\frac{7}{K} \\ -k{t}_{1} & =\ln\left(\frac{7}{K}\right) \\ {t}_{1} & =-\frac{1}{k}\ln\left(\frac{7}{K}\right)\end{aligned}
$$

Substitute the values of $K$ and $k$ to obtain the time measured since cooling began:

$$
\begin{aligned}{t}_{1} & =-\frac{1}{\frac{\ln{\left(2 \right)}}{4}}\ln\left(\frac{7}{42\left(\frac{42}{21}\right)^{\frac{3}{4}}}\right) \\ {t}_{1} & =3+4\frac{\ln(\frac{1}{6})}{\ln(\frac{1}{2})}≈13\,\text{min}.\end{aligned}
$$
