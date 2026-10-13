# Original and generated review

Raw source evidence, supported completions and authored variants are labeled separately. Correct choices are marked only where a designation exists.

## ORIGINAL PARAMETERIZED RAW REPLAY q-106691 — unrated

A factory's management noted that the growth of the unit production is directly proportional to the difference between the maximum number of units a factory worker can produce and the current production quantity. Let $P(t)$ be the production quantity, measured in units produced, and let $t \ge 0$ be the time in days. If the maximum number of units that a worker can produce is $70$ $units/day$, which differential equation could be used to model the factory's production? Assume that $k > 0$ is a constant of proportionality.

- $\frac{dP}{dt} =-k(70 + P)$
- $\frac{dP}{dt} =-k(70 - P)$
- $\frac{dP}{dt} = k(70 - P)$
- $\frac{dP}{dt} = kP(70 - P)$
- $\frac{dP}{dt} = kP^{2}(70 - P)$

## GENERATED OBSERVED BANK VARIANT q-106691 — unrated

A factory's management noted that the growth of the unit production is directly proportional to the difference between the maximum number of units a factory worker can produce and the current production quantity. Let $P(t)$ be the production quantity, measured in units produced, and let $t \ge 0$ be the time in days. If the maximum number of units that a worker can produce is $140$ $units/day$, which differential equation could be used to model the factory's production? Assume that $k > 0$ is a constant of proportionality.

- $\frac{dP}{dt} = kP(140 - P)$
- $\frac{dP}{dt} =-k(140 - P)$
- $\frac{dP}{dt} = k(140 - P)$
- $\frac{dP}{dt} =-k(140 + P)$
- $\frac{dP}{dt} = kP^{2}(140 - P)$

## GENERATED SUPPORTED PRESENTATION/FIELD COMPLETION q-106691 — easy

A factory's management noted that the growth of the unit production is directly proportional to the difference between the maximum number of units a factory worker can produce and the current production quantity. Let $P(t)$ be the production quantity, measured in units produced, and let $t \ge 0$ be the time in days. If the maximum number of units that a worker can produce is $70$ $units$, which differential equation could be used to model the factory's production? Assume that $k > 0$ is a constant of proportionality.

- $\frac{dP}{dt} =-k(70 + P)$
- $\frac{dP}{dt} =-k(70 - P)$
- $\frac{dP}{dt} = kP(70 - P)$
- $\frac{dP}{dt} = kP^{2}(70 - P)$
- $\frac{dP}{dt} = k(70 - P)$ **Correct**

Worked solution:
The rate of change is proportional to the gap between the maximum quantity and the current quantity. Therefore,

$$
\frac{\text{d}P}{\text{d}t}=k(a-P),
$$

where $a$ is the maximum quantity and $k>0$.

Here $a=70$, so

$$
\frac{\text{d}P}{\text{d}t}=k(70-P).
$$

## ORIGINAL PARAMETERIZED RAW REPLAY q-37376 — unrated

A rehabilitation center initially has $20$ children. The number of children in the center $R(t)$ increases at a rate that obeys an inhibited growth model, where $t \ge 0$ is the time in months. If the maximum capacity of the center is $85$ children, which differential equation could be used to model the population of the rehabilitation center? Assume that $k > 0$ is a constant of proportionality.

- $\frac{dR}{dt} = k(85 - R)$
- $\frac{dR}{dt} = k(105 - R)$
- $\frac{dR}{dt} = k(55 - R)$
- $\frac{dR}{dt} = k(1700 - R)$
- $\frac{dR}{dt} = k(65 - R)$

## GENERATED OBSERVED BANK VARIANT q-37376 — unrated

A rehabilitation center initially has $40$ children. The number of children in the center $R(t)$ increases at a rate that obeys an inhibited growth model, where $t \ge 0$ is the time in months. If the maximum capacity of the center is $170$ children, which differential equation could be used to model the population of the rehabilitation center? Assume that $k > 0$ is a constant of proportionality.

- $\frac{dR}{dt} = k(3400 - R)$
- $\frac{dR}{dt} = k(210 - R)$
- $\frac{dR}{dt} = k(110 - R)$
- $\frac{dR}{dt} = k(170 - R)$
- $\frac{dR}{dt} = k(130 - R)$

## GENERATED SUPPORTED PRESENTATION/FIELD COMPLETION q-37376 — easy

A rehabilitation center initially has $20$ children. The number of children in the center $R(t)$ increases at a rate that obeys an inhibited growth model, where $t \ge 0$ is the time in months. If the maximum capacity of the center is $85$ children, which differential equation could be used to model the population of the rehabilitation center? Assume that $k > 0$ is a constant of proportionality.

- $\frac{dR}{dt} = k(85 - R)$ **Correct**
- $\frac{dR}{dt} = k(105 - R)$
- $\frac{dR}{dt} = k(1700 - R)$
- $\frac{dR}{dt} = k(65 - R)$
- $\frac{dR}{dt} = k(55 - R)$

Worked solution:
The rate of change is proportional to the gap between the maximum quantity and the current quantity. Therefore,

$$
\frac{\text{d}R}{\text{d}t}=k(a-R),
$$

where $a$ is the maximum quantity and $k>0$.

Here $a=85$, so

$$
\frac{\text{d}R}{\text{d}t}=k(85-R).
$$

## ORIGINAL PARAMETERIZED RAW REPLAY q-335135 — easy

A wildlife manager noted that the growth of the number of deer in a protected forest is directly proportional to the difference between the forest’s maximum deer population and the current population. Let $N(t)$ be the deer population, measured in number of deer, and let $t\ge 0$ be the time in years. If the maximum deer population that the forest can support is $150$ deer, which differential equation could be used to model the forest’s deer population? Assume that $k>0$ is a constant of proportionality.

- $\frac{\text{d}N}{\text{d}t}=kN(150-N)$
- $\frac{\text{d}N}{\text{d}t}=-k(150-N)$
- $\frac{\text{d}N}{\text{d}t}=k(150-N)$ **Correct**
- $\frac{\text{d}N}{\text{d}t}=k{N}^{2}(150-N)$
- $\frac{\text{d}N}{\text{d}t}=-k(150+N)$

Worked solution:
The rate at which the deer population $N(t)$ of the forest changes is proportional to the difference between the maximum deer population the forest can support and the current deer population. Therefore, we have the differential equation

$$
\frac{\text{d}N}{\text{d}t}=k(a-N),
$$

where $a$ is the maximum deer population the forest can support, and $k>0$ is a constant of proportionality.

