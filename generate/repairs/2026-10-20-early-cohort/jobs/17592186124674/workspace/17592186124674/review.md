# Labeled original/generated review

Raw absent difficulty, solution and designation remain absent. Repaired completion and authored levels are labeled separately.

## ORIGINAL PARAMETERIZED RAW REPLAY q-106691 — unrated

A factory's management noted that the growth of the unit production is directly proportional to the difference between the maximum number of units a factory worker can produce and the current production quantity. Let $P(t)$ be the production quantity, measured in units produced, and let $t \ge 0$ be the time in days. If the maximum number of units that a worker can produce is $70$ $units/day$, which differential equation could be used to model the factory's production? Assume that $k > 0$ is a constant of proportionality.

- $\frac{dP}{dt} =-k(70 + P)$
- $\frac{dP}{dt} =-k(70 - P)$
- $\frac{dP}{dt} = k(70 - P)$
- $\frac{dP}{dt} = kP(70 - P)$
- $\frac{dP}{dt} = kP^{2}(70 - P)$

Metadata: `{"version": "inhibited-growth-model-1", "seed": 7, "template": "source_17592186124766", "profile": "observed_17592186124766", "parameters": {"capacity": 70}, "source": {"database": "math", "basis": 1356, "lineage": "01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1"}, "source_id": "q-106691", "raw_evidence": true, "evidence_only": true, "eligible_for_learning": false, "origin": "observed-operations", "content_sha256": "67eda7dd1da9ad1756316db68c050b392ad951bc9736a587faab4cf3cff445bb", "mathematical_fingerprint": "3283c30187b595e8fba10904a2d94e345ca30873c85e709e131cc3b28b155f34", "symbol": "P", "domains": {"capacity": "positive integer; current stock below capacity", "k": "positive", "time": "t>=0"}, "recipes": [{"scale_numerator": 70, "scale_denominator": 70, "equation_mask": "\\frac{dP}{dt} =-k(<<constant>> - P)", "operation": "reverse_gap", "derived_constant": 70}, {"scale_numerator": 70, "scale_denominator": 70, "equation_mask": "\\frac{dP}{dt} = kP(<<constant>> - P)", "operation": "population_factor", "derived_constant": 70}, {"scale_numerator": 70, "scale_denominator": 70, "equation_mask": "\\frac{dP}{dt} = kP^{2}(<<constant>> - P)", "operation": "quadratic_factor", "derived_constant": 70}, {"scale_numerator": 70, "scale_denominator": 70, "equation_mask": "\\frac{dP}{dt} = k(<<constant>> - P)", "operation": "correct", "derived_constant": 70}, {"scale_numerator": 70, "scale_denominator": 70, "equation_mask": "\\frac{dP}{dt} =-k(<<constant>> + P)", "operation": "negative_sum", "derived_constant": 70}], "plots": []}`

## GENERATED OBSERVED BANK VARIANT q-106691 — unrated

A factory's management noted that the growth of the unit production is directly proportional to the difference between the maximum number of units a factory worker can produce and the current production quantity. Let $P(t)$ be the production quantity, measured in units produced, and let $t \ge 0$ be the time in days. If the maximum number of units that a worker can produce is $140$ $units/day$, which differential equation could be used to model the factory's production? Assume that $k > 0$ is a constant of proportionality.

- $\frac{dP}{dt} = kP(140 - P)$
- $\frac{dP}{dt} =-k(140 - P)$
- $\frac{dP}{dt} = k(140 - P)$
- $\frac{dP}{dt} =-k(140 + P)$
- $\frac{dP}{dt} = kP^{2}(140 - P)$

Metadata: `{"version": "inhibited-growth-model-1", "seed": 13, "template": "source_17592186124766", "profile": "observed_17592186124766", "parameters": {"capacity": 140}, "source": {"database": "math", "basis": 1356, "lineage": "01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1"}, "source_id": "q-106691", "raw_evidence": true, "evidence_only": true, "eligible_for_learning": false, "origin": "observed-operations", "content_sha256": "4cd5a0205e21709b4cef4448439abc4261088e90ea22a30973ab33b0b4511e4d", "mathematical_fingerprint": "8983bc14f7e25c4de0625fcef760945a95c0f2d535a9ce732b62bac7791aa343", "symbol": "P", "domains": {"capacity": "positive integer; current stock below capacity", "k": "positive", "time": "t>=0"}, "recipes": [{"scale_numerator": 70, "scale_denominator": 70, "equation_mask": "\\frac{dP}{dt} =-k(<<constant>> - P)", "operation": "reverse_gap", "derived_constant": 140}, {"scale_numerator": 70, "scale_denominator": 70, "equation_mask": "\\frac{dP}{dt} = kP(<<constant>> - P)", "operation": "population_factor", "derived_constant": 140}, {"scale_numerator": 70, "scale_denominator": 70, "equation_mask": "\\frac{dP}{dt} = kP^{2}(<<constant>> - P)", "operation": "quadratic_factor", "derived_constant": 140}, {"scale_numerator": 70, "scale_denominator": 70, "equation_mask": "\\frac{dP}{dt} = k(<<constant>> - P)", "operation": "correct", "derived_constant": 140}, {"scale_numerator": 70, "scale_denominator": 70, "equation_mask": "\\frac{dP}{dt} =-k(<<constant>> + P)", "operation": "negative_sum", "derived_constant": 140}], "plots": []}`

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

Metadata: `{"version": "inhibited-growth-model-1", "seed": 9, "template": "source_17592186124766", "profile": "repaired_17592186124766", "parameters": {"capacity": 70}, "source": {"database": "math", "basis": 1356, "lineage": "01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1"}, "source_id": "q-106691", "raw_evidence": false, "evidence_only": false, "eligible_for_learning": true, "origin": "source-format-repair", "content_sha256": "aef0a1bf0ca4f2bdc749ee7647bcaacd98bfc2da4d4600a2a1f50963ddd12579", "mathematical_fingerprint": "3283c30187b595e8fba10904a2d94e345ca30873c85e709e131cc3b28b155f34", "symbol": "P", "domains": {"capacity": "positive integer; current stock below capacity", "k": "positive", "time": "t>=0"}, "recipes": [{"scale_numerator": 70, "scale_denominator": 70, "equation_mask": "\\frac{dP}{dt} =-k(<<constant>> - P)", "operation": "reverse_gap", "derived_constant": 70}, {"scale_numerator": 70, "scale_denominator": 70, "equation_mask": "\\frac{dP}{dt} = kP(<<constant>> - P)", "operation": "population_factor", "derived_constant": 70}, {"scale_numerator": 70, "scale_denominator": 70, "equation_mask": "\\frac{dP}{dt} = kP^{2}(<<constant>> - P)", "operation": "quadratic_factor", "derived_constant": 70}, {"scale_numerator": 70, "scale_denominator": 70, "equation_mask": "\\frac{dP}{dt} = k(<<constant>> - P)", "operation": "correct", "derived_constant": 70}, {"scale_numerator": 70, "scale_denominator": 70, "equation_mask": "\\frac{dP}{dt} =-k(<<constant>> + P)", "operation": "negative_sum", "derived_constant": 70}], "plots": []}`

## ORIGINAL PARAMETERIZED RAW REPLAY q-37376 — unrated

A rehabilitation center initially has $20$ children. The number of children in the center $R(t)$ increases at a rate that obeys an inhibited growth model, where $t \ge 0$ is the time in months. If the maximum capacity of the center is $85$ children, which differential equation could be used to model the population of the rehabilitation center? Assume that $k > 0$ is a constant of proportionality.

- $\frac{dR}{dt} = k(85 - R)$
- $\frac{dR}{dt} = k(105 - R)$
- $\frac{dR}{dt} = k(55 - R)$
- $\frac{dR}{dt} = k(1700 - R)$
- $\frac{dR}{dt} = k(65 - R)$

Metadata: `{"version": "inhibited-growth-model-1", "seed": 7, "template": "source_17592186125066", "profile": "observed_17592186125066", "parameters": {"capacity": 85, "initial": 20}, "source": {"database": "math", "basis": 1356, "lineage": "01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1"}, "source_id": "q-37376", "raw_evidence": true, "evidence_only": true, "eligible_for_learning": false, "origin": "observed-opaque", "content_sha256": "8d0a217f089bc9b3411f90a0532f243dd05b3743b3662f7569eb1eaf9916b747", "mathematical_fingerprint": "95560d508218bfba4195064392402db24edda14909d34c2807151991cc9a2229", "symbol": "R", "domains": {"capacity": "positive integer; current stock below capacity", "k": "positive", "time": "t>=0"}, "recipes": [{"scale_numerator": 105, "scale_denominator": 85, "equation_mask": "\\frac{dR}{dt} = k(<<constant>> - R)", "operation": "opaque_capacity_ratio", "derived_constant": 105}, {"scale_numerator": 1700, "scale_denominator": 85, "equation_mask": "\\frac{dR}{dt} = k(<<constant>> - R)", "operation": "opaque_capacity_ratio", "derived_constant": 1700}, {"scale_numerator": 65, "scale_denominator": 85, "equation_mask": "\\frac{dR}{dt} = k(<<constant>> - R)", "operation": "opaque_capacity_ratio", "derived_constant": 65}, {"scale_numerator": 55, "scale_denominator": 85, "equation_mask": "\\frac{dR}{dt} = k(<<constant>> - R)", "operation": "opaque_capacity_ratio", "derived_constant": 55}, {"scale_numerator": 85, "scale_denominator": 85, "equation_mask": "\\frac{dR}{dt} = k(<<constant>> - R)", "operation": "correct", "derived_constant": 85}], "plots": []}`

