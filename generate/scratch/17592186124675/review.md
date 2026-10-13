# Original and generated review

Source basis 1356. All original profiles are empirical replay with unknown intent. Authored operation banks are default.

## original source replay q-15370

### Captured original

A University Campus has a total of $1\,500$ students.
At the beginning of the new semester at the University, flu affected $300$ students. After $10$ days, the number of students affected by the flu increases to $500.$ To the nearest day, how long does it take for the flu-stricken campus population to reach $800$ students?

*Hint: You may assume that the number of students affected by the flu, $P(t),$ increases at a rate that obeys an inhibited growth model, where $t\ge 0$ is the time, in days.*

- $12$ days
- $21$ days
- $17$ days
- $30$ days
- $45$ days

The rate at which the campus population affected by the flu, $P(t),$ changes is proportional to the difference between the total campus population and its current population affected. Therefore, we have the inhibited growth equation

$$
\frac{dP}{dt}=k(a-P),
$$

where $a$ is the total population of the campus, and $k>0$ is a constant of proportionality.

In our case, $a=1\,500$ students, and we have

$$
\frac{dP}{dt}=k(1\,500-P).
$$

First, we integrate our differential equation by separating the variables:

$$
\begin{aligned}\frac{dP}{1\,500-P} & =k\,dt \\ \int \frac{dP}{1\,500-P} & =\int k\,dt \\ -\operatorname{ln}⁡|1\,500-P| & =kt+C\end{aligned}
$$

Since this is the solution to an inhibited growth equation, we have $1\,500-P>0$ for all $t\ge 0.$
Next, we solve for $P(t),$ as follows:

$$
\begin{aligned}1\,500-P & ={e}^{-kt-C} \\ 1\,500-P & ={e}^{-C}{e}^{-kt} \\ 1\,500-P & =K{e}^{-kt} \\ P & =1\,500-K{e}^{-kt}\end{aligned}
$$

Note that $K={e}^{-C}$ is a constant of integration. 

We're told that the initial campus population affected by the flu was $300$ students. So, we apply the initial condition $P(0)=300,$ and solve for $K:$

$$
\begin{aligned}P(0) & =300 \\ 1\,500-K{e}^{0} & =300 \\ 1\,500-K & =300 \\ K & =1\,200\end{aligned}
$$

Therefore, we have the following expression for $P(t):$

$$
P(t)=1\,500-1\,200{e}^{-kt}
$$

We're also told that, after $10$ days, the campus population affected by flu was $500$ students. So, applying the condition $P(10)=500,$ we can solve for $k:$

$$
\begin{aligned}P(10) & =500 \\ 1\,500-1\,200{e}^{-10k} & =500 \\ 1\,000 & =1\,200{e}^{-10k} \\ {e}^{-10k} & =\frac{5}{6} \\ -10k & =\operatorname{ln}⁡(\frac{5}{6}) \\ k & =-\frac{1}{10}\operatorname{ln}⁡(\frac{5}{6})\end{aligned}
$$

Finally, let ${t}_{1}$ be the time when $800$ students are affected by the flu. Then, we have

$$
\begin{aligned}P({t}_{1}) & =800 \\ 1\,500-1\,200{e}^{-k{t}_{1}} & =800 \\ 700 & =1\,200{e}^{-k{t}_{1}} \\ {e}^{-k{t}_{1}} & =\frac{7}{12} \\ -k{t}_{1} & =\operatorname{ln}⁡(\frac{7}{12}) \\ {t}_{1} & =-\frac{1}{k}\operatorname{ln}⁡(\frac{7}{12}).\end{aligned}
$$

Substituting in our value for $k,$ we conclude that $800$ students will be affected by the flu after

$$
{t}_{1}=\frac{-\operatorname{ln}⁡(\frac{7}{12})}{-\frac{1}{10}\operatorname{ln}⁡(\frac{5}{6})}=29.562…≈30\,\text{days},
$$

rounded to the nearest day.

### Generated record

A University Campus has a total of $1\,500$ students.
At the beginning of the new semester at the University, flu affected $300$ students. After $10$ days, the number of students affected by the flu increases to $500.$ To the nearest day, how long does it take for the flu-stricken campus population to reach $800$ students?

*Hint: You may assume that the number of students affected by the flu, $P(t),$ increases at a rate that obeys an inhibited growth model, where $t\ge 0$ is the time, in days.*

- $17$ days
- $21$ days
- $12$ days
- $45$ days
- $30$ days **correct**

The rate at which the campus population affected by the flu, $P(t),$ changes is proportional to the difference between the total campus population and its current population affected. Therefore, we have the inhibited growth equation

$$
\frac{dP}{dt}=k(a-P),
$$

where $a$ is the total population of the campus, and $k>0$ is a constant of proportionality.

In our case, $a=1\,500$ students, and we have

$$
\frac{dP}{dt}=k(1\,500-P).
$$

First, we integrate our differential equation by separating the variables:

$$
\begin{aligned}\frac{dP}{1\,500-P} & =k\,dt \\ \int \frac{dP}{1\,500-P} & =\int k\,dt \\ -\operatorname{ln}⁡|1\,500-P| & =kt+C\end{aligned}
$$

Since this is the solution to an inhibited growth equation, we have $1\,500-P>0$ for all $t\ge 0.$
Next, we solve for $P(t),$ as follows:

$$
\begin{aligned}1\,500-P & ={e}^{-kt-C} \\ 1\,500-P & ={e}^{-C}{e}^{-kt} \\ 1\,500-P & =K{e}^{-kt} \\ P & =1\,500-K{e}^{-kt}\end{aligned}
$$

Note that $K={e}^{-C}$ is a constant of integration. 

We're told that the initial campus population affected by the flu was $300$ students. So, we apply the initial condition $P(0)=300,$ and solve for $K:$

$$
\begin{aligned}P(0) & =300 \\ 1\,500-K{e}^{0} & =300 \\ 1\,500-K & =300 \\ K & =1\,200\end{aligned}
$$

Therefore, we have the following expression for $P(t):$

$$
P(t)=1\,500-1\,200{e}^{-kt}
$$

We're also told that, after $10$ days, the campus population affected by flu was $500$ students. So, applying the condition $P(10)=500,$ we can solve for $k:$

$$
\begin{aligned}P(10) & =500 \\ 1\,500-1\,200{e}^{-10k} & =500 \\ 1\,000 & =1\,200{e}^{-10k} \\ {e}^{-10k} & =\frac{5}{6} \\ -10k & =\operatorname{ln}⁡(\frac{5}{6}) \\ k & =-\frac{1}{10}\operatorname{ln}⁡(\frac{5}{6})\end{aligned}
$$

Finally, let ${t}_{1}$ be the time when $800$ students are affected by the flu. Then, we have

$$
\begin{aligned}P({t}_{1}) & =800 \\ 1\,500-1\,200{e}^{-k{t}_{1}} & =800 \\ 700 & =1\,200{e}^{-k{t}_{1}} \\ {e}^{-k{t}_{1}} & =\frac{7}{12} \\ -k{t}_{1} & =\operatorname{ln}⁡(\frac{7}{12}) \\ {t}_{1} & =-\frac{1}{k}\operatorname{ln}⁡(\frac{7}{12}).\end{aligned}
$$

Substituting in our value for $k,$ we conclude that $800$ students will be affected by the flu after

$$
{t}_{1}=\frac{-\operatorname{ln}⁡(\frac{7}{12})}{-\frac{1}{10}\operatorname{ln}⁡(\frac{5}{6})}=29.562…≈30\,\text{days},
$$

rounded to the nearest day.

## generated variant; observed empirical unknown intent q-15370 0

### Generated record

A University Campus has a total of $6\,000$ students.
At the beginning of the new semester at the University, flu affected $1200$ students. After $20$ days, the number of students affected by the flu increases to $2000.$ To the nearest day, how long does it take for the flu-stricken campus population to reach $3200$ students?

*Hint: You may assume that the number of students affected by the flu, $P(t),$ increases at a rate that obeys an inhibited growth model, where $t\ge 0$ is the time, in days.*

- $33$ days
- $59$ days **correct**
- $24$ days
- $41$ days
- $89$ days

The rate at which the campus population affected by the flu, $P(t),$ changes is proportional to the difference between the total campus population and its current population affected. Therefore, we have the inhibited growth equation

$$
\frac{dP}{dt}=k(a-P),
$$

where $a$ is the total population of the campus, and $k>0$ is a constant of proportionality.

In our case, $a=6\,000$ students, and we have

$$
\frac{dP}{dt}=k(6\,000-P).
$$

First, we integrate our differential equation by separating the variables:

$$
\begin{aligned}\frac{dP}{6\,000-P} & =k\,dt \\ \int \frac{dP}{6\,000-P} & =\int k\,dt \\ -\operatorname{ln}⁡|6\,000-P| & =kt+C\end{aligned}
$$

Since this is the solution to an inhibited growth equation, we have $6\,000-P>0$ for all $t\ge 0.$
Next, we solve for $P(t),$ as follows:

$$
\begin{aligned}6\,000-P & ={e}^{-kt-C} \\ 6\,000-P & ={e}^{-C}{e}^{-kt} \\ 6\,000-P & =K{e}^{-kt} \\ P & =6\,000-K{e}^{-kt}\end{aligned}
$$

Note that $K={e}^{-C}$ is a constant of integration. 

We're told that the initial campus population affected by the flu was $1200$ students. So, we apply the initial condition $P(0)=1200,$ and solve for $K:$

$$
\begin{aligned}P(0) & =1200 \\ 6\,000-K{e}^{0} & =1200 \\ 6\,000-K & =1200 \\ K & =4\,800\end{aligned}
$$

Therefore, we have the following expression for $P(t):$

$$
P(t)=6\,000-4\,800{e}^{-kt}
$$

We're also told that, after $20$ days, the campus population affected by flu was $2000$ students. So, applying the condition $P(20)=2000,$ we can solve for $k:$

$$
\begin{aligned}P(20) & =2000 \\ 6\,000-4\,800{e}^{-20k} & =2000 \\ 4\,000 & =4\,800{e}^{-20k} \\ {e}^{-20k} & =\frac{5}{6} \\ -20k & =\operatorname{ln}⁡(\frac{5}{6}) \\ k & =-\frac{1}{20}\operatorname{ln}⁡(\frac{5}{6})\end{aligned}
$$

Finally, let ${t}_{1}$ be the time when $3200$ students are affected by the flu. Then, we have

$$
\begin{aligned}P({t}_{1}) & =3200 \\ 6\,000-4\,800{e}^{-k{t}_{1}} & =3200 \\ 2800 & =4\,800{e}^{-k{t}_{1}} \\ {e}^{-k{t}_{1}} & =\frac{7}{12} \\ -k{t}_{1} & =\operatorname{ln}⁡(\frac{7}{12}) \\ {t}_{1} & =-\frac{1}{k}\operatorname{ln}⁡(\frac{7}{12}).\end{aligned}
$$

Substituting in our value for $k,$ we conclude that $3200$ students will be affected by the flu after

$$
{t}_{1}=\frac{-\operatorname{ln}⁡(\frac{7}{12})}{-\frac{1}{20}\operatorname{ln}⁡(\frac{5}{6})}=59.125…≈59\,\text{days},
$$

rounded to the nearest day.

## generated variant; observed empirical unknown intent q-15370 1

### Generated record

A University Campus has a total of $3\,000$ students.
At the beginning of the new semester at the University, flu affected $600$ students. After $20$ days, the number of students affected by the flu increases to $1000.$ To the nearest day, how long does it take for the flu-stricken campus population to reach $1600$ students?

*Hint: You may assume that the number of students affected by the flu, $P(t),$ increases at a rate that obeys an inhibited growth model, where $t\ge 0$ is the time, in days.*

- $89$ days
- $59$ days **correct**
- $33$ days
- $41$ days
- $24$ days

The rate at which the campus population affected by the flu, $P(t),$ changes is proportional to the difference between the total campus population and its current population affected. Therefore, we have the inhibited growth equation

$$
\frac{dP}{dt}=k(a-P),
$$

where $a$ is the total population of the campus, and $k>0$ is a constant of proportionality.

In our case, $a=3\,000$ students, and we have

$$
\frac{dP}{dt}=k(3\,000-P).
$$

First, we integrate our differential equation by separating the variables:

$$
\begin{aligned}\frac{dP}{3\,000-P} & =k\,dt \\ \int \frac{dP}{3\,000-P} & =\int k\,dt \\ -\operatorname{ln}⁡|3\,000-P| & =kt+C\end{aligned}
$$

Since this is the solution to an inhibited growth equation, we have $3\,000-P>0$ for all $t\ge 0.$
Next, we solve for $P(t),$ as follows:

$$
\begin{aligned}3\,000-P & ={e}^{-kt-C} \\ 3\,000-P & ={e}^{-C}{e}^{-kt} \\ 3\,000-P & =K{e}^{-kt} \\ P & =3\,000-K{e}^{-kt}\end{aligned}
$$

Note that $K={e}^{-C}$ is a constant of integration. 

We're told that the initial campus population affected by the flu was $600$ students. So, we apply the initial condition $P(0)=600,$ and solve for $K:$

$$
\begin{aligned}P(0) & =600 \\ 3\,000-K{e}^{0} & =600 \\ 3\,000-K & =600 \\ K & =2\,400\end{aligned}
$$

Therefore, we have the following expression for $P(t):$

$$
P(t)=3\,000-2\,400{e}^{-kt}
$$

We're also told that, after $20$ days, the campus population affected by flu was $1000$ students. So, applying the condition $P(20)=1000,$ we can solve for $k:$

$$
\begin{aligned}P(20) & =1000 \\ 3\,000-2\,400{e}^{-20k} & =1000 \\ 2\,000 & =2\,400{e}^{-20k} \\ {e}^{-20k} & =\frac{5}{6} \\ -20k & =\operatorname{ln}⁡(\frac{5}{6}) \\ k & =-\frac{1}{20}\operatorname{ln}⁡(\frac{5}{6})\end{aligned}
$$

Finally, let ${t}_{1}$ be the time when $1600$ students are affected by the flu. Then, we have

$$
\begin{aligned}P({t}_{1}) & =1600 \\ 3\,000-2\,400{e}^{-k{t}_{1}} & =1600 \\ 1400 & =2\,400{e}^{-k{t}_{1}} \\ {e}^{-k{t}_{1}} & =\frac{7}{12} \\ -k{t}_{1} & =\operatorname{ln}⁡(\frac{7}{12}) \\ {t}_{1} & =-\frac{1}{k}\operatorname{ln}⁡(\frac{7}{12}).\end{aligned}
$$

Substituting in our value for $k,$ we conclude that $1600$ students will be affected by the flu after

$$
{t}_{1}=\frac{-\operatorname{ln}⁡(\frac{7}{12})}{-\frac{1}{20}\operatorname{ln}⁡(\frac{5}{6})}=59.125…≈59\,\text{days},
$$

rounded to the nearest day.

## generated variant; authored operation bank q-15370 0

### Generated record

A University Campus has a total of $1\,300$ students.
At the beginning of the new semester at the University, flu affected $350$ students. After $10$ days, the number of students affected by the flu increases to $750.$ To the nearest day, how long does it take for the flu-stricken campus population to reach $1100$ students?

*Hint: You may assume that the number of students affected by the flu, $P(t),$ increases at a rate that obeys an inhibited growth model, where $t\ge 0$ is the time, in days.*

- $29$ days **correct**
- $18$ days
- $21$ days
- $14$ days
- $2$ days

The rate at which the campus population affected by the flu, $P(t),$ changes is proportional to the difference between the total campus population and its current population affected. Therefore, we have the inhibited growth equation

$$
\frac{dP}{dt}=k(a-P),
$$

where $a$ is the total population of the campus, and $k>0$ is a constant of proportionality.

In our case, $a=1\,300$ students, and we have

$$
\frac{dP}{dt}=k(1\,300-P).
$$

First, we integrate our differential equation by separating the variables:

$$
\begin{aligned}\frac{dP}{1\,300-P} & =k\,dt \\ \int \frac{dP}{1\,300-P} & =\int k\,dt \\ -\operatorname{ln}⁡|1\,300-P| & =kt+C\end{aligned}
$$

Since this is the solution to an inhibited growth equation, we have $1\,300-P>0$ for all $t\ge 0.$
Next, we solve for $P(t),$ as follows:

$$
\begin{aligned}1\,300-P & ={e}^{-kt-C} \\ 1\,300-P & ={e}^{-C}{e}^{-kt} \\ 1\,300-P & =K{e}^{-kt} \\ P & =1\,300-K{e}^{-kt}\end{aligned}
$$

Note that $K={e}^{-C}$ is a constant of integration. 

We're told that the initial campus population affected by the flu was $350$ students. So, we apply the initial condition $P(0)=350,$ and solve for $K:$

$$
\begin{aligned}P(0) & =350 \\ 1\,300-K{e}^{0} & =350 \\ 1\,300-K & =350 \\ K & =950\end{aligned}
$$

Therefore, we have the following expression for $P(t):$

$$
P(t)=1\,300-950{e}^{-kt}
$$

We're also told that, after $10$ days, the campus population affected by flu was $750$ students. So, applying the condition $P(10)=750,$ we can solve for $k:$

$$
\begin{aligned}P(10) & =750 \\ 1\,300-950{e}^{-10k} & =750 \\ 550 & =950{e}^{-10k} \\ {e}^{-10k} & =\frac{11}{19} \\ -10k & =\operatorname{ln}⁡(\frac{11}{19}) \\ k & =-\frac{1}{10}\operatorname{ln}⁡(\frac{11}{19})\end{aligned}
$$

Finally, let ${t}_{1}$ be the time when $1100$ students are affected by the flu. Then, we have

$$
\begin{aligned}P({t}_{1}) & =1100 \\ 1\,300-950{e}^{-k{t}_{1}} & =1100 \\ 200 & =950{e}^{-k{t}_{1}} \\ {e}^{-k{t}_{1}} & =\frac{4}{19} \\ -k{t}_{1} & =\operatorname{ln}⁡(\frac{4}{19}) \\ {t}_{1} & =-\frac{1}{k}\operatorname{ln}⁡(\frac{4}{19}).\end{aligned}
$$

Substituting in our value for $k,$ we conclude that $1100$ students will be affected by the flu after

$$
{t}_{1}=\frac{-\operatorname{ln}⁡(\frac{4}{19})}{-\frac{1}{10}\operatorname{ln}⁡(\frac{11}{19})}=28.509…≈29\,\text{days},
$$

rounded to the nearest day.

## generated variant; authored operation bank q-15370 1

### Generated record

A University Campus has a total of $1\,200$ students.
At the beginning of the new semester at the University, flu affected $100$ students. After $5$ days, the number of students affected by the flu increases to $200.$ To the nearest day, how long does it take for the flu-stricken campus population to reach $1150$ students?

*Hint: You may assume that the number of students affected by the flu, $P(t),$ increases at a rate that obeys an inhibited growth model, where $t\ge 0$ is the time, in days.*

- $128$ days
- $50$ days
- $162$ days **correct**
- $52$ days
- $3$ days

The rate at which the campus population affected by the flu, $P(t),$ changes is proportional to the difference between the total campus population and its current population affected. Therefore, we have the inhibited growth equation

$$
\frac{dP}{dt}=k(a-P),
$$

where $a$ is the total population of the campus, and $k>0$ is a constant of proportionality.

In our case, $a=1\,200$ students, and we have

$$
\frac{dP}{dt}=k(1\,200-P).
$$

First, we integrate our differential equation by separating the variables:

$$
\begin{aligned}\frac{dP}{1\,200-P} & =k\,dt \\ \int \frac{dP}{1\,200-P} & =\int k\,dt \\ -\operatorname{ln}⁡|1\,200-P| & =kt+C\end{aligned}
$$

Since this is the solution to an inhibited growth equation, we have $1\,200-P>0$ for all $t\ge 0.$
Next, we solve for $P(t),$ as follows:

$$
\begin{aligned}1\,200-P & ={e}^{-kt-C} \\ 1\,200-P & ={e}^{-C}{e}^{-kt} \\ 1\,200-P & =K{e}^{-kt} \\ P & =1\,200-K{e}^{-kt}\end{aligned}
$$

Note that $K={e}^{-C}$ is a constant of integration. 

We're told that the initial campus population affected by the flu was $100$ students. So, we apply the initial condition $P(0)=100,$ and solve for $K:$

$$
\begin{aligned}P(0) & =100 \\ 1\,200-K{e}^{0} & =100 \\ 1\,200-K & =100 \\ K & =1\,100\end{aligned}
$$

Therefore, we have the following expression for $P(t):$

$$
P(t)=1\,200-1\,100{e}^{-kt}
$$

We're also told that, after $5$ days, the campus population affected by flu was $200$ students. So, applying the condition $P(5)=200,$ we can solve for $k:$

$$
\begin{aligned}P(5) & =200 \\ 1\,200-1\,100{e}^{-5k} & =200 \\ 1\,000 & =1\,100{e}^{-5k} \\ {e}^{-5k} & =\frac{10}{11} \\ -5k & =\operatorname{ln}⁡(\frac{10}{11}) \\ k & =-\frac{1}{5}\operatorname{ln}⁡(\frac{10}{11})\end{aligned}
$$

Finally, let ${t}_{1}$ be the time when $1150$ students are affected by the flu. Then, we have

$$
\begin{aligned}P({t}_{1}) & =1150 \\ 1\,200-1\,100{e}^{-k{t}_{1}} & =1150 \\ 50 & =1\,100{e}^{-k{t}_{1}} \\ {e}^{-k{t}_{1}} & =\frac{1}{22} \\ -k{t}_{1} & =\operatorname{ln}⁡(\frac{1}{22}) \\ {t}_{1} & =-\frac{1}{k}\operatorname{ln}⁡(\frac{1}{22}).\end{aligned}
$$

Substituting in our value for $k,$ we conclude that $1150$ students will be affected by the flu after

$$
{t}_{1}=\frac{-\operatorname{ln}⁡(\frac{1}{22})}{-\frac{1}{5}\operatorname{ln}⁡(\frac{10}{11})}=162.156…≈162\,\text{days},
$$

rounded to the nearest day.

## original source replay q-37389

### Captured original