In our case, $a=150\text{ deer},$ and we have

$$
\frac{\text{d}N}{\text{d}t}=k(150-N).
$$

## GENERATED OBSERVED BANK VARIANT q-335135 — easy

A wildlife manager noted that the growth of the number of deer in a protected forest is directly proportional to the difference between the forest’s maximum deer population and the current population. Let $N(t)$ be the deer population, measured in number of deer, and let $t\ge 0$ be the time in years. If the maximum deer population that the forest can support is $300$ deer, which differential equation could be used to model the forest’s deer population? Assume that $k>0$ is a constant of proportionality.

- $\frac{\text{d}N}{\text{d}t}=k{N}^{2}(300-N)$
- $\frac{\text{d}N}{\text{d}t}=-k(300-N)$
- $\frac{\text{d}N}{\text{d}t}=k(300-N)$ **Correct**
- $\frac{\text{d}N}{\text{d}t}=kN(300-N)$
- $\frac{\text{d}N}{\text{d}t}=-k(300+N)$

Worked solution:
The rate at which the deer population $N(t)$ of the forest changes is proportional to the difference between the maximum deer population the forest can support and the current deer population. Therefore, we have the differential equation

$$
\frac{\text{d}N}{\text{d}t}=k(a-N),
$$

where $a$ is the maximum deer population the forest can support, and $k>0$ is a constant of proportionality.

In our case, $a=300\text{ deer},$ and we have

$$
\frac{\text{d}N}{\text{d}t}=k(300-N).
$$

## GENERATED SUPPORTED PRESENTATION/FIELD COMPLETION q-335135 — easy

A wildlife manager noted that the growth of the number of deer in a protected forest is directly proportional to the difference between the forest’s maximum deer population and the current population. Let $N(t)$ be the deer population, measured in number of deer, and let $t\ge 0$ be the time in years. If the maximum deer population that the forest can support is $150$ deer, which differential equation could be used to model the forest’s deer population? Assume that $k>0$ is a constant of proportionality.

- $\frac{\text{d}N}{\text{d}t}=kN(150-N)$
- $\frac{\text{d}N}{\text{d}t}=-k(150-N)$
- $\frac{\text{d}N}{\text{d}t}=k{N}^{2}(150-N)$
- $\frac{\text{d}N}{\text{d}t}=-k(150+N)$
- $\frac{\text{d}N}{\text{d}t}=k(150-N)$ **Correct**

Worked solution:
The rate at which the deer population $N(t)$ of the forest changes is proportional to the difference between the maximum deer population the forest can support and the current deer population. Therefore, we have the differential equation

$$
\frac{\text{d}N}{\text{d}t}=k(a-N),
$$

where $a$ is the maximum deer population the forest can support, and $k>0$ is a constant of proportionality.

In our case, $a=150\text{ deer},$ and we have

$$
\frac{\text{d}N}{\text{d}t}=k(150-N).
$$

## ORIGINAL PARAMETERIZED RAW REPLAY q-335142 — easy

A tutoring center currently has $10$ enrolled students. The number of students in the center $T(t)$ increases at a rate that obeys an inhibited growth model, where $t\ge 0$ is the time in months. If the maximum capacity of the tutoring center is $95$ students, which differential equation could be used to model the student population of the center? Assume that $k>0$ is a constant of proportionality.

- $\frac{dT}{dt}=k(950-T)$
- $\frac{dT}{dt}=k(95-T)$ **Correct**
- $\frac{dT}{dt}=k(100-T)$
- $\frac{dT}{dt}=k(30-T)$
- $\frac{dT}{dt}=k(60-T)$

Worked solution:
Since the number of students in the center obeys an inhibited growth model, the rate at which the number of students changes is proportional to the difference between the maximum capacity and the number of students in the center. Therefore, we have the differential equation

$$
\frac{\text{d}T}{\text{d}t}=k(a-T),
$$

where $a$ is the maximum capacity of the tutoring center, and $k>0$ is a constant of proportionality.

In our case, $a=95$ students, and we have

$$
\frac{\text{d}T}{\text{d}t}=k(95-T).
$$

## GENERATED OBSERVED BANK VARIANT q-335142 — easy

A tutoring center currently has $20$ enrolled students. The number of students in the center $T(t)$ increases at a rate that obeys an inhibited growth model, where $t\ge 0$ is the time in months. If the maximum capacity of the tutoring center is $190$ students, which differential equation could be used to model the student population of the center? Assume that $k>0$ is a constant of proportionality.

- $\frac{dT}{dt}=k(60-T)$
- $\frac{dT}{dt}=k(190-T)$ **Correct**
- $\frac{dT}{dt}=k(200-T)$
- $\frac{dT}{dt}=k(1900-T)$
- $\frac{dT}{dt}=k(120-T)$

Worked solution:
Since the number of students in the center obeys an inhibited growth model, the rate at which the number of students changes is proportional to the difference between the maximum capacity and the number of students in the center. Therefore, we have the differential equation

$$
\frac{\text{d}T}{\text{d}t}=k(a-T),
$$

where $a$ is the maximum capacity of the tutoring center, and $k>0$ is a constant of proportionality.

In our case, $a=190$ students, and we have

$$
\frac{\text{d}T}{\text{d}t}=k(190-T).
$$

## GENERATED SUPPORTED PRESENTATION/FIELD COMPLETION q-335142 — easy

A tutoring center currently has $10$ enrolled students. The number of students in the center $T(t)$ increases at a rate that obeys an inhibited growth model, where $t\ge 0$ is the time in months. If the maximum capacity of the tutoring center is $95$ students, which differential equation could be used to model the student population of the center? Assume that $k>0$ is a constant of proportionality.

- $\frac{dT}{dt}=k(950-T)$
- $\frac{dT}{dt}=k(95-T)$ **Correct**
- $\frac{dT}{dt}=k(30-T)$
- $\frac{dT}{dt}=k(60-T)$
- $\frac{dT}{dt}=k(100-T)$

Worked solution:
Since the number of students in the center obeys an inhibited growth model, the rate at which the number of students changes is proportional to the difference between the maximum capacity and the number of students in the center. Therefore, we have the differential equation

$$
\frac{\text{d}T}{\text{d}t}=k(a-T),
$$

where $a$ is the maximum capacity of the tutoring center, and $k>0$ is a constant of proportionality.

In our case, $a=95$ students, and we have

$$
\frac{\text{d}T}{\text{d}t}=k(95-T).
$$