## GENERATED OBSERVED BANK VARIANT q-37376 — unrated

A rehabilitation center initially has $40$ children. The number of children in the center $R(t)$ increases at a rate that obeys an inhibited growth model, where $t \ge 0$ is the time in months. If the maximum capacity of the center is $170$ children, which differential equation could be used to model the population of the rehabilitation center? Assume that $k > 0$ is a constant of proportionality.

- $\frac{dR}{dt} = k(3400 - R)$
- $\frac{dR}{dt} = k(210 - R)$
- $\frac{dR}{dt} = k(110 - R)$
- $\frac{dR}{dt} = k(170 - R)$
- $\frac{dR}{dt} = k(130 - R)$

Metadata: `{"version": "inhibited-growth-model-1", "seed": 13, "template": "source_17592186125066", "profile": "observed_17592186125066", "parameters": {"capacity": 170, "initial": 40}, "source": {"database": "math", "basis": 1356, "lineage": "01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1"}, "source_id": "q-37376", "raw_evidence": true, "evidence_only": true, "eligible_for_learning": false, "origin": "observed-opaque", "content_sha256": "cd8bf53669d20212c9423f7f536541eabb2855bdd4e9f497661db70f84a2e5ca", "mathematical_fingerprint": "20793f463c246e4b3ff4e7a4db0955141e7df233a0837e2a8399f465580dbe17", "symbol": "R", "domains": {"capacity": "positive integer; current stock below capacity", "k": "positive", "time": "t>=0"}, "recipes": [{"scale_numerator": 105, "scale_denominator": 85, "equation_mask": "\\frac{dR}{dt} = k(<<constant>> - R)", "operation": "opaque_capacity_ratio", "derived_constant": 210}, {"scale_numerator": 1700, "scale_denominator": 85, "equation_mask": "\\frac{dR}{dt} = k(<<constant>> - R)", "operation": "opaque_capacity_ratio", "derived_constant": 3400}, {"scale_numerator": 65, "scale_denominator": 85, "equation_mask": "\\frac{dR}{dt} = k(<<constant>> - R)", "operation": "opaque_capacity_ratio", "derived_constant": 130}, {"scale_numerator": 55, "scale_denominator": 85, "equation_mask": "\\frac{dR}{dt} = k(<<constant>> - R)", "operation": "opaque_capacity_ratio", "derived_constant": 110}, {"scale_numerator": 85, "scale_denominator": 85, "equation_mask": "\\frac{dR}{dt} = k(<<constant>> - R)", "operation": "correct", "derived_constant": 170}], "plots": []}`

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

Metadata: `{"version": "inhibited-growth-model-1", "seed": 9, "template": "source_17592186125066", "profile": "repaired_17592186125066", "parameters": {"capacity": 85, "initial": 20}, "source": {"database": "math", "basis": 1356, "lineage": "01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1"}, "source_id": "q-37376", "raw_evidence": false, "evidence_only": true, "eligible_for_learning": false, "origin": "source-format-repair", "content_sha256": "bfa0f8a39295e278354eabf982de9c1cdc4da61b6fe34fd3881554550f3ff41d", "mathematical_fingerprint": "95560d508218bfba4195064392402db24edda14909d34c2807151991cc9a2229", "symbol": "R", "domains": {"capacity": "positive integer; current stock below capacity", "k": "positive", "time": "t>=0"}, "recipes": [{"scale_numerator": 105, "scale_denominator": 85, "equation_mask": "\\frac{dR}{dt} = k(<<constant>> - R)", "operation": "opaque_capacity_ratio", "derived_constant": 105}, {"scale_numerator": 1700, "scale_denominator": 85, "equation_mask": "\\frac{dR}{dt} = k(<<constant>> - R)", "operation": "opaque_capacity_ratio", "derived_constant": 1700}, {"scale_numerator": 65, "scale_denominator": 85, "equation_mask": "\\frac{dR}{dt} = k(<<constant>> - R)", "operation": "opaque_capacity_ratio", "derived_constant": 65}, {"scale_numerator": 55, "scale_denominator": 85, "equation_mask": "\\frac{dR}{dt} = k(<<constant>> - R)", "operation": "opaque_capacity_ratio", "derived_constant": 55}, {"scale_numerator": 85, "scale_denominator": 85, "equation_mask": "\\frac{dR}{dt} = k(<<constant>> - R)", "operation": "correct", "derived_constant": 85}], "plots": []}`

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

Metadata: `{"version": "inhibited-growth-model-1", "seed": 7, "template": "source_17592186308738", "profile": "observed_17592186308738", "parameters": {"capacity": 150}, "source": {"database": "math", "basis": 1356, "lineage": "01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1"}, "source_id": "q-335135", "raw_evidence": true, "evidence_only": true, "eligible_for_learning": false, "origin": "observed-operations", "content_sha256": "557efce86fb0aa3eaafc8fd278070a1671290eb039794a5e2e41cb20af1c447c", "mathematical_fingerprint": "68c81d0d345d9029a23142b2afca4b0ebdbb6d95b813e26911b5ed58adccca77", "symbol": "N", "domains": {"capacity": "positive integer; current stock below capacity", "k": "positive", "time": "t>=0"}, "recipes": [{"scale_numerator": 150, "scale_denominator": 150, "equation_mask": "\\frac{\\text{d}N}{\\text{d}t}=-k(<<constant>>-N)", "operation": "reverse_gap", "derived_constant": 150}, {"scale_numerator": 150, "scale_denominator": 150, "equation_mask": "\\frac{\\text{d}N}{\\text{d}t}=k{N}^{2}(<<constant>>-N)", "operation": "quadratic_factor", "derived_constant": 150}, {"scale_numerator": 150, "scale_denominator": 150, "equation_mask": "\\frac{\\text{d}N}{\\text{d}t}=-k(<<constant>>+N)", "operation": "negative_sum", "derived_constant": 150}, {"scale_numerator": 150, "scale_denominator": 150, "equation_mask": "\\frac{\\text{d}N}{\\text{d}t}=k(<<constant>>-N)", "operation": "correct", "derived_constant": 150}, {"scale_numerator": 150, "scale_denominator": 150, "equation_mask": "\\frac{\\text{d}N}{\\text{d}t}=kN(<<constant>>-N)", "operation": "population_factor", "derived_constant": 150}], "plots": []}`

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

Metadata: `{"version": "inhibited-growth-model-1", "seed": 13, "template": "source_17592186308738", "profile": "observed_17592186308738", "parameters": {"capacity": 300}, "source": {"database": "math", "basis": 1356, "lineage": "01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1"}, "source_id": "q-335135", "raw_evidence": true, "evidence_only": true, "eligible_for_learning": false, "origin": "observed-operations", "content_sha256": "eb9d8a0dbda814605eecf2bb0b4bb877ec3866683855faec6029a385d7703082", "mathematical_fingerprint": "ccbdbaf1ff7d0b4075b689f458e7054c7eafabcb2eb3f5eadf957dc90a5ec0c1", "symbol": "N", "domains": {"capacity": "positive integer; current stock below capacity", "k": "positive", "time": "t>=0"}, "recipes": [{"scale_numerator": 150, "scale_denominator": 150, "equation_mask": "\\frac{\\text{d}N}{\\text{d}t}=-k(<<constant>>-N)", "operation": "reverse_gap", "derived_constant": 300}, {"scale_numerator": 150, "scale_denominator": 150, "equation_mask": "\\frac{\\text{d}N}{\\text{d}t}=k{N}^{2}(<<constant>>-N)", "operation": "quadratic_factor", "derived_constant": 300}, {"scale_numerator": 150, "scale_denominator": 150, "equation_mask": "\\frac{\\text{d}N}{\\text{d}t}=-k(<<constant>>+N)", "operation": "negative_sum", "derived_constant": 300}, {"scale_numerator": 150, "scale_denominator": 150, "equation_mask": "\\frac{\\text{d}N}{\\text{d}t}=k(<<constant>>-N)", "operation": "correct", "derived_constant": 300}, {"scale_numerator": 150, "scale_denominator": 150, "equation_mask": "\\frac{\\text{d}N}{\\text{d}t}=kN(<<constant>>-N)", "operation": "population_factor", "derived_constant": 300}], "plots": []}`

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