A poultry farmer has egg-laying chickens. She knows that her farm can produce a maximum of $500$ eggs a day; however, it is far behind it.
Since she started monitoring, the chickens laid $390$ eggs and $400$ eggs on days $3$ and $6$, respectively. How many eggs do the chickens lay on day $42$?
Round your answer to the nearest integer.

*Hint: You may assume that the egg production $E(t)$ increases at a rate that obeys an inhibited growth model, where $t$ is the time, in days.*

- $468$ eggs
- $489$ eggs
- $420$ eggs
- $486$ eggs
- $442$ eggs

No captured solution. Hard assignment and solution below are authored.

### Generated record

A poultry farmer has egg-laying chickens. She knows that her farm can produce a maximum of $500$ eggs a day; however, it is far behind it.
Since she started monitoring, the chickens laid $390$ eggs and $400$ eggs on days $3$ and $6$, respectively. How many eggs do the chickens lay on day $42$?
Round your answer to the nearest integer.

*Hint: You may assume that the egg production $E(t)$ increases at a rate that obeys an inhibited growth model, where $t$ is the time, in days.*

- $420$ eggs
- $489$ eggs
- $468$ eggs **correct**
- $442$ eggs
- $486$ eggs

The rate at which the egg production $E(t)$ changes is proportional to the difference between the maximum possible egg production and its current egg production. Therefore, we have the inhibited growth equation

$$
\frac{dE}{dt}=k(a-E),
$$

where $a$ is the maximum production of the farm, and $k>0$ is a constant of proportionality.

In our case, $a=500$ eggs, and we have

$$
\frac{dE}{dt}=k(500-E).
$$

First, we integrate our differential equation by separating the variables:

$$
\begin{aligned}\frac{dE}{500-E} & =k\,dt \\ \int \frac{dE}{500-E} & =\int k\,\text{d}t \\ -\operatorname{ln}⁡|500-E| & =kt+C\end{aligned}
$$

Since this is the solution to an inhibited growth equation, we have $500-E>0$ for all $t\ge 0.$ Next, we solve for $E(t),$ as follows:

$$
\begin{aligned}500-E & ={e}^{-kt-C} \\ 500-E & ={e}^{-C}{e}^{-kt} \\ 500-E & =K{e}^{-kt} \\ E & =500-K{e}^{-kt}\end{aligned}
$$

Note that $K={e}^{-C}$ is a constant of integration.

We're told that, on day $3,$ the egg production was $390$ eggs. So, applying the condition $E(3)=390,$ we have

$$
\begin{aligned}E(3) & =390 \\ 500-K{e}^{-3k} & =390 \\ K{e}^{-3k} & =110.\end{aligned}
$$

We're also told that, on day $6,$ the egg production was $400$ eggs. So, applying the condition $E(6)=400,$ we get

$$
\begin{aligned}E(6) & =400 \\ 500-K{e}^{-6k} & =400 \\ K{e}^{-6k} & =100.\end{aligned}
$$

Then, by dividing the result of the first condition by the result of the second, we can solve for $k:$

$$
\begin{aligned}\frac{K{e}^{-3k}}{K{e}^{-6k}} & =\frac{110}{100} \\ {e}^{3k} & =\frac{11}{10} \\ 3k & =\operatorname{ln}⁡(\frac{11}{10}) \\ k & =\frac{1}{3}\operatorname{ln}⁡(\frac{11}{10})\end{aligned}
$$

Now, substituting back into the result of the first condition, we solve for $K:$

$$
\begin{aligned}K{e}^{-3\cdot (1/3)\operatorname{ln}⁡(11/10)} & =110 \\ K & =110{e}^{\operatorname{ln}⁡(11/10)} \\ K & =121\end{aligned}
$$

Therefore, we have the following expression for $E(t):$

$$
E(t)=500-121{e}^{-(t/3)\operatorname{ln}⁡(11/10)}
$$

Finally, the number of eggs laid on day $t=42$ is

$$
E(42)=500-121{e}^{-(42/3)\operatorname{ln}⁡(11/10)}≈468.136…≈468\,\text{eggs},
$$

rounded to the nearest integer.

## generated variant; observed empirical unknown intent q-37389 0

### Generated record

A poultry farmer has egg-laying chickens. She knows that her farm can produce a maximum of $2000$ eggs a day; however, it is far behind it.
Since she started monitoring, the chickens laid $1560$ eggs and $1600$ eggs on days $6$ and $12$, respectively. How many eggs do the chickens lay on day $84$?
Round your answer to the nearest integer.

*Hint: You may assume that the egg production $E(t)$ increases at a rate that obeys an inhibited growth model, where $t$ is the time, in days.*

- $1681$ eggs
- $1945$ eggs
- $1873$ eggs **correct**
- $1957$ eggs
- $1769$ eggs

The rate at which the egg production $E(t)$ changes is proportional to the difference between the maximum possible egg production and its current egg production. Therefore, we have the inhibited growth equation

$$
\frac{dE}{dt}=k(a-E),
$$

where $a$ is the maximum production of the farm, and $k>0$ is a constant of proportionality.

In our case, $a=2000$ eggs, and we have

$$
\frac{dE}{dt}=k(2000-E).
$$

First, we integrate our differential equation by separating the variables:

$$
\begin{aligned}\frac{dE}{2000-E} & =k\,dt \\ \int \frac{dE}{2000-E} & =\int k\,\text{d}t \\ -\operatorname{ln}⁡|2000-E| & =kt+C\end{aligned}
$$

Since this is the solution to an inhibited growth equation, we have $2000-E>0$ for all $t\ge 0.$ Next, we solve for $E(t),$ as follows:

$$
\begin{aligned}2000-E & ={e}^{-kt-C} \\ 2000-E & ={e}^{-C}{e}^{-kt} \\ 2000-E & =K{e}^{-kt} \\ E & =2000-K{e}^{-kt}\end{aligned}
$$

Note that $K={e}^{-C}$ is a constant of integration.

We're told that, on day $6,$ the egg production was $1560$ eggs. So, applying the condition $E(6)=1560,$ we have

$$
\begin{aligned}E(6) & =1560 \\ 2000-K{e}^{-6k} & =1560 \\ K{e}^{-6k} & =440.\end{aligned}
$$

We're also told that, on day $12,$ the egg production was $1600$ eggs. So, applying the condition $E(12)=1600,$ we get

$$
\begin{aligned}E(12) & =1600 \\ 2000-K{e}^{-12k} & =1600 \\ K{e}^{-12k} & =400.\end{aligned}
$$

Then, by dividing the result of the first condition by the result of the second, we can solve for $k:$

$$
\begin{aligned}\frac{K{e}^{-6k}}{K{e}^{-12k}} & =\frac{440}{400} \\ {e}^{6k} & =\frac{11}{10} \\ 6k & =\operatorname{ln}⁡(\frac{11}{10}) \\ k & =\frac{1}{6}\operatorname{ln}⁡(\frac{11}{10})\end{aligned}
$$

Now, substituting back into the result of the first condition, we solve for $K:$

$$
\begin{aligned}K{e}^{-6\cdot (1/6)\operatorname{ln}⁡(11/10)} & =440 \\ K & =440{e}^{\operatorname{ln}⁡(11/10)} \\ K & =484\end{aligned}
$$

Therefore, we have the following expression for $E(t):$

$$
E(t)=2000-484{e}^{-(t/6)\operatorname{ln}⁡(11/10)}
$$

Finally, the number of eggs laid on day $t=84$ is

$$
E(84)=2000-484{e}^{-(84/6)\operatorname{ln}⁡(11/10)}≈1872.547…≈1873\,\text{eggs},
$$

rounded to the nearest integer.

## generated variant; observed empirical unknown intent q-37389 1

### Generated record

A poultry farmer has egg-laying chickens. She knows that her farm can produce a maximum of $1000$ eggs a day; however, it is far behind it.
Since she started monitoring, the chickens laid $780$ eggs and $800$ eggs on days $6$ and $12$, respectively. How many eggs do the chickens lay on day $84$?
Round your answer to the nearest integer.

*Hint: You may assume that the egg production $E(t)$ increases at a rate that obeys an inhibited growth model, where $t$ is the time, in days.*

- $884$ eggs
- $972$ eggs
- $840$ eggs
- $978$ eggs
- $936$ eggs **correct**

The rate at which the egg production $E(t)$ changes is proportional to the difference between the maximum possible egg production and its current egg production. Therefore, we have the inhibited growth equation

$$
\frac{dE}{dt}=k(a-E),
$$

where $a$ is the maximum production of the farm, and $k>0$ is a constant of proportionality.

In our case, $a=1000$ eggs, and we have

$$
\frac{dE}{dt}=k(1000-E).
$$

First, we integrate our differential equation by separating the variables:

$$
\begin{aligned}\frac{dE}{1000-E} & =k\,dt \\ \int \frac{dE}{1000-E} & =\int k\,\text{d}t \\ -\operatorname{ln}⁡|1000-E| & =kt+C\end{aligned}
$$

Since this is the solution to an inhibited growth equation, we have $1000-E>0$ for all $t\ge 0.$ Next, we solve for $E(t),$ as follows:

$$
\begin{aligned}1000-E & ={e}^{-kt-C} \\ 1000-E & ={e}^{-C}{e}^{-kt} \\ 1000-E & =K{e}^{-kt} \\ E & =1000-K{e}^{-kt}\end{aligned}
$$

Note that $K={e}^{-C}$ is a constant of integration.

We're told that, on day $6,$ the egg production was $780$ eggs. So, applying the condition $E(6)=780,$ we have

$$
\begin{aligned}E(6) & =780 \\ 1000-K{e}^{-6k} & =780 \\ K{e}^{-6k} & =220.\end{aligned}
$$

We're also told that, on day $12,$ the egg production was $800$ eggs. So, applying the condition $E(12)=800,$ we get

$$
\begin{aligned}E(12) & =800 \\ 1000-K{e}^{-12k} & =800 \\ K{e}^{-12k} & =200.\end{aligned}
$$

Then, by dividing the result of the first condition by the result of the second, we can solve for $k:$

$$
\begin{aligned}\frac{K{e}^{-6k}}{K{e}^{-12k}} & =\frac{220}{200} \\ {e}^{6k} & =\frac{11}{10} \\ 6k & =\operatorname{ln}⁡(\frac{11}{10}) \\ k & =\frac{1}{6}\operatorname{ln}⁡(\frac{11}{10})\end{aligned}
$$

Now, substituting back into the result of the first condition, we solve for $K:$

$$
\begin{aligned}K{e}^{-6\cdot (1/6)\operatorname{ln}⁡(11/10)} & =220 \\ K & =220{e}^{\operatorname{ln}⁡(11/10)} \\ K & =242\end{aligned}
$$

Therefore, we have the following expression for $E(t):$

$$
E(t)=1000-242{e}^{-(t/6)\operatorname{ln}⁡(11/10)}
$$

Finally, the number of eggs laid on day $t=84$ is

$$
E(84)=1000-242{e}^{-(84/6)\operatorname{ln}⁡(11/10)}≈936.273…≈936\,\text{eggs},
$$

rounded to the nearest integer.

## generated variant; authored operation bank q-37389 0

### Generated record

A poultry farmer has egg-laying chickens. She knows that her farm can produce a maximum of $800$ eggs a day; however, it is far behind it.
Since she started monitoring, the chickens laid $700$ eggs and $720$ eggs on days $3$ and $6$, respectively. How many eggs do the chickens lay on day $36$?
Round your answer to the nearest integer.

*Hint: You may assume that the egg production $E(t)$ increases at a rate that obeys an inhibited growth model, where $t$ is the time, in days.*

- $791$ eggs **correct**
- $48$ eggs
- $745$ eggs
- $684$ eggs
- $752$ eggs

The rate at which the egg production $E(t)$ changes is proportional to the difference between the maximum possible egg production and its current egg production. Therefore, we have the inhibited growth equation

$$
\frac{dE}{dt}=k(a-E),
$$

where $a$ is the maximum production of the farm, and $k>0$ is a constant of proportionality.

In our case, $a=800$ eggs, and we have

$$
\frac{dE}{dt}=k(800-E).
$$

First, we integrate our differential equation by separating the variables:

$$
\begin{aligned}\frac{dE}{800-E} & =k\,dt \\ \int \frac{dE}{800-E} & =\int k\,\text{d}t \\ -\operatorname{ln}⁡|800-E| & =kt+C\end{aligned}
$$

Since this is the solution to an inhibited growth equation, we have $800-E>0$ for all $t\ge 0.$ Next, we solve for $E(t),$ as follows:

$$
\begin{aligned}800-E & ={e}^{-kt-C} \\ 800-E & ={e}^{-C}{e}^{-kt} \\ 800-E & =K{e}^{-kt} \\ E & =800-K{e}^{-kt}\end{aligned}
$$

Note that $K={e}^{-C}$ is a constant of integration.

We're told that, on day $3,$ the egg production was $700$ eggs. So, applying the condition $E(3)=700,$ we have

$$
\begin{aligned}E(3) & =700 \\ 800-K{e}^{-3k} & =700 \\ K{e}^{-3k} & =100.\end{aligned}
$$

We're also told that, on day $6,$ the egg production was $720$ eggs. So, applying the condition $E(6)=720,$ we get

$$
\begin{aligned}E(6) & =720 \\ 800-K{e}^{-6k} & =720 \\ K{e}^{-6k} & =80.\end{aligned}
$$

Then, by dividing the result of the first condition by the result of the second, we can solve for $k:$

$$
\begin{aligned}\frac{K{e}^{-3k}}{K{e}^{-6k}} & =\frac{100}{80} \\ {e}^{3k} & =\frac{5}{4} \\ 3k & =\operatorname{ln}⁡(\frac{5}{4}) \\ k & =\frac{1}{3}\operatorname{ln}⁡(\frac{5}{4})\end{aligned}
$$

Now, substituting back into the result of the first condition, we solve for $K:$

$$
\begin{aligned}K{e}^{-3\cdot (1/3)\operatorname{ln}⁡(5/4)} & =100 \\ K & =100{e}^{\operatorname{ln}⁡(5/4)} \\ K & =125\end{aligned}
$$

Therefore, we have the following expression for $E(t):$

$$
E(t)=800-125{e}^{-(t/3)\operatorname{ln}⁡(5/4)}
$$

Finally, the number of eggs laid on day $t=36$ is

$$
E(36)=800-125{e}^{-(36/3)\operatorname{ln}⁡(5/4)}≈791.410…≈791\,\text{eggs},
$$

rounded to the nearest integer.

## generated variant; authored operation bank q-37389 1

### Generated record

A poultry farmer has egg-laying chickens. She knows that her farm can produce a maximum of $700$ eggs a day; however, it is far behind it.
Since she started monitoring, the chickens laid $600$ eggs and $620$ eggs on days $3$ and $6$, respectively. How many eggs do the chickens lay on day $24$?
Round your answer to the nearest integer.

*Hint: You may assume that the egg production $E(t)$ increases at a rate that obeys an inhibited growth model, where $t$ is the time, in days.*

- $583$ eggs
- $584$ eggs
- $679$ eggs **correct**
- $101$ eggs
- $599$ eggs

The rate at which the egg production $E(t)$ changes is proportional to the difference between the maximum possible egg production and its current egg production. Therefore, we have the inhibited growth equation

$$
\frac{dE}{dt}=k(a-E),
$$

where $a$ is the maximum production of the farm, and $k>0$ is a constant of proportionality.

In our case, $a=700$ eggs, and we have

$$
\frac{dE}{dt}=k(700-E).
$$

First, we integrate our differential equation by separating the variables:

$$
\begin{aligned}\frac{dE}{700-E} & =k\,dt \\ \int \frac{dE}{700-E} & =\int k\,\text{d}t \\ -\operatorname{ln}⁡|700-E| & =kt+C\end{aligned}
$$

Since this is the solution to an inhibited growth equation, we have $700-E>0$ for all $t\ge 0.$ Next, we solve for $E(t),$ as follows:

$$
\begin{aligned}700-E & ={e}^{-kt-C} \\ 700-E & ={e}^{-C}{e}^{-kt} \\ 700-E & =K{e}^{-kt} \\ E & =700-K{e}^{-kt}\end{aligned}
$$

Note that $K={e}^{-C}$ is a constant of integration.

We're told that, on day $3,$ the egg production was $600$ eggs. So, applying the condition $E(3)=600,$ we have

$$
\begin{aligned}E(3) & =600 \\ 700-K{e}^{-3k} & =600 \\ K{e}^{-3k} & =100.\end{aligned}
$$

We're also told that, on day $6,$ the egg production was $620$ eggs. So, applying the condition $E(6)=620,$ we get

$$
\begin{aligned}E(6) & =620 \\ 700-K{e}^{-6k} & =620 \\ K{e}^{-6k} & =80.\end{aligned}
$$

Then, by dividing the result of the first condition by the result of the second, we can solve for $k:$

$$
\begin{aligned}\frac{K{e}^{-3k}}{K{e}^{-6k}} & =\frac{100}{80} \\ {e}^{3k} & =\frac{5}{4} \\ 3k & =\operatorname{ln}⁡(\frac{5}{4}) \\ k & =\frac{1}{3}\operatorname{ln}⁡(\frac{5}{4})\end{aligned}
$$

Now, substituting back into the result of the first condition, we solve for $K:$

$$
\begin{aligned}K{e}^{-3\cdot (1/3)\operatorname{ln}⁡(5/4)} & =100 \\ K & =100{e}^{\operatorname{ln}⁡(5/4)} \\ K & =125\end{aligned}
$$

Therefore, we have the following expression for $E(t):$

$$
E(t)=700-125{e}^{-(t/3)\operatorname{ln}⁡(5/4)}
$$

Finally, the number of eggs laid on day $t=24$ is

$$
E(24)=700-125{e}^{-(24/3)\operatorname{ln}⁡(5/4)}≈679.028…≈679\,\text{eggs},
$$

rounded to the nearest integer.

## original source replay q-37400

### Captured original

The population of students $P(t)$ in a school can be modeled by the differential equation

$$
\frac{dP}{dt}=0.016(2\,500-P),
$$

where $t>0$ is the time, measured in years. If the initial population of the school is $800$ students, calculate the population after $4$ years. Round your answer to the nearest integer.

- $986$ students
- $905$ students
- $1005$ students
- $942$ students
- $850$ students

We're told that the population in the school is modeled by the inhibited growth equation

$$
\frac{dP}{dt}=0.016(2\,500-P).
$$

First, we integrate our differential equation by separating the variables:

$$
\begin{aligned}\frac{dP}{2\,500-P} & =0.016\,dt \\ \int \frac{dP}{2\,500-P} & =\int 0.016\,\text{d}t \\ -\operatorname{ln}⁡|2\,500-P| & =0.016t+C\end{aligned}
$$

Since this is the solution to an inhibited growth equation, we have $2\,500-P>0$ for all $t\ge 0.$
Next, we solve for $P(t),$ as follows:

$$
\begin{aligned}2500-P & ={e}^{-0.016t-C} \\ 2500-P & ={e}^{-C}{e}^{-0.016t} \\ 2,500-P & =K{e}^{-0.016t} \\ P & =2\,500-K{e}^{-0.016t}\end{aligned}
$$

Note that $K={e}^{-C}$ is a constant of integration.

We're told that the initial population of the school was $800$ students. So, we apply the initial condition $P(0)=800,$ and solve for $K:$

$$
\begin{aligned}800 & =2\,500-K{e}^{0} \\ 800 & =2\,500-K \\ K & =1\,700\end{aligned}
$$

Therefore, the solution to our initial value problem is

$$
P(t)=2\,500-1\,700{e}^{-0.016t}.
$$

Finally, the population in the school after $t=4$ years is

$$
P(4)=2\,500-1\,700{e}^{-0.016\cdot 4}≈905\,\text{students},
$$

rounded to the nearest integer.

### Generated record

The population of students $P(t)$ in a school can be modeled by the differential equation

$$
\frac{dP}{dt}=0.016(2\,500-P),
$$

where $t>0$ is the time, measured in years. If the initial population of the school is $800$ students, calculate the population after $4$ years. Round your answer to the nearest integer.

- $1005$ students
- $905$ students **correct**
- $986$ students
- $850$ students
- $942$ students

We're told that the population in the school is modeled by the inhibited growth equation

$$
\frac{dP}{dt}=0.016(2\,500-P).
$$

First, we integrate our differential equation by separating the variables:

$$
\begin{aligned}\frac{dP}{2\,500-P} & =0.016\,dt \\ \int \frac{dP}{2\,500-P} & =\int 0.016\,\text{d}t \\ -\operatorname{ln}⁡|2\,500-P| & =0.016t+C\end{aligned}
$$

Since this is the solution to an inhibited growth equation, we have $2\,500-P>0$ for all $t\ge 0.$
Next, we solve for $P(t),$ as follows:

$$
\begin{aligned}2500-P & ={e}^{-0.016t-C} \\ 2500-P & ={e}^{-C}{e}^{-0.016t} \\ 2,500-P & =K{e}^{-0.016t} \\ P & =2\,500-K{e}^{-0.016t}\end{aligned}
$$

Note that $K={e}^{-C}$ is a constant of integration.

We're told that the initial population of the school was $800$ students. So, we apply the initial condition $P(0)=800,$ and solve for $K:$

$$
\begin{aligned}800 & =2\,500-K{e}^{0} \\ 800 & =2\,500-K \\ K & =1\,700\end{aligned}
$$

Therefore, the solution to our initial value problem is

$$
P(t)=2\,500-1\,700{e}^{-0.016t}.
$$

Finally, the population in the school after $t=4$ years is

$$
P(4)=2\,500-1\,700{e}^{-0.016\cdot 4}≈905\,\text{students},
$$

rounded to the nearest integer.

## generated variant; observed empirical unknown intent q-37400 0

### Generated record

The population of students $P(t)$ in a school can be modeled by the differential equation

$$
\frac{dP}{dt}=0.008(10\,000-P),
$$

where $t>0$ is the time, measured in years. If the initial population of the school is $3200$ students, calculate the population after $8$ years. Round your answer to the nearest integer.

- $4022$ students
- $3770$ students
- $3946$ students
- $3622$ students **correct**
- $3402$ students

We're told that the population in the school is modeled by the inhibited growth equation

$$
\frac{dP}{dt}=0.008(10\,000-P).
$$

First, we integrate our differential equation by separating the variables:

$$
\begin{aligned}\frac{dP}{10\,000-P} & =0.008\,dt \\ \int \frac{dP}{10\,000-P} & =\int 0.008\,\text{d}t \\ -\operatorname{ln}⁡|10\,000-P| & =0.008t+C\end{aligned}
$$

Since this is the solution to an inhibited growth equation, we have $10\,000-P>0$ for all $t\ge 0.$
Next, we solve for $P(t),$ as follows:

$$
\begin{aligned}10000-P & ={e}^{-0.008t-C} \\ 10000-P & ={e}^{-C}{e}^{-0.008t} \\ 10,000-P & =K{e}^{-0.008t} \\ P & =10\,000-K{e}^{-0.008t}\end{aligned}
$$

Note that $K={e}^{-C}$ is a constant of integration.

We're told that the initial population of the school was $3200$ students. So, we apply the initial condition $P(0)=3200,$ and solve for $K:$

$$
\begin{aligned}3200 & =10\,000-K{e}^{0} \\ 3200 & =10\,000-K \\ K & =6\,800\end{aligned}
$$

Therefore, the solution to our initial value problem is

$$
P(t)=10\,000-6\,800{e}^{-0.008t}.
$$

Finally, the population in the school after $t=8$ years is

$$
P(8)=10\,000-6\,800{e}^{-0.008\cdot 8}≈3622\,\text{students},
$$

rounded to the nearest integer.

## generated variant; observed empirical unknown intent q-37400 1

### Generated record

The population of students $P(t)$ in a school can be modeled by the differential equation

$$
\frac{dP}{dt}=0.008(5\,000-P),
$$

where $t>0$ is the time, measured in years. If the initial population of the school is $1600$ students, calculate the population after $8$ years. Round your answer to the nearest integer.

- $1701$ students
- $1885$ students
- $2011$ students
- $1811$ students **correct**
- $1973$ students

We're told that the population in the school is modeled by the inhibited growth equation

$$
\frac{dP}{dt}=0.008(5\,000-P).
$$

First, we integrate our differential equation by separating the variables:

$$
\begin{aligned}\frac{dP}{5\,000-P} & =0.008\,dt \\ \int \frac{dP}{5\,000-P} & =\int 0.008\,\text{d}t \\ -\operatorname{ln}⁡|5\,000-P| & =0.008t+C\end{aligned}
$$

Since this is the solution to an inhibited growth equation, we have $5\,000-P>0$ for all $t\ge 0.$
Next, we solve for $P(t),$ as follows:

$$
\begin{aligned}5000-P & ={e}^{-0.008t-C} \\ 5000-P & ={e}^{-C}{e}^{-0.008t} \\ 5,000-P & =K{e}^{-0.008t} \\ P & =5\,000-K{e}^{-0.008t}\end{aligned}
$$

Note that $K={e}^{-C}$ is a constant of integration.

We're told that the initial population of the school was $1600$ students. So, we apply the initial condition $P(0)=1600,$ and solve for $K:$

$$
\begin{aligned}1600 & =5\,000-K{e}^{0} \\ 1600 & =5\,000-K \\ K & =3\,400\end{aligned}
$$

Therefore, the solution to our initial value problem is

$$
P(t)=5\,000-3\,400{e}^{-0.008t}.
$$

Finally, the population in the school after $t=8$ years is

$$
P(8)=5\,000-3\,400{e}^{-0.008\cdot 8}≈1811\,\text{students},
$$

rounded to the nearest integer.

## generated variant; authored operation bank q-37400 0

### Generated record

The population of students $P(t)$ in a school can be modeled by the differential equation

$$
\frac{dP}{dt}=0.025(3\,000-P),
$$

where $t>0$ is the time, measured in years. If the initial population of the school is $550$ students, calculate the population after $5$ years. Round your answer to the nearest integer.

- $838$ students **correct**
- $485$ students
- $353$ students
- $610$ students
- $2515$ students

We're told that the population in the school is modeled by the inhibited growth equation

$$
\frac{dP}{dt}=0.025(3\,000-P).
$$

First, we integrate our differential equation by separating the variables:

$$
\begin{aligned}\frac{dP}{3\,000-P} & =0.025\,dt \\ \int \frac{dP}{3\,000-P} & =\int 0.025\,\text{d}t \\ -\operatorname{ln}⁡|3\,000-P| & =0.025t+C\end{aligned}
$$

Since this is the solution to an inhibited growth equation, we have $3\,000-P>0$ for all $t\ge 0.$
Next, we solve for $P(t),$ as follows:

$$
\begin{aligned}3000-P & ={e}^{-0.025t-C} \\ 3000-P & ={e}^{-C}{e}^{-0.025t} \\ 3,000-P & =K{e}^{-0.025t} \\ P & =3\,000-K{e}^{-0.025t}\end{aligned}
$$

Note that $K={e}^{-C}$ is a constant of integration.

We're told that the initial population of the school was $550$ students. So, we apply the initial condition $P(0)=550,$ and solve for $K:$

$$
\begin{aligned}550 & =3\,000-K{e}^{0} \\ 550 & =3\,000-K \\ K & =2\,450\end{aligned}
$$

Therefore, the solution to our initial value problem is

$$
P(t)=3\,000-2\,450{e}^{-0.025t}.
$$

Finally, the population in the school after $t=5$ years is

$$
P(5)=3\,000-2\,450{e}^{-0.025\cdot 5}≈838\,\text{students},
$$

rounded to the nearest integer.

## generated variant; authored operation bank q-37400 1

### Generated record

The population of students $P(t)$ in a school can be modeled by the differential equation

$$
\frac{dP}{dt}=0.017(4\,000-P),
$$

where $t>0$ is the time, measured in years. If the initial population of the school is $300$ students, calculate the population after $2$ years. Round your answer to the nearest integer.

- $134$ students
- $362$ students
- $424$ students **correct**
- $290$ students
- $3710$ students

We're told that the population in the school is modeled by the inhibited growth equation

$$
\frac{dP}{dt}=0.017(4\,000-P).
$$

First, we integrate our differential equation by separating the variables:

$$
\begin{aligned}\frac{dP}{4\,000-P} & =0.017\,dt \\ \int \frac{dP}{4\,000-P} & =\int 0.017\,\text{d}t \\ -\operatorname{ln}⁡|4\,000-P| & =0.017t+C\end{aligned}
$$

Since this is the solution to an inhibited growth equation, we have $4\,000-P>0$ for all $t\ge 0.$
Next, we solve for $P(t),$ as follows:

$$
\begin{aligned}4000-P & ={e}^{-0.017t-C} \\ 4000-P & ={e}^{-C}{e}^{-0.017t} \\ 4,000-P & =K{e}^{-0.017t} \\ P & =4\,000-K{e}^{-0.017t}\end{aligned}
$$

Note that $K={e}^{-C}$ is a constant of integration.

We're told that the initial population of the school was $300$ students. So, we apply the initial condition $P(0)=300,$ and solve for $K:$

$$
\begin{aligned}300 & =4\,000-K{e}^{0} \\ 300 & =4\,000-K \\ K & =3\,700\end{aligned}
$$

Therefore, the solution to our initial value problem is

$$
P(t)=4\,000-3\,700{e}^{-0.017t}.
$$

Finally, the population in the school after $t=2$ years is

$$
P(2)=4\,000-3\,700{e}^{-0.017\cdot 2}≈424\,\text{students},
$$

rounded to the nearest integer.

## original source replay q-335280

### Captured original

A can of soda is taken out of a refrigerator and left in a room that stays at a constant temperature of $20{\,}^{∘}\text{C}.$ The soda’s temperature $T(t)$ (in degrees Celsius) can be modeled by the differential equation:

$$
\frac{dT}{dt}=k(20-T),
$$

where $t\ge 0$ is the time, measured in minutes, and $k>0$ is a constant. The initial temperature of the soda is $8{\,}^{∘}\text{C},$ and after $5$ minutes, the soda has warmed to $12{\,}^{∘}\text{C}.$ To the nearest minute, how long does it take for the soda to reach $16{\,}^{∘}\text{C}?$

- $19$ minutes
- $14$ minutes
- $12$ minutes
- $10$ minutes
- $8$ minutes

We're told that the temperature of the can is modeled by the inhibited growth equation

$$
\frac{dT}{dt}=k(20-T).
$$

We separate variables and integrate:

$$
\begin{aligned}\frac{dT}{20-T} & =k\,dt \\ \int \frac{dT}{20-T} & =\int k\,dt \\ -\operatorname{ln}⁡|20-T| & =kt+C\end{aligned}
$$

Since this is the solution to an inhibited growth equation, we have $20-T>0$ for all $t\ge 0.$ Next, we solve for $T(t),$ as follows:

$$
\begin{aligned}20-T & ={e}^{-kt-C} \\ 20-T & ={e}^{-C}{e}^{-kt} \\ 20-T & =K{e}^{-kt} \\ T & =20-K{e}^{-kt}\end{aligned}
$$

Note that $K={e}^{-C}$ is a constant of integration.

We're told that the initial temperature was $8{\,}^{∘}\text{C}.$ So, we apply the initial condition $T(0)=8,$ and solve for $K:$

$$
\begin{aligned}8 & =20-K{e}^{0} \\ 8 & =20-K \\ K & =12\end{aligned}
$$

Therefore, the solution to our initial value problem is

$$
T(t)=20-12{e}^{-kt}.
$$

We're also told that, after $5$ minutes, the temperature of the soda was $12{\,}^{∘}\text{C}.$ So, applying the condition $T(5)=12,$  we can solve for $k:$

$$
\begin{aligned}12 & =20-12{e}^{-5k} \\ 8 & =12{e}^{-5k} \\ {e}^{-5k} & =\frac{2}{3} \\ -5k & =\operatorname{ln}⁡(\frac{2}{3}) \\ k & =-\frac{1}{5}\operatorname{ln}⁡(\frac{2}{3})\end{aligned}
$$

Finally, let ${t}_{1}$  be the time when the soda can reaches $16{\,}^{∘}\text{C}.$ Then, we have

$$
\begin{aligned}T({t}_{1}) & =16 \\ 20-12{e}^{-k{t}_{1}} & =16 \\ 4 & =12{e}^{-k{t}_{1}} \\ {e}^{-k{t}_{1}} & =\frac{1}{3} \\ -k{t}_{1} & =\operatorname{ln}⁡(\frac{1}{3}) \\ {t}_{1} & =-\frac{1}{k}\operatorname{ln}⁡(\frac{1}{3})\end{aligned}
$$

Substituting the value of $k,$ we get:

$$
{t}_{1}=\frac{-\operatorname{ln}⁡(\frac{1}{3})}{-\frac{1}{5}\operatorname{ln}⁡(\frac{2}{3})}=13.547…≈14\text{ }\text{minutes},
$$

rounded to the nearest minute.

### Generated record

A can of soda is taken out of a refrigerator and left in a room that stays at a constant temperature of $20{\,}^{∘}\text{C}.$ The soda’s temperature $T(t)$ (in degrees Celsius) can be modeled by the differential equation:

$$
\frac{dT}{dt}=k(20-T),
$$

where $t\ge 0$ is the time, measured in minutes, and $k>0$ is a constant. The initial temperature of the soda is $8{\,}^{∘}\text{C},$ and after $5$ minutes, the soda has warmed to $12{\,}^{∘}\text{C}.$ To the nearest minute, how long does it take for the soda to reach $16{\,}^{∘}\text{C}?$

- $12$ minutes
- $14$ minutes **correct**
- $19$ minutes
- $8$ minutes
- $10$ minutes

We're told that the temperature of the can is modeled by the inhibited growth equation

$$
\frac{dT}{dt}=k(20-T).
$$

We separate variables and integrate:

$$
\begin{aligned}\frac{dT}{20-T} & =k\,dt \\ \int \frac{dT}{20-T} & =\int k\,dt \\ -\operatorname{ln}⁡|20-T| & =kt+C\end{aligned}
$$

Since this is the solution to an inhibited growth equation, we have $20-T>0$ for all $t\ge 0.$ Next, we solve for $T(t),$ as follows:

$$
\begin{aligned}20-T & ={e}^{-kt-C} \\ 20-T & ={e}^{-C}{e}^{-kt} \\ 20-T & =K{e}^{-kt} \\ T & =20-K{e}^{-kt}\end{aligned}
$$

Note that $K={e}^{-C}$ is a constant of integration.

We're told that the initial temperature was $8{\,}^{∘}\text{C}.$ So, we apply the initial condition $T(0)=8,$ and solve for $K:$

$$
\begin{aligned}8 & =20-K{e}^{0} \\ 8 & =20-K \\ K & =12\end{aligned}
$$

Therefore, the solution to our initial value problem is

$$
T(t)=20-12{e}^{-kt}.
$$

We're also told that, after $5$ minutes, the temperature of the soda was $12{\,}^{∘}\text{C}.$ So, applying the condition $T(5)=12,$  we can solve for $k:$

$$
\begin{aligned}12 & =20-12{e}^{-5k} \\ 8 & =12{e}^{-5k} \\ {e}^{-5k} & =\frac{2}{3} \\ -5k & =\operatorname{ln}⁡(\frac{2}{3}) \\ k & =-\frac{1}{5}\operatorname{ln}⁡(\frac{2}{3})\end{aligned}
$$

Finally, let ${t}_{1}$  be the time when the soda can reaches $16{\,}^{∘}\text{C}.$ Then, we have

$$
\begin{aligned}T({t}_{1}) & =16 \\ 20-12{e}^{-k{t}_{1}} & =16 \\ 4 & =12{e}^{-k{t}_{1}} \\ {e}^{-k{t}_{1}} & =\frac{1}{3} \\ -k{t}_{1} & =\operatorname{ln}⁡(\frac{1}{3}) \\ {t}_{1} & =-\frac{1}{k}\operatorname{ln}⁡(\frac{1}{3})\end{aligned}
$$

Substituting the value of $k,$ we get:

$$
{t}_{1}=\frac{-\operatorname{ln}⁡(\frac{1}{3})}{-\frac{1}{5}\operatorname{ln}⁡(\frac{2}{3})}=13.547…≈14\text{ }\text{minutes},
$$

rounded to the nearest minute.

## generated variant; observed empirical unknown intent q-335280 0

### Generated record

A can of soda is taken out of a refrigerator and left in a room that stays at a constant temperature of $80{\,}^{∘}\text{C}.$ The soda’s temperature $T(t)$ (in degrees Celsius) can be modeled by the differential equation:

$$
\frac{dT}{dt}=k(80-T),
$$

where $t\ge 0$ is the time, measured in minutes, and $k>0$ is a constant. The initial temperature of the soda is $32{\,}^{∘}\text{C},$ and after $10$ minutes, the soda has warmed to $48{\,}^{∘}\text{C}.$ To the nearest minute, how long does it take for the soda to reach $64{\,}^{∘}\text{C}?$

- $23$ minutes
- $19$ minutes
- $37$ minutes
- $27$ minutes **correct**
- $15$ minutes

We're told that the temperature of the can is modeled by the inhibited growth equation

$$
\frac{dT}{dt}=k(80-T).
$$

We separate variables and integrate:

$$
\begin{aligned}\frac{dT}{80-T} & =k\,dt \\ \int \frac{dT}{80-T} & =\int k\,dt \\ -\operatorname{ln}⁡|80-T| & =kt+C\end{aligned}
$$

Since this is the solution to an inhibited growth equation, we have $80-T>0$ for all $t\ge 0.$ Next, we solve for $T(t),$ as follows:

$$
\begin{aligned}80-T & ={e}^{-kt-C} \\ 80-T & ={e}^{-C}{e}^{-kt} \\ 80-T & =K{e}^{-kt} \\ T & =80-K{e}^{-kt}\end{aligned}
$$

Note that $K={e}^{-C}$ is a constant of integration.

We're told that the initial temperature was $32{\,}^{∘}\text{C}.$ So, we apply the initial condition $T(0)=32,$ and solve for $K:$

$$
\begin{aligned}32 & =80-K{e}^{0} \\ 32 & =80-K \\ K & =48\end{aligned}
$$

Therefore, the solution to our initial value problem is

$$
T(t)=80-48{e}^{-kt}.
$$

We're also told that, after $10$ minutes, the temperature of the soda was $48{\,}^{∘}\text{C}.$ So, applying the condition $T(10)=48,$  we can solve for $k:$

$$
\begin{aligned}48 & =80-48{e}^{-10k} \\ 32 & =48{e}^{-10k} \\ {e}^{-10k} & =\frac{2}{3} \\ -10k & =\operatorname{ln}⁡(\frac{2}{3}) \\ k & =-\frac{1}{10}\operatorname{ln}⁡(\frac{2}{3})\end{aligned}
$$

Finally, let ${t}_{1}$  be the time when the soda can reaches $64{\,}^{∘}\text{C}.$ Then, we have

$$
\begin{aligned}T({t}_{1}) & =64 \\ 80-48{e}^{-k{t}_{1}} & =64 \\ 16 & =48{e}^{-k{t}_{1}} \\ {e}^{-k{t}_{1}} & =\frac{1}{3} \\ -k{t}_{1} & =\operatorname{ln}⁡(\frac{1}{3}) \\ {t}_{1} & =-\frac{1}{k}\operatorname{ln}⁡(\frac{1}{3})\end{aligned}
$$

Substituting the value of $k,$ we get:

$$
{t}_{1}=\frac{-\operatorname{ln}⁡(\frac{1}{3})}{-\frac{1}{10}\operatorname{ln}⁡(\frac{2}{3})}=27.095…≈27\text{ }\text{minutes},
$$

rounded to the nearest minute.

## generated variant; observed empirical unknown intent q-335280 1

### Generated record

A can of soda is taken out of a refrigerator and left in a room that stays at a constant temperature of $40{\,}^{∘}\text{C}.$ The soda’s temperature $T(t)$ (in degrees Celsius) can be modeled by the differential equation:

$$
\frac{dT}{dt}=k(40-T),
$$

where $t\ge 0$ is the time, measured in minutes, and $k>0$ is a constant. The initial temperature of the soda is $16{\,}^{∘}\text{C},$ and after $10$ minutes, the soda has warmed to $24{\,}^{∘}\text{C}.$ To the nearest minute, how long does it take for the soda to reach $32{\,}^{∘}\text{C}?$

- $15$ minutes
- $19$ minutes
- $23$ minutes
- $27$ minutes **correct**
- $37$ minutes

We're told that the temperature of the can is modeled by the inhibited growth equation

$$
\frac{dT}{dt}=k(40-T).
$$

We separate variables and integrate:

$$
\begin{aligned}\frac{dT}{40-T} & =k\,dt \\ \int \frac{dT}{40-T} & =\int k\,dt \\ -\operatorname{ln}⁡|40-T| & =kt+C\end{aligned}
$$

Since this is the solution to an inhibited growth equation, we have $40-T>0$ for all $t\ge 0.$ Next, we solve for $T(t),$ as follows:

$$
\begin{aligned}40-T & ={e}^{-kt-C} \\ 40-T & ={e}^{-C}{e}^{-kt} \\ 40-T & =K{e}^{-kt} \\ T & =40-K{e}^{-kt}\end{aligned}
$$

Note that $K={e}^{-C}$ is a constant of integration.

We're told that the initial temperature was $16{\,}^{∘}\text{C}.$ So, we apply the initial condition $T(0)=16,$ and solve for $K:$

$$
\begin{aligned}16 & =40-K{e}^{0} \\ 16 & =40-K \\ K & =24\end{aligned}
$$

Therefore, the solution to our initial value problem is

$$
T(t)=40-24{e}^{-kt}.
$$

We're also told that, after $10$ minutes, the temperature of the soda was $24{\,}^{∘}\text{C}.$ So, applying the condition $T(10)=24,$  we can solve for $k:$

$$
\begin{aligned}24 & =40-24{e}^{-10k} \\ 16 & =24{e}^{-10k} \\ {e}^{-10k} & =\frac{2}{3} \\ -10k & =\operatorname{ln}⁡(\frac{2}{3}) \\ k & =-\frac{1}{10}\operatorname{ln}⁡(\frac{2}{3})\end{aligned}
$$

Finally, let ${t}_{1}$  be the time when the soda can reaches $32{\,}^{∘}\text{C}.$ Then, we have

$$
\begin{aligned}T({t}_{1}) & =32 \\ 40-24{e}^{-k{t}_{1}} & =32 \\ 8 & =24{e}^{-k{t}_{1}} \\ {e}^{-k{t}_{1}} & =\frac{1}{3} \\ -k{t}_{1} & =\operatorname{ln}⁡(\frac{1}{3}) \\ {t}_{1} & =-\frac{1}{k}\operatorname{ln}⁡(\frac{1}{3})\end{aligned}
$$

Substituting the value of $k,$ we get:

$$
{t}_{1}=\frac{-\operatorname{ln}⁡(\frac{1}{3})}{-\frac{1}{10}\operatorname{ln}⁡(\frac{2}{3})}=27.095…≈27\text{ }\text{minutes},
$$

rounded to the nearest minute.

## generated variant; authored operation bank q-335280 0

### Generated record

A can of soda is taken out of a refrigerator and left in a room that stays at a constant temperature of $25{\,}^{∘}\text{C}.$ The soda’s temperature $T(t)$ (in degrees Celsius) can be modeled by the differential equation:

$$
\frac{dT}{dt}=k(25-T),
$$

where $t\ge 0$ is the time, measured in minutes, and $k>0$ is a constant. The initial temperature of the soda is $6{\,}^{∘}\text{C},$ and after $9$ minutes, the soda has warmed to $19{\,}^{∘}\text{C}.$ To the nearest minute, how long does it take for the soda to reach $22{\,}^{∘}\text{C}?$

- $14$ minutes **correct**
- $8$ minutes
- $10$ minutes
- $7$ minutes
- $2$ minutes

We're told that the temperature of the can is modeled by the inhibited growth equation

$$
\frac{dT}{dt}=k(25-T).
$$

We separate variables and integrate:

$$
\begin{aligned}\frac{dT}{25-T} & =k\,dt \\ \int \frac{dT}{25-T} & =\int k\,dt \\ -\operatorname{ln}⁡|25-T| & =kt+C\end{aligned}
$$

Since this is the solution to an inhibited growth equation, we have $25-T>0$ for all $t\ge 0.$ Next, we solve for $T(t),$ as follows:

$$
\begin{aligned}25-T & ={e}^{-kt-C} \\ 25-T & ={e}^{-C}{e}^{-kt} \\ 25-T & =K{e}^{-kt} \\ T & =25-K{e}^{-kt}\end{aligned}
$$

Note that $K={e}^{-C}$ is a constant of integration.

We're told that the initial temperature was $6{\,}^{∘}\text{C}.$ So, we apply the initial condition $T(0)=6,$ and solve for $K:$

$$
\begin{aligned}6 & =25-K{e}^{0} \\ 6 & =25-K \\ K & =19\end{aligned}
$$

Therefore, the solution to our initial value problem is

$$
T(t)=25-19{e}^{-kt}.
$$

We're also told that, after $9$ minutes, the temperature of the soda was $19{\,}^{∘}\text{C}.$ So, applying the condition $T(9)=19,$  we can solve for $k:$

$$
\begin{aligned}19 & =25-19{e}^{-9k} \\ 6 & =19{e}^{-9k} \\ {e}^{-9k} & =\frac{6}{19} \\ -9k & =\operatorname{ln}⁡(\frac{6}{19}) \\ k & =-\frac{1}{9}\operatorname{ln}⁡(\frac{6}{19})\end{aligned}
$$

Finally, let ${t}_{1}$  be the time when the soda can reaches $22{\,}^{∘}\text{C}.$ Then, we have

$$
\begin{aligned}T({t}_{1}) & =22 \\ 25-19{e}^{-k{t}_{1}} & =22 \\ 3 & =19{e}^{-k{t}_{1}} \\ {e}^{-k{t}_{1}} & =\frac{3}{19} \\ -k{t}_{1} & =\operatorname{ln}⁡(\frac{3}{19}) \\ {t}_{1} & =-\frac{1}{k}\operatorname{ln}⁡(\frac{3}{19})\end{aligned}
$$

Substituting the value of $k,$ we get:

$$
{t}_{1}=\frac{-\operatorname{ln}⁡(\frac{3}{19})}{-\frac{1}{9}\operatorname{ln}⁡(\frac{6}{19})}=14.412…≈14\text{ }\text{minutes},
$$

rounded to the nearest minute.

## generated variant; authored operation bank q-335280 1

### Generated record

A can of soda is taken out of a refrigerator and left in a room that stays at a constant temperature of $21{\,}^{∘}\text{C}.$ The soda’s temperature $T(t)$ (in degrees Celsius) can be modeled by the differential equation:

$$
\frac{dT}{dt}=k(21-T),
$$

where $t\ge 0$ is the time, measured in minutes, and $k>0$ is a constant. The initial temperature of the soda is $5{\,}^{∘}\text{C},$ and after $5$ minutes, the soda has warmed to $16{\,}^{∘}\text{C}.$ To the nearest minute, how long does it take for the soda to reach $17{\,}^{∘}\text{C}?$

- $5$ minutes
- $3$ minutes
- $6$ minutes **correct**
- $4$ minutes
- $1$ minute

We're told that the temperature of the can is modeled by the inhibited growth equation

$$
\frac{dT}{dt}=k(21-T).
$$

We separate variables and integrate:

$$
\begin{aligned}\frac{dT}{21-T} & =k\,dt \\ \int \frac{dT}{21-T} & =\int k\,dt \\ -\operatorname{ln}⁡|21-T| & =kt+C\end{aligned}
$$

Since this is the solution to an inhibited growth equation, we have $21-T>0$ for all $t\ge 0.$ Next, we solve for $T(t),$ as follows:

$$
\begin{aligned}21-T & ={e}^{-kt-C} \\ 21-T & ={e}^{-C}{e}^{-kt} \\ 21-T & =K{e}^{-kt} \\ T & =21-K{e}^{-kt}\end{aligned}
$$

Note that $K={e}^{-C}$ is a constant of integration.

We're told that the initial temperature was $5{\,}^{∘}\text{C}.$ So, we apply the initial condition $T(0)=5,$ and solve for $K:$

$$
\begin{aligned}5 & =21-K{e}^{0} \\ 5 & =21-K \\ K & =16\end{aligned}
$$

Therefore, the solution to our initial value problem is

$$
T(t)=21-16{e}^{-kt}.
$$

We're also told that, after $5$ minutes, the temperature of the soda was $16{\,}^{∘}\text{C}.$ So, applying the condition $T(5)=16,$  we can solve for $k:$

$$
\begin{aligned}16 & =21-16{e}^{-5k} \\ 5 & =16{e}^{-5k} \\ {e}^{-5k} & =\frac{5}{16} \\ -5k & =\operatorname{ln}⁡(\frac{5}{16}) \\ k & =-\frac{1}{5}\operatorname{ln}⁡(\frac{5}{16})\end{aligned}
$$

Finally, let ${t}_{1}$  be the time when the soda can reaches $17{\,}^{∘}\text{C}.$ Then, we have

$$
\begin{aligned}T({t}_{1}) & =17 \\ 21-16{e}^{-k{t}_{1}} & =17 \\ 4 & =16{e}^{-k{t}_{1}} \\ {e}^{-k{t}_{1}} & =\frac{1}{4} \\ -k{t}_{1} & =\operatorname{ln}⁡(\frac{1}{4}) \\ {t}_{1} & =-\frac{1}{k}\operatorname{ln}⁡(\frac{1}{4})\end{aligned}
$$

Substituting the value of $k,$ we get:

$$
{t}_{1}=\frac{-\operatorname{ln}⁡(\frac{1}{4})}{-\frac{1}{5}\operatorname{ln}⁡(\frac{5}{16})}=5.959…≈6\text{ }\text{minutes},
$$

rounded to the nearest minute.

## original source replay q-335282

### Captured original

The volume $X(t)$ (in $\text{L}$) of water in a container as it fills toward its maximum capacity can be modeled by the differential equation

$$
\frac{dX}{dt}=0.4(3-X),
$$

where $t\ge 0$ is the time, measured in minutes. If the initial volume is $1.5\,\text{L},$ how long does it take for the container to reach a volume of $2\,\text{L}?$ Round your answer to the nearest integer.

- $1$ minute
- $3$ minutes
- $4$ minutes
- $2$ minutes
- $5$ minutes

We're told that the container's volume is modeled by the inhibited growth equation

$$
\frac{dX}{dt}=0.4(3-X).
$$

First, we integrate our differential equation by separating the variables:

$$
\begin{aligned}\frac{dX}{3-X} & =0.4\,dt \\ \int \frac{dX}{3-X} & =\int 0.4\,\text{d}t \\ -\operatorname{ln}⁡|3-X| & =0.4t+C\end{aligned}
$$

Since this is the solution to an inhibited growth equation, we have $3-X>0$ for all $t\ge 0.$
Next, we solve for $X(t),$ as follows:

$$
\begin{aligned}3-X & ={e}^{-0.4t-C} \\ 3-X & ={e}^{-C}{e}^{-0.4t} \\ 3-X & =K{e}^{-0.4t} \\ X & =3-K{e}^{-0.4t}\end{aligned}
$$

Note that $K={e}^{-C}$ is a constant of integration.

We're told that the initial volume was $1.5\,\text{L}.$ So, we apply the initial condition $X(0)=1.5,$ and solve for $K:$

$$
\begin{aligned}1.5 & =3-K{e}^{0} \\ 1.5 & =3-K \\ K & =1.5\end{aligned}
$$

Therefore, the solution to our initial value problem is

$$
X(t)=3-1.5{e}^{-0.4t}.
$$

Finally, let ${t}_{1}$ be the time when the volume is $2\,\text{L}.$ Then, we have

$$
\begin{aligned}X({t}_{1}) & =2 \\ 3-1.5{e}^{-0.4{t}_{1}} & =2 \\ 1 & =1.5{e}^{-0.4{t}_{1}} \\ {e}^{-0.4{t}_{1}} & =\frac{2}{3} \\ -0.4{t}_{1} & =\operatorname{ln}⁡(\frac{2}{3}) \\ {t}_{1} & =-\frac{1}{0.4}\operatorname{ln}⁡(\frac{2}{3}) \\  & =1.013… \\  & ≈1\,\text{minute},\end{aligned}
$$

rounded to the nearest integer.

### Generated record

The volume $X(t)$ (in $\text{L}$) of water in a container as it fills toward its maximum capacity can be modeled by the differential equation

$$
\frac{dX}{dt}=0.4(3-X),
$$

where $t\ge 0$ is the time, measured in minutes. If the initial volume is $1.5\,\text{L},$ how long does it take for the container to reach a volume of $2\,\text{L}?$ Round your answer to the nearest integer.

- $4$ minutes
- $3$ minutes
- $1$ minute **correct**
- $5$ minutes
- $2$ minutes

We're told that the container's volume is modeled by the inhibited growth equation

$$
\frac{dX}{dt}=0.4(3-X).
$$

First, we integrate our differential equation by separating the variables:

$$
\begin{aligned}\frac{dX}{3-X} & =0.4\,dt \\ \int \frac{dX}{3-X} & =\int 0.4\,\text{d}t \\ -\operatorname{ln}⁡|3-X| & =0.4t+C\end{aligned}
$$

Since this is the solution to an inhibited growth equation, we have $3-X>0$ for all $t\ge 0.$
Next, we solve for $X(t),$ as follows:

$$
\begin{aligned}3-X & ={e}^{-0.4t-C} \\ 3-X & ={e}^{-C}{e}^{-0.4t} \\ 3-X & =K{e}^{-0.4t} \\ X & =3-K{e}^{-0.4t}\end{aligned}
$$

Note that $K={e}^{-C}$ is a constant of integration.

We're told that the initial volume was $1.5\,\text{L}.$ So, we apply the initial condition $X(0)=1.5,$ and solve for $K:$

$$
\begin{aligned}1.5 & =3-K{e}^{0} \\ 1.5 & =3-K \\ K & =1.5\end{aligned}
$$

Therefore, the solution to our initial value problem is

$$
X(t)=3-1.5{e}^{-0.4t}.
$$

Finally, let ${t}_{1}$ be the time when the volume is $2\,\text{L}.$ Then, we have

$$
\begin{aligned}X({t}_{1}) & =2 \\ 3-1.5{e}^{-0.4{t}_{1}} & =2 \\ 1 & =1.5{e}^{-0.4{t}_{1}} \\ {e}^{-0.4{t}_{1}} & =\frac{2}{3} \\ -0.4{t}_{1} & =\operatorname{ln}⁡(\frac{2}{3}) \\ {t}_{1} & =-\frac{1}{0.4}\operatorname{ln}⁡(\frac{2}{3}) \\  & =1.013… \\  & ≈1\,\text{minute},\end{aligned}
$$

rounded to the nearest integer.

## generated variant; observed empirical unknown intent q-335282 0

### Generated record

The volume $X(t)$ (in $\text{L}$) of water in a container as it fills toward its maximum capacity can be modeled by the differential equation

$$
\frac{dX}{dt}=0.2(12-X),
$$

where $t\ge 0$ is the time, measured in minutes. If the initial volume is $6\,\text{L},$ how long does it take for the container to reach a volume of $8\,\text{L}?$ Round your answer to the nearest integer.

- $8$ minutes
- $4$ minutes
- $2$ minutes **correct**
- $6$ minutes
- $10$ minutes

We're told that the container's volume is modeled by the inhibited growth equation

$$
\frac{dX}{dt}=0.2(12-X).
$$

First, we integrate our differential equation by separating the variables:

$$
\begin{aligned}\frac{dX}{12-X} & =0.2\,dt \\ \int \frac{dX}{12-X} & =\int 0.2\,\text{d}t \\ -\operatorname{ln}⁡|12-X| & =0.2t+C\end{aligned}
$$

Since this is the solution to an inhibited growth equation, we have $12-X>0$ for all $t\ge 0.$
Next, we solve for $X(t),$ as follows:

$$
\begin{aligned}12-X & ={e}^{-0.2t-C} \\ 12-X & ={e}^{-C}{e}^{-0.2t} \\ 12-X & =K{e}^{-0.2t} \\ X & =12-K{e}^{-0.2t}\end{aligned}
$$

Note that $K={e}^{-C}$ is a constant of integration.

We're told that the initial volume was $6\,\text{L}.$ So, we apply the initial condition $X(0)=6,$ and solve for $K:$

$$
\begin{aligned}6 & =12-K{e}^{0} \\ 6 & =12-K \\ K & =6\end{aligned}
$$

Therefore, the solution to our initial value problem is

$$
X(t)=12-6{e}^{-0.2t}.
$$

Finally, let ${t}_{1}$ be the time when the volume is $8\,\text{L}.$ Then, we have

$$
\begin{aligned}X({t}_{1}) & =8 \\ 12-6{e}^{-0.2{t}_{1}} & =8 \\ 4 & =6{e}^{-0.2{t}_{1}} \\ {e}^{-0.2{t}_{1}} & =\frac{2}{3} \\ -0.2{t}_{1} & =\operatorname{ln}⁡(\frac{2}{3}) \\ {t}_{1} & =-\frac{1}{0.2}\operatorname{ln}⁡(\frac{2}{3}) \\  & =2.027… \\  & ≈2\,\text{minutes},\end{aligned}
$$

rounded to the nearest integer.

## generated variant; observed empirical unknown intent q-335282 1

### Generated record

The volume $X(t)$ (in $\text{L}$) of water in a container as it fills toward its maximum capacity can be modeled by the differential equation

$$
\frac{dX}{dt}=0.2(6-X),
$$

where $t\ge 0$ is the time, measured in minutes. If the initial volume is $3\,\text{L},$ how long does it take for the container to reach a volume of $4\,\text{L}?$ Round your answer to the nearest integer.

- $10$ minutes
- $4$ minutes
- $8$ minutes
- $6$ minutes
- $2$ minutes **correct**

We're told that the container's volume is modeled by the inhibited growth equation

$$
\frac{dX}{dt}=0.2(6-X).
$$

First, we integrate our differential equation by separating the variables:

$$
\begin{aligned}\frac{dX}{6-X} & =0.2\,dt \\ \int \frac{dX}{6-X} & =\int 0.2\,\text{d}t \\ -\operatorname{ln}⁡|6-X| & =0.2t+C\end{aligned}
$$

Since this is the solution to an inhibited growth equation, we have $6-X>0$ for all $t\ge 0.$
Next, we solve for $X(t),$ as follows:

$$
\begin{aligned}6-X & ={e}^{-0.2t-C} \\ 6-X & ={e}^{-C}{e}^{-0.2t} \\ 6-X & =K{e}^{-0.2t} \\ X & =6-K{e}^{-0.2t}\end{aligned}
$$

Note that $K={e}^{-C}$ is a constant of integration.

We're told that the initial volume was $3\,\text{L}.$ So, we apply the initial condition $X(0)=3,$ and solve for $K:$

$$
\begin{aligned}3 & =6-K{e}^{0} \\ 3 & =6-K \\ K & =3\end{aligned}
$$

Therefore, the solution to our initial value problem is

$$
X(t)=6-3{e}^{-0.2t}.
$$

Finally, let ${t}_{1}$ be the time when the volume is $4\,\text{L}.$ Then, we have

$$
\begin{aligned}X({t}_{1}) & =4 \\ 6-3{e}^{-0.2{t}_{1}} & =4 \\ 2 & =3{e}^{-0.2{t}_{1}} \\ {e}^{-0.2{t}_{1}} & =\frac{2}{3} \\ -0.2{t}_{1} & =\operatorname{ln}⁡(\frac{2}{3}) \\ {t}_{1} & =-\frac{1}{0.2}\operatorname{ln}⁡(\frac{2}{3}) \\  & =2.027… \\  & ≈2\,\text{minutes},\end{aligned}
$$

rounded to the nearest integer.

## generated variant; authored operation bank q-335282 0

### Generated record

The volume $X(t)$ (in $\text{L}$) of water in a container as it fills toward its maximum capacity can be modeled by the differential equation

$$
\frac{dX}{dt}=0.1(4-X),
$$

where $t\ge 0$ is the time, measured in minutes. If the initial volume is $2\,\text{L},$ how long does it take for the container to reach a volume of $3\,\text{L}?$ Round your answer to the nearest integer.

- $7$ minutes **correct**
- $10$ minutes
- $4$ minutes
- $5$ minutes
- $1$ minute

We're told that the container's volume is modeled by the inhibited growth equation

$$
\frac{dX}{dt}=0.1(4-X).
$$

First, we integrate our differential equation by separating the variables:

$$
\begin{aligned}\frac{dX}{4-X} & =0.1\,dt \\ \int \frac{dX}{4-X} & =\int 0.1\,\text{d}t \\ -\operatorname{ln}⁡|4-X| & =0.1t+C\end{aligned}
$$

Since this is the solution to an inhibited growth equation, we have $4-X>0$ for all $t\ge 0.$
Next, we solve for $X(t),$ as follows:

$$
\begin{aligned}4-X & ={e}^{-0.1t-C} \\ 4-X & ={e}^{-C}{e}^{-0.1t} \\ 4-X & =K{e}^{-0.1t} \\ X & =4-K{e}^{-0.1t}\end{aligned}
$$

Note that $K={e}^{-C}$ is a constant of integration.

We're told that the initial volume was $2\,\text{L}.$ So, we apply the initial condition $X(0)=2,$ and solve for $K:$

$$
\begin{aligned}2 & =4-K{e}^{0} \\ 2 & =4-K \\ K & =2\end{aligned}
$$

Therefore, the solution to our initial value problem is

$$
X(t)=4-2{e}^{-0.1t}.
$$

Finally, let ${t}_{1}$ be the time when the volume is $3\,\text{L}.$ Then, we have

$$
\begin{aligned}X({t}_{1}) & =3 \\ 4-2{e}^{-0.1{t}_{1}} & =3 \\ 1 & =2{e}^{-0.1{t}_{1}} \\ {e}^{-0.1{t}_{1}} & =\frac{1}{2} \\ -0.1{t}_{1} & =\operatorname{ln}⁡(\frac{1}{2}) \\ {t}_{1} & =-\frac{1}{0.1}\operatorname{ln}⁡(\frac{1}{2}) \\  & =6.931… \\  & ≈7\,\text{minutes},\end{aligned}
$$

rounded to the nearest integer.

## generated variant; authored operation bank q-335282 1

### Generated record

The volume $X(t)$ (in $\text{L}$) of water in a container as it fills toward its maximum capacity can be modeled by the differential equation

$$
\frac{dX}{dt}=0.1(4-X),
$$

where $t\ge 0$ is the time, measured in minutes. If the initial volume is $2\,\text{L},$ how long does it take for the container to reach a volume of $3\,\text{L}?$ Round your answer to the nearest integer.

- $4$ minutes
- $5$ minutes
- $7$ minutes **correct**
- $10$ minutes
- $1$ minute

We're told that the container's volume is modeled by the inhibited growth equation

$$
\frac{dX}{dt}=0.1(4-X).
$$

First, we integrate our differential equation by separating the variables:

$$
\begin{aligned}\frac{dX}{4-X} & =0.1\,dt \\ \int \frac{dX}{4-X} & =\int 0.1\,\text{d}t \\ -\operatorname{ln}⁡|4-X| & =0.1t+C\end{aligned}
$$

Since this is the solution to an inhibited growth equation, we have $4-X>0$ for all $t\ge 0.$
Next, we solve for $X(t),$ as follows:

$$
\begin{aligned}4-X & ={e}^{-0.1t-C} \\ 4-X & ={e}^{-C}{e}^{-0.1t} \\ 4-X & =K{e}^{-0.1t} \\ X & =4-K{e}^{-0.1t}\end{aligned}
$$

Note that $K={e}^{-C}$ is a constant of integration.

We're told that the initial volume was $2\,\text{L}.$ So, we apply the initial condition $X(0)=2,$ and solve for $K:$

$$
\begin{aligned}2 & =4-K{e}^{0} \\ 2 & =4-K \\ K & =2\end{aligned}
$$

Therefore, the solution to our initial value problem is

$$
X(t)=4-2{e}^{-0.1t}.
$$

Finally, let ${t}_{1}$ be the time when the volume is $3\,\text{L}.$ Then, we have

$$
\begin{aligned}X({t}_{1}) & =3 \\ 4-2{e}^{-0.1{t}_{1}} & =3 \\ 1 & =2{e}^{-0.1{t}_{1}} \\ {e}^{-0.1{t}_{1}} & =\frac{1}{2} \\ -0.1{t}_{1} & =\operatorname{ln}⁡(\frac{1}{2}) \\ {t}_{1} & =-\frac{1}{0.1}\operatorname{ln}⁡(\frac{1}{2}) \\  & =6.931… \\  & ≈7\,\text{minutes},\end{aligned}
$$

rounded to the nearest integer.

## original source replay q-335578

### Captured original

Throughout an experiment in a laboratory, a culture contains $1\,200$ bacteria in total (limited by nutrients and space). At the beginning of the experiment, $200$ of the $1\,200$ bacteria are resistant to a new antibiotic. After $4$ hours, the number of resistant bacteria increases to $500.$ To the nearest hour, how long does it take for the number of resistant bacteria to reach $900?$

*Hint: You may assume that the number of resistant bacteria, $P(t),$ increases at a rate that obeys an inhibited growth model, where $t\ge 0$ is the time, in hours.*

- $10$ hours
- $20$ hours
- $18$ hours
- $8$ hours
- $14$ hours

The rate at which the resistant bacteria population, $P(t),$ changes is proportional to the difference between the total bacteria population in the culture and its current resistant population. Therefore, we have the inhibited growth equation

$$
\frac{dP}{dt}=k(a-P),
$$

where $a$ is the total bacteria population the culture can support, and $k>0$ is a constant of proportionality.

In our case, $a=1\,200$ bacteria, and we have

$$
\frac{dP}{dt}=k(1\,200-P).
$$

First, we integrate our differential equation by separating the variables:

$$
\begin{aligned}\frac{dP}{1\,200-P} & =k\,dt \\ \int \frac{dP}{1\,200-P} & =\int k\,dt \\ -\operatorname{ln}⁡|1\,200-P| & =kt+C\end{aligned}
$$

Since this is the solution to an inhibited growth equation, we have $1\,200-P>0$ for all $t\ge 0.$
Next, we solve for $P(t),$ as follows:

$$
\begin{aligned}1\,200-P & ={e}^{-kt-C} \\ 1\,200-P & ={e}^{-C}{e}^{-kt} \\ 1\,200-P & =K{e}^{-kt} \\ P & =1\,200-K{e}^{-kt}\end{aligned}
$$