## ORIGINAL PARAMETERIZED RAW REPLAY q-335145 — easy

A marine rehabilitation aquarium initially houses $25$ marine animals. The number of animals in the aquarium $M(t)$ increases at a rate that obeys an inhibited growth model, where $t\ge 0$ is the time in months. If the maximum capacity of the aquarium is $60$ animals, which differential equation could be used to model the animal population? Assume that $k>0$ is a constant of proportionality.

- $\frac{dM}{dt}=k(50-M)$
- $\frac{dM}{dt}=k(35-M)$
- $\frac{dM}{dt}=k(250-M)$
- $\frac{dM}{dt}=k(60-M)$ **Correct**
- $\frac{dM}{dt}=k(150-M)$

Worked solution:
Since the number of animals in the aquarium obeys an inhibited growth model, the rate at which the number of animals changes is proportional to the difference between the maximum capacity and the number of animals in the aquarium. Therefore, we have the differential equation

$$
\frac{\text{d}M}{\text{d}t}=k(a-M),
$$

where $a$ is the maximum capacity of the aquarium, and $k>0$ is a constant of proportionality.

In our case, $a=60$ animals, and we have

$$
\frac{\text{d}M}{\text{d}t}=k(60-M).
$$

## GENERATED OBSERVED BANK VARIANT q-335145 — easy

A marine rehabilitation aquarium initially houses $50$ marine animals. The number of animals in the aquarium $M(t)$ increases at a rate that obeys an inhibited growth model, where $t\ge 0$ is the time in months. If the maximum capacity of the aquarium is $120$ animals, which differential equation could be used to model the animal population? Assume that $k>0$ is a constant of proportionality.

- $\frac{dM}{dt}=k(120-M)$ **Correct**
- $\frac{dM}{dt}=k(70-M)$
- $\frac{dM}{dt}=k(500-M)$
- $\frac{dM}{dt}=k(100-M)$
- $\frac{dM}{dt}=k(300-M)$

Worked solution:
Since the number of animals in the aquarium obeys an inhibited growth model, the rate at which the number of animals changes is proportional to the difference between the maximum capacity and the number of animals in the aquarium. Therefore, we have the differential equation

$$
\frac{\text{d}M}{\text{d}t}=k(a-M),
$$

where $a$ is the maximum capacity of the aquarium, and $k>0$ is a constant of proportionality.

In our case, $a=120$ animals, and we have

$$
\frac{\text{d}M}{\text{d}t}=k(120-M).
$$

## GENERATED SUPPORTED PRESENTATION/FIELD COMPLETION q-335145 — easy

A marine rehabilitation aquarium initially houses $25$ marine animals. The number of animals in the aquarium $M(t)$ increases at a rate that obeys an inhibited growth model, where $t\ge 0$ is the time in months. If the maximum capacity of the aquarium is $60$ animals, which differential equation could be used to model the animal population? Assume that $k>0$ is a constant of proportionality.

- $\frac{dM}{dt}=k(50-M)$
- $\frac{dM}{dt}=k(35-M)$
- $\frac{dM}{dt}=k(60-M)$ **Correct**
- $\frac{dM}{dt}=k(150-M)$
- $\frac{dM}{dt}=k(250-M)$

Worked solution:
Since the number of animals in the aquarium obeys an inhibited growth model, the rate at which the number of animals changes is proportional to the difference between the maximum capacity and the number of animals in the aquarium. Therefore, we have the differential equation

$$
\frac{\text{d}M}{\text{d}t}=k(a-M),
$$

where $a$ is the maximum capacity of the aquarium, and $k>0$ is a constant of proportionality.

In our case, $a=60$ animals, and we have

$$
\frac{\text{d}M}{\text{d}t}=k(60-M).
$$

## ORIGINAL PARAMETERIZED RAW REPLAY q-344214 — easy

An ecologist found that the growth of the number of frogs in a wetland is directly proportional to the difference between the wetland’s maximum frog population and the current population. Let $F(t)$ be the frog population, measured in number of frogs, and let $t\ge 0$ be the time in years. If the maximum frog population the wetland can support is $100$ frogs, which differential equation could be used to model the frog population? Assume that $k>0$ is a constant of proportionality.

- $\frac{\text{d}F}{\text{d}t}=-k(100+F)$
- $\frac{\text{d}F}{\text{d}t}=-k(100-F)$
- $\frac{\text{d}F}{\text{d}t}=k(100-F)$ **Correct**
- $\frac{\text{d}F}{\text{d}t}=k{F}^{2}(100-F)$
- $\frac{\text{d}F}{\text{d}t}=kF(100-F)$

Worked solution:
The rate at which the frog population $F(t)$ of the wetland changes is proportional to the difference between the maximum frog population the wetland can support and the current frog population. Therefore, we have the differential equation

$$
\frac{\text{d}F}{\text{d}t}=k(a-F),
$$

where $a$ is the maximum frog population the wetland can support, and $k>0$ is a constant of proportionality.

In our case, $a=100\text{ frogs},$ and we have

$$
\frac{\text{d}F}{\text{d}t}=k(100-F).
$$

## GENERATED OBSERVED BANK VARIANT q-344214 — easy

An ecologist found that the growth of the number of frogs in a wetland is directly proportional to the difference between the wetland’s maximum frog population and the current population. Let $F(t)$ be the frog population, measured in number of frogs, and let $t\ge 0$ be the time in years. If the maximum frog population the wetland can support is $200$ frogs, which differential equation could be used to model the frog population? Assume that $k>0$ is a constant of proportionality.

- $\frac{\text{d}F}{\text{d}t}=k{F}^{2}(200-F)$
- $\frac{\text{d}F}{\text{d}t}=-k(200-F)$
- $\frac{\text{d}F}{\text{d}t}=k(200-F)$ **Correct**
- $\frac{\text{d}F}{\text{d}t}=-k(200+F)$
- $\frac{\text{d}F}{\text{d}t}=kF(200-F)$

Worked solution:
The rate at which the frog population $F(t)$ of the wetland changes is proportional to the difference between the maximum frog population the wetland can support and the current frog population. Therefore, we have the differential equation

$$
\frac{\text{d}F}{\text{d}t}=k(a-F),
$$

where $a$ is the maximum frog population the wetland can support, and $k>0$ is a constant of proportionality.

In our case, $a=200\text{ frogs},$ and we have

$$
\frac{\text{d}F}{\text{d}t}=k(200-F).
$$