Metadata: `{"version": "inhibited-growth-model-1", "seed": 9, "template": "source_17592186308738", "profile": "repaired_17592186308738", "parameters": {"capacity": 150}, "source": {"database": "math", "basis": 1356, "lineage": "01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1"}, "source_id": "q-335135", "raw_evidence": false, "evidence_only": false, "eligible_for_learning": true, "origin": "source-format-repair", "content_sha256": "557efce86fb0aa3eaafc8fd278070a1671290eb039794a5e2e41cb20af1c447c", "mathematical_fingerprint": "68c81d0d345d9029a23142b2afca4b0ebdbb6d95b813e26911b5ed58adccca77", "symbol": "N", "domains": {"capacity": "positive integer; current stock below capacity", "k": "positive", "time": "t>=0"}, "recipes": [{"scale_numerator": 150, "scale_denominator": 150, "equation_mask": "\\frac{\\text{d}N}{\\text{d}t}=-k(<<constant>>-N)", "operation": "reverse_gap", "derived_constant": 150}, {"scale_numerator": 150, "scale_denominator": 150, "equation_mask": "\\frac{\\text{d}N}{\\text{d}t}=k{N}^{2}(<<constant>>-N)", "operation": "quadratic_factor", "derived_constant": 150}, {"scale_numerator": 150, "scale_denominator": 150, "equation_mask": "\\frac{\\text{d}N}{\\text{d}t}=-k(<<constant>>+N)", "operation": "negative_sum", "derived_constant": 150}, {"scale_numerator": 150, "scale_denominator": 150, "equation_mask": "\\frac{\\text{d}N}{\\text{d}t}=k(<<constant>>-N)", "operation": "correct", "derived_constant": 150}, {"scale_numerator": 150, "scale_denominator": 150, "equation_mask": "\\frac{\\text{d}N}{\\text{d}t}=kN(<<constant>>-N)", "operation": "population_factor", "derived_constant": 150}], "plots": []}`

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

Metadata: `{"version": "inhibited-growth-model-1", "seed": 7, "template": "source_17592186308739", "profile": "observed_17592186308739", "parameters": {"capacity": 95, "initial": 10}, "source": {"database": "math", "basis": 1356, "lineage": "01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1"}, "source_id": "q-335142", "raw_evidence": true, "evidence_only": true, "eligible_for_learning": false, "origin": "observed-opaque", "content_sha256": "100f486febaafc79e1bf1290513c069a9fb2d7ac87126b41227e0323e1c6d0b5", "mathematical_fingerprint": "b935e2c948a7dd4b5c951b4db1ee1cf5353c7222b8ba6ed817b4f62a3c7ab5d9", "symbol": "T", "domains": {"capacity": "positive integer; current stock below capacity", "k": "positive", "time": "t>=0"}, "recipes": [{"scale_numerator": 95, "scale_denominator": 95, "equation_mask": "\\frac{dT}{dt}=k(<<constant>>-T)", "operation": "correct", "derived_constant": 95}, {"scale_numerator": 30, "scale_denominator": 95, "equation_mask": "\\frac{dT}{dt}=k(<<constant>>-T)", "operation": "opaque_capacity_ratio", "derived_constant": 30}, {"scale_numerator": 60, "scale_denominator": 95, "equation_mask": "\\frac{dT}{dt}=k(<<constant>>-T)", "operation": "opaque_capacity_ratio", "derived_constant": 60}, {"scale_numerator": 100, "scale_denominator": 95, "equation_mask": "\\frac{dT}{dt}=k(<<constant>>-T)", "operation": "opaque_capacity_ratio", "derived_constant": 100}, {"scale_numerator": 950, "scale_denominator": 95, "equation_mask": "\\frac{dT}{dt}=k(<<constant>>-T)", "operation": "opaque_capacity_ratio", "derived_constant": 950}], "plots": []}`

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

Metadata: `{"version": "inhibited-growth-model-1", "seed": 13, "template": "source_17592186308739", "profile": "observed_17592186308739", "parameters": {"capacity": 190, "initial": 20}, "source": {"database": "math", "basis": 1356, "lineage": "01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1"}, "source_id": "q-335142", "raw_evidence": true, "evidence_only": true, "eligible_for_learning": false, "origin": "observed-opaque", "content_sha256": "65ed54822c68ecb56bc214f0c199615a5c10abb8e5b9d494fd1875ccc09d7e7d", "mathematical_fingerprint": "bc0fdbb8cc93f814726ec387b638265dd4fd44213a055cf033133bb5e3d63331", "symbol": "T", "domains": {"capacity": "positive integer; current stock below capacity", "k": "positive", "time": "t>=0"}, "recipes": [{"scale_numerator": 95, "scale_denominator": 95, "equation_mask": "\\frac{dT}{dt}=k(<<constant>>-T)", "operation": "correct", "derived_constant": 190}, {"scale_numerator": 30, "scale_denominator": 95, "equation_mask": "\\frac{dT}{dt}=k(<<constant>>-T)", "operation": "opaque_capacity_ratio", "derived_constant": 60}, {"scale_numerator": 60, "scale_denominator": 95, "equation_mask": "\\frac{dT}{dt}=k(<<constant>>-T)", "operation": "opaque_capacity_ratio", "derived_constant": 120}, {"scale_numerator": 100, "scale_denominator": 95, "equation_mask": "\\frac{dT}{dt}=k(<<constant>>-T)", "operation": "opaque_capacity_ratio", "derived_constant": 200}, {"scale_numerator": 950, "scale_denominator": 95, "equation_mask": "\\frac{dT}{dt}=k(<<constant>>-T)", "operation": "opaque_capacity_ratio", "derived_constant": 1900}], "plots": []}`

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

Metadata: `{"version": "inhibited-growth-model-1", "seed": 9, "template": "source_17592186308739", "profile": "repaired_17592186308739", "parameters": {"capacity": 95, "initial": 10}, "source": {"database": "math", "basis": 1356, "lineage": "01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1"}, "source_id": "q-335142", "raw_evidence": false, "evidence_only": true, "eligible_for_learning": false, "origin": "source-format-repair", "content_sha256": "100f486febaafc79e1bf1290513c069a9fb2d7ac87126b41227e0323e1c6d0b5", "mathematical_fingerprint": "b935e2c948a7dd4b5c951b4db1ee1cf5353c7222b8ba6ed817b4f62a3c7ab5d9", "symbol": "T", "domains": {"capacity": "positive integer; current stock below capacity", "k": "positive", "time": "t>=0"}, "recipes": [{"scale_numerator": 95, "scale_denominator": 95, "equation_mask": "\\frac{dT}{dt}=k(<<constant>>-T)", "operation": "correct", "derived_constant": 95}, {"scale_numerator": 30, "scale_denominator": 95, "equation_mask": "\\frac{dT}{dt}=k(<<constant>>-T)", "operation": "opaque_capacity_ratio", "derived_constant": 30}, {"scale_numerator": 60, "scale_denominator": 95, "equation_mask": "\\frac{dT}{dt}=k(<<constant>>-T)", "operation": "opaque_capacity_ratio", "derived_constant": 60}, {"scale_numerator": 100, "scale_denominator": 95, "equation_mask": "\\frac{dT}{dt}=k(<<constant>>-T)", "operation": "opaque_capacity_ratio", "derived_constant": 100}, {"scale_numerator": 950, "scale_denominator": 95, "equation_mask": "\\frac{dT}{dt}=k(<<constant>>-T)", "operation": "opaque_capacity_ratio", "derived_constant": 950}], "plots": []}`

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

Metadata: `{"version": "inhibited-growth-model-1", "seed": 7, "template": "source_17592186308740", "profile": "observed_17592186308740", "parameters": {"capacity": 60, "initial": 25}, "source": {"database": "math", "basis": 1356, "lineage": "01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1"}, "source_id": "q-335145", "raw_evidence": true, "evidence_only": true, "eligible_for_learning": false, "origin": "observed-opaque", "content_sha256": "34de183e4cfe8309d12fa9a9dd75dd6ece606bd0b050e9b173d79f5a7e24a2be", "mathematical_fingerprint": "ada6bedf1aecaa5e887830e5141b8b657e706f7a60988b4460eb8b666c78c6ec", "symbol": "M", "domains": {"capacity": "positive integer; current stock below capacity", "k": "positive", "time": "t>=0"}, "recipes": [{"scale_numerator": 35, "scale_denominator": 60, "equation_mask": "\\frac{dM}{dt}=k(<<constant>>-M)", "operation": "opaque_capacity_ratio", "derived_constant": 35}, {"scale_numerator": 60, "scale_denominator": 60, "equation_mask": "\\frac{dM}{dt}=k(<<constant>>-M)", "operation": "correct", "derived_constant": 60}, {"scale_numerator": 150, "scale_denominator": 60, "equation_mask": "\\frac{dM}{dt}=k(<<constant>>-M)", "operation": "opaque_capacity_ratio", "derived_constant": 150}, {"scale_numerator": 250, "scale_denominator": 60, "equation_mask": "\\frac{dM}{dt}=k(<<constant>>-M)", "operation": "opaque_capacity_ratio", "derived_constant": 250}, {"scale_numerator": 50, "scale_denominator": 60, "equation_mask": "\\frac{dM}{dt}=k(<<constant>>-M)", "operation": "opaque_capacity_ratio", "derived_constant": 50}], "plots": []}`

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