Note that $K={e}^{-C}$ is a constant of integration. 

We're told that the initial population of resistant bacteria was $200$ cells. So, we apply the initial condition $P(0)=200,$ and solve for $K:$

$$
\begin{aligned}P(0) & =200 \\ 1\,200-K{e}^{0} & =200 \\ 1\,200-K & =200 \\ K & =1\,000\end{aligned}
$$

Therefore, we have the following expression for $P(t):$

$$
P(t)=1\,200-1\,000{e}^{-kt}
$$

We're also told that, after $4$ hours, the resistant bacteria population was $500$ cells. So, applying the condition $P(4)=500,$ we can solve for $k:$

$$
\begin{aligned}P(4) & =500 \\ 1\,200-1\,000{e}^{-4k} & =500 \\ 700 & =1\,000{e}^{-4k} \\ {e}^{-4k} & =\frac{700}{1\,000}=\frac{7}{10} \\ -4k & =\operatorname{ln}⁡(\frac{7}{10}) \\ k & =-\frac{1}{4}\operatorname{ln}⁡(\frac{7}{10})\end{aligned}
$$

Finally, let ${t}_{1}$ be the time when $900$ bacteria are resistant to the antibiotic. Then, we have

$$
\begin{aligned}P({t}_{1}) & =900 \\ 1\,200-1\,000{e}^{-k{t}_{1}} & =900 \\ 300 & =1\,000{e}^{-k{t}_{1}} \\ {e}^{-k{t}_{1}} & =\frac{300}{1\,000}=\frac{3}{10} \\ -k{t}_{1} & =\operatorname{ln}⁡(\frac{3}{10}) \\ {t}_{1} & =-\frac{1}{k}\operatorname{ln}⁡(\frac{3}{10}).\end{aligned}
$$

Substituting in our value for $k,$ we conclude that $900$ bacteria will be resistant to the antibiotic after

$$
{t}_{1}=\frac{-\operatorname{ln}⁡(\frac{3}{10})}{-\frac{1}{4}\operatorname{ln}⁡(\frac{7}{10})}=13.502…≈14\,\text{hours},
$$

rounded to the nearest hour.

### Generated record

Throughout an experiment in a laboratory, a culture contains $1\,200$ bacteria in total (limited by nutrients and space). At the beginning of the experiment, $200$ of the $1\,200$ bacteria are resistant to a new antibiotic. After $4$ hours, the number of resistant bacteria increases to $500.$ To the nearest hour, how long does it take for the number of resistant bacteria to reach $900?$

*Hint: You may assume that the number of resistant bacteria, $P(t),$ increases at a rate that obeys an inhibited growth model, where $t\ge 0$ is the time, in hours.*

- $18$ hours
- $20$ hours
- $10$ hours
- $14$ hours **correct**
- $8$ hours

The rate at which the resistant bacteria population, $P(t),$ changes is proportional to the difference between the total bacteria population in the culture and its current resistant population. Therefore, we have the inhibited growth equation

$$
\frac{dP}{dt}=k(a-P),
$$

where $a$ is the total bacteria population the culture can support, and $k>0$ is a constant of proportionality.

In our case, $a=1\,200$ bacteria, and we have

$$
\frac{dP}{dt}=k(1\,200-P).
$$

First, we integrate our differential equation by separating the variables:

$$
\begin{aligned}\frac{dP}{1\,200-P} & =k\,dt \\ \int \frac{dP}{1\,200-P} & =\int k\,dt \\ -\operatorname{ln}⁡|1\,200-P| & =kt+C\end{aligned}
$$

Since this is the solution to an inhibited growth equation, we have $1\,200-P>0$ for all $t\ge 0.$
Next, we solve for $P(t),$ as follows:

$$
\begin{aligned}1\,200-P & ={e}^{-kt-C} \\ 1\,200-P & ={e}^{-C}{e}^{-kt} \\ 1\,200-P & =K{e}^{-kt} \\ P & =1\,200-K{e}^{-kt}\end{aligned}
$$

Note that $K={e}^{-C}$ is a constant of integration. 

We're told that the initial population of resistant bacteria was $200$ cells. So, we apply the initial condition $P(0)=200,$ and solve for $K:$

$$
\begin{aligned}P(0) & =200 \\ 1\,200-K{e}^{0} & =200 \\ 1\,200-K & =200 \\ K & =1\,000\end{aligned}
$$

Therefore, we have the following expression for $P(t):$

$$
P(t)=1\,200-1\,000{e}^{-kt}
$$

We're also told that, after $4$ hours, the resistant bacteria population was $500$ cells. So, applying the condition $P(4)=500,$ we can solve for $k:$

$$
\begin{aligned}P(4) & =500 \\ 1\,200-1\,000{e}^{-4k} & =500 \\ 700 & =1\,000{e}^{-4k} \\ {e}^{-4k} & =\frac{700}{1\,000}=\frac{7}{10} \\ -4k & =\operatorname{ln}⁡(\frac{7}{10}) \\ k & =-\frac{1}{4}\operatorname{ln}⁡(\frac{7}{10})\end{aligned}
$$

Finally, let ${t}_{1}$ be the time when $900$ bacteria are resistant to the antibiotic. Then, we have

$$
\begin{aligned}P({t}_{1}) & =900 \\ 1\,200-1\,000{e}^{-k{t}_{1}} & =900 \\ 300 & =1\,000{e}^{-k{t}_{1}} \\ {e}^{-k{t}_{1}} & =\frac{300}{1\,000}=\frac{3}{10} \\ -k{t}_{1} & =\operatorname{ln}⁡(\frac{3}{10}) \\ {t}_{1} & =-\frac{1}{k}\operatorname{ln}⁡(\frac{3}{10}).\end{aligned}
$$

Substituting in our value for $k,$ we conclude that $900$ bacteria will be resistant to the antibiotic after

$$
{t}_{1}=\frac{-\operatorname{ln}⁡(\frac{3}{10})}{-\frac{1}{4}\operatorname{ln}⁡(\frac{7}{10})}=13.502…≈14\,\text{hours},
$$

rounded to the nearest hour.

## generated variant; observed empirical unknown intent q-335578 0

### Generated record

Throughout an experiment in a laboratory, a culture contains $4\,800$ bacteria in total (limited by nutrients and space). At the beginning of the experiment, $800$ of the $4\,800$ bacteria are resistant to a new antibiotic. After $8$ hours, the number of resistant bacteria increases to $2000.$ To the nearest hour, how long does it take for the number of resistant bacteria to reach $3600?$

*Hint: You may assume that the number of resistant bacteria, $P(t),$ increases at a rate that obeys an inhibited growth model, where $t\ge 0$ is the time, in hours.*

- $35$ hours
- $15$ hours
- $19$ hours
- $39$ hours
- $27$ hours **correct**

The rate at which the resistant bacteria population, $P(t),$ changes is proportional to the difference between the total bacteria population in the culture and its current resistant population. Therefore, we have the inhibited growth equation

$$
\frac{dP}{dt}=k(a-P),
$$

where $a$ is the total bacteria population the culture can support, and $k>0$ is a constant of proportionality.

In our case, $a=4\,800$ bacteria, and we have

$$
\frac{dP}{dt}=k(4\,800-P).
$$

First, we integrate our differential equation by separating the variables:

$$
\begin{aligned}\frac{dP}{4\,800-P} & =k\,dt \\ \int \frac{dP}{4\,800-P} & =\int k\,dt \\ -\operatorname{ln}⁡|4\,800-P| & =kt+C\end{aligned}
$$

Since this is the solution to an inhibited growth equation, we have $4\,800-P>0$ for all $t\ge 0.$
Next, we solve for $P(t),$ as follows:

$$
\begin{aligned}4\,800-P & ={e}^{-kt-C} \\ 4\,800-P & ={e}^{-C}{e}^{-kt} \\ 4\,800-P & =K{e}^{-kt} \\ P & =4\,800-K{e}^{-kt}\end{aligned}
$$

Note that $K={e}^{-C}$ is a constant of integration. 

We're told that the initial population of resistant bacteria was $800$ cells. So, we apply the initial condition $P(0)=800,$ and solve for $K:$

$$
\begin{aligned}P(0) & =800 \\ 4\,800-K{e}^{0} & =800 \\ 4\,800-K & =800 \\ K & =4\,000\end{aligned}
$$

Therefore, we have the following expression for $P(t):$

$$
P(t)=4\,800-4\,000{e}^{-kt}
$$

We're also told that, after $8$ hours, the resistant bacteria population was $2000$ cells. So, applying the condition $P(8)=2000,$ we can solve for $k:$

$$
\begin{aligned}P(8) & =2000 \\ 4\,800-4\,000{e}^{-8k} & =2000 \\ 2800 & =4\,000{e}^{-8k} \\ {e}^{-8k} & =\frac{2800}{4\,000}=\frac{7}{10} \\ -8k & =\operatorname{ln}⁡(\frac{7}{10}) \\ k & =-\frac{1}{8}\operatorname{ln}⁡(\frac{7}{10})\end{aligned}
$$

Finally, let ${t}_{1}$ be the time when $3600$ bacteria are resistant to the antibiotic. Then, we have

$$
\begin{aligned}P({t}_{1}) & =3600 \\ 4\,800-4\,000{e}^{-k{t}_{1}} & =3600 \\ 1200 & =4\,000{e}^{-k{t}_{1}} \\ {e}^{-k{t}_{1}} & =\frac{1200}{4\,000}=\frac{3}{10} \\ -k{t}_{1} & =\operatorname{ln}⁡(\frac{3}{10}) \\ {t}_{1} & =-\frac{1}{k}\operatorname{ln}⁡(\frac{3}{10}).\end{aligned}
$$

Substituting in our value for $k,$ we conclude that $3600$ bacteria will be resistant to the antibiotic after

$$
{t}_{1}=\frac{-\operatorname{ln}⁡(\frac{3}{10})}{-\frac{1}{8}\operatorname{ln}⁡(\frac{7}{10})}=27.004…≈27\,\text{hours},
$$

rounded to the nearest hour.

## generated variant; observed empirical unknown intent q-335578 1

### Generated record

Throughout an experiment in a laboratory, a culture contains $2\,400$ bacteria in total (limited by nutrients and space). At the beginning of the experiment, $400$ of the $2\,400$ bacteria are resistant to a new antibiotic. After $8$ hours, the number of resistant bacteria increases to $1000.$ To the nearest hour, how long does it take for the number of resistant bacteria to reach $1800?$

*Hint: You may assume that the number of resistant bacteria, $P(t),$ increases at a rate that obeys an inhibited growth model, where $t\ge 0$ is the time, in hours.*

- $27$ hours **correct**
- $15$ hours
- $35$ hours
- $39$ hours
- $19$ hours

The rate at which the resistant bacteria population, $P(t),$ changes is proportional to the difference between the total bacteria population in the culture and its current resistant population. Therefore, we have the inhibited growth equation

$$
\frac{dP}{dt}=k(a-P),
$$

where $a$ is the total bacteria population the culture can support, and $k>0$ is a constant of proportionality.

In our case, $a=2\,400$ bacteria, and we have

$$
\frac{dP}{dt}=k(2\,400-P).
$$

First, we integrate our differential equation by separating the variables:

$$
\begin{aligned}\frac{dP}{2\,400-P} & =k\,dt \\ \int \frac{dP}{2\,400-P} & =\int k\,dt \\ -\operatorname{ln}⁡|2\,400-P| & =kt+C\end{aligned}
$$

Since this is the solution to an inhibited growth equation, we have $2\,400-P>0$ for all $t\ge 0.$
Next, we solve for $P(t),$ as follows:

$$
\begin{aligned}2\,400-P & ={e}^{-kt-C} \\ 2\,400-P & ={e}^{-C}{e}^{-kt} \\ 2\,400-P & =K{e}^{-kt} \\ P & =2\,400-K{e}^{-kt}\end{aligned}
$$

Note that $K={e}^{-C}$ is a constant of integration. 

We're told that the initial population of resistant bacteria was $400$ cells. So, we apply the initial condition $P(0)=400,$ and solve for $K:$

$$
\begin{aligned}P(0) & =400 \\ 2\,400-K{e}^{0} & =400 \\ 2\,400-K & =400 \\ K & =2\,000\end{aligned}
$$

Therefore, we have the following expression for $P(t):$

$$
P(t)=2\,400-2\,000{e}^{-kt}
$$

We're also told that, after $8$ hours, the resistant bacteria population was $1000$ cells. So, applying the condition $P(8)=1000,$ we can solve for $k:$

$$
\begin{aligned}P(8) & =1000 \\ 2\,400-2\,000{e}^{-8k} & =1000 \\ 1400 & =2\,000{e}^{-8k} \\ {e}^{-8k} & =\frac{1400}{2\,000}=\frac{7}{10} \\ -8k & =\operatorname{ln}⁡(\frac{7}{10}) \\ k & =-\frac{1}{8}\operatorname{ln}⁡(\frac{7}{10})\end{aligned}
$$

Finally, let ${t}_{1}$ be the time when $1800$ bacteria are resistant to the antibiotic. Then, we have

$$
\begin{aligned}P({t}_{1}) & =1800 \\ 2\,400-2\,000{e}^{-k{t}_{1}} & =1800 \\ 600 & =2\,000{e}^{-k{t}_{1}} \\ {e}^{-k{t}_{1}} & =\frac{600}{2\,000}=\frac{3}{10} \\ -k{t}_{1} & =\operatorname{ln}⁡(\frac{3}{10}) \\ {t}_{1} & =-\frac{1}{k}\operatorname{ln}⁡(\frac{3}{10}).\end{aligned}
$$

Substituting in our value for $k,$ we conclude that $1800$ bacteria will be resistant to the antibiotic after

$$
{t}_{1}=\frac{-\operatorname{ln}⁡(\frac{3}{10})}{-\frac{1}{8}\operatorname{ln}⁡(\frac{7}{10})}=27.004…≈27\,\text{hours},
$$

rounded to the nearest hour.

## generated variant; authored operation bank q-335578 0

### Generated record

Throughout an experiment in a laboratory, a culture contains $1\,300$ bacteria in total (limited by nutrients and space). At the beginning of the experiment, $350$ of the $1\,300$ bacteria are resistant to a new antibiotic. After $10$ hours, the number of resistant bacteria increases to $750.$ To the nearest hour, how long does it take for the number of resistant bacteria to reach $1100?$

*Hint: You may assume that the number of resistant bacteria, $P(t),$ increases at a rate that obeys an inhibited growth model, where $t\ge 0$ is the time, in hours.*

- $29$ hours **correct**
- $18$ hours
- $21$ hours
- $14$ hours
- $2$ hours

The rate at which the resistant bacteria population, $P(t),$ changes is proportional to the difference between the total bacteria population in the culture and its current resistant population. Therefore, we have the inhibited growth equation

$$
\frac{dP}{dt}=k(a-P),
$$

where $a$ is the total bacteria population the culture can support, and $k>0$ is a constant of proportionality.

In our case, $a=1\,300$ bacteria, and we have

$$
\frac{dP}{dt}=k(1\,300-P).
$$

First, we integrate our differential equation by separating the variables:

$$
\begin{aligned}\frac{dP}{1\,300-P} & =k\,dt \\ \int \frac{dP}{1\,300-P} & =\int k\,dt \\ -\operatorname{ln}⁡|1\,300-P| & =kt+C\end{aligned}
$$

Since this is the solution to an inhibited growth equation, we have $1\,300-P>0$ for all $t\ge 0.$
Next, we solve for $P(t),$ as follows:

$$
\begin{aligned}1\,300-P & ={e}^{-kt-C} \\ 1\,300-P & ={e}^{-C}{e}^{-kt} \\ 1\,300-P & =K{e}^{-kt} \\ P & =1\,300-K{e}^{-kt}\end{aligned}
$$

Note that $K={e}^{-C}$ is a constant of integration. 

We're told that the initial population of resistant bacteria was $350$ cells. So, we apply the initial condition $P(0)=350,$ and solve for $K:$

$$
\begin{aligned}P(0) & =350 \\ 1\,300-K{e}^{0} & =350 \\ 1\,300-K & =350 \\ K & =950\end{aligned}
$$

Therefore, we have the following expression for $P(t):$

$$
P(t)=1\,300-950{e}^{-kt}
$$

We're also told that, after $10$ hours, the resistant bacteria population was $750$ cells. So, applying the condition $P(10)=750,$ we can solve for $k:$

$$
\begin{aligned}P(10) & =750 \\ 1\,300-950{e}^{-10k} & =750 \\ 550 & =950{e}^{-10k} \\ {e}^{-10k} & =\frac{550}{950}=\frac{11}{19} \\ -10k & =\operatorname{ln}⁡(\frac{11}{19}) \\ k & =-\frac{1}{10}\operatorname{ln}⁡(\frac{11}{19})\end{aligned}
$$

Finally, let ${t}_{1}$ be the time when $1100$ bacteria are resistant to the antibiotic. Then, we have

$$
\begin{aligned}P({t}_{1}) & =1100 \\ 1\,300-950{e}^{-k{t}_{1}} & =1100 \\ 200 & =950{e}^{-k{t}_{1}} \\ {e}^{-k{t}_{1}} & =\frac{200}{950}=\frac{4}{19} \\ -k{t}_{1} & =\operatorname{ln}⁡(\frac{4}{19}) \\ {t}_{1} & =-\frac{1}{k}\operatorname{ln}⁡(\frac{4}{19}).\end{aligned}
$$

Substituting in our value for $k,$ we conclude that $1100$ bacteria will be resistant to the antibiotic after

$$
{t}_{1}=\frac{-\operatorname{ln}⁡(\frac{4}{19})}{-\frac{1}{10}\operatorname{ln}⁡(\frac{11}{19})}=28.509…≈29\,\text{hours},
$$

rounded to the nearest hour.

## generated variant; authored operation bank q-335578 1

### Generated record

Throughout an experiment in a laboratory, a culture contains $1\,200$ bacteria in total (limited by nutrients and space). At the beginning of the experiment, $100$ of the $1\,200$ bacteria are resistant to a new antibiotic. After $5$ hours, the number of resistant bacteria increases to $200.$ To the nearest hour, how long does it take for the number of resistant bacteria to reach $1150?$

*Hint: You may assume that the number of resistant bacteria, $P(t),$ increases at a rate that obeys an inhibited growth model, where $t\ge 0$ is the time, in hours.*

- $128$ hours
- $50$ hours
- $162$ hours **correct**
- $52$ hours
- $3$ hours

The rate at which the resistant bacteria population, $P(t),$ changes is proportional to the difference between the total bacteria population in the culture and its current resistant population. Therefore, we have the inhibited growth equation

$$
\frac{dP}{dt}=k(a-P),
$$

where $a$ is the total bacteria population the culture can support, and $k>0$ is a constant of proportionality.

In our case, $a=1\,200$ bacteria, and we have

$$
\frac{dP}{dt}=k(1\,200-P).
$$

First, we integrate our differential equation by separating the variables:

$$
\begin{aligned}\frac{dP}{1\,200-P} & =k\,dt \\ \int \frac{dP}{1\,200-P} & =\int k\,dt \\ -\operatorname{ln}⁡|1\,200-P| & =kt+C\end{aligned}
$$

Since this is the solution to an inhibited growth equation, we have $1\,200-P>0$ for all $t\ge 0.$
Next, we solve for $P(t),$ as follows:

$$
\begin{aligned}1\,200-P & ={e}^{-kt-C} \\ 1\,200-P & ={e}^{-C}{e}^{-kt} \\ 1\,200-P & =K{e}^{-kt} \\ P & =1\,200-K{e}^{-kt}\end{aligned}
$$

Note that $K={e}^{-C}$ is a constant of integration. 

We're told that the initial population of resistant bacteria was $100$ cells. So, we apply the initial condition $P(0)=100,$ and solve for $K:$

$$
\begin{aligned}P(0) & =100 \\ 1\,200-K{e}^{0} & =100 \\ 1\,200-K & =100 \\ K & =1\,100\end{aligned}
$$

Therefore, we have the following expression for $P(t):$

$$
P(t)=1\,200-1\,100{e}^{-kt}
$$

We're also told that, after $5$ hours, the resistant bacteria population was $200$ cells. So, applying the condition $P(5)=200,$ we can solve for $k:$

$$
\begin{aligned}P(5) & =200 \\ 1\,200-1\,100{e}^{-5k} & =200 \\ 1000 & =1\,100{e}^{-5k} \\ {e}^{-5k} & =\frac{1000}{1\,100}=\frac{10}{11} \\ -5k & =\operatorname{ln}⁡(\frac{10}{11}) \\ k & =-\frac{1}{5}\operatorname{ln}⁡(\frac{10}{11})\end{aligned}
$$

Finally, let ${t}_{1}$ be the time when $1150$ bacteria are resistant to the antibiotic. Then, we have

$$
\begin{aligned}P({t}_{1}) & =1150 \\ 1\,200-1\,100{e}^{-k{t}_{1}} & =1150 \\ 50 & =1\,100{e}^{-k{t}_{1}} \\ {e}^{-k{t}_{1}} & =\frac{50}{1\,100}=\frac{1}{22} \\ -k{t}_{1} & =\operatorname{ln}⁡(\frac{1}{22}) \\ {t}_{1} & =-\frac{1}{k}\operatorname{ln}⁡(\frac{1}{22}).\end{aligned}
$$

Substituting in our value for $k,$ we conclude that $1150$ bacteria will be resistant to the antibiotic after

$$
{t}_{1}=\frac{-\operatorname{ln}⁡(\frac{1}{22})}{-\frac{1}{5}\operatorname{ln}⁡(\frac{10}{11})}=162.156…≈162\,\text{hours},
$$

rounded to the nearest hour.

## original source replay q-335542

### Captured original

A wildlife reserve can support a total of $800$ deer.
At the beginning of a disease study in the reserve, a parasitic infection has affected $80$ deer. After $10$ days, the number of deer affected by the parasite increases to $300.$ To the nearest day, how long does it take for the infected deer population to reach $600$ animals?

*Hint: You may assume that the number of deer affected by the parasite, $P(t),$ increases at a rate that obeys an inhibited growth model, where $t\ge 0$ is the time, in days.*

- $35$ days
- $50$ days
- $40$ days
- $20$ days
- $28$ days