## GENERATED SUPPORTED PRESENTATION/FIELD COMPLETION q-344214 — easy

An ecologist found that the growth of the number of frogs in a wetland is directly proportional to the difference between the wetland’s maximum frog population and the current population. Let $F(t)$ be the frog population, measured in number of frogs, and let $t\ge 0$ be the time in years. If the maximum frog population the wetland can support is $100$ frogs, which differential equation could be used to model the frog population? Assume that $k>0$ is a constant of proportionality.

- $\frac{\text{d}F}{\text{d}t}=-k(100+F)$
- $\frac{\text{d}F}{\text{d}t}=-k(100-F)$
- $\frac{\text{d}F}{\text{d}t}=k{F}^{2}(100-F)$
- $\frac{\text{d}F}{\text{d}t}=kF(100-F)$
- $\frac{\text{d}F}{\text{d}t}=k(100-F)$ **Correct**

Worked solution:
The rate at which the frog population $F(t)$ of the wetland changes is proportional to the difference between the maximum frog population the wetland can support and the current frog population. Therefore, we have the differential equation

$$
\frac{\text{d}F}{\text{d}t}=k(a-F),
$$

where $a$ is the maximum frog population the wetland can support, and $k>0$ is a constant of proportionality.

In our case, $a=100\text{ frogs},$ and we have

$$
\frac{\text{d}F}{\text{d}t}=k(100-F).
$$

## ORIGINAL PARAMETERIZED RAW REPLAY q-344218 — easy

A school administrator observed that the growth of the number of students enrolled in a program is directly proportional to the difference between the program’s maximum enrollment capacity and the current number of students enrolled. Let $S(t)$ be the number of students enrolled, measured in students, and let $t\ge 0$ be the time in years. If the maximum number of students the program can support is $500$ students, which differential equation could be used to model the number of students enrolled in the program? Assume that $k>0$ is a constant of proportionality.

- $\frac{\text{d}S}{\text{d}t}=-k(500+S)$
- $\frac{\text{d}S}{\text{d}t}=k(500-S)$ **Correct**
- $\frac{\text{d}S}{\text{d}t}=-k(500-S)$
- $\frac{\text{d}S}{\text{d}t}=kS(500-S)$
- $\frac{\text{d}S}{\text{d}t}=k{S}^{2}(500-S)$

Worked solution:
The rate at which the number of students enrolled $S(t)$ in the program changes is proportional to the difference between the maximum number of students the program can support and the current number of students enrolled. Therefore, we have the differential equation

$$
\frac{\text{d}S}{\text{d}t}=k(a-S),
$$

where $a$ is the maximum number of students the program can support, and $k>0$ is a constant of proportionality.

In our case, $a=500\text{ students},$ and we have

$$
\frac{\text{d}S}{\text{d}t}=k(500-S).
$$

## GENERATED OBSERVED BANK VARIANT q-344218 — easy

A school administrator observed that the growth of the number of students enrolled in a program is directly proportional to the difference between the program’s maximum enrollment capacity and the current number of students enrolled. Let $S(t)$ be the number of students enrolled, measured in students, and let $t\ge 0$ be the time in years. If the maximum number of students the program can support is $1000$ students, which differential equation could be used to model the number of students enrolled in the program? Assume that $k>0$ is a constant of proportionality.

- $\frac{\text{d}S}{\text{d}t}=kS(1000-S)$
- $\frac{\text{d}S}{\text{d}t}=k(1000-S)$ **Correct**
- $\frac{\text{d}S}{\text{d}t}=-k(1000-S)$
- $\frac{\text{d}S}{\text{d}t}=-k(1000+S)$
- $\frac{\text{d}S}{\text{d}t}=k{S}^{2}(1000-S)$

Worked solution:
The rate at which the number of students enrolled $S(t)$ in the program changes is proportional to the difference between the maximum number of students the program can support and the current number of students enrolled. Therefore, we have the differential equation

$$
\frac{\text{d}S}{\text{d}t}=k(a-S),
$$

where $a$ is the maximum number of students the program can support, and $k>0$ is a constant of proportionality.

In our case, $a=1000\text{ students},$ and we have

$$
\frac{\text{d}S}{\text{d}t}=k(1000-S).
$$

## GENERATED SUPPORTED PRESENTATION/FIELD COMPLETION q-344218 — easy

A school administrator observed that the growth of the number of students enrolled in a program is directly proportional to the difference between the program’s maximum enrollment capacity and the current number of students enrolled. Let $S(t)$ be the number of students enrolled, measured in students, and let $t\ge 0$ be the time in years. If the maximum number of students the program can support is $500$ students, which differential equation could be used to model the number of students enrolled in the program? Assume that $k>0$ is a constant of proportionality.

- $\frac{\text{d}S}{\text{d}t}=-k(500+S)$
- $\frac{\text{d}S}{\text{d}t}=k(500-S)$ **Correct**
- $\frac{\text{d}S}{\text{d}t}=kS(500-S)$
- $\frac{\text{d}S}{\text{d}t}=k{S}^{2}(500-S)$
- $\frac{\text{d}S}{\text{d}t}=-k(500-S)$

Worked solution:
The rate at which the number of students enrolled $S(t)$ in the program changes is proportional to the difference between the maximum number of students the program can support and the current number of students enrolled. Therefore, we have the differential equation

$$
\frac{\text{d}S}{\text{d}t}=k(a-S),
$$

where $a$ is the maximum number of students the program can support, and $k>0$ is a constant of proportionality.

In our case, $a=500\text{ students},$ and we have

$$
\frac{\text{d}S}{\text{d}t}=k(500-S).
$$

## ORIGINAL PARAMETERIZED RAW REPLAY q-344219 — easy

An engineer observed that the growth of the number of solar panels installed at a facility is directly proportional to the difference between the facility’s maximum number of solar panels and the current number installed. Let $P(t)$ be the number of solar panels, measured in panels, and let $t\ge 0$ be the time in years. If the maximum number of solar panels the facility can support is $240$ panels, which differential equation could be used to model the number of solar panels installed? Assume that $k>0$ is a constant of proportionality.

- $\frac{\text{d}P}{\text{d}t}=-k(240+P)$
- $\frac{\text{d}P}{\text{d}t}=k(240-P)$ **Correct**
- $\frac{\text{d}P}{\text{d}t}=k{P}^{2}(240-P)$
- $\frac{\text{d}P}{\text{d}t}=kP(240-P)$
- $\frac{\text{d}P}{\text{d}t}=-k(240-P)$