Metadata: `{"version": "inhibited-growth-model-1", "seed": 13, "template": "source_17592186308740", "profile": "observed_17592186308740", "parameters": {"capacity": 120, "initial": 50}, "source": {"database": "math", "basis": 1356, "lineage": "01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1"}, "source_id": "q-335145", "raw_evidence": true, "evidence_only": true, "eligible_for_learning": false, "origin": "observed-opaque", "content_sha256": "21b134d33e82fe9ea0fb98de6e44bc46dac6b30a292daa0d9a30f896200fc537", "mathematical_fingerprint": "f57a8923bedcde4c50e698179a3a55ba589b5ffedc228a6f2b3fb8bf357f6c5a", "symbol": "M", "domains": {"capacity": "positive integer; current stock below capacity", "k": "positive", "time": "t>=0"}, "recipes": [{"scale_numerator": 35, "scale_denominator": 60, "equation_mask": "\\frac{dM}{dt}=k(<<constant>>-M)", "operation": "opaque_capacity_ratio", "derived_constant": 70}, {"scale_numerator": 60, "scale_denominator": 60, "equation_mask": "\\frac{dM}{dt}=k(<<constant>>-M)", "operation": "correct", "derived_constant": 120}, {"scale_numerator": 150, "scale_denominator": 60, "equation_mask": "\\frac{dM}{dt}=k(<<constant>>-M)", "operation": "opaque_capacity_ratio", "derived_constant": 300}, {"scale_numerator": 250, "scale_denominator": 60, "equation_mask": "\\frac{dM}{dt}=k(<<constant>>-M)", "operation": "opaque_capacity_ratio", "derived_constant": 500}, {"scale_numerator": 50, "scale_denominator": 60, "equation_mask": "\\frac{dM}{dt}=k(<<constant>>-M)", "operation": "opaque_capacity_ratio", "derived_constant": 100}], "plots": []}`

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

Metadata: `{"version": "inhibited-growth-model-1", "seed": 9, "template": "source_17592186308740", "profile": "repaired_17592186308740", "parameters": {"capacity": 60, "initial": 25}, "source": {"database": "math", "basis": 1356, "lineage": "01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1"}, "source_id": "q-335145", "raw_evidence": false, "evidence_only": true, "eligible_for_learning": false, "origin": "source-format-repair", "content_sha256": "34de183e4cfe8309d12fa9a9dd75dd6ece606bd0b050e9b173d79f5a7e24a2be", "mathematical_fingerprint": "ada6bedf1aecaa5e887830e5141b8b657e706f7a60988b4460eb8b666c78c6ec", "symbol": "M", "domains": {"capacity": "positive integer; current stock below capacity", "k": "positive", "time": "t>=0"}, "recipes": [{"scale_numerator": 35, "scale_denominator": 60, "equation_mask": "\\frac{dM}{dt}=k(<<constant>>-M)", "operation": "opaque_capacity_ratio", "derived_constant": 35}, {"scale_numerator": 60, "scale_denominator": 60, "equation_mask": "\\frac{dM}{dt}=k(<<constant>>-M)", "operation": "correct", "derived_constant": 60}, {"scale_numerator": 150, "scale_denominator": 60, "equation_mask": "\\frac{dM}{dt}=k(<<constant>>-M)", "operation": "opaque_capacity_ratio", "derived_constant": 150}, {"scale_numerator": 250, "scale_denominator": 60, "equation_mask": "\\frac{dM}{dt}=k(<<constant>>-M)", "operation": "opaque_capacity_ratio", "derived_constant": 250}, {"scale_numerator": 50, "scale_denominator": 60, "equation_mask": "\\frac{dM}{dt}=k(<<constant>>-M)", "operation": "opaque_capacity_ratio", "derived_constant": 50}], "plots": []}`

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

Metadata: `{"version": "inhibited-growth-model-1", "seed": 7, "template": "source_17592186317472", "profile": "observed_17592186317472", "parameters": {"capacity": 100}, "source": {"database": "math", "basis": 1356, "lineage": "01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1"}, "source_id": "q-344214", "raw_evidence": true, "evidence_only": true, "eligible_for_learning": false, "origin": "observed-operations", "content_sha256": "949ac524353f325ec7580adbd42915122eaaf90d7a9b6a64b98b513cf65a25b0", "mathematical_fingerprint": "f70e9c38f43d46ac051bfa51a527538f07a0682f7a42e80a8adbe355b6052180", "symbol": "F", "domains": {"capacity": "positive integer; current stock below capacity", "k": "positive", "time": "t>=0"}, "recipes": [{"scale_numerator": 100, "scale_denominator": 100, "equation_mask": "\\frac{\\text{d}F}{\\text{d}t}=-k(<<constant>>-F)", "operation": "reverse_gap", "derived_constant": 100}, {"scale_numerator": 100, "scale_denominator": 100, "equation_mask": "\\frac{\\text{d}F}{\\text{d}t}=k{F}^{2}(<<constant>>-F)", "operation": "quadratic_factor", "derived_constant": 100}, {"scale_numerator": 100, "scale_denominator": 100, "equation_mask": "\\frac{\\text{d}F}{\\text{d}t}=kF(<<constant>>-F)", "operation": "population_factor", "derived_constant": 100}, {"scale_numerator": 100, "scale_denominator": 100, "equation_mask": "\\frac{\\text{d}F}{\\text{d}t}=k(<<constant>>-F)", "operation": "correct", "derived_constant": 100}, {"scale_numerator": 100, "scale_denominator": 100, "equation_mask": "\\frac{\\text{d}F}{\\text{d}t}=-k(<<constant>>+F)", "operation": "negative_sum", "derived_constant": 100}], "plots": []}`

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

Metadata: `{"version": "inhibited-growth-model-1", "seed": 13, "template": "source_17592186317472", "profile": "observed_17592186317472", "parameters": {"capacity": 200}, "source": {"database": "math", "basis": 1356, "lineage": "01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1"}, "source_id": "q-344214", "raw_evidence": true, "evidence_only": true, "eligible_for_learning": false, "origin": "observed-operations", "content_sha256": "6544aecb5c8bd8cef4ca07fe4c2b494000f673578ba505176df2a5cbc4599924", "mathematical_fingerprint": "aeaaa5c63692a0e3bf295041f2af26a1042088f743cd1a1d03524e650f245346", "symbol": "F", "domains": {"capacity": "positive integer; current stock below capacity", "k": "positive", "time": "t>=0"}, "recipes": [{"scale_numerator": 100, "scale_denominator": 100, "equation_mask": "\\frac{\\text{d}F}{\\text{d}t}=-k(<<constant>>-F)", "operation": "reverse_gap", "derived_constant": 200}, {"scale_numerator": 100, "scale_denominator": 100, "equation_mask": "\\frac{\\text{d}F}{\\text{d}t}=k{F}^{2}(<<constant>>-F)", "operation": "quadratic_factor", "derived_constant": 200}, {"scale_numerator": 100, "scale_denominator": 100, "equation_mask": "\\frac{\\text{d}F}{\\text{d}t}=kF(<<constant>>-F)", "operation": "population_factor", "derived_constant": 200}, {"scale_numerator": 100, "scale_denominator": 100, "equation_mask": "\\frac{\\text{d}F}{\\text{d}t}=k(<<constant>>-F)", "operation": "correct", "derived_constant": 200}, {"scale_numerator": 100, "scale_denominator": 100, "equation_mask": "\\frac{\\text{d}F}{\\text{d}t}=-k(<<constant>>+F)", "operation": "negative_sum", "derived_constant": 200}], "plots": []}`

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

Metadata: `{"version": "inhibited-growth-model-1", "seed": 9, "template": "source_17592186317472", "profile": "repaired_17592186317472", "parameters": {"capacity": 100}, "source": {"database": "math", "basis": 1356, "lineage": "01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1"}, "source_id": "q-344214", "raw_evidence": false, "evidence_only": false, "eligible_for_learning": true, "origin": "source-format-repair", "content_sha256": "949ac524353f325ec7580adbd42915122eaaf90d7a9b6a64b98b513cf65a25b0", "mathematical_fingerprint": "f70e9c38f43d46ac051bfa51a527538f07a0682f7a42e80a8adbe355b6052180", "symbol": "F", "domains": {"capacity": "positive integer; current stock below capacity", "k": "positive", "time": "t>=0"}, "recipes": [{"scale_numerator": 100, "scale_denominator": 100, "equation_mask": "\\frac{\\text{d}F}{\\text{d}t}=-k(<<constant>>-F)", "operation": "reverse_gap", "derived_constant": 100}, {"scale_numerator": 100, "scale_denominator": 100, "equation_mask": "\\frac{\\text{d}F}{\\text{d}t}=k{F}^{2}(<<constant>>-F)", "operation": "quadratic_factor", "derived_constant": 100}, {"scale_numerator": 100, "scale_denominator": 100, "equation_mask": "\\frac{\\text{d}F}{\\text{d}t}=kF(<<constant>>-F)", "operation": "population_factor", "derived_constant": 100}, {"scale_numerator": 100, "scale_denominator": 100, "equation_mask": "\\frac{\\text{d}F}{\\text{d}t}=k(<<constant>>-F)", "operation": "correct", "derived_constant": 100}, {"scale_numerator": 100, "scale_denominator": 100, "equation_mask": "\\frac{\\text{d}F}{\\text{d}t}=-k(<<constant>>+F)", "operation": "negative_sum", "derived_constant": 100}], "plots": []}`

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