The rate at which the deer population affected by the parasite, $P(t),$ changes is proportional to the difference between the total deer population and its current population affected. Therefore, we have the inhibited growth equation

$$
\frac{dP}{dt}=k(a-P),
$$

where $a$ is the total deer population in the reserve, and $k>0$ is a constant of proportionality.

In our case, $a=800$ deer, and we have

$$
\frac{dP}{dt}=k(800-P).
$$

First, we integrate our differential equation by separating the variables:

$$
\begin{aligned}\frac{dP}{800-P} & =k\,dt \\ \int \frac{dP}{800-P} & =\int k\,dt \\ -\operatorname{ln}⁡|800-P| & =kt+C\end{aligned}
$$

Since this is the solution to an inhibited growth equation, we have $800-P>0$ for all $t\ge 0.$
Next, we solve for $P(t),$ as follows:

$$
\begin{aligned}800-P & ={e}^{-kt-C} \\ 800-P & ={e}^{-C}{e}^{-kt} \\ 800-P & =K{e}^{-kt} \\ P & =800-K{e}^{-kt}\end{aligned}
$$

Note that $K={e}^{-C}$ is a constant of integration. 

We're told that the initial deer population affected by the parasite was $80$ animals. So, we apply the initial condition $P(0)=80,$ and solve for $K:$

$$
\begin{aligned}P(0) & =80 \\ 800-K{e}^{0} & =80 \\ 800-K & =80 \\ K & =720\end{aligned}
$$

Therefore, we have the following expression for $P(t):$

$$
P(t)=800-720{e}^{-kt}
$$

We're also told that, after $10$ days, the deer population affected by the parasite was $300$ animals. So, applying the condition $P(10)=300,$ we can solve for $k:$

$$
\begin{aligned}P(10) & =300 \\ 800-720{e}^{-10k} & =300 \\ 500 & =720{e}^{-10k} \\ {e}^{-10k} & =\frac{500}{720}=\frac{25}{36} \\ -10k & =\operatorname{ln}⁡(\frac{25}{36}) \\ k & =-\frac{1}{10}\operatorname{ln}⁡(\frac{25}{36})\end{aligned}
$$

Finally, let ${t}_{1}$ be the time when $600$ deer are affected by the parasite. Then, we have

$$
\begin{aligned}P({t}_{1}) & =600 \\ 800-720{e}^{-k{t}_{1}} & =600 \\ 200 & =720{e}^{-k{t}_{1}} \\ {e}^{-k{t}_{1}} & =\frac{200}{720}=\frac{5}{18} \\ -k{t}_{1} & =\operatorname{ln}⁡(\frac{5}{18}) \\ {t}_{1} & =-\frac{1}{k}\operatorname{ln}⁡(\frac{5}{18}).\end{aligned}
$$

Substituting in our value for $k,$ we conclude that $600$ deer will be affected by the parasite after

$$
{t}_{1}=\frac{-\operatorname{ln}⁡(\frac{5}{18})}{-\frac{1}{10}\operatorname{ln}⁡(\frac{25}{36})}=35.128…≈35\,\text{days},
$$

rounded to the nearest day.

### Generated record

A wildlife reserve can support a total of $800$ deer.
At the beginning of a disease study in the reserve, a parasitic infection has affected $80$ deer. After $10$ days, the number of deer affected by the parasite increases to $300.$ To the nearest day, how long does it take for the infected deer population to reach $600$ animals?

*Hint: You may assume that the number of deer affected by the parasite, $P(t),$ increases at a rate that obeys an inhibited growth model, where $t\ge 0$ is the time, in days.*

- $40$ days
- $50$ days
- $35$ days **correct**
- $28$ days
- $20$ days

The rate at which the deer population affected by the parasite, $P(t),$ changes is proportional to the difference between the total deer population and its current population affected. Therefore, we have the inhibited growth equation

$$
\frac{dP}{dt}=k(a-P),
$$

where $a$ is the total deer population in the reserve, and $k>0$ is a constant of proportionality.

In our case, $a=800$ deer, and we have

$$
\frac{dP}{dt}=k(800-P).
$$

First, we integrate our differential equation by separating the variables:

$$
\begin{aligned}\frac{dP}{800-P} & =k\,dt \\ \int \frac{dP}{800-P} & =\int k\,dt \\ -\operatorname{ln}⁡|800-P| & =kt+C\end{aligned}
$$

Since this is the solution to an inhibited growth equation, we have $800-P>0$ for all $t\ge 0.$
Next, we solve for $P(t),$ as follows:

$$
\begin{aligned}800-P & ={e}^{-kt-C} \\ 800-P & ={e}^{-C}{e}^{-kt} \\ 800-P & =K{e}^{-kt} \\ P & =800-K{e}^{-kt}\end{aligned}
$$

Note that $K={e}^{-C}$ is a constant of integration. 

We're told that the initial deer population affected by the parasite was $80$ animals. So, we apply the initial condition $P(0)=80,$ and solve for $K:$

$$
\begin{aligned}P(0) & =80 \\ 800-K{e}^{0} & =80 \\ 800-K & =80 \\ K & =720\end{aligned}
$$

Therefore, we have the following expression for $P(t):$

$$
P(t)=800-720{e}^{-kt}
$$

We're also told that, after $10$ days, the deer population affected by the parasite was $300$ animals. So, applying the condition $P(10)=300,$ we can solve for $k:$

$$
\begin{aligned}P(10) & =300 \\ 800-720{e}^{-10k} & =300 \\ 500 & =720{e}^{-10k} \\ {e}^{-10k} & =\frac{500}{720}=\frac{25}{36} \\ -10k & =\operatorname{ln}⁡(\frac{25}{36}) \\ k & =-\frac{1}{10}\operatorname{ln}⁡(\frac{25}{36})\end{aligned}
$$

Finally, let ${t}_{1}$ be the time when $600$ deer are affected by the parasite. Then, we have

$$
\begin{aligned}P({t}_{1}) & =600 \\ 800-720{e}^{-k{t}_{1}} & =600 \\ 200 & =720{e}^{-k{t}_{1}} \\ {e}^{-k{t}_{1}} & =\frac{200}{720}=\frac{5}{18} \\ -k{t}_{1} & =\operatorname{ln}⁡(\frac{5}{18}) \\ {t}_{1} & =-\frac{1}{k}\operatorname{ln}⁡(\frac{5}{18}).\end{aligned}
$$

Substituting in our value for $k,$ we conclude that $600$ deer will be affected by the parasite after

$$
{t}_{1}=\frac{-\operatorname{ln}⁡(\frac{5}{18})}{-\frac{1}{10}\operatorname{ln}⁡(\frac{25}{36})}=35.128…≈35\,\text{days},
$$

rounded to the nearest day.

## generated variant; observed empirical unknown intent q-335542 0

### Generated record

A wildlife reserve can support a total of $3200$ deer.
At the beginning of a disease study in the reserve, a parasitic infection has affected $320$ deer. After $20$ days, the number of deer affected by the parasite increases to $1200.$ To the nearest day, how long does it take for the infected deer population to reach $2400$ animals?

*Hint: You may assume that the number of deer affected by the parasite, $P(t),$ increases at a rate that obeys an inhibited growth model, where $t\ge 0$ is the time, in days.*

- $80$ days
- $40$ days
- $70$ days **correct**
- $100$ days
- $56$ days

The rate at which the deer population affected by the parasite, $P(t),$ changes is proportional to the difference between the total deer population and its current population affected. Therefore, we have the inhibited growth equation

$$
\frac{dP}{dt}=k(a-P),
$$

where $a$ is the total deer population in the reserve, and $k>0$ is a constant of proportionality.

In our case, $a=3200$ deer, and we have

$$
\frac{dP}{dt}=k(3200-P).
$$

First, we integrate our differential equation by separating the variables:

$$
\begin{aligned}\frac{dP}{3200-P} & =k\,dt \\ \int \frac{dP}{3200-P} & =\int k\,dt \\ -\operatorname{ln}⁡|3200-P| & =kt+C\end{aligned}
$$

Since this is the solution to an inhibited growth equation, we have $3200-P>0$ for all $t\ge 0.$
Next, we solve for $P(t),$ as follows:

$$
\begin{aligned}3200-P & ={e}^{-kt-C} \\ 3200-P & ={e}^{-C}{e}^{-kt} \\ 3200-P & =K{e}^{-kt} \\ P & =3200-K{e}^{-kt}\end{aligned}
$$

Note that $K={e}^{-C}$ is a constant of integration. 

We're told that the initial deer population affected by the parasite was $320$ animals. So, we apply the initial condition $P(0)=320,$ and solve for $K:$

$$
\begin{aligned}P(0) & =320 \\ 3200-K{e}^{0} & =320 \\ 3200-K & =320 \\ K & =2880\end{aligned}
$$

Therefore, we have the following expression for $P(t):$

$$
P(t)=3200-2880{e}^{-kt}
$$

We're also told that, after $20$ days, the deer population affected by the parasite was $1200$ animals. So, applying the condition $P(20)=1200,$ we can solve for $k:$

$$
\begin{aligned}P(20) & =1200 \\ 3200-2880{e}^{-20k} & =1200 \\ 2000 & =2880{e}^{-20k} \\ {e}^{-20k} & =\frac{2000}{2880}=\frac{25}{36} \\ -20k & =\operatorname{ln}⁡(\frac{25}{36}) \\ k & =-\frac{1}{20}\operatorname{ln}⁡(\frac{25}{36})\end{aligned}
$$

Finally, let ${t}_{1}$ be the time when $2400$ deer are affected by the parasite. Then, we have

$$
\begin{aligned}P({t}_{1}) & =2400 \\ 3200-2880{e}^{-k{t}_{1}} & =2400 \\ 800 & =2880{e}^{-k{t}_{1}} \\ {e}^{-k{t}_{1}} & =\frac{800}{2880}=\frac{5}{18} \\ -k{t}_{1} & =\operatorname{ln}⁡(\frac{5}{18}) \\ {t}_{1} & =-\frac{1}{k}\operatorname{ln}⁡(\frac{5}{18}).\end{aligned}
$$

Substituting in our value for $k,$ we conclude that $2400$ deer will be affected by the parasite after

$$
{t}_{1}=\frac{-\operatorname{ln}⁡(\frac{5}{18})}{-\frac{1}{20}\operatorname{ln}⁡(\frac{25}{36})}=70.256…≈70\,\text{days},
$$

rounded to the nearest day.

## generated variant; observed empirical unknown intent q-335542 1

### Generated record

A wildlife reserve can support a total of $1600$ deer.
At the beginning of a disease study in the reserve, a parasitic infection has affected $160$ deer. After $20$ days, the number of deer affected by the parasite increases to $600.$ To the nearest day, how long does it take for the infected deer population to reach $1200$ animals?

*Hint: You may assume that the number of deer affected by the parasite, $P(t),$ increases at a rate that obeys an inhibited growth model, where $t\ge 0$ is the time, in days.*

- $56$ days
- $40$ days
- $80$ days
- $100$ days
- $70$ days **correct**

The rate at which the deer population affected by the parasite, $P(t),$ changes is proportional to the difference between the total deer population and its current population affected. Therefore, we have the inhibited growth equation

$$
\frac{dP}{dt}=k(a-P),
$$

where $a$ is the total deer population in the reserve, and $k>0$ is a constant of proportionality.

In our case, $a=1600$ deer, and we have

$$
\frac{dP}{dt}=k(1600-P).
$$

First, we integrate our differential equation by separating the variables:

$$
\begin{aligned}\frac{dP}{1600-P} & =k\,dt \\ \int \frac{dP}{1600-P} & =\int k\,dt \\ -\operatorname{ln}⁡|1600-P| & =kt+C\end{aligned}
$$

Since this is the solution to an inhibited growth equation, we have $1600-P>0$ for all $t\ge 0.$
Next, we solve for $P(t),$ as follows:

$$
\begin{aligned}1600-P & ={e}^{-kt-C} \\ 1600-P & ={e}^{-C}{e}^{-kt} \\ 1600-P & =K{e}^{-kt} \\ P & =1600-K{e}^{-kt}\end{aligned}
$$

Note that $K={e}^{-C}$ is a constant of integration. 

We're told that the initial deer population affected by the parasite was $160$ animals. So, we apply the initial condition $P(0)=160,$ and solve for $K:$

$$
\begin{aligned}P(0) & =160 \\ 1600-K{e}^{0} & =160 \\ 1600-K & =160 \\ K & =1440\end{aligned}
$$

Therefore, we have the following expression for $P(t):$

$$
P(t)=1600-1440{e}^{-kt}
$$

We're also told that, after $20$ days, the deer population affected by the parasite was $600$ animals. So, applying the condition $P(20)=600,$ we can solve for $k:$

$$
\begin{aligned}P(20) & =600 \\ 1600-1440{e}^{-20k} & =600 \\ 1000 & =1440{e}^{-20k} \\ {e}^{-20k} & =\frac{1000}{1440}=\frac{25}{36} \\ -20k & =\operatorname{ln}⁡(\frac{25}{36}) \\ k & =-\frac{1}{20}\operatorname{ln}⁡(\frac{25}{36})\end{aligned}
$$

Finally, let ${t}_{1}$ be the time when $1200$ deer are affected by the parasite. Then, we have

$$
\begin{aligned}P({t}_{1}) & =1200 \\ 1600-1440{e}^{-k{t}_{1}} & =1200 \\ 400 & =1440{e}^{-k{t}_{1}} \\ {e}^{-k{t}_{1}} & =\frac{400}{1440}=\frac{5}{18} \\ -k{t}_{1} & =\operatorname{ln}⁡(\frac{5}{18}) \\ {t}_{1} & =-\frac{1}{k}\operatorname{ln}⁡(\frac{5}{18}).\end{aligned}
$$

Substituting in our value for $k,$ we conclude that $1200$ deer will be affected by the parasite after

$$
{t}_{1}=\frac{-\operatorname{ln}⁡(\frac{5}{18})}{-\frac{1}{20}\operatorname{ln}⁡(\frac{25}{36})}=70.256…≈70\,\text{days},
$$

rounded to the nearest day.

## generated variant; authored operation bank q-335542 0

### Generated record

A wildlife reserve can support a total of $1300$ deer.
At the beginning of a disease study in the reserve, a parasitic infection has affected $350$ deer. After $10$ days, the number of deer affected by the parasite increases to $750.$ To the nearest day, how long does it take for the infected deer population to reach $1100$ animals?

*Hint: You may assume that the number of deer affected by the parasite, $P(t),$ increases at a rate that obeys an inhibited growth model, where $t\ge 0$ is the time, in days.*

- $29$ days **correct**
- $18$ days
- $21$ days
- $14$ days
- $2$ days

The rate at which the deer population affected by the parasite, $P(t),$ changes is proportional to the difference between the total deer population and its current population affected. Therefore, we have the inhibited growth equation

$$
\frac{dP}{dt}=k(a-P),
$$

where $a$ is the total deer population in the reserve, and $k>0$ is a constant of proportionality.

In our case, $a=1300$ deer, and we have

$$
\frac{dP}{dt}=k(1300-P).
$$

First, we integrate our differential equation by separating the variables:

$$
\begin{aligned}\frac{dP}{1300-P} & =k\,dt \\ \int \frac{dP}{1300-P} & =\int k\,dt \\ -\operatorname{ln}⁡|1300-P| & =kt+C\end{aligned}
$$

Since this is the solution to an inhibited growth equation, we have $1300-P>0$ for all $t\ge 0.$
Next, we solve for $P(t),$ as follows:

$$
\begin{aligned}1300-P & ={e}^{-kt-C} \\ 1300-P & ={e}^{-C}{e}^{-kt} \\ 1300-P & =K{e}^{-kt} \\ P & =1300-K{e}^{-kt}\end{aligned}
$$

Note that $K={e}^{-C}$ is a constant of integration. 

We're told that the initial deer population affected by the parasite was $350$ animals. So, we apply the initial condition $P(0)=350,$ and solve for $K:$

$$
\begin{aligned}P(0) & =350 \\ 1300-K{e}^{0} & =350 \\ 1300-K & =350 \\ K & =950\end{aligned}
$$

Therefore, we have the following expression for $P(t):$

$$
P(t)=1300-950{e}^{-kt}
$$

We're also told that, after $10$ days, the deer population affected by the parasite was $750$ animals. So, applying the condition $P(10)=750,$ we can solve for $k:$

$$
\begin{aligned}P(10) & =750 \\ 1300-950{e}^{-10k} & =750 \\ 550 & =950{e}^{-10k} \\ {e}^{-10k} & =\frac{550}{950}=\frac{11}{19} \\ -10k & =\operatorname{ln}⁡(\frac{11}{19}) \\ k & =-\frac{1}{10}\operatorname{ln}⁡(\frac{11}{19})\end{aligned}
$$

Finally, let ${t}_{1}$ be the time when $1100$ deer are affected by the parasite. Then, we have

$$
\begin{aligned}P({t}_{1}) & =1100 \\ 1300-950{e}^{-k{t}_{1}} & =1100 \\ 200 & =950{e}^{-k{t}_{1}} \\ {e}^{-k{t}_{1}} & =\frac{200}{950}=\frac{4}{19} \\ -k{t}_{1} & =\operatorname{ln}⁡(\frac{4}{19}) \\ {t}_{1} & =-\frac{1}{k}\operatorname{ln}⁡(\frac{4}{19}).\end{aligned}
$$

Substituting in our value for $k,$ we conclude that $1100$ deer will be affected by the parasite after

$$
{t}_{1}=\frac{-\operatorname{ln}⁡(\frac{4}{19})}{-\frac{1}{10}\operatorname{ln}⁡(\frac{11}{19})}=28.509…≈29\,\text{days},
$$

rounded to the nearest day.

## generated variant; authored operation bank q-335542 1

### Generated record

A wildlife reserve can support a total of $1200$ deer.
At the beginning of a disease study in the reserve, a parasitic infection has affected $100$ deer. After $5$ days, the number of deer affected by the parasite increases to $200.$ To the nearest day, how long does it take for the infected deer population to reach $1150$ animals?

*Hint: You may assume that the number of deer affected by the parasite, $P(t),$ increases at a rate that obeys an inhibited growth model, where $t\ge 0$ is the time, in days.*

- $128$ days
- $50$ days
- $162$ days **correct**
- $52$ days
- $3$ days

The rate at which the deer population affected by the parasite, $P(t),$ changes is proportional to the difference between the total deer population and its current population affected. Therefore, we have the inhibited growth equation

$$
\frac{dP}{dt}=k(a-P),
$$

where $a$ is the total deer population in the reserve, and $k>0$ is a constant of proportionality.

In our case, $a=1200$ deer, and we have

$$
\frac{dP}{dt}=k(1200-P).
$$

First, we integrate our differential equation by separating the variables:

$$
\begin{aligned}\frac{dP}{1200-P} & =k\,dt \\ \int \frac{dP}{1200-P} & =\int k\,dt \\ -\operatorname{ln}⁡|1200-P| & =kt+C\end{aligned}
$$

Since this is the solution to an inhibited growth equation, we have $1200-P>0$ for all $t\ge 0.$
Next, we solve for $P(t),$ as follows:

$$
\begin{aligned}1200-P & ={e}^{-kt-C} \\ 1200-P & ={e}^{-C}{e}^{-kt} \\ 1200-P & =K{e}^{-kt} \\ P & =1200-K{e}^{-kt}\end{aligned}
$$

Note that $K={e}^{-C}$ is a constant of integration. 

We're told that the initial deer population affected by the parasite was $100$ animals. So, we apply the initial condition $P(0)=100,$ and solve for $K:$

$$
\begin{aligned}P(0) & =100 \\ 1200-K{e}^{0} & =100 \\ 1200-K & =100 \\ K & =1100\end{aligned}
$$

Therefore, we have the following expression for $P(t):$

$$
P(t)=1200-1100{e}^{-kt}
$$

We're also told that, after $5$ days, the deer population affected by the parasite was $200$ animals. So, applying the condition $P(5)=200,$ we can solve for $k:$

$$
\begin{aligned}P(5) & =200 \\ 1200-1100{e}^{-5k} & =200 \\ 1000 & =1100{e}^{-5k} \\ {e}^{-5k} & =\frac{1000}{1100}=\frac{10}{11} \\ -5k & =\operatorname{ln}⁡(\frac{10}{11}) \\ k & =-\frac{1}{5}\operatorname{ln}⁡(\frac{10}{11})\end{aligned}
$$

Finally, let ${t}_{1}$ be the time when $1150$ deer are affected by the parasite. Then, we have

$$
\begin{aligned}P({t}_{1}) & =1150 \\ 1200-1100{e}^{-k{t}_{1}} & =1150 \\ 50 & =1100{e}^{-k{t}_{1}} \\ {e}^{-k{t}_{1}} & =\frac{50}{1100}=\frac{1}{22} \\ -k{t}_{1} & =\operatorname{ln}⁡(\frac{1}{22}) \\ {t}_{1} & =-\frac{1}{k}\operatorname{ln}⁡(\frac{1}{22}).\end{aligned}
$$

Substituting in our value for $k,$ we conclude that $1150$ deer will be affected by the parasite after

$$
{t}_{1}=\frac{-\operatorname{ln}⁡(\frac{1}{22})}{-\frac{1}{5}\operatorname{ln}⁡(\frac{10}{11})}=162.156…≈162\,\text{days},
$$

rounded to the nearest day.

## original source replay q-335590

### Captured original

A small bakery produces loaves of bread. The owner knows that the bakery can produce a maximum of $600$ loaves a day; however, current production is below this maximum. Since she started monitoring, the bakers produced $480$ loaves and $500$ loaves on days $4$ and $8,$ respectively. How many loaves do they produce on day $40?$ Round your answer to the nearest integer.

*Hint: You may assume that the bread production $E(t)$ increases at a rate that obeys an inhibited growth model, where $t$ is the time, in days.*

- $570$ loaves
- $560$ loaves
- $577$ loaves
- $550$ loaves
- $590$ loaves

The rate at which the bread production $E(t)$ changes is proportional to the difference between the maximum possible bread production and its current bread production. Therefore, we have the inhibited growth equation

$$
\frac{dE}{dt}=k(a-E),
$$

where $a$ is the maximum production of the bakery, and $k>0$ is a constant of proportionality.