Worked solution:
The rate at which the number of solar panels $P(t)$ installed changes is proportional to the difference between the maximum number of solar panels the facility can support and the current number of solar panels. Therefore, we have the differential equation

$$
\frac{\text{d}P}{\text{d}t}=k(a-P),
$$

where $a$ is the maximum number of solar panels the facility can support, and $k>0$ is a constant of proportionality.

In our case, $a=240\text{ panels},$ and we have

$$
\frac{\text{d}P}{\text{d}t}=k(240-P).
$$

## GENERATED OBSERVED BANK VARIANT q-344219 — easy

An engineer observed that the growth of the number of solar panels installed at a facility is directly proportional to the difference between the facility’s maximum number of solar panels and the current number installed. Let $P(t)$ be the number of solar panels, measured in panels, and let $t\ge 0$ be the time in years. If the maximum number of solar panels the facility can support is $480$ panels, which differential equation could be used to model the number of solar panels installed? Assume that $k>0$ is a constant of proportionality.

- $\frac{\text{d}P}{\text{d}t}=kP(480-P)$
- $\frac{\text{d}P}{\text{d}t}=k(480-P)$ **Correct**
- $\frac{\text{d}P}{\text{d}t}=k{P}^{2}(480-P)$
- $\frac{\text{d}P}{\text{d}t}=-k(480+P)$
- $\frac{\text{d}P}{\text{d}t}=-k(480-P)$

Worked solution:
The rate at which the number of solar panels $P(t)$ installed changes is proportional to the difference between the maximum number of solar panels the facility can support and the current number of solar panels. Therefore, we have the differential equation

$$
\frac{\text{d}P}{\text{d}t}=k(a-P),
$$

where $a$ is the maximum number of solar panels the facility can support, and $k>0$ is a constant of proportionality.

In our case, $a=480\text{ panels},$ and we have

$$
\frac{\text{d}P}{\text{d}t}=k(480-P).
$$

## GENERATED SUPPORTED PRESENTATION/FIELD COMPLETION q-344219 — easy

An engineer observed that the growth of the number of solar panels installed at a facility is directly proportional to the difference between the facility’s maximum number of solar panels and the current number installed. Let $P(t)$ be the number of solar panels, measured in panels, and let $t\ge 0$ be the time in years. If the maximum number of solar panels the facility can support is $240$ panels, which differential equation could be used to model the number of solar panels installed? Assume that $k>0$ is a constant of proportionality.

- $\frac{\text{d}P}{\text{d}t}=-k(240+P)$
- $\frac{\text{d}P}{\text{d}t}=k(240-P)$ **Correct**
- $\frac{\text{d}P}{\text{d}t}=kP(240-P)$
- $\frac{\text{d}P}{\text{d}t}=-k(240-P)$
- $\frac{\text{d}P}{\text{d}t}=k{P}^{2}(240-P)$

Worked solution:
The rate at which the number of solar panels $P(t)$ installed changes is proportional to the difference between the maximum number of solar panels the facility can support and the current number of solar panels. Therefore, we have the differential equation

$$
\frac{\text{d}P}{\text{d}t}=k(a-P),
$$

where $a$ is the maximum number of solar panels the facility can support, and $k>0$ is a constant of proportionality.

In our case, $a=240\text{ panels},$ and we have

$$
\frac{\text{d}P}{\text{d}t}=k(240-P).
$$

## ORIGINAL PARAMETERIZED RAW REPLAY q-344228 — easy

A laboratory incubator initially contains $18$ bacterial cultures. The number of cultures in the incubator $B(t)$ increases at a rate that obeys an inhibited growth model, where $t\ge 0$ is the time in days. If the maximum capacity of the incubator is $50$ cultures, which differential equation could be used to model the number of cultures? Assume that $k>0$ is a constant of proportionality.

- $\frac{dB}{dt}=k(18-B)$
- $\frac{dB}{dt}=k(80-B)$
- $\frac{dB}{dt}=k(50-B)$ **Correct**
- $\frac{dB}{dt}=k(35-B)$
- $\frac{dB}{dt}=k(25-B)$

Worked solution:
Since the number of cultures in the incubator obeys an inhibited growth model, the rate at which the number of cultures changes is proportional to the difference between the maximum capacity and the number of cultures in the incubator. Therefore, we have the differential equation

$$
\frac{\text{d}B}{\text{d}t}=k(a-B),
$$

where $a$ is the maximum capacity of the incubator, and $k>0$ is a constant of proportionality.

In our case, $a=50$ cultures, and we have

$$
\frac{\text{d}B}{\text{d}t}=k(50-B).
$$

## GENERATED OBSERVED BANK VARIANT q-344228 — easy

A laboratory incubator initially contains $36$ bacterial cultures. The number of cultures in the incubator $B(t)$ increases at a rate that obeys an inhibited growth model, where $t\ge 0$ is the time in days. If the maximum capacity of the incubator is $100$ cultures, which differential equation could be used to model the number of cultures? Assume that $k>0$ is a constant of proportionality.

- $\frac{dB}{dt}=k(70-B)$
- $\frac{dB}{dt}=k(160-B)$
- $\frac{dB}{dt}=k(100-B)$ **Correct**
- $\frac{dB}{dt}=k(36-B)$
- $\frac{dB}{dt}=k(50-B)$

Worked solution:
Since the number of cultures in the incubator obeys an inhibited growth model, the rate at which the number of cultures changes is proportional to the difference between the maximum capacity and the number of cultures in the incubator. Therefore, we have the differential equation

$$
\frac{\text{d}B}{\text{d}t}=k(a-B),
$$

where $a$ is the maximum capacity of the incubator, and $k>0$ is a constant of proportionality.

In our case, $a=100$ cultures, and we have

$$
\frac{\text{d}B}{\text{d}t}=k(100-B).
$$

## GENERATED SUPPORTED PRESENTATION/FIELD COMPLETION q-344228 — easy

A laboratory incubator initially contains $18$ bacterial cultures. The number of cultures in the incubator $B(t)$ increases at a rate that obeys an inhibited growth model, where $t\ge 0$ is the time in days. If the maximum capacity of the incubator is $50$ cultures, which differential equation could be used to model the number of cultures? Assume that $k>0$ is a constant of proportionality.

- $\frac{dB}{dt}=k(18-B)$
- $\frac{dB}{dt}=k(80-B)$
- $\frac{dB}{dt}=k(35-B)$
- $\frac{dB}{dt}=k(25-B)$
- $\frac{dB}{dt}=k(50-B)$ **Correct**