Metadata: `{"version": "inhibited-growth-model-1", "seed": 7, "template": "source_17592186317473", "profile": "observed_17592186317473", "parameters": {"capacity": 500}, "source": {"database": "math", "basis": 1356, "lineage": "01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1"}, "source_id": "q-344218", "raw_evidence": true, "evidence_only": true, "eligible_for_learning": false, "origin": "observed-operations", "content_sha256": "083d321c9cb338316aada5b59d7e245fd18f02f357c0ce72495b699153931ab2", "mathematical_fingerprint": "0346f5d359acca50f018000ad33de5cb7e9a1c15ee4ed26f41c0bafdbb212c39", "symbol": "S", "domains": {"capacity": "positive integer; current stock below capacity", "k": "positive", "time": "t>=0"}, "recipes": [{"scale_numerator": 500, "scale_denominator": 500, "equation_mask": "\\frac{\\text{d}S}{\\text{d}t}=k(<<constant>>-S)", "operation": "correct", "derived_constant": 500}, {"scale_numerator": 500, "scale_denominator": 500, "equation_mask": "\\frac{\\text{d}S}{\\text{d}t}=kS(<<constant>>-S)", "operation": "population_factor", "derived_constant": 500}, {"scale_numerator": 500, "scale_denominator": 500, "equation_mask": "\\frac{\\text{d}S}{\\text{d}t}=k{S}^{2}(<<constant>>-S)", "operation": "quadratic_factor", "derived_constant": 500}, {"scale_numerator": 500, "scale_denominator": 500, "equation_mask": "\\frac{\\text{d}S}{\\text{d}t}=-k(<<constant>>-S)", "operation": "reverse_gap", "derived_constant": 500}, {"scale_numerator": 500, "scale_denominator": 500, "equation_mask": "\\frac{\\text{d}S}{\\text{d}t}=-k(<<constant>>+S)", "operation": "negative_sum", "derived_constant": 500}], "plots": []}`

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

Metadata: `{"version": "inhibited-growth-model-1", "seed": 13, "template": "source_17592186317473", "profile": "observed_17592186317473", "parameters": {"capacity": 1000}, "source": {"database": "math", "basis": 1356, "lineage": "01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1"}, "source_id": "q-344218", "raw_evidence": true, "evidence_only": true, "eligible_for_learning": false, "origin": "observed-operations", "content_sha256": "3a6ced3ad58671d42a7e66f589e1e0b0aa53cf8a7574b6a9185e0172f995c17a", "mathematical_fingerprint": "3741226fc0caced121c41c10f27088e4a861d093dfc547571bc2654f2fd754d1", "symbol": "S", "domains": {"capacity": "positive integer; current stock below capacity", "k": "positive", "time": "t>=0"}, "recipes": [{"scale_numerator": 500, "scale_denominator": 500, "equation_mask": "\\frac{\\text{d}S}{\\text{d}t}=k(<<constant>>-S)", "operation": "correct", "derived_constant": 1000}, {"scale_numerator": 500, "scale_denominator": 500, "equation_mask": "\\frac{\\text{d}S}{\\text{d}t}=kS(<<constant>>-S)", "operation": "population_factor", "derived_constant": 1000}, {"scale_numerator": 500, "scale_denominator": 500, "equation_mask": "\\frac{\\text{d}S}{\\text{d}t}=k{S}^{2}(<<constant>>-S)", "operation": "quadratic_factor", "derived_constant": 1000}, {"scale_numerator": 500, "scale_denominator": 500, "equation_mask": "\\frac{\\text{d}S}{\\text{d}t}=-k(<<constant>>-S)", "operation": "reverse_gap", "derived_constant": 1000}, {"scale_numerator": 500, "scale_denominator": 500, "equation_mask": "\\frac{\\text{d}S}{\\text{d}t}=-k(<<constant>>+S)", "operation": "negative_sum", "derived_constant": 1000}], "plots": []}`

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

Metadata: `{"version": "inhibited-growth-model-1", "seed": 9, "template": "source_17592186317473", "profile": "repaired_17592186317473", "parameters": {"capacity": 500}, "source": {"database": "math", "basis": 1356, "lineage": "01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1"}, "source_id": "q-344218", "raw_evidence": false, "evidence_only": false, "eligible_for_learning": true, "origin": "source-format-repair", "content_sha256": "083d321c9cb338316aada5b59d7e245fd18f02f357c0ce72495b699153931ab2", "mathematical_fingerprint": "0346f5d359acca50f018000ad33de5cb7e9a1c15ee4ed26f41c0bafdbb212c39", "symbol": "S", "domains": {"capacity": "positive integer; current stock below capacity", "k": "positive", "time": "t>=0"}, "recipes": [{"scale_numerator": 500, "scale_denominator": 500, "equation_mask": "\\frac{\\text{d}S}{\\text{d}t}=k(<<constant>>-S)", "operation": "correct", "derived_constant": 500}, {"scale_numerator": 500, "scale_denominator": 500, "equation_mask": "\\frac{\\text{d}S}{\\text{d}t}=kS(<<constant>>-S)", "operation": "population_factor", "derived_constant": 500}, {"scale_numerator": 500, "scale_denominator": 500, "equation_mask": "\\frac{\\text{d}S}{\\text{d}t}=k{S}^{2}(<<constant>>-S)", "operation": "quadratic_factor", "derived_constant": 500}, {"scale_numerator": 500, "scale_denominator": 500, "equation_mask": "\\frac{\\text{d}S}{\\text{d}t}=-k(<<constant>>-S)", "operation": "reverse_gap", "derived_constant": 500}, {"scale_numerator": 500, "scale_denominator": 500, "equation_mask": "\\frac{\\text{d}S}{\\text{d}t}=-k(<<constant>>+S)", "operation": "negative_sum", "derived_constant": 500}], "plots": []}`

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

Metadata: `{"version": "inhibited-growth-model-1", "seed": 7, "template": "source_17592186317474", "profile": "observed_17592186317474", "parameters": {"capacity": 240}, "source": {"database": "math", "basis": 1356, "lineage": "01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1"}, "source_id": "q-344219", "raw_evidence": true, "evidence_only": true, "eligible_for_learning": false, "origin": "observed-operations", "content_sha256": "1e6f396a28440b78ee10b5f7d6a913760bfec15117e80f7847de6078fc256bdf", "mathematical_fingerprint": "66e981988e110e904c03c8a83d30c309136ce4aa2b844d2892c3ab39e3135dc8", "symbol": "P", "domains": {"capacity": "positive integer; current stock below capacity", "k": "positive", "time": "t>=0"}, "recipes": [{"scale_numerator": 240, "scale_denominator": 240, "equation_mask": "\\frac{\\text{d}P}{\\text{d}t}=k(<<constant>>-P)", "operation": "correct", "derived_constant": 240}, {"scale_numerator": 240, "scale_denominator": 240, "equation_mask": "\\frac{\\text{d}P}{\\text{d}t}=kP(<<constant>>-P)", "operation": "population_factor", "derived_constant": 240}, {"scale_numerator": 240, "scale_denominator": 240, "equation_mask": "\\frac{\\text{d}P}{\\text{d}t}=-k(<<constant>>-P)", "operation": "reverse_gap", "derived_constant": 240}, {"scale_numerator": 240, "scale_denominator": 240, "equation_mask": "\\frac{\\text{d}P}{\\text{d}t}=k{P}^{2}(<<constant>>-P)", "operation": "quadratic_factor", "derived_constant": 240}, {"scale_numerator": 240, "scale_denominator": 240, "equation_mask": "\\frac{\\text{d}P}{\\text{d}t}=-k(<<constant>>+P)", "operation": "negative_sum", "derived_constant": 240}], "plots": []}`

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

Metadata: `{"version": "inhibited-growth-model-1", "seed": 13, "template": "source_17592186317474", "profile": "observed_17592186317474", "parameters": {"capacity": 480}, "source": {"database": "math", "basis": 1356, "lineage": "01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1"}, "source_id": "q-344219", "raw_evidence": true, "evidence_only": true, "eligible_for_learning": false, "origin": "observed-operations", "content_sha256": "31ef4fa7a9b76d7493790ec7db9ddfc87dd581310b80056c22775070fc887fed", "mathematical_fingerprint": "fac7050e90c51c4a7d1c97e61aa390dbfc53e69e88f09940339af4c0430ca179", "symbol": "P", "domains": {"capacity": "positive integer; current stock below capacity", "k": "positive", "time": "t>=0"}, "recipes": [{"scale_numerator": 240, "scale_denominator": 240, "equation_mask": "\\frac{\\text{d}P}{\\text{d}t}=k(<<constant>>-P)", "operation": "correct", "derived_constant": 480}, {"scale_numerator": 240, "scale_denominator": 240, "equation_mask": "\\frac{\\text{d}P}{\\text{d}t}=kP(<<constant>>-P)", "operation": "population_factor", "derived_constant": 480}, {"scale_numerator": 240, "scale_denominator": 240, "equation_mask": "\\frac{\\text{d}P}{\\text{d}t}=-k(<<constant>>-P)", "operation": "reverse_gap", "derived_constant": 480}, {"scale_numerator": 240, "scale_denominator": 240, "equation_mask": "\\frac{\\text{d}P}{\\text{d}t}=k{P}^{2}(<<constant>>-P)", "operation": "quadratic_factor", "derived_constant": 480}, {"scale_numerator": 240, "scale_denominator": 240, "equation_mask": "\\frac{\\text{d}P}{\\text{d}t}=-k(<<constant>>+P)", "operation": "negative_sum", "derived_constant": 480}], "plots": []}`

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