In our case, $a=600$ loaves, and we have

$$
\frac{dE}{dt}=k(600-E).
$$

First, we integrate our differential equation by separating the variables:

$$
\begin{aligned}\frac{dE}{600-E} & =k\,dt \\ \int \frac{dE}{600-E} & =\int k\,\text{d}t \\ -\operatorname{ln}⁡|600-E| & =kt+C\end{aligned}
$$

Since this is the solution to an inhibited growth equation, we have $600-E>0$ for all $t\ge 0.$ Next, we solve for $E(t),$ as follows:

$$
\begin{aligned}600-E & ={e}^{-kt-C} \\ 600-E & ={e}^{-C}{e}^{-kt} \\ 600-E & =K{e}^{-kt} \\ E & =600-K{e}^{-kt}\end{aligned}
$$

Note that $K={e}^{-C}$ is a constant of integration.

We're told that, on day $4,$ the bread production was $480$ loaves. So, applying the condition $E(4)=480,$ we have

$$
\begin{aligned}E(4) & =480 \\ 600-K{e}^{-4k} & =480 \\ K{e}^{-4k} & =120.\end{aligned}
$$

We're also told that, on day $8,$ the bread production was $500$ loaves. So, applying the condition $E(8)=500,$ we get

$$
\begin{aligned}E(8) & =500 \\ 600-K{e}^{-8k} & =500 \\ K{e}^{-8k} & =100.\end{aligned}
$$

Then, by dividing the result of the first condition by the result of the second, we can solve for $k:$

$$
\begin{aligned}\frac{K{e}^{-4k}}{K{e}^{-8k}} & =\frac{120}{100} \\ {e}^{4k} & =\frac{6}{5} \\ 4k & =\operatorname{ln}⁡(\frac{6}{5}) \\ k & =\frac{1}{4}\operatorname{ln}⁡(\frac{6}{5})\end{aligned}
$$

Now, substituting back into the result of the first condition, we solve for $K:$

$$
\begin{aligned}K{e}^{-4\cdot (1/4)\operatorname{ln}⁡(6/5)} & =120 \\ K & =120{e}^{\operatorname{ln}⁡(6/5)} \\ K & =144\end{aligned}
$$

Therefore, we have the following expression for $E(t):$

$$
E(t)=600-144{e}^{-(t/4)\operatorname{ln}⁡(6/5)}
$$

Finally, the number of loaves baked on day $t=40$ is

$$
E(40)=600-144{e}^{-(40/4)\operatorname{ln}⁡(6/5)}≈576.743…≈577\,\text{loaves},
$$

rounded to the nearest integer.

### Generated record

A small bakery produces loaves of bread. The owner knows that the bakery can produce a maximum of $600$ loaves a day; however, current production is below this maximum. Since she started monitoring, the bakers produced $480$ loaves and $500$ loaves on days $4$ and $8,$ respectively. How many loaves do they produce on day $40?$ Round your answer to the nearest integer.

*Hint: You may assume that the bread production $E(t)$ increases at a rate that obeys an inhibited growth model, where $t$ is the time, in days.*

- $577$ loaves **correct**
- $560$ loaves
- $570$ loaves
- $590$ loaves
- $550$ loaves

The rate at which the bread production $E(t)$ changes is proportional to the difference between the maximum possible bread production and its current bread production. Therefore, we have the inhibited growth equation

$$
\frac{dE}{dt}=k(a-E),
$$

where $a$ is the maximum production of the bakery, and $k>0$ is a constant of proportionality.

In our case, $a=600$ loaves, and we have

$$
\frac{dE}{dt}=k(600-E).
$$

First, we integrate our differential equation by separating the variables:

$$
\begin{aligned}\frac{dE}{600-E} & =k\,dt \\ \int \frac{dE}{600-E} & =\int k\,\text{d}t \\ -\operatorname{ln}⁡|600-E| & =kt+C\end{aligned}
$$

Since this is the solution to an inhibited growth equation, we have $600-E>0$ for all $t\ge 0.$ Next, we solve for $E(t),$ as follows:

$$
\begin{aligned}600-E & ={e}^{-kt-C} \\ 600-E & ={e}^{-C}{e}^{-kt} \\ 600-E & =K{e}^{-kt} \\ E & =600-K{e}^{-kt}\end{aligned}
$$

Note that $K={e}^{-C}$ is a constant of integration.

We're told that, on day $4,$ the bread production was $480$ loaves. So, applying the condition $E(4)=480,$ we have

$$
\begin{aligned}E(4) & =480 \\ 600-K{e}^{-4k} & =480 \\ K{e}^{-4k} & =120.\end{aligned}
$$

We're also told that, on day $8,$ the bread production was $500$ loaves. So, applying the condition $E(8)=500,$ we get

$$
\begin{aligned}E(8) & =500 \\ 600-K{e}^{-8k} & =500 \\ K{e}^{-8k} & =100.\end{aligned}
$$

Then, by dividing the result of the first condition by the result of the second, we can solve for $k:$

$$
\begin{aligned}\frac{K{e}^{-4k}}{K{e}^{-8k}} & =\frac{120}{100} \\ {e}^{4k} & =\frac{6}{5} \\ 4k & =\operatorname{ln}⁡(\frac{6}{5}) \\ k & =\frac{1}{4}\operatorname{ln}⁡(\frac{6}{5})\end{aligned}
$$

Now, substituting back into the result of the first condition, we solve for $K:$

$$
\begin{aligned}K{e}^{-4\cdot (1/4)\operatorname{ln}⁡(6/5)} & =120 \\ K & =120{e}^{\operatorname{ln}⁡(6/5)} \\ K & =144\end{aligned}
$$

Therefore, we have the following expression for $E(t):$

$$
E(t)=600-144{e}^{-(t/4)\operatorname{ln}⁡(6/5)}
$$

Finally, the number of loaves baked on day $t=40$ is

$$
E(40)=600-144{e}^{-(40/4)\operatorname{ln}⁡(6/5)}≈576.743…≈577\,\text{loaves},
$$

rounded to the nearest integer.

## generated variant; observed empirical unknown intent q-335590 0

### Generated record

A small bakery produces loaves of bread. The owner knows that the bakery can produce a maximum of $2400$ loaves a day; however, current production is below this maximum. Since she started monitoring, the bakers produced $1920$ loaves and $2000$ loaves on days $8$ and $16,$ respectively. How many loaves do they produce on day $80?$ Round your answer to the nearest integer.

*Hint: You may assume that the bread production $E(t)$ increases at a rate that obeys an inhibited growth model, where $t$ is the time, in days.*

- $2307$ loaves **correct**
- $2199$ loaves
- $2279$ loaves
- $2239$ loaves
- $2359$ loaves

The rate at which the bread production $E(t)$ changes is proportional to the difference between the maximum possible bread production and its current bread production. Therefore, we have the inhibited growth equation

$$
\frac{dE}{dt}=k(a-E),
$$

where $a$ is the maximum production of the bakery, and $k>0$ is a constant of proportionality.

In our case, $a=2400$ loaves, and we have

$$
\frac{dE}{dt}=k(2400-E).
$$

First, we integrate our differential equation by separating the variables:

$$
\begin{aligned}\frac{dE}{2400-E} & =k\,dt \\ \int \frac{dE}{2400-E} & =\int k\,\text{d}t \\ -\operatorname{ln}⁡|2400-E| & =kt+C\end{aligned}
$$

Since this is the solution to an inhibited growth equation, we have $2400-E>0$ for all $t\ge 0.$ Next, we solve for $E(t),$ as follows:

$$
\begin{aligned}2400-E & ={e}^{-kt-C} \\ 2400-E & ={e}^{-C}{e}^{-kt} \\ 2400-E & =K{e}^{-kt} \\ E & =2400-K{e}^{-kt}\end{aligned}
$$

Note that $K={e}^{-C}$ is a constant of integration.

We're told that, on day $8,$ the bread production was $1920$ loaves. So, applying the condition $E(8)=1920,$ we have

$$
\begin{aligned}E(8) & =1920 \\ 2400-K{e}^{-8k} & =1920 \\ K{e}^{-8k} & =480.\end{aligned}
$$

We're also told that, on day $16,$ the bread production was $2000$ loaves. So, applying the condition $E(16)=2000,$ we get

$$
\begin{aligned}E(16) & =2000 \\ 2400-K{e}^{-16k} & =2000 \\ K{e}^{-16k} & =400.\end{aligned}
$$

Then, by dividing the result of the first condition by the result of the second, we can solve for $k:$

$$
\begin{aligned}\frac{K{e}^{-8k}}{K{e}^{-16k}} & =\frac{480}{400} \\ {e}^{8k} & =\frac{6}{5} \\ 8k & =\operatorname{ln}⁡(\frac{6}{5}) \\ k & =\frac{1}{8}\operatorname{ln}⁡(\frac{6}{5})\end{aligned}
$$

Now, substituting back into the result of the first condition, we solve for $K:$

$$
\begin{aligned}K{e}^{-8\cdot (1/8)\operatorname{ln}⁡(6/5)} & =480 \\ K & =480{e}^{\operatorname{ln}⁡(6/5)} \\ K & =576\end{aligned}
$$

Therefore, we have the following expression for $E(t):$

$$
E(t)=2400-576{e}^{-(t/8)\operatorname{ln}⁡(6/5)}
$$

Finally, the number of loaves baked on day $t=80$ is

$$
E(80)=2400-576{e}^{-(80/8)\operatorname{ln}⁡(6/5)}≈2306.972…≈2307\,\text{loaves},
$$

rounded to the nearest integer.

## generated variant; observed empirical unknown intent q-335590 1

### Generated record

A small bakery produces loaves of bread. The owner knows that the bakery can produce a maximum of $1200$ loaves a day; however, current production is below this maximum. Since she started monitoring, the bakers produced $960$ loaves and $1000$ loaves on days $8$ and $16,$ respectively. How many loaves do they produce on day $80?$ Round your answer to the nearest integer.

*Hint: You may assume that the bread production $E(t)$ increases at a rate that obeys an inhibited growth model, where $t$ is the time, in days.*

- $1179$ loaves
- $1099$ loaves
- $1153$ loaves **correct**
- $1119$ loaves
- $1139$ loaves

The rate at which the bread production $E(t)$ changes is proportional to the difference between the maximum possible bread production and its current bread production. Therefore, we have the inhibited growth equation

$$
\frac{dE}{dt}=k(a-E),
$$

where $a$ is the maximum production of the bakery, and $k>0$ is a constant of proportionality.

In our case, $a=1200$ loaves, and we have

$$
\frac{dE}{dt}=k(1200-E).
$$

First, we integrate our differential equation by separating the variables:

$$
\begin{aligned}\frac{dE}{1200-E} & =k\,dt \\ \int \frac{dE}{1200-E} & =\int k\,\text{d}t \\ -\operatorname{ln}⁡|1200-E| & =kt+C\end{aligned}
$$

Since this is the solution to an inhibited growth equation, we have $1200-E>0$ for all $t\ge 0.$ Next, we solve for $E(t),$ as follows:

$$
\begin{aligned}1200-E & ={e}^{-kt-C} \\ 1200-E & ={e}^{-C}{e}^{-kt} \\ 1200-E & =K{e}^{-kt} \\ E & =1200-K{e}^{-kt}\end{aligned}
$$

Note that $K={e}^{-C}$ is a constant of integration.

We're told that, on day $8,$ the bread production was $960$ loaves. So, applying the condition $E(8)=960,$ we have

$$
\begin{aligned}E(8) & =960 \\ 1200-K{e}^{-8k} & =960 \\ K{e}^{-8k} & =240.\end{aligned}
$$

We're also told that, on day $16,$ the bread production was $1000$ loaves. So, applying the condition $E(16)=1000,$ we get

$$
\begin{aligned}E(16) & =1000 \\ 1200-K{e}^{-16k} & =1000 \\ K{e}^{-16k} & =200.\end{aligned}
$$

Then, by dividing the result of the first condition by the result of the second, we can solve for $k:$

$$
\begin{aligned}\frac{K{e}^{-8k}}{K{e}^{-16k}} & =\frac{240}{200} \\ {e}^{8k} & =\frac{6}{5} \\ 8k & =\operatorname{ln}⁡(\frac{6}{5}) \\ k & =\frac{1}{8}\operatorname{ln}⁡(\frac{6}{5})\end{aligned}
$$

Now, substituting back into the result of the first condition, we solve for $K:$

$$
\begin{aligned}K{e}^{-8\cdot (1/8)\operatorname{ln}⁡(6/5)} & =240 \\ K & =240{e}^{\operatorname{ln}⁡(6/5)} \\ K & =288\end{aligned}
$$

Therefore, we have the following expression for $E(t):$

$$
E(t)=1200-288{e}^{-(t/8)\operatorname{ln}⁡(6/5)}
$$

Finally, the number of loaves baked on day $t=80$ is

$$
E(80)=1200-288{e}^{-(80/8)\operatorname{ln}⁡(6/5)}≈1153.486…≈1153\,\text{loaves},
$$

rounded to the nearest integer.

## generated variant; authored operation bank q-335590 0

### Generated record

A small bakery produces loaves of bread. The owner knows that the bakery can produce a maximum of $800$ loaves a day; however, current production is below this maximum. Since she started monitoring, the bakers produced $700$ loaves and $720$ loaves on days $3$ and $6,$ respectively. How many loaves do they produce on day $36?$ Round your answer to the nearest integer.

*Hint: You may assume that the bread production $E(t)$ increases at a rate that obeys an inhibited growth model, where $t$ is the time, in days.*

- $791$ loaves **correct**
- $48$ loaves
- $745$ loaves
- $684$ loaves
- $752$ loaves

The rate at which the bread production $E(t)$ changes is proportional to the difference between the maximum possible bread production and its current bread production. Therefore, we have the inhibited growth equation

$$
\frac{dE}{dt}=k(a-E),
$$

where $a$ is the maximum production of the bakery, and $k>0$ is a constant of proportionality.

In our case, $a=800$ loaves, and we have

$$
\frac{dE}{dt}=k(800-E).
$$

First, we integrate our differential equation by separating the variables:

$$
\begin{aligned}\frac{dE}{800-E} & =k\,dt \\ \int \frac{dE}{800-E} & =\int k\,\text{d}t \\ -\operatorname{ln}⁡|800-E| & =kt+C\end{aligned}
$$

Since this is the solution to an inhibited growth equation, we have $800-E>0$ for all $t\ge 0.$ Next, we solve for $E(t),$ as follows:

$$
\begin{aligned}800-E & ={e}^{-kt-C} \\ 800-E & ={e}^{-C}{e}^{-kt} \\ 800-E & =K{e}^{-kt} \\ E & =800-K{e}^{-kt}\end{aligned}
$$

Note that $K={e}^{-C}$ is a constant of integration.

We're told that, on day $3,$ the bread production was $700$ loaves. So, applying the condition $E(3)=700,$ we have

$$
\begin{aligned}E(3) & =700 \\ 800-K{e}^{-3k} & =700 \\ K{e}^{-3k} & =100.\end{aligned}
$$

We're also told that, on day $6,$ the bread production was $720$ loaves. So, applying the condition $E(6)=720,$ we get

$$
\begin{aligned}E(6) & =720 \\ 800-K{e}^{-6k} & =720 \\ K{e}^{-6k} & =80.\end{aligned}
$$

Then, by dividing the result of the first condition by the result of the second, we can solve for $k:$

$$
\begin{aligned}\frac{K{e}^{-3k}}{K{e}^{-6k}} & =\frac{100}{80} \\ {e}^{3k} & =\frac{5}{4} \\ 3k & =\operatorname{ln}⁡(\frac{5}{4}) \\ k & =\frac{1}{3}\operatorname{ln}⁡(\frac{5}{4})\end{aligned}
$$

Now, substituting back into the result of the first condition, we solve for $K:$

$$
\begin{aligned}K{e}^{-3\cdot (1/3)\operatorname{ln}⁡(5/4)} & =100 \\ K & =100{e}^{\operatorname{ln}⁡(5/4)} \\ K & =125\end{aligned}
$$

Therefore, we have the following expression for $E(t):$

$$
E(t)=800-125{e}^{-(t/3)\operatorname{ln}⁡(5/4)}
$$

Finally, the number of loaves baked on day $t=36$ is

$$
E(36)=800-125{e}^{-(36/3)\operatorname{ln}⁡(5/4)}≈791.410…≈791\,\text{loaves},
$$

rounded to the nearest integer.

## generated variant; authored operation bank q-335590 1

### Generated record

A small bakery produces loaves of bread. The owner knows that the bakery can produce a maximum of $700$ loaves a day; however, current production is below this maximum. Since she started monitoring, the bakers produced $600$ loaves and $620$ loaves on days $3$ and $6,$ respectively. How many loaves do they produce on day $24?$ Round your answer to the nearest integer.

*Hint: You may assume that the bread production $E(t)$ increases at a rate that obeys an inhibited growth model, where $t$ is the time, in days.*

- $583$ loaves
- $584$ loaves
- $679$ loaves **correct**
- $101$ loaves
- $599$ loaves

The rate at which the bread production $E(t)$ changes is proportional to the difference between the maximum possible bread production and its current bread production. Therefore, we have the inhibited growth equation

$$
\frac{dE}{dt}=k(a-E),
$$

where $a$ is the maximum production of the bakery, and $k>0$ is a constant of proportionality.

In our case, $a=700$ loaves, and we have

$$
\frac{dE}{dt}=k(700-E).
$$

First, we integrate our differential equation by separating the variables:

$$
\begin{aligned}\frac{dE}{700-E} & =k\,dt \\ \int \frac{dE}{700-E} & =\int k\,\text{d}t \\ -\operatorname{ln}⁡|700-E| & =kt+C\end{aligned}
$$

Since this is the solution to an inhibited growth equation, we have $700-E>0$ for all $t\ge 0.$ Next, we solve for $E(t),$ as follows:

$$
\begin{aligned}700-E & ={e}^{-kt-C} \\ 700-E & ={e}^{-C}{e}^{-kt} \\ 700-E & =K{e}^{-kt} \\ E & =700-K{e}^{-kt}\end{aligned}
$$

Note that $K={e}^{-C}$ is a constant of integration.

We're told that, on day $3,$ the bread production was $600$ loaves. So, applying the condition $E(3)=600,$ we have

$$
\begin{aligned}E(3) & =600 \\ 700-K{e}^{-3k} & =600 \\ K{e}^{-3k} & =100.\end{aligned}
$$

We're also told that, on day $6,$ the bread production was $620$ loaves. So, applying the condition $E(6)=620,$ we get

$$
\begin{aligned}E(6) & =620 \\ 700-K{e}^{-6k} & =620 \\ K{e}^{-6k} & =80.\end{aligned}
$$

Then, by dividing the result of the first condition by the result of the second, we can solve for $k:$

$$
\begin{aligned}\frac{K{e}^{-3k}}{K{e}^{-6k}} & =\frac{100}{80} \\ {e}^{3k} & =\frac{5}{4} \\ 3k & =\operatorname{ln}⁡(\frac{5}{4}) \\ k & =\frac{1}{3}\operatorname{ln}⁡(\frac{5}{4})\end{aligned}
$$

Now, substituting back into the result of the first condition, we solve for $K:$

$$
\begin{aligned}K{e}^{-3\cdot (1/3)\operatorname{ln}⁡(5/4)} & =100 \\ K & =100{e}^{\operatorname{ln}⁡(5/4)} \\ K & =125\end{aligned}
$$

Therefore, we have the following expression for $E(t):$

$$
E(t)=700-125{e}^{-(t/3)\operatorname{ln}⁡(5/4)}
$$

Finally, the number of loaves baked on day $t=24$ is

$$
E(24)=700-125{e}^{-(24/3)\operatorname{ln}⁡(5/4)}≈679.028…≈679\,\text{loaves},
$$

rounded to the nearest integer.

## original source replay q-335619

### Captured original

A national park is monitoring the number of people who have downloaded a new park app. The system can support a maximum of $800$ users, but the total is still below this limit. Since the park began tracking downloads, the number of users reached $620$ on day $3$ and $720$ on day $9.$ On what day will the number of users reach $760?$ Round your answer to the nearest integer.

*Hint: You may assume that the number of users, $P(t),$ increases at a rate that obeys an inhibited growth model, where $t$ is the time, in days.*

- $25\text{th}$ day
- $14\text{th}$ day
- $12\text{th}$ day
- $20\text{th}$ day
- $10\text{th}$ day

The rate at which the number of app users $P(t)$ changes is proportional to the difference between the maximum population and its current population. Therefore, we have the inhibited growth equation

$$
\frac{dP}{dt}=k(a-P),
$$

where $a$ is the maximum number of users the system can support, and $k>0$ is a constant of proportionality.

In our case, $a=800$ users, and we have

$$
\frac{dP}{dt}=k(800-P).
$$

First, we integrate our differential equation by separating the variables:

$$
\begin{aligned}\frac{dP}{800-P} & =k\,dt \\ \int \frac{dP}{800-P} & =\int k\,\text{d}t \\ -\operatorname{ln}⁡|800-P| & =kt+C\end{aligned}
$$

Since this is the solution to an inhibited growth equation, we have $800-P>0$ for all $t\ge 0.$ Next, we solve for $P(t),$ as follows:

$$
\begin{aligned}800-P & ={e}^{-kt-C} \\ 800-P & ={e}^{-C}{e}^{-kt} \\ 800-P & =K{e}^{-kt} \\ P & =800-K{e}^{-kt}\end{aligned}
$$

Note that $K={e}^{-C}$ is a constant of integration.

We're told that, on day $3,$ the number of users was $620.$ So, applying the condition $P(3)=620,$ we have

$$
\begin{aligned}P(3) & =620 \\ 800-K{e}^{-3k} & =620 \\ K{e}^{-3k} & =180.\end{aligned}
$$

We're also told that, on day $9,$ the number of users was $720.$ So, applying the condition $P(9)=720,$ we get

$$
\begin{aligned}P(9) & =720 \\ 800-K{e}^{-9k} & =720 \\ K{e}^{-9k} & =80.\end{aligned}
$$

Then, by dividing the result of the first condition by the result of the second, we can solve for $k:$