Worked solution:
Since the number of cultures in the incubator obeys an inhibited growth model, the rate at which the number of cultures changes is proportional to the difference between the maximum capacity and the number of cultures in the incubator. Therefore, we have the differential equation

$$
\frac{\text{d}B}{\text{d}t}=k(a-B),
$$

where $a$ is the maximum capacity of the incubator, and $k>0$ is a constant of proportionality.

In our case, $a=50$ cultures, and we have

$$
\frac{\text{d}B}{\text{d}t}=k(50-B).
$$

## ORIGINAL PARAMETERIZED RAW REPLAY q-344233 — easy

A data center initially contains $320$ computers. The number of computers in the data center $C(t)$ increases at a rate that obeys an inhibited growth model, where $t\ge 0$ is the time in months. If the maximum capacity of the data center is $1000$ computers, which differential equation could be used to model the number of computers? Assume that $k>0$ is a constant of proportionality.

- $\frac{dC}{dt}=k(1500-C)$
- $\frac{dC}{dt}=k(320-C)$
- $\frac{dC}{dt}=k(500-C)$
- $\frac{dC}{dt}=k(800-C)$
- $\frac{dC}{dt}=k(1000-C)$ **Correct**

Worked solution:
Since the number of computers in the data center obeys an inhibited growth model, the rate at which the number of computers changes is proportional to the difference between the maximum capacity and the number of computers in the data center. Therefore, we have the differential equation

$$
\frac{\text{d}C}{\text{d}t}=k(a-C),
$$

where $a$ is the maximum capacity of the data center, and $k>0$ is a constant of proportionality.

In our case, $a=1000$ computers, and we have

$$
\frac{\text{d}C}{\text{d}t}=k(1000-C).
$$

## GENERATED OBSERVED BANK VARIANT q-344233 — easy

A data center initially contains $640$ computers. The number of computers in the data center $C(t)$ increases at a rate that obeys an inhibited growth model, where $t\ge 0$ is the time in months. If the maximum capacity of the data center is $2000$ computers, which differential equation could be used to model the number of computers? Assume that $k>0$ is a constant of proportionality.

- $\frac{dC}{dt}=k(1600-C)$
- $\frac{dC}{dt}=k(640-C)$
- $\frac{dC}{dt}=k(1000-C)$
- $\frac{dC}{dt}=k(3000-C)$
- $\frac{dC}{dt}=k(2000-C)$ **Correct**

Worked solution:
Since the number of computers in the data center obeys an inhibited growth model, the rate at which the number of computers changes is proportional to the difference between the maximum capacity and the number of computers in the data center. Therefore, we have the differential equation

$$
\frac{\text{d}C}{\text{d}t}=k(a-C),
$$

where $a$ is the maximum capacity of the data center, and $k>0$ is a constant of proportionality.

In our case, $a=2000$ computers, and we have

$$
\frac{\text{d}C}{\text{d}t}=k(2000-C).
$$

## GENERATED SUPPORTED PRESENTATION/FIELD COMPLETION q-344233 — easy

A data center initially contains $320$ computers. The number of computers in the data center $C(t)$ increases at a rate that obeys an inhibited growth model, where $t\ge 0$ is the time in months. If the maximum capacity of the data center is $1000$ computers, which differential equation could be used to model the number of computers? Assume that $k>0$ is a constant of proportionality.

- $\frac{dC}{dt}=k(1500-C)$
- $\frac{dC}{dt}=k(320-C)$
- $\frac{dC}{dt}=k(800-C)$
- $\frac{dC}{dt}=k(1000-C)$ **Correct**
- $\frac{dC}{dt}=k(500-C)$

Worked solution:
Since the number of computers in the data center obeys an inhibited growth model, the rate at which the number of computers changes is proportional to the difference between the maximum capacity and the number of computers in the data center. Therefore, we have the differential equation

$$
\frac{\text{d}C}{\text{d}t}=k(a-C),
$$

where $a$ is the maximum capacity of the data center, and $k>0$ is a constant of proportionality.

In our case, $a=1000$ computers, and we have

$$
\frac{\text{d}C}{\text{d}t}=k(1000-C).
$$

## ORIGINAL PARAMETERIZED RAW REPLAY q-335137 — easy

A shipping company’s management noted that the growth of a ship’s speed is directly proportional to the difference between the ship’s maximum cruising speed and its current speed. Let $V(t)$ be the speed of the ship, measured in kilometers per hour, and let $t\ge 0$ be the time in hours. If the maximum cruising speed of the ship is $90$ $\text{km/h}$, which differential equation could be used to model the ship’s speed? Assume that $k>0$ is a constant of proportionality.

- $\frac{\text{d}V}{\text{d}t}=k(90-V)$ **Correct**
- $\frac{\text{d}V}{\text{d}t}=-k(90-V)$
- $\frac{\text{d}V}{\text{d}t}=-k(90+V)$
- $\frac{\text{d}V}{\text{d}t}=k{V}^{2}(90-V)$
- $\frac{\text{d}V}{\text{d}t}=kV(90-V)$

Worked solution:
The rate at which the speed $V(t)$ of the ship changes is proportional to the difference between the maximum cruising speed and the current speed. Therefore, we have the differential equation

$$
\frac{\text{d}V}{\text{d}t}=k(a-V),
$$

where $a$ is the maximum cruising speed of the ship, and $k>0$ is a constant of proportionality.

In our case, $a=90\text{ km/h},$ and we have

$$
\frac{\text{d}V}{\text{d}t}=k(90-V).
$$

## GENERATED OBSERVED BANK VARIANT q-335137 — easy

A shipping company’s management noted that the growth of a ship’s speed is directly proportional to the difference between the ship’s maximum cruising speed and its current speed. Let $V(t)$ be the speed of the ship, measured in kilometers per hour, and let $t\ge 0$ be the time in hours. If the maximum cruising speed of the ship is $180$ $\text{km/h}$, which differential equation could be used to model the ship’s speed? Assume that $k>0$ is a constant of proportionality.

- $\frac{\text{d}V}{\text{d}t}=k{V}^{2}(180-V)$
- $\frac{\text{d}V}{\text{d}t}=-k(180-V)$
- $\frac{\text{d}V}{\text{d}t}=-k(180+V)$
- $\frac{\text{d}V}{\text{d}t}=k(180-V)$ **Correct**
- $\frac{\text{d}V}{\text{d}t}=kV(180-V)$