Metadata: `{"version": "inhibited-growth-model-1", "seed": 9, "template": "source_17592186317474", "profile": "repaired_17592186317474", "parameters": {"capacity": 240}, "source": {"database": "math", "basis": 1356, "lineage": "01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1"}, "source_id": "q-344219", "raw_evidence": false, "evidence_only": false, "eligible_for_learning": true, "origin": "source-format-repair", "content_sha256": "1e6f396a28440b78ee10b5f7d6a913760bfec15117e80f7847de6078fc256bdf", "mathematical_fingerprint": "66e981988e110e904c03c8a83d30c309136ce4aa2b844d2892c3ab39e3135dc8", "symbol": "P", "domains": {"capacity": "positive integer; current stock below capacity", "k": "positive", "time": "t>=0"}, "recipes": [{"scale_numerator": 240, "scale_denominator": 240, "equation_mask": "\\frac{\\text{d}P}{\\text{d}t}=k(<<constant>>-P)", "operation": "correct", "derived_constant": 240}, {"scale_numerator": 240, "scale_denominator": 240, "equation_mask": "\\frac{\\text{d}P}{\\text{d}t}=kP(<<constant>>-P)", "operation": "population_factor", "derived_constant": 240}, {"scale_numerator": 240, "scale_denominator": 240, "equation_mask": "\\frac{\\text{d}P}{\\text{d}t}=-k(<<constant>>-P)", "operation": "reverse_gap", "derived_constant": 240}, {"scale_numerator": 240, "scale_denominator": 240, "equation_mask": "\\frac{\\text{d}P}{\\text{d}t}=k{P}^{2}(<<constant>>-P)", "operation": "quadratic_factor", "derived_constant": 240}, {"scale_numerator": 240, "scale_denominator": 240, "equation_mask": "\\frac{\\text{d}P}{\\text{d}t}=-k(<<constant>>+P)", "operation": "negative_sum", "derived_constant": 240}], "plots": []}`

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

Metadata: `{"version": "inhibited-growth-model-1", "seed": 7, "template": "source_17592186317477", "profile": "observed_17592186317477", "parameters": {"capacity": 50, "initial": 18}, "source": {"database": "math", "basis": 1356, "lineage": "01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1"}, "source_id": "q-344228", "raw_evidence": true, "evidence_only": true, "eligible_for_learning": false, "origin": "observed-opaque", "content_sha256": "0e64c742fd882cb73e4ce1dcf58c4ba01fb8685d25df93e35383ee5b11fd2be9", "mathematical_fingerprint": "a7c644469413a51bb570ddfe8f5881e0d4d3919c6aaadb6cf74d7b3f3a949400", "symbol": "B", "domains": {"capacity": "positive integer; current stock below capacity", "k": "positive", "time": "t>=0"}, "recipes": [{"scale_numerator": 80, "scale_denominator": 50, "equation_mask": "\\frac{dB}{dt}=k(<<constant>>-B)", "operation": "opaque_capacity_ratio", "derived_constant": 80}, {"scale_numerator": 35, "scale_denominator": 50, "equation_mask": "\\frac{dB}{dt}=k(<<constant>>-B)", "operation": "opaque_capacity_ratio", "derived_constant": 35}, {"scale_numerator": 25, "scale_denominator": 50, "equation_mask": "\\frac{dB}{dt}=k(<<constant>>-B)", "operation": "opaque_capacity_ratio", "derived_constant": 25}, {"scale_numerator": 50, "scale_denominator": 50, "equation_mask": "\\frac{dB}{dt}=k(<<constant>>-B)", "operation": "correct", "derived_constant": 50}, {"scale_numerator": 18, "scale_denominator": 50, "equation_mask": "\\frac{dB}{dt}=k(<<constant>>-B)", "operation": "opaque_capacity_ratio", "derived_constant": 18}], "plots": []}`

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

Metadata: `{"version": "inhibited-growth-model-1", "seed": 13, "template": "source_17592186317477", "profile": "observed_17592186317477", "parameters": {"capacity": 100, "initial": 36}, "source": {"database": "math", "basis": 1356, "lineage": "01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1"}, "source_id": "q-344228", "raw_evidence": true, "evidence_only": true, "eligible_for_learning": false, "origin": "observed-opaque", "content_sha256": "68bdbfd3bf04be178b3ff1faf852a0ac4abd82abc3e09a5f35411d7add8dd9a1", "mathematical_fingerprint": "f70e9c38f43d46ac051bfa51a527538f07a0682f7a42e80a8adbe355b6052180", "symbol": "B", "domains": {"capacity": "positive integer; current stock below capacity", "k": "positive", "time": "t>=0"}, "recipes": [{"scale_numerator": 80, "scale_denominator": 50, "equation_mask": "\\frac{dB}{dt}=k(<<constant>>-B)", "operation": "opaque_capacity_ratio", "derived_constant": 160}, {"scale_numerator": 35, "scale_denominator": 50, "equation_mask": "\\frac{dB}{dt}=k(<<constant>>-B)", "operation": "opaque_capacity_ratio", "derived_constant": 70}, {"scale_numerator": 25, "scale_denominator": 50, "equation_mask": "\\frac{dB}{dt}=k(<<constant>>-B)", "operation": "opaque_capacity_ratio", "derived_constant": 50}, {"scale_numerator": 50, "scale_denominator": 50, "equation_mask": "\\frac{dB}{dt}=k(<<constant>>-B)", "operation": "correct", "derived_constant": 100}, {"scale_numerator": 18, "scale_denominator": 50, "equation_mask": "\\frac{dB}{dt}=k(<<constant>>-B)", "operation": "opaque_capacity_ratio", "derived_constant": 36}], "plots": []}`

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

Metadata: `{"version": "inhibited-growth-model-1", "seed": 9, "template": "source_17592186317477", "profile": "repaired_17592186317477", "parameters": {"capacity": 50, "initial": 18}, "source": {"database": "math", "basis": 1356, "lineage": "01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1"}, "source_id": "q-344228", "raw_evidence": false, "evidence_only": true, "eligible_for_learning": false, "origin": "source-format-repair", "content_sha256": "0e64c742fd882cb73e4ce1dcf58c4ba01fb8685d25df93e35383ee5b11fd2be9", "mathematical_fingerprint": "a7c644469413a51bb570ddfe8f5881e0d4d3919c6aaadb6cf74d7b3f3a949400", "symbol": "B", "domains": {"capacity": "positive integer; current stock below capacity", "k": "positive", "time": "t>=0"}, "recipes": [{"scale_numerator": 80, "scale_denominator": 50, "equation_mask": "\\frac{dB}{dt}=k(<<constant>>-B)", "operation": "opaque_capacity_ratio", "derived_constant": 80}, {"scale_numerator": 35, "scale_denominator": 50, "equation_mask": "\\frac{dB}{dt}=k(<<constant>>-B)", "operation": "opaque_capacity_ratio", "derived_constant": 35}, {"scale_numerator": 25, "scale_denominator": 50, "equation_mask": "\\frac{dB}{dt}=k(<<constant>>-B)", "operation": "opaque_capacity_ratio", "derived_constant": 25}, {"scale_numerator": 50, "scale_denominator": 50, "equation_mask": "\\frac{dB}{dt}=k(<<constant>>-B)", "operation": "correct", "derived_constant": 50}, {"scale_numerator": 18, "scale_denominator": 50, "equation_mask": "\\frac{dB}{dt}=k(<<constant>>-B)", "operation": "opaque_capacity_ratio", "derived_constant": 18}], "plots": []}`

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

Metadata: `{"version": "inhibited-growth-model-1", "seed": 7, "template": "source_17592186317478", "profile": "observed_17592186317478", "parameters": {"capacity": 1000, "initial": 320}, "source": {"database": "math", "basis": 1356, "lineage": "01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1"}, "source_id": "q-344233", "raw_evidence": true, "evidence_only": true, "eligible_for_learning": false, "origin": "observed-opaque", "content_sha256": "dcfa7236accfe0c8b1614b10221ae3a32ea6ca584e217d6cba9bd107645b9351", "mathematical_fingerprint": "3741226fc0caced121c41c10f27088e4a861d093dfc547571bc2654f2fd754d1", "symbol": "C", "domains": {"capacity": "positive integer; current stock below capacity", "k": "positive", "time": "t>=0"}, "recipes": [{"scale_numerator": 320, "scale_denominator": 1000, "equation_mask": "\\frac{dC}{dt}=k(<<constant>>-C)", "operation": "opaque_capacity_ratio", "derived_constant": 320}, {"scale_numerator": 800, "scale_denominator": 1000, "equation_mask": "\\frac{dC}{dt}=k(<<constant>>-C)", "operation": "opaque_capacity_ratio", "derived_constant": 800}, {"scale_numerator": 1000, "scale_denominator": 1000, "equation_mask": "\\frac{dC}{dt}=k(<<constant>>-C)", "operation": "correct", "derived_constant": 1000}, {"scale_numerator": 500, "scale_denominator": 1000, "equation_mask": "\\frac{dC}{dt}=k(<<constant>>-C)", "operation": "opaque_capacity_ratio", "derived_constant": 500}, {"scale_numerator": 1500, "scale_denominator": 1000, "equation_mask": "\\frac{dC}{dt}=k(<<constant>>-C)", "operation": "opaque_capacity_ratio", "derived_constant": 1500}], "plots": []}`

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