$$
\begin{aligned}\frac{K{e}^{-3k}}{K{e}^{-9k}} & =\frac{180}{80} \\ {e}^{6k} & =\frac{9}{4} \\ 6k & =\operatorname{ln}⁡(\frac{9}{4}) \\ k & =\frac{1}{6}\operatorname{ln}⁡(\frac{9}{4})\end{aligned}
$$

Now, substituting back into the result of the first condition, we solve for $K:$

$$
\begin{aligned}K{e}^{-3\cdot (1/6)\operatorname{ln}⁡(9/4)} & =180 \\ K & =180{e}^{(1/2)\operatorname{ln}⁡(9/4)} \\ K & =180\sqrt{\frac{9}{4}} \\ K & =180\cdot \frac{3}{2} \\ K & =270\end{aligned}
$$

Therefore, we have the following expression for $P(t):$

$$
P(t)=800-270{e}^{-(t/6)\operatorname{ln}⁡(9/4)}.
$$

Finally, let $d$  be the day when the app reaches $760$ users. Then, we have

$$
\begin{aligned}P(d) & =760 \\ 800-270{e}^{-kd} & =760 \\ 40 & =270{e}^{-kd} \\ {e}^{-kd} & =\frac{40}{270} \\ {e}^{-kd} & =\frac{4}{27} \\ -kd & =\operatorname{ln}⁡(\frac{4}{27}) \\ d & =-\frac{1}{k}\operatorname{ln}⁡(\frac{4}{27}).\end{aligned}
$$

Substituting in our value for $k,$ we conclude that the number of users will be $760$ on day

$$
d=\frac{-\operatorname{ln}⁡(\frac{4}{27})}{\frac{1}{6}\operatorname{ln}⁡(\frac{9}{4})}=14.1285…≈14,
$$

rounded to the nearest day.

### Generated record

A national park is monitoring the number of people who have downloaded a new park app. The system can support a maximum of $800$ users, but the total is still below this limit. Since the park began tracking downloads, the number of users reached $620$ on day $3$ and $720$ on day $9.$ On what day will the number of users reach $760?$ Round your answer to the nearest integer.

*Hint: You may assume that the number of users, $P(t),$ increases at a rate that obeys an inhibited growth model, where $t$ is the time, in days.*

- $12\text{th}$ day
- $14\text{th}$ day **correct**
- $25\text{th}$ day
- $10\text{th}$ day
- $20\text{th}$ day

The rate at which the number of app users $P(t)$ changes is proportional to the difference between the maximum population and its current population. Therefore, we have the inhibited growth equation

$$
\frac{dP}{dt}=k(a-P),
$$

where $a$ is the maximum number of users the system can support, and $k>0$ is a constant of proportionality.

In our case, $a=800$ users, and we have

$$
\frac{dP}{dt}=k(800-P).
$$

First, we integrate our differential equation by separating the variables:

$$
\begin{aligned}\frac{dP}{800-P} & =k\,dt \\ \int \frac{dP}{800-P} & =\int k\,\text{d}t \\ -\operatorname{ln}⁡|800-P| & =kt+C\end{aligned}
$$

Since this is the solution to an inhibited growth equation, we have $800-P>0$ for all $t\ge 0.$ Next, we solve for $P(t),$ as follows:

$$
\begin{aligned}800-P & ={e}^{-kt-C} \\ 800-P & ={e}^{-C}{e}^{-kt} \\ 800-P & =K{e}^{-kt} \\ P & =800-K{e}^{-kt}\end{aligned}
$$

Note that $K={e}^{-C}$ is a constant of integration.

We're told that, on day $3,$ the number of users was $620.$ So, applying the condition $P(3)=620,$ we have

$$
\begin{aligned}P(3) & =620 \\ 800-K{e}^{-3k} & =620 \\ K{e}^{-3k} & =180.\end{aligned}
$$

We're also told that, on day $9,$ the number of users was $720.$ So, applying the condition $P(9)=720,$ we get

$$
\begin{aligned}P(9) & =720 \\ 800-K{e}^{-9k} & =720 \\ K{e}^{-9k} & =80.\end{aligned}
$$

Then, by dividing the result of the first condition by the result of the second, we can solve for $k:$

$$
\begin{aligned}\frac{K{e}^{-3k}}{K{e}^{-9k}} & =\frac{180}{80} \\ {e}^{6k} & =\frac{9}{4} \\ 6k & =\operatorname{ln}⁡(\frac{9}{4}) \\ k & =\frac{1}{6}\operatorname{ln}⁡(\frac{9}{4})\end{aligned}
$$

Now, substituting back into the result of the first condition, we solve for $K:$

$$
\begin{aligned}K{e}^{-3\cdot (1/6)\operatorname{ln}⁡(9/4)} & =180 \\ K & =180{e}^{(1/2)\operatorname{ln}⁡(9/4)} \\ K & =180\sqrt{\frac{9}{4}} \\ K & =180\cdot \frac{3}{2} \\ K & =270\end{aligned}
$$

Therefore, we have the following expression for $P(t):$

$$
P(t)=800-270{e}^{-(t/6)\operatorname{ln}⁡(9/4)}.
$$

Finally, let $d$  be the day when the app reaches $760$ users. Then, we have

$$
\begin{aligned}P(d) & =760 \\ 800-270{e}^{-kd} & =760 \\ 40 & =270{e}^{-kd} \\ {e}^{-kd} & =\frac{40}{270} \\ {e}^{-kd} & =\frac{4}{27} \\ -kd & =\operatorname{ln}⁡(\frac{4}{27}) \\ d & =-\frac{1}{k}\operatorname{ln}⁡(\frac{4}{27}).\end{aligned}
$$

Substituting in our value for $k,$ we conclude that the number of users will be $760$ on day

$$
d=\frac{-\operatorname{ln}⁡(\frac{4}{27})}{\frac{1}{6}\operatorname{ln}⁡(\frac{9}{4})}=14.1285…≈14,
$$

rounded to the nearest day.

## generated variant; observed empirical unknown intent q-335619 0

### Generated record

A national park is monitoring the number of people who have downloaded a new park app. The system can support a maximum of $3200$ users, but the total is still below this limit. Since the park began tracking downloads, the number of users reached $2480$ on day $6$ and $2880$ on day $18.$ On what day will the number of users reach $3040?$ Round your answer to the nearest integer.

*Hint: You may assume that the number of users, $P(t),$ increases at a rate that obeys an inhibited growth model, where $t$ is the time, in days.*

- $24\text{th}$ day
- $40\text{th}$ day
- $50\text{th}$ day
- $28\text{th}$ day **correct**
- $20\text{th}$ day

The rate at which the number of app users $P(t)$ changes is proportional to the difference between the maximum population and its current population. Therefore, we have the inhibited growth equation

$$
\frac{dP}{dt}=k(a-P),
$$

where $a$ is the maximum number of users the system can support, and $k>0$ is a constant of proportionality.

In our case, $a=3200$ users, and we have

$$
\frac{dP}{dt}=k(3200-P).
$$

First, we integrate our differential equation by separating the variables:

$$
\begin{aligned}\frac{dP}{3200-P} & =k\,dt \\ \int \frac{dP}{3200-P} & =\int k\,\text{d}t \\ -\operatorname{ln}⁡|3200-P| & =kt+C\end{aligned}
$$

Since this is the solution to an inhibited growth equation, we have $3200-P>0$ for all $t\ge 0.$ Next, we solve for $P(t),$ as follows:

$$
\begin{aligned}3200-P & ={e}^{-kt-C} \\ 3200-P & ={e}^{-C}{e}^{-kt} \\ 3200-P & =K{e}^{-kt} \\ P & =3200-K{e}^{-kt}\end{aligned}
$$

Note that $K={e}^{-C}$ is a constant of integration.

We're told that, on day $6,$ the number of users was $2480.$ So, applying the condition $P(6)=2480,$ we have

$$
\begin{aligned}P(6) & =2480 \\ 3200-K{e}^{-6k} & =2480 \\ K{e}^{-6k} & =720.\end{aligned}
$$

We're also told that, on day $18,$ the number of users was $2880.$ So, applying the condition $P(18)=2880,$ we get

$$
\begin{aligned}P(18) & =2880 \\ 3200-K{e}^{-18k} & =2880 \\ K{e}^{-18k} & =320.\end{aligned}
$$

Then, by dividing the result of the first condition by the result of the second, we can solve for $k:$

$$
\begin{aligned}\frac{K{e}^{-6k}}{K{e}^{-18k}} & =\frac{720}{320} \\ {e}^{12k} & =\frac{9}{4} \\ 12k & =\operatorname{ln}⁡(\frac{9}{4}) \\ k & =\frac{1}{12}\operatorname{ln}⁡(\frac{9}{4})\end{aligned}
$$

Now, substituting back into the result of the first condition, we solve for $K:$

$$
\begin{aligned}K{e}^{-6\cdot (1/12)\operatorname{ln}⁡(9/4)} & =720 \\ K & =720{e}^{(1/2)\operatorname{ln}⁡(9/4)} \\ K & =720\sqrt{\frac{9}{4}} \\ K & =720\cdot \frac{3}{2} \\ K & =1080\end{aligned}
$$

Therefore, we have the following expression for $P(t):$

$$
P(t)=3200-1080{e}^{-(t/12)\operatorname{ln}⁡(9/4)}.
$$

Finally, let $d$  be the day when the app reaches $3040$ users. Then, we have

$$
\begin{aligned}P(d) & =3040 \\ 3200-1080{e}^{-kd} & =3040 \\ 160 & =1080{e}^{-kd} \\ {e}^{-kd} & =\frac{160}{1080} \\ {e}^{-kd} & =\frac{4}{27} \\ -kd & =\operatorname{ln}⁡(\frac{4}{27}) \\ d & =-\frac{1}{k}\operatorname{ln}⁡(\frac{4}{27}).\end{aligned}
$$

Substituting in our value for $k,$ we conclude that the number of users will be $3040$ on day

$$
d=\frac{-\operatorname{ln}⁡(\frac{4}{27})}{\frac{1}{12}\operatorname{ln}⁡(\frac{9}{4})}=28.2570…≈28,
$$

rounded to the nearest day.

## generated variant; observed empirical unknown intent q-335619 1

### Generated record

A national park is monitoring the number of people who have downloaded a new park app. The system can support a maximum of $1600$ users, but the total is still below this limit. Since the park began tracking downloads, the number of users reached $1240$ on day $6$ and $1440$ on day $18.$ On what day will the number of users reach $1520?$ Round your answer to the nearest integer.

*Hint: You may assume that the number of users, $P(t),$ increases at a rate that obeys an inhibited growth model, where $t$ is the time, in days.*

- $20\text{th}$ day
- $40\text{th}$ day
- $24\text{th}$ day
- $28\text{th}$ day **correct**
- $50\text{th}$ day

The rate at which the number of app users $P(t)$ changes is proportional to the difference between the maximum population and its current population. Therefore, we have the inhibited growth equation

$$
\frac{dP}{dt}=k(a-P),
$$

where $a$ is the maximum number of users the system can support, and $k>0$ is a constant of proportionality.

In our case, $a=1600$ users, and we have

$$
\frac{dP}{dt}=k(1600-P).
$$

First, we integrate our differential equation by separating the variables:

$$
\begin{aligned}\frac{dP}{1600-P} & =k\,dt \\ \int \frac{dP}{1600-P} & =\int k\,\text{d}t \\ -\operatorname{ln}⁡|1600-P| & =kt+C\end{aligned}
$$

Since this is the solution to an inhibited growth equation, we have $1600-P>0$ for all $t\ge 0.$ Next, we solve for $P(t),$ as follows:

$$
\begin{aligned}1600-P & ={e}^{-kt-C} \\ 1600-P & ={e}^{-C}{e}^{-kt} \\ 1600-P & =K{e}^{-kt} \\ P & =1600-K{e}^{-kt}\end{aligned}
$$

Note that $K={e}^{-C}$ is a constant of integration.

We're told that, on day $6,$ the number of users was $1240.$ So, applying the condition $P(6)=1240,$ we have

$$
\begin{aligned}P(6) & =1240 \\ 1600-K{e}^{-6k} & =1240 \\ K{e}^{-6k} & =360.\end{aligned}
$$

We're also told that, on day $18,$ the number of users was $1440.$ So, applying the condition $P(18)=1440,$ we get

$$
\begin{aligned}P(18) & =1440 \\ 1600-K{e}^{-18k} & =1440 \\ K{e}^{-18k} & =160.\end{aligned}
$$

Then, by dividing the result of the first condition by the result of the second, we can solve for $k:$

$$
\begin{aligned}\frac{K{e}^{-6k}}{K{e}^{-18k}} & =\frac{360}{160} \\ {e}^{12k} & =\frac{9}{4} \\ 12k & =\operatorname{ln}⁡(\frac{9}{4}) \\ k & =\frac{1}{12}\operatorname{ln}⁡(\frac{9}{4})\end{aligned}
$$

Now, substituting back into the result of the first condition, we solve for $K:$

$$
\begin{aligned}K{e}^{-6\cdot (1/12)\operatorname{ln}⁡(9/4)} & =360 \\ K & =360{e}^{(1/2)\operatorname{ln}⁡(9/4)} \\ K & =360\sqrt{\frac{9}{4}} \\ K & =360\cdot \frac{3}{2} \\ K & =540\end{aligned}
$$

Therefore, we have the following expression for $P(t):$

$$
P(t)=1600-540{e}^{-(t/12)\operatorname{ln}⁡(9/4)}.
$$

Finally, let $d$  be the day when the app reaches $1520$ users. Then, we have

$$
\begin{aligned}P(d) & =1520 \\ 1600-540{e}^{-kd} & =1520 \\ 80 & =540{e}^{-kd} \\ {e}^{-kd} & =\frac{80}{540} \\ {e}^{-kd} & =\frac{4}{27} \\ -kd & =\operatorname{ln}⁡(\frac{4}{27}) \\ d & =-\frac{1}{k}\operatorname{ln}⁡(\frac{4}{27}).\end{aligned}
$$

Substituting in our value for $k,$ we conclude that the number of users will be $1520$ on day

$$
d=\frac{-\operatorname{ln}⁡(\frac{4}{27})}{\frac{1}{12}\operatorname{ln}⁡(\frac{9}{4})}=28.2570…≈28,
$$

rounded to the nearest day.

## generated variant; authored operation bank q-335619 0

### Generated record

A national park is monitoring the number of people who have downloaded a new park app. The system can support a maximum of $700$ users, but the total is still below this limit. Since the park began tracking downloads, the number of users reached $540$ on day $5$ and $660$ on day $15.$ On what day will the number of users reach $690?$ Round your answer to the nearest integer.

*Hint: You may assume that the number of users, $P(t),$ increases at a rate that obeys an inhibited growth model, where $t$ is the time, in days.*

- $25\text{th}$ day **correct**
- $7\text{th}$ day
- $2\text{nd}$ day
- $12\text{th}$ day
- $3\text{rd}$ day

The rate at which the number of app users $P(t)$ changes is proportional to the difference between the maximum population and its current population. Therefore, we have the inhibited growth equation

$$
\frac{dP}{dt}=k(a-P),
$$

where $a$ is the maximum number of users the system can support, and $k>0$ is a constant of proportionality.

In our case, $a=700$ users, and we have

$$
\frac{dP}{dt}=k(700-P).
$$

First, we integrate our differential equation by separating the variables:

$$
\begin{aligned}\frac{dP}{700-P} & =k\,dt \\ \int \frac{dP}{700-P} & =\int k\,\text{d}t \\ -\operatorname{ln}⁡|700-P| & =kt+C\end{aligned}
$$

Since this is the solution to an inhibited growth equation, we have $700-P>0$ for all $t\ge 0.$ Next, we solve for $P(t),$ as follows:

$$
\begin{aligned}700-P & ={e}^{-kt-C} \\ 700-P & ={e}^{-C}{e}^{-kt} \\ 700-P & =K{e}^{-kt} \\ P & =700-K{e}^{-kt}\end{aligned}
$$

Note that $K={e}^{-C}$ is a constant of integration.

We're told that, on day $5,$ the number of users was $540.$ So, applying the condition $P(5)=540,$ we have

$$
\begin{aligned}P(5) & =540 \\ 700-K{e}^{-5k} & =540 \\ K{e}^{-5k} & =160.\end{aligned}
$$

We're also told that, on day $15,$ the number of users was $660.$ So, applying the condition $P(15)=660,$ we get

$$
\begin{aligned}P(15) & =660 \\ 700-K{e}^{-15k} & =660 \\ K{e}^{-15k} & =40.\end{aligned}
$$

Then, by dividing the result of the first condition by the result of the second, we can solve for $k:$

$$
\begin{aligned}\frac{K{e}^{-5k}}{K{e}^{-15k}} & =\frac{160}{40} \\ {e}^{10k} & =\frac{4}{1} \\ 10k & =\operatorname{ln}⁡(\frac{4}{1}) \\ k & =\frac{1}{10}\operatorname{ln}⁡(\frac{4}{1})\end{aligned}
$$

Now, substituting back into the result of the first condition, we solve for $K:$

$$
\begin{aligned}K{e}^{-5\cdot (1/10)\operatorname{ln}⁡(4)} & =160 \\ K & =160{e}^{(1/2)\operatorname{ln}⁡(4)} \\ K & =160\sqrt{\frac{4}{1}} \\ K & =160\cdot \frac{2}{1} \\ K & =320\end{aligned}
$$

Therefore, we have the following expression for $P(t):$

$$
P(t)=700-320{e}^{-(t/10)\operatorname{ln}⁡(4)}.
$$

Finally, let $d$  be the day when the app reaches $690$ users. Then, we have

$$
\begin{aligned}P(d) & =690 \\ 700-320{e}^{-kd} & =690 \\ 10 & =320{e}^{-kd} \\ {e}^{-kd} & =\frac{10}{320} \\ {e}^{-kd} & =\frac{1}{32} \\ -kd & =\operatorname{ln}⁡(\frac{1}{32}) \\ d & =-\frac{1}{k}\operatorname{ln}⁡(\frac{1}{32}).\end{aligned}
$$

Substituting in our value for $k,$ we conclude that the number of users will be $690$ on day

$$
d=\frac{-\operatorname{ln}⁡(\frac{1}{32})}{\frac{1}{10}\operatorname{ln}⁡(\frac{4}{1})}=25.0000…≈25,
$$

rounded to the nearest day.

## generated variant; authored operation bank q-335619 1

### Generated record

A national park is monitoring the number of people who have downloaded a new park app. The system can support a maximum of $700$ users, but the total is still below this limit. Since the park began tracking downloads, the number of users reached $500$ on day $3$ and $650$ on day $9.$ On what day will the number of users reach $670?$ Round your answer to the nearest integer.

*Hint: You may assume that the number of users, $P(t),$ increases at a rate that obeys an inhibited growth model, where $t$ is the time, in days.*

- $1\text{st}$ day
- $7\text{th}$ day
- $11\text{th}$ day **correct**
- $4\text{th}$ day
- $3\text{rd}$ day

The rate at which the number of app users $P(t)$ changes is proportional to the difference between the maximum population and its current population. Therefore, we have the inhibited growth equation

$$
\frac{dP}{dt}=k(a-P),
$$

where $a$ is the maximum number of users the system can support, and $k>0$ is a constant of proportionality.

In our case, $a=700$ users, and we have

$$
\frac{dP}{dt}=k(700-P).
$$

First, we integrate our differential equation by separating the variables:

$$
\begin{aligned}\frac{dP}{700-P} & =k\,dt \\ \int \frac{dP}{700-P} & =\int k\,\text{d}t \\ -\operatorname{ln}⁡|700-P| & =kt+C\end{aligned}
$$

Since this is the solution to an inhibited growth equation, we have $700-P>0$ for all $t\ge 0.$ Next, we solve for $P(t),$ as follows:

$$
\begin{aligned}700-P & ={e}^{-kt-C} \\ 700-P & ={e}^{-C}{e}^{-kt} \\ 700-P & =K{e}^{-kt} \\ P & =700-K{e}^{-kt}\end{aligned}
$$

Note that $K={e}^{-C}$ is a constant of integration.

We're told that, on day $3,$ the number of users was $500.$ So, applying the condition $P(3)=500,$ we have

$$
\begin{aligned}P(3) & =500 \\ 700-K{e}^{-3k} & =500 \\ K{e}^{-3k} & =200.\end{aligned}
$$

We're also told that, on day $9,$ the number of users was $650.$ So, applying the condition $P(9)=650,$ we get

$$
\begin{aligned}P(9) & =650 \\ 700-K{e}^{-9k} & =650 \\ K{e}^{-9k} & =50.\end{aligned}
$$

Then, by dividing the result of the first condition by the result of the second, we can solve for $k:$

$$
\begin{aligned}\frac{K{e}^{-3k}}{K{e}^{-9k}} & =\frac{200}{50} \\ {e}^{6k} & =\frac{4}{1} \\ 6k & =\operatorname{ln}⁡(\frac{4}{1}) \\ k & =\frac{1}{6}\operatorname{ln}⁡(\frac{4}{1})\end{aligned}
$$

Now, substituting back into the result of the first condition, we solve for $K:$

$$
\begin{aligned}K{e}^{-3\cdot (1/6)\operatorname{ln}⁡(4)} & =200 \\ K & =200{e}^{(1/2)\operatorname{ln}⁡(4)} \\ K & =200\sqrt{\frac{4}{1}} \\ K & =200\cdot \frac{2}{1} \\ K & =400\end{aligned}
$$

Therefore, we have the following expression for $P(t):$

$$
P(t)=700-400{e}^{-(t/6)\operatorname{ln}⁡(4)}.
$$

Finally, let $d$  be the day when the app reaches $670$ users. Then, we have

$$
\begin{aligned}P(d) & =670 \\ 700-400{e}^{-kd} & =670 \\ 30 & =400{e}^{-kd} \\ {e}^{-kd} & =\frac{30}{400} \\ {e}^{-kd} & =\frac{3}{40} \\ -kd & =\operatorname{ln}⁡(\frac{3}{40}) \\ d & =-\frac{1}{k}\operatorname{ln}⁡(\frac{3}{40}).\end{aligned}
$$

Substituting in our value for $k,$ we conclude that the number of users will be $670$ on day

$$
d=\frac{-\operatorname{ln}⁡(\frac{3}{40})}{\frac{1}{6}\operatorname{ln}⁡(\frac{4}{1})}=11.2108…≈11,
$$

rounded to the nearest day.