Worked solution:
The rate at which the speed $V(t)$ of the ship changes is proportional to the difference between the maximum cruising speed and the current speed. Therefore, we have the differential equation

$$
\frac{\text{d}V}{\text{d}t}=k(a-V),
$$

where $a$ is the maximum cruising speed of the ship, and $k>0$ is a constant of proportionality.

In our case, $a=180\text{ km/h},$ and we have

$$
\frac{\text{d}V}{\text{d}t}=k(180-V).
$$

## GENERATED SUPPORTED PRESENTATION/FIELD COMPLETION q-335137 — easy

A shipping company’s management noted that the growth of a ship’s speed is directly proportional to the difference between the ship’s maximum cruising speed and its current speed. Let $V(t)$ be the speed of the ship, measured in kilometers per hour, and let $t\ge 0$ be the time in hours. If the maximum cruising speed of the ship is $90$ $\text{km/h}$, which differential equation could be used to model the ship’s speed? Assume that $k>0$ is a constant of proportionality.

- $\frac{\text{d}V}{\text{d}t}=k(90-V)$ **Correct**
- $\frac{\text{d}V}{\text{d}t}=-k(90-V)$
- $\frac{\text{d}V}{\text{d}t}=k{V}^{2}(90-V)$
- $\frac{\text{d}V}{\text{d}t}=kV(90-V)$
- $\frac{\text{d}V}{\text{d}t}=-k(90+V)$

Worked solution:
The rate at which the speed $V(t)$ of the ship changes is proportional to the difference between the maximum cruising speed and the current speed. Therefore, we have the differential equation

$$
\frac{\text{d}V}{\text{d}t}=k(a-V),
$$

where $a$ is the maximum cruising speed of the ship, and $k>0$ is a constant of proportionality.

In our case, $a=90\text{ km/h},$ and we have

$$
\frac{\text{d}V}{\text{d}t}=k(90-V).
$$

## GENERATED AUTHORED EASY seed=0 — easy

The growth of the number of cultures in a laboratory incubator is directly proportional to the difference between its maximum capacity and its current population. Let $B(t)$ be the number of cultures, and let $t\ge 0$ be the time in days. If the maximum capacity is $452$ cultures, which differential equation models this population? Assume that $k>0$ is a constant of proportionality.

- $\frac{\text{d}B}{\text{d}t}=kB(452-B)$
- $\frac{\text{d}B}{\text{d}t}=-k(452-B)$
- $\frac{\text{d}B}{\text{d}t}=k(452-B)$ **Correct**
- $\frac{\text{d}B}{\text{d}t}=-k(452+B)$
- $\frac{\text{d}B}{\text{d}t}=k{B}^{2}(452-B)$

Worked solution:
The rate of change is proportional to the difference between the maximum capacity and the current population. Therefore,

$$
\frac{\text{d}B}{\text{d}t}=k(a-B),
$$

where $a$ is the maximum capacity and $k>0$.

Here $a=452$ cultures, so

$$
\frac{\text{d}B}{\text{d}t}=k(452-B).
$$

## GENERATED AUTHORED EASY seed=1 — easy

The growth of the number of computers in a data center is directly proportional to the difference between its maximum capacity and its current population. Let $C(t)$ be the number of computers, and let $t\ge 0$ be the time in months. If the maximum capacity is $88$ computers, which differential equation models this population? Assume that $k>0$ is a constant of proportionality.

- $\frac{\text{d}C}{\text{d}t}=kC(88-C)$
- $\frac{\text{d}C}{\text{d}t}=k{C}^{2}(88-C)$
- $\frac{\text{d}C}{\text{d}t}=-k(88+C)$
- $\frac{\text{d}C}{\text{d}t}=k(88-C)$ **Correct**
- $\frac{\text{d}C}{\text{d}t}=-k(88-C)$

Worked solution:
The rate of change is proportional to the difference between the maximum capacity and the current population. Therefore,

$$
\frac{\text{d}C}{\text{d}t}=k(a-C),
$$

where $a$ is the maximum capacity and $k>0$.

Here $a=88$ computers, so

$$
\frac{\text{d}C}{\text{d}t}=k(88-C).
$$

## GENERATED AUTHORED EASY seed=2 — easy

The growth of the number of deer in a protected forest is directly proportional to the difference between its maximum capacity and its current population. Let $N(t)$ be the number of deer, and let $t\ge 0$ be the time in years. If the maximum capacity is $461$ deer, which differential equation models this population? Assume that $k>0$ is a constant of proportionality.

- $\frac{\text{d}N}{\text{d}t}=kN(461-N)$
- $\frac{\text{d}N}{\text{d}t}=-k(461-N)$
- $\frac{\text{d}N}{\text{d}t}=k{N}^{2}(461-N)$
- $\frac{\text{d}N}{\text{d}t}=-k(461+N)$
- $\frac{\text{d}N}{\text{d}t}=k(461-N)$ **Correct**

Worked solution:
The rate of change is proportional to the difference between the maximum capacity and the current population. Therefore,

$$
\frac{\text{d}N}{\text{d}t}=k(a-N),
$$

where $a$ is the maximum capacity and $k>0$.

Here $a=461$ deer, so

$$
\frac{\text{d}N}{\text{d}t}=k(461-N).
$$

## GENERATED AUTHORED MODERATE seed=0 — moderate

A laboratory incubator initially contains $21$ cultures, and its maximum capacity is $452$ cultures. Let $B(t)$ be the number of cultures, where $t\ge 0$ is the time in days. Its population obeys an inhibited growth model. The rate of increase equals $5$ times the difference between the maximum capacity and the current population. Which differential equation models this population?

- $\frac{\text{d}B}{\text{d}t}=-5(452-B)$
- $\frac{\text{d}B}{\text{d}t}=(452-B)$
- $\frac{\text{d}B}{\text{d}t}=5(452-B)$ **Correct**
- $\frac{\text{d}B}{\text{d}t}=2260-B$
- $\frac{\text{d}B}{\text{d}t}=5(21-B)$

Worked solution:
The rate at which the number of cultures $B(t)$ in the laboratory incubator changes is proportional to the difference between the maximum capacity and the current number of cultures. Therefore, we have the differential equation

$$
\frac{\text{d}B}{\text{d}t}=k(a-B),
$$

where $a$ is the maximum capacity, and $k>0$ is a constant of proportionality.

In our case, $a=452$ cultures, and $k=5$. Therefore,

$$
\frac{\text{d}B}{\text{d}t}=5(452-B).
$$