Metadata: `{"version": "inhibited-growth-model-1", "seed": 13, "template": "source_17592186317478", "profile": "observed_17592186317478", "parameters": {"capacity": 2000, "initial": 640}, "source": {"database": "math", "basis": 1356, "lineage": "01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1"}, "source_id": "q-344233", "raw_evidence": true, "evidence_only": true, "eligible_for_learning": false, "origin": "observed-opaque", "content_sha256": "9f5cee7b9ffb714f0ea0389840effa5afad486fe966378f52033d71e445e0269", "mathematical_fingerprint": "c0e852ecb5fd64a7657892ec42c25bc529099b3914b9d1a61e5b7fcbdda7abab", "symbol": "C", "domains": {"capacity": "positive integer; current stock below capacity", "k": "positive", "time": "t>=0"}, "recipes": [{"scale_numerator": 320, "scale_denominator": 1000, "equation_mask": "\\frac{dC}{dt}=k(<<constant>>-C)", "operation": "opaque_capacity_ratio", "derived_constant": 640}, {"scale_numerator": 800, "scale_denominator": 1000, "equation_mask": "\\frac{dC}{dt}=k(<<constant>>-C)", "operation": "opaque_capacity_ratio", "derived_constant": 1600}, {"scale_numerator": 1000, "scale_denominator": 1000, "equation_mask": "\\frac{dC}{dt}=k(<<constant>>-C)", "operation": "correct", "derived_constant": 2000}, {"scale_numerator": 500, "scale_denominator": 1000, "equation_mask": "\\frac{dC}{dt}=k(<<constant>>-C)", "operation": "opaque_capacity_ratio", "derived_constant": 1000}, {"scale_numerator": 1500, "scale_denominator": 1000, "equation_mask": "\\frac{dC}{dt}=k(<<constant>>-C)", "operation": "opaque_capacity_ratio", "derived_constant": 3000}], "plots": []}`

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

Metadata: `{"version": "inhibited-growth-model-1", "seed": 9, "template": "source_17592186317478", "profile": "repaired_17592186317478", "parameters": {"capacity": 1000, "initial": 320}, "source": {"database": "math", "basis": 1356, "lineage": "01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1"}, "source_id": "q-344233", "raw_evidence": false, "evidence_only": true, "eligible_for_learning": false, "origin": "source-format-repair", "content_sha256": "dcfa7236accfe0c8b1614b10221ae3a32ea6ca584e217d6cba9bd107645b9351", "mathematical_fingerprint": "3741226fc0caced121c41c10f27088e4a861d093dfc547571bc2654f2fd754d1", "symbol": "C", "domains": {"capacity": "positive integer; current stock below capacity", "k": "positive", "time": "t>=0"}, "recipes": [{"scale_numerator": 320, "scale_denominator": 1000, "equation_mask": "\\frac{dC}{dt}=k(<<constant>>-C)", "operation": "opaque_capacity_ratio", "derived_constant": 320}, {"scale_numerator": 800, "scale_denominator": 1000, "equation_mask": "\\frac{dC}{dt}=k(<<constant>>-C)", "operation": "opaque_capacity_ratio", "derived_constant": 800}, {"scale_numerator": 1000, "scale_denominator": 1000, "equation_mask": "\\frac{dC}{dt}=k(<<constant>>-C)", "operation": "correct", "derived_constant": 1000}, {"scale_numerator": 500, "scale_denominator": 1000, "equation_mask": "\\frac{dC}{dt}=k(<<constant>>-C)", "operation": "opaque_capacity_ratio", "derived_constant": 500}, {"scale_numerator": 1500, "scale_denominator": 1000, "equation_mask": "\\frac{dC}{dt}=k(<<constant>>-C)", "operation": "opaque_capacity_ratio", "derived_constant": 1500}], "plots": []}`

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

Metadata: `{"version": "inhibited-growth-model-1", "seed": 7, "template": "source_17592186372691", "profile": "observed_17592186372691", "parameters": {"capacity": 90}, "source": {"database": "math", "basis": 1356, "lineage": "01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1"}, "source_id": "q-335137", "raw_evidence": true, "evidence_only": true, "eligible_for_learning": false, "origin": "observed-operations", "content_sha256": "98d33575a86a68ef72ed086a96a9308b962acb3e3aa8269c648f1a0d0d0ecb74", "mathematical_fingerprint": "32fe134d74657380f3fcb0b9c5155e84cfb399cc6c65277186ea74a1e9c66a20", "symbol": "V", "domains": {"capacity": "positive integer; current stock below capacity", "k": "positive", "time": "t>=0"}, "recipes": [{"scale_numerator": 90, "scale_denominator": 90, "equation_mask": "\\frac{\\text{d}V}{\\text{d}t}=-k(<<constant>>-V)", "operation": "reverse_gap", "derived_constant": 90}, {"scale_numerator": 90, "scale_denominator": 90, "equation_mask": "\\frac{\\text{d}V}{\\text{d}t}=k{V}^{2}(<<constant>>-V)", "operation": "quadratic_factor", "derived_constant": 90}, {"scale_numerator": 90, "scale_denominator": 90, "equation_mask": "\\frac{\\text{d}V}{\\text{d}t}=kV(<<constant>>-V)", "operation": "population_factor", "derived_constant": 90}, {"scale_numerator": 90, "scale_denominator": 90, "equation_mask": "\\frac{\\text{d}V}{\\text{d}t}=-k(<<constant>>+V)", "operation": "negative_sum", "derived_constant": 90}, {"scale_numerator": 90, "scale_denominator": 90, "equation_mask": "\\frac{\\text{d}V}{\\text{d}t}=k(<<constant>>-V)", "operation": "correct", "derived_constant": 90}], "plots": []}`

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

Metadata: `{"version": "inhibited-growth-model-1", "seed": 13, "template": "source_17592186372691", "profile": "observed_17592186372691", "parameters": {"capacity": 180}, "source": {"database": "math", "basis": 1356, "lineage": "01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1"}, "source_id": "q-335137", "raw_evidence": true, "evidence_only": true, "eligible_for_learning": false, "origin": "observed-operations", "content_sha256": "42480d06c69c99d99e85d5e2d394bb9fde469b6cc8b973dfcb7c50f9bab780db", "mathematical_fingerprint": "264ac53e5c5f738081b47c9c9eaa35a072d9ade525f2ab7c9e1b13f3d41bd63b", "symbol": "V", "domains": {"capacity": "positive integer; current stock below capacity", "k": "positive", "time": "t>=0"}, "recipes": [{"scale_numerator": 90, "scale_denominator": 90, "equation_mask": "\\frac{\\text{d}V}{\\text{d}t}=-k(<<constant>>-V)", "operation": "reverse_gap", "derived_constant": 180}, {"scale_numerator": 90, "scale_denominator": 90, "equation_mask": "\\frac{\\text{d}V}{\\text{d}t}=k{V}^{2}(<<constant>>-V)", "operation": "quadratic_factor", "derived_constant": 180}, {"scale_numerator": 90, "scale_denominator": 90, "equation_mask": "\\frac{\\text{d}V}{\\text{d}t}=kV(<<constant>>-V)", "operation": "population_factor", "derived_constant": 180}, {"scale_numerator": 90, "scale_denominator": 90, "equation_mask": "\\frac{\\text{d}V}{\\text{d}t}=-k(<<constant>>+V)", "operation": "negative_sum", "derived_constant": 180}, {"scale_numerator": 90, "scale_denominator": 90, "equation_mask": "\\frac{\\text{d}V}{\\text{d}t}=k(<<constant>>-V)", "operation": "correct", "derived_constant": 180}], "plots": []}`

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

Metadata: `{"version": "inhibited-growth-model-1", "seed": 9, "template": "source_17592186372691", "profile": "repaired_17592186372691", "parameters": {"capacity": 90}, "source": {"database": "math", "basis": 1356, "lineage": "01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1"}, "source_id": "q-335137", "raw_evidence": false, "evidence_only": false, "eligible_for_learning": true, "origin": "source-format-repair", "content_sha256": "98d33575a86a68ef72ed086a96a9308b962acb3e3aa8269c648f1a0d0d0ecb74", "mathematical_fingerprint": "32fe134d74657380f3fcb0b9c5155e84cfb399cc6c65277186ea74a1e9c66a20", "symbol": "V", "domains": {"capacity": "positive integer; current stock below capacity", "k": "positive", "time": "t>=0"}, "recipes": [{"scale_numerator": 90, "scale_denominator": 90, "equation_mask": "\\frac{\\text{d}V}{\\text{d}t}=-k(<<constant>>-V)", "operation": "reverse_gap", "derived_constant": 90}, {"scale_numerator": 90, "scale_denominator": 90, "equation_mask": "\\frac{\\text{d}V}{\\text{d}t}=k{V}^{2}(<<constant>>-V)", "operation": "quadratic_factor", "derived_constant": 90}, {"scale_numerator": 90, "scale_denominator": 90, "equation_mask": "\\frac{\\text{d}V}{\\text{d}t}=kV(<<constant>>-V)", "operation": "population_factor", "derived_constant": 90}, {"scale_numerator": 90, "scale_denominator": 90, "equation_mask": "\\frac{\\text{d}V}{\\text{d}t}=-k(<<constant>>+V)", "operation": "negative_sum", "derived_constant": 90}, {"scale_numerator": 90, "scale_denominator": 90, "equation_mask": "\\frac{\\text{d}V}{\\text{d}t}=k(<<constant>>-V)", "operation": "correct", "derived_constant": 90}], "plots": []}`

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

Metadata: `{"version": "inhibited-growth-model-1", "seed": 0, "template": "direct_model", "profile": "model_operations", "parameters": {"capacity": 452, "context": "cultures"}, "source": {"database": "math", "basis": 1356, "lineage": "01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1"}, "source_id": null, "raw_evidence": false, "evidence_only": false, "eligible_for_learning": true, "origin": "observed-method/authored-context", "content_sha256": "7e1e47d1a3aad45a65879c7b83a363ae1688d2ff13bb2ad66fc07389fc01a8b8", "mathematical_fingerprint": "43b2c744cd82fefeb3674e054e298d9fcd9416c3f5dc02116bbb9fe97c8447dd", "symbol": "B", "domains": {"capacity": "positive integer; current stock below capacity", "k": "positive", "time": "t>=0"}, "recipes": ["correct", "reverse_gap", "population_factor", "quadratic_factor", "negative_sum"], "plots": []}`

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

Metadata: `{"version": "inhibited-growth-model-1", "seed": 1, "template": "direct_model", "profile": "model_operations", "parameters": {"capacity": 88, "context": "computers"}, "source": {"database": "math", "basis": 1356, "lineage": "01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1"}, "source_id": null, "raw_evidence": false, "evidence_only": false, "eligible_for_learning": true, "origin": "observed-method/authored-context", "content_sha256": "daa042ad586ef20cdfc29844d4e9bd54e9105dd582234edb3c0b65ab2ad3195d", "mathematical_fingerprint": "193fce484c87e59bf50525fdf02f5426953f6b24c71cf0f3c519be4853766078", "symbol": "C", "domains": {"capacity": "positive integer; current stock below capacity", "k": "positive", "time": "t>=0"}, "recipes": ["correct", "reverse_gap", "population_factor", "quadratic_factor", "negative_sum"], "plots": []}`

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

Metadata: `{"version": "inhibited-growth-model-1", "seed": 2, "template": "direct_model", "profile": "model_operations", "parameters": {"capacity": 461, "context": "deer"}, "source": {"database": "math", "basis": 1356, "lineage": "01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1"}, "source_id": null, "raw_evidence": false, "evidence_only": false, "eligible_for_learning": true, "origin": "observed-method/authored-context", "content_sha256": "506b0994bf46046fca692d38abca0321e83cc253f153e5dabc01ddbf9feadb1c", "mathematical_fingerprint": "bf5d3cb67b01fe21754739d79b98c1f4f299b7192ebc437d9344127379ed63ac", "symbol": "N", "domains": {"capacity": "positive integer; current stock below capacity", "k": "positive", "time": "t>=0"}, "recipes": ["correct", "reverse_gap", "population_factor", "quadratic_factor", "negative_sum"], "plots": []}`

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

Metadata: `{"version": "inhibited-growth-model-1", "seed": 0, "template": "known_integer_rate", "profile": "integer_placement", "parameters": {"capacity": 452, "context": "cultures", "initial": 21, "numerator": 5, "denominator": 1}, "source": {"database": "math", "basis": 1356, "lineage": "01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1"}, "source_id": null, "raw_evidence": false, "evidence_only": false, "eligible_for_learning": true, "origin": "authored", "content_sha256": "e0317bf0c6aecebd8fe3bb83960671498766f6aa8e4c561a572ba008ad5971d0", "mathematical_fingerprint": "4d3514f7fdca8b81d2422bd382102c0f8f1a6bff3192a01018d879c06b927454", "symbol": "B", "domains": {"capacity": "positive integer; current stock below capacity", "k": "positive", "time": "t>=0"}, "recipes": ["correct", "omit_rate", "reverse_gap", "use_initial_capacity", "apply_rate_only_to_capacity"], "plots": []}`

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

Metadata: `{"version": "inhibited-growth-model-1", "seed": 1, "template": "known_integer_rate", "profile": "integer_placement", "parameters": {"capacity": 88, "context": "computers", "initial": 33, "numerator": 2, "denominator": 1}, "source": {"database": "math", "basis": 1356, "lineage": "01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1"}, "source_id": null, "raw_evidence": false, "evidence_only": false, "eligible_for_learning": true, "origin": "authored", "content_sha256": "9d42d27a11562ddbe2cc535b983cfdb87cdcdbd22b62f44c7f953d1b5140e945", "mathematical_fingerprint": "822f26f433ccf22d6154889edd9985b01399d45e883810933b9ece0eaf09f9ee", "symbol": "C", "domains": {"capacity": "positive integer; current stock below capacity", "k": "positive", "time": "t>=0"}, "recipes": ["correct", "omit_rate", "reverse_gap", "use_initial_capacity", "apply_rate_only_to_capacity"], "plots": []}`

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

Metadata: `{"version": "inhibited-growth-model-1", "seed": 2, "template": "known_integer_rate", "profile": "integer_placement", "parameters": {"capacity": 461, "context": "deer", "initial": 44, "numerator": 2, "denominator": 1}, "source": {"database": "math", "basis": 1356, "lineage": "01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1"}, "source_id": null, "raw_evidence": false, "evidence_only": false, "eligible_for_learning": true, "origin": "authored", "content_sha256": "cd53194ccdeb4a753b7b87825a949de4bbf99bdcbafbc3c6cda43d3635093ea2", "mathematical_fingerprint": "58e48793f628695c62ab912d968f1b25d91e15af4bf5d2db0968d08861362b63", "symbol": "N", "domains": {"capacity": "positive integer; current stock below capacity", "k": "positive", "time": "t>=0"}, "recipes": ["correct", "omit_rate", "reverse_gap", "use_initial_capacity", "apply_rate_only_to_capacity"], "plots": []}`

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

Metadata: `{"version": "inhibited-growth-model-1", "seed": 0, "template": "known_fractional_rate", "profile": "fractional_placement", "parameters": {"capacity": 452, "context": "cultures", "initial": 21, "numerator": 2, "denominator": 5}, "source": {"database": "math", "basis": 1356, "lineage": "01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1"}, "source_id": null, "raw_evidence": false, "evidence_only": false, "eligible_for_learning": true, "origin": "authored", "content_sha256": "35baf7fe26bca46d94c019d55c76a975eeccd03c7a229e8e895f8d04a3b3649e", "mathematical_fingerprint": "fae4977c9e84ceeb76ac13a9dbb788df3965a09d1edf3f0e63fe9858daa12cdd", "symbol": "B", "domains": {"capacity": "positive integer; current stock below capacity", "k": "positive", "time": "t>=0"}, "recipes": ["correct", "invert_rate", "omit_denominator", "apply_rate_only_to_capacity", "use_initial_capacity"], "plots": []}`

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

Metadata: `{"version": "inhibited-growth-model-1", "seed": 1, "template": "known_fractional_rate", "profile": "fractional_placement", "parameters": {"capacity": 88, "context": "computers", "initial": 33, "numerator": 1, "denominator": 3}, "source": {"database": "math", "basis": 1356, "lineage": "01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1"}, "source_id": null, "raw_evidence": false, "evidence_only": false, "eligible_for_learning": true, "origin": "authored", "content_sha256": "342c004ea10d65fbc18d90d4638437fd7170ea07492952e03c983168221d01c7", "mathematical_fingerprint": "9e5a383c99faba1962066c29a5dc2df9634d0a6df7334b41d198605701c52cd7", "symbol": "C", "domains": {"capacity": "positive integer; current stock below capacity", "k": "positive", "time": "t>=0"}, "recipes": ["correct", "invert_rate", "omit_denominator", "apply_rate_only_to_capacity", "use_initial_capacity"], "plots": []}`

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

Metadata: `{"version": "inhibited-growth-model-1", "seed": 2, "template": "known_fractional_rate", "profile": "fractional_placement", "parameters": {"capacity": 461, "context": "deer", "initial": 44, "numerator": 1, "denominator": 3}, "source": {"database": "math", "basis": 1356, "lineage": "01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1"}, "source_id": null, "raw_evidence": false, "evidence_only": false, "eligible_for_learning": true, "origin": "authored", "content_sha256": "7b325db8351a97810d2d7ff0d52c421e81c8f25711d3e1eb603b99757d8255d8", "mathematical_fingerprint": "84f7a6ea4428e93422f50a9dc95562e5e225d85704488407ad73c67636044193", "symbol": "N", "domains": {"capacity": "positive integer; current stock below capacity", "k": "positive", "time": "t>=0"}, "recipes": ["correct", "invert_rate", "omit_denominator", "apply_rate_only_to_capacity", "use_initial_capacity"], "plots": []}`