## GENERATED AUTHORED MODERATE seed=1 — moderate

A data center initially contains $33$ computers, and its maximum capacity is $88$ computers. Let $C(t)$ be the number of computers, where $t\ge 0$ is the time in months. Its population obeys an inhibited growth model. The rate of increase equals $2$ times the difference between the maximum capacity and the current population. Which differential equation models this population?

- $\frac{\text{d}C}{\text{d}t}=-2(88-C)$
- $\frac{\text{d}C}{\text{d}t}=2(33-C)$
- $\frac{\text{d}C}{\text{d}t}=176-C$
- $\frac{\text{d}C}{\text{d}t}=2(88-C)$ **Correct**
- $\frac{\text{d}C}{\text{d}t}=(88-C)$

Worked solution:
The rate at which the number of computers $C(t)$ in the data center changes is proportional to the difference between the maximum capacity and the current number of computers. Therefore, we have the differential equation

$$
\frac{\text{d}C}{\text{d}t}=k(a-C),
$$

where $a$ is the maximum capacity, and $k>0$ is a constant of proportionality.

In our case, $a=88$ computers, and $k=2$. Therefore,

$$
\frac{\text{d}C}{\text{d}t}=2(88-C).
$$

## GENERATED AUTHORED MODERATE seed=2 — moderate

A protected forest initially contains $44$ deer, and its maximum capacity is $461$ deer. Let $N(t)$ be the number of deer, where $t\ge 0$ is the time in years. Its population obeys an inhibited growth model. The rate of increase equals $2$ times the difference between the maximum capacity and the current population. Which differential equation models this population?

- $\frac{\text{d}N}{\text{d}t}=-2(461-N)$
- $\frac{\text{d}N}{\text{d}t}=(461-N)$
- $\frac{\text{d}N}{\text{d}t}=2(44-N)$
- $\frac{\text{d}N}{\text{d}t}=922-N$
- $\frac{\text{d}N}{\text{d}t}=2(461-N)$ **Correct**

Worked solution:
The rate at which the number of deer $N(t)$ in the protected forest changes is proportional to the difference between the maximum capacity and the current number of deer. Therefore, we have the differential equation

$$
\frac{\text{d}N}{\text{d}t}=k(a-N),
$$

where $a$ is the maximum capacity, and $k>0$ is a constant of proportionality.

In our case, $a=461$ deer, and $k=2$. Therefore,

$$
\frac{\text{d}N}{\text{d}t}=2(461-N).
$$

## GENERATED AUTHORED HARD seed=0 — hard

A laboratory incubator initially contains $21$ cultures, and its maximum capacity is $452$ cultures. Let $B(t)$ be the number of cultures, where $t\ge 0$ is the time in days. Its population obeys an inhibited growth model. The rate of increase equals $\frac{2}{5}$ times the difference between the maximum capacity and the current population. Which differential equation models this population?

- $\frac{\text{d}B}{\text{d}t}=2(452-B)$
- $\frac{\text{d}B}{\text{d}t}=\frac{5}{2}(452-B)$
- $\frac{\text{d}B}{\text{d}t}=\frac{2}{5}(452-B)$ **Correct**
- $\frac{\text{d}B}{\text{d}t}=\frac{2}{5}(21-B)$
- $\frac{\text{d}B}{\text{d}t}=\frac{904}{5}-B$

Worked solution:
The rate at which the number of cultures $B(t)$ in the laboratory incubator changes is proportional to the difference between the maximum capacity and the current number of cultures. Therefore, we have the differential equation

$$
\frac{\text{d}B}{\text{d}t}=k(a-B),
$$

where $a$ is the maximum capacity, and $k>0$ is a constant of proportionality.

In our case, $a=452$ cultures, and $k=\frac{2}{5}$. Therefore,

$$
\frac{\text{d}B}{\text{d}t}=\frac{2}{5}(452-B).
$$

## GENERATED AUTHORED HARD seed=1 — hard

A data center initially contains $33$ computers, and its maximum capacity is $88$ computers. Let $C(t)$ be the number of computers, where $t\ge 0$ is the time in months. Its population obeys an inhibited growth model. The rate of increase equals $\frac{1}{3}$ times the difference between the maximum capacity and the current population. Which differential equation models this population?

- $\frac{\text{d}C}{\text{d}t}=1(88-C)$
- $\frac{\text{d}C}{\text{d}t}=\frac{88}{3}-C$
- $\frac{\text{d}C}{\text{d}t}=\frac{1}{3}(33-C)$
- $\frac{\text{d}C}{\text{d}t}=\frac{1}{3}(88-C)$ **Correct**
- $\frac{\text{d}C}{\text{d}t}=3(88-C)$

Worked solution:
The rate at which the number of computers $C(t)$ in the data center changes is proportional to the difference between the maximum capacity and the current number of computers. Therefore, we have the differential equation

$$
\frac{\text{d}C}{\text{d}t}=k(a-C),
$$

where $a$ is the maximum capacity, and $k>0$ is a constant of proportionality.

In our case, $a=88$ computers, and $k=\frac{1}{3}$. Therefore,

$$
\frac{\text{d}C}{\text{d}t}=\frac{1}{3}(88-C).
$$

## GENERATED AUTHORED HARD seed=2 — hard

A protected forest initially contains $44$ deer, and its maximum capacity is $461$ deer. Let $N(t)$ be the number of deer, where $t\ge 0$ is the time in years. Its population obeys an inhibited growth model. The rate of increase equals $\frac{1}{3}$ times the difference between the maximum capacity and the current population. Which differential equation models this population?

- $\frac{\text{d}N}{\text{d}t}=1(461-N)$
- $\frac{\text{d}N}{\text{d}t}=3(461-N)$
- $\frac{\text{d}N}{\text{d}t}=\frac{461}{3}-N$
- $\frac{\text{d}N}{\text{d}t}=\frac{1}{3}(44-N)$
- $\frac{\text{d}N}{\text{d}t}=\frac{1}{3}(461-N)$ **Correct**

Worked solution:
The rate at which the number of deer $N(t)$ in the protected forest changes is proportional to the difference between the maximum capacity and the current number of deer. Therefore, we have the differential equation

$$
\frac{\text{d}N}{\text{d}t}=k(a-N),
$$

where $a$ is the maximum capacity, and $k>0$ is a constant of proportionality.

In our case, $a=461$ deer, and $k=\frac{1}{3}$. Therefore,

$$
\frac{\text{d}N}{\text{d}t}=\frac{1}{3}(461-N).
$$
