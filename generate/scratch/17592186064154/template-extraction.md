# Template extraction

## Stage 1 — Specific original descriptions

Every original raw prompt, worked-solution string, field and complete bank is preserved in source.json; review.md displays these alongside public-API replay. Parameters below retain decimal source notation and calendar origins.

### q-48935: crocodiles

Original parameters `{"a": 6, "b": 4, "k": "0.25", "t": 12, "year": 2000, "target": 2012}`; units crocodiles per year; rounding to 0 decimal places; layout radio.

### q-48936: pool

Original parameters `{"a": 1, "b": 1, "k": "1/4", "t": 2}`; units liters per minute; exact answer; layout radio.

### q-112382: drug

Original parameters `{"a": 300, "base": 2, "k": "-0.7", "t": 5}`; units milligrams per hour; rounding to 0 decimal places; layout blank.

### q-142994: stock_h

Original parameters `{"a": 3, "t": 9}`; units thousand dollars per week; exact answer; layout blank.

### q-48608: krill

Original parameters `{"a": 5, "base": 2, "k": "0.7", "t": 10, "year": 1998, "target": 2008}`; units thousand tons per year; exact answer; layout blank.

### q-167562: stock_g

Original parameters `{"a": 1, "t": 4}`; units thousand dollars per week; exact answer; layout blank.

### q-112381: muons

Original parameters `{"a": 2, "k": "-2", "t": "0.5"}`; units muons per microsecond; rounding to 3 decimal places; layout radio.

### q-112383: battery

Original parameters `{"a": 100, "base": 5, "k": "-0.2", "t": 5}`; units percent per hour; exact answer; layout radio.

### q-112507: factory

Original parameters `{"a": 100, "b": 50, "k": "-0.1", "t": 28, "amp": 10, "period": 7}`; units cars per day; rounding to 0 decimal places; layout radio.

### q-48902: bacteria

Original parameters `{"a": 100, "base": 2, "k": "0.5", "t": 6}`; units bacteria per hour; exact answer; layout radio.

### q-48914: elephants

Original parameters `{"a": 500, "b": 400, "base": 2, "exit_base": 3, "k": "0.125", "t": 8, "year": 1990, "target": 1998}`; units elephants per year; exact answer; layout radio.

## Stage 2 — Shared patterns

Each exponential single-rate template substitutes elapsed time, simplifies the exponent, and preserves source-specific additional power/quotient rows before collecting. The two stock templates evaluate a supplied reciprocal-square-root endpoint (three rows for nonunit divisor h, two for unit divisor g). The calendar templates subtract the origin year first. Two-rate templates retain the formal entry-minus-exit expression, substitution, separate component evaluation and final subtraction; factory additionally keeps the distributed subtraction with sine before its familiar-value reduction. No new differentiation occurs.

## Stage 3 — Complete components and banks

Each bank is selected whole before parameters are sampled. `correct` uses independently computed exact/rounded result. `coefficient-scale` means a times the documented rational ratio, rounded to the original option’s displayed decimal precision; it preserves the observed scalar pattern but does not identify an author mistake. The sole observed expression choice in bacteria omits the exponent coefficient: a·base^t. Bank operations never become learner-facing feedback.

### crocodiles

Parameters: {"a": 6, "b": 4, "k": "0.25", "t": 12, "year": 2000, "target": 2012}

Prompt mask:

```text
The birth rate of crocodiles in a river is modeled by $B(t) = @@a@@ \cdot e^{@@k@@t}$ crocodiles per year, while the rate of death is modeled by $D(t) = @@b@@ \cdot e^{@@k@@t}$ crocodiles per year, where $t$ represents the number of years since the year $@@year@@$.

What was the rate of change of the crocodile population in $@@target@@$? Round your answer to the nearest integer.

> A scientific calculator is required to answer this question.
```

Solution prose mask (complete ordered block inserted at the marked slot):

```text
The rate of change of the crocodile population is the birth rate minus the death rate.

$$
B(t)-D(t).
$$

Since $@@target@@$ is $@@t@@$ years after $@@year@@$, substitute $t=@@t@@$.

$$
@@block@@
$$

Therefore, the rate of change is $@@answer@@$ crocodiles per year.
```

| Original choice | Recipe | Parameterized value | Profile |

|---|---|---|---|

| $55$ crocodiles per year | coefficient-scale | round_to_original_precision(a × 55/6) | observed_crocodiles |

| $40$ crocodiles per year | correct | computed exact/rounded result | observed_crocodiles |

| $-6$ crocodiles per year | coefficient-scale | round_to_original_precision(a × -1) | observed_crocodiles |

| $77$ crocodiles per year | coefficient-scale | round_to_original_precision(a × 77/6) | observed_crocodiles |

| $66$ crocodiles per year | coefficient-scale | round_to_original_precision(a × 11) | observed_crocodiles |

### pool

Parameters: {"a": 1, "b": 1, "k": "1/4", "t": 2}

Prompt mask:

```text
The rate $F$ at which a swimming pool is being filled can be modeled as $F(t) = @@poly@@$ liters per minute, where $t$ is the time, in minutes, since the pool began to be filled. The rate at which water is leaking from the pool can be modeled as $L(t) = @@ktex@@t^{2}$ liters per minute, where $t$ is also the time, in minutes, since the pool began to be filled.

What is the rate of change of the volume of water in the pool $@@t@@$ minutes after the pool began to be filled?

> A scientific calculator is required to answer this question.
```

Solution prose mask (complete ordered block inserted at the marked slot):

```text
The rate of change of the volume of water is the filling rate minus the leaking rate.

$$
F(t)-L(t).
$$

Substituting $t=@@t@@$,

$$
@@block@@
$$

Therefore, the rate of change is $@@answer@@$ liter@@plural@@ per minute.
```

| Original choice | Recipe | Parameterized value | Profile |

|---|---|---|---|

| $3$ liters per minute | coefficient-scale | round_to_original_precision(a × 3) | observed_pool |

| $1.4$ liters per minute | coefficient-scale | round_to_original_precision(a × 7/5) | observed_pool |

| $1$ liter per minute | correct | computed exact/rounded result | observed_pool |

| $2$ liters per minute | coefficient-scale | round_to_original_precision(a × 2) | observed_pool |

| $1.5$ liters per minute | coefficient-scale | round_to_original_precision(a × 3/2) | observed_pool |

### drug

Parameters: {"a": 300, "base": 2, "k": "-0.7", "t": 5}

Prompt mask:

```text
After taking a pill containing $@@a@@$ milligrams of a particular drug, the quantity of the drug in a patient's body decreases at a rate of $c(t)=@@a@@\cdot {@@base@@}^{@@k@@t}$ milligrams per hour, where $t$ is the time, in hours, since the patient consumed the pill. What will be the rate of decrease after $@@t@@$ hours? Round your answer to the nearest integer.
```

Solution prose mask (complete ordered block inserted at the marked slot):

```text
Since we want to determine the rate of decrease in the quantity of the drug in the patient's body after $@@t@@$ hours, we have $t=5.$

Thus, the rate of decrease in the quantity of the drug after $@@t@@$ hours will be

$$
@@block@@
$$

Therefore, the rate of decrease will be $@@answer@@$ milligrams per hour.
```

Blank fragment: exact numeric value only; supplied units remain in the prompt.

### stock_h

Parameters: {"a": 3, "t": 9}

Prompt mask:

```text
What was the exact rate of change of the stock's value at week $@@t@@?$

{{field-1}}$\,$ thousand dollars per week.
```

Solution prose mask (complete ordered block inserted at the marked slot):

```text
The function ${h}^{'}(x)$ models the rate of change of the value of the stock, applicable in the domain of $h(x).$

Thus, the rate of change of the value of the stock at $x=@@t@@$ weeks is

$$
@@block@@
$$

Therefore, the rate of change in the stock price was $@@answer@@$ thousand dollars per week.
```

| Original choice | Recipe | Parameterized value | Profile |

|---|---|---|---|

| 1/9 | correct | computed exact/rounded result | observed_stock_h |

### krill

Parameters: {"a": 5, "base": 2, "k": "0.7", "t": 10, "year": 1998, "target": 2008}

Prompt mask:

```text
The birth rate of a krill population is modeled by $B(t)=@@a@@\cdot {@@base@@}^{@@k@@t}$ thousands of tons per year, where $t$ is the time, in years, since $@@year@@.$ What was the birth rate, in thousands of tons per year, for the krill in $@@target@@?$
```

Solution prose mask (complete ordered block inserted at the marked slot):

```text
The function $B(t)$ models the birth rate for the krill, in thousands of tons, $t$ years since $1998.$ Since we want the birth rate in $@@target@@$, then $t=@@t@@$ years.

Thus, the birth rate for the krill in $@@target@@$ was

$$
@@block@@
$$

Therefore, the birth rate for the krill in $@@target@@$ was $@@answer@@$ thousand tons per year.
```

Blank fragment: exact numeric value only; supplied units remain in the prompt.

### stock_g

Parameters: {"a": 1, "t": 4}

Prompt mask:

```text
What was the exact rate of change of the stock's value at week $@@t@@?$

                            
                                    
                                        
                                            

                                                

                                        
                                        
                                        

                                    
                                
                                    
                            
                                        {{field-1}}                
                                    
                                
                                    
                                        
                                        $\,$ thousand dollars per week.
```

Solution prose mask (complete ordered block inserted at the marked slot):

```text
The function ${g}^{′}(x)$ models the rate of change of the value of the stock, applicable in the domain of $g(x).$

Thus, the rate of change of the value of the stock at $x=@@t@@$ weeks is

$$
@@block@@
$$

Therefore, the rate of change in the stock price was $@@answer@@$ thousand dollars per week.
```

| Original choice | Recipe | Parameterized value | Profile |

|---|---|---|---|

| 1/2 | correct | computed exact/rounded result | observed_stock_g |

### muons

Parameters: {"a": 2, "k": "-2", "t": "0.5"}

Prompt mask:

```text
The decay rate $M$ of muons in a beam traveling at high speed can be modeled by the function $M(t)=@@a@@\cdot {e}^{@@k@@t},$ where $t$ is the time, in microseconds, since observations started. What will be the decay rate of the muons after $@@t@@$ microseconds? Round your answer to three decimal places.
```

Solution prose mask (complete ordered block inserted at the marked slot):

```text
The function $M(t)$ models the decay rate for the particles $t$ microseconds since observations started.

Thus, the decay rate of the muons after $@@t@@$ microseconds is

$$
@@block@@
$$

Therefore, the decay rate of the particles is $@@answer@@$ muons per microsecond.
```

| Original choice | Recipe | Parameterized value | Profile |

|---|---|---|---|

| $0.899$ muons per microsecond | coefficient-scale | round_to_original_precision(a × 899/2000) | observed_muons |

| $0.736$ muons per microsecond | correct | computed exact/rounded result | observed_muons |

| $0.311$ muons per microsecond | coefficient-scale | round_to_original_precision(a × 311/2000) | observed_muons |

| $0.346$ muons per microsecond | coefficient-scale | round_to_original_precision(a × 173/1000) | observed_muons |

| $0.566$ muons per microsecond | coefficient-scale | round_to_original_precision(a × 283/1000) | observed_muons |

### battery

Parameters: {"a": 100, "base": 5, "k": "-0.2", "t": 5}

Prompt mask:

```text
After charging the battery of a PC, the percentage of charge decreases at a rate of $c(t)=@@a@@\cdot {@@base@@}^{@@k@@t}$ percent per hour, where $t$ is the time, in hours, since the battery had completed its charge. What will be the rate of decrease after $@@t@@$ hours?
```

Solution prose mask (complete ordered block inserted at the marked slot):

```text
Since we want to determine the rate of decrease in the amount of charge after $@@t@@$ hours, we have $t=5.$

Thus, the rate of decrease of the amount of charge after $@@t@@$ hours will be

$$
@@block@@
$$

Therefore, the rate of decrease will be $@@answer@@$ percent per hour.
```

| Original choice | Recipe | Parameterized value | Profile |

|---|---|---|---|

| $20$ percent per hour | correct | computed exact/rounded result | observed_battery |

| $2$ percent per hour | coefficient-scale | round_to_original_precision(a × 1/50) | observed_battery |

| $10$ percent per hour | coefficient-scale | round_to_original_precision(a × 1/10) | observed_battery |

| $40$ percent per hour | coefficient-scale | round_to_original_precision(a × 2/5) | observed_battery |

| $4$ percent per hour | coefficient-scale | round_to_original_precision(a × 1/25) | observed_battery |

### factory

Parameters: {"a": 100, "b": 50, "k": "-0.1", "t": 28, "amp": 10, "period": 7}

Prompt mask:

```text
The rate $O$ of the orders a car factory receives can be modeled as $O(t)=@@a@@t{e}^{@@k@@t}$ cars per day. The rate at which cars are completed can be modeled as $C(t)=@@b@@+@@amp@@sin⁡(\frac{2\pi }{@@period@@}t)$ cars per day. In both cases, $t$ is the time, in days, since the launch of the new model. 

What is the rate of change in the number of cars under construction $@@t@@$ days after the model's launch? Assume that an ordered car goes into construction as soon as the factory receives its order. Round your answer to the nearest integer.
```

Solution prose mask (complete ordered block inserted at the marked slot):

```text
The rate of change of the number of cars under construction at time $t$ is equal to the order rate minus the completion rate, that is,

$$
O(t)-C(t).
$$

Substituting $t=@@t@@,$ the rate of change in the number of cars under construction after $@@t@@$ days is

$$
@@block@@
$$

Therefore, the rate of change in the number of cars in construction after $@@t@@$ days is $@@answer@@$ cars per day.
```

| Original choice | Recipe | Parameterized value | Profile |

|---|---|---|---|

| $162$ cars per day | coefficient-scale | round_to_original_precision(a × 81/50) | observed_factory |

| $140$ cars per day | coefficient-scale | round_to_original_precision(a × 7/5) | observed_factory |

| $125$ cars per day | coefficient-scale | round_to_original_precision(a × 5/4) | observed_factory |

| $100$ cars per day | coefficient-scale | round_to_original_precision(a × 1) | observed_factory |

| $120$ cars per day | correct | computed exact/rounded result | observed_factory |

### bacteria

Parameters: {"a": 100, "base": 2, "k": "0.5", "t": 6}

Prompt mask:

```text
The growth rate, $G(t)$, of the number of bacteria in a culture can be modeled by the function $G(t)=@@a@@\cdot {@@base@@}^{@@k@@t}$, where $t$ is the time, in hours, since a sample of bacteria was placed in a Petri dish.  What will be the growth rate of the bacteria after $@@t@@$ hours?
```

Solution prose mask (complete ordered block inserted at the marked slot):

```text
The function $G(t)$ models the growth rate for the bacteria $t$ hours since the sample was put in the Petri dish.

Thus, the growth rate of the bacteria culture after $@@t@@$ hours is

$$
@@block@@
$$

Therefore, the growth rate of the bacteria is $@@answer@@$ bacteria per hour.
```

| Original choice | Recipe | Parameterized value | Profile |

|---|---|---|---|

| $900$ bacteria per hour | coefficient-scale | round_to_original_precision(a × 9) | observed_bacteria |

| $800$ bacteria per hour | correct | computed exact/rounded result | observed_bacteria |

| $700$ bacteria per hour | coefficient-scale | round_to_original_precision(a × 7) | observed_bacteria |

| $600$ bacteria per hour | coefficient-scale | round_to_original_precision(a × 6) | observed_bacteria |

| $100\cdot {2}^{6}$ bacteria per hour | omit-exponent-scale | a × base^t | observed_bacteria |

### elephants

Parameters: {"a": 500, "b": 400, "base": 2, "exit_base": 3, "k": "0.125", "t": 8, "year": 1990, "target": 1998}

Prompt mask:

```text
The birth rate of a herd of elephants in a region in Africa is modeled by the function  $B(t)=@@a@@\cdot {@@base@@}^{@@k@@t}$ while the rate of death is modeled by $D(t)=@@b@@\cdot {@@exit_base@@}^{@@k@@t}.$ In both cases, $t$ represents the number of years since $@@year@@.$  

What was the rate of change of the elephant population in that region in $@@target@@?$
```

Solution prose mask (complete ordered block inserted at the marked slot):

```text
The  rate of change in the number of elephants  $t$ years since $@@year@@$ is equal to the difference between the two given rates, that is

$$
B(t)-D(t).
$$

As $@@target@@$ is $@@t@@$ years after $@@year@@$, we have $t=8.$  Hence, the  rate of change in the elephant population in that region in $@@target@@$ was 

$$
@@block@@
$$

Therefore, the rate of change in the elephant population was $@@answer@@$ elephants per year.
```

| Original choice | Recipe | Parameterized value | Profile |

|---|---|---|---|

| $-94$ elephants per year | coefficient-scale | round_to_original_precision(a × -47/250) | observed_elephants |

| $-200$ elephants per year | correct | computed exact/rounded result | observed_elephants |

| $-220$ elephants per year | coefficient-scale | round_to_original_precision(a × -11/25) | observed_elephants |

| $420$ elephants per year | coefficient-scale | round_to_original_precision(a × 21/25) | observed_elephants |

| $240$ elephants per year | coefficient-scale | round_to_original_precision(a × 12/25) | observed_elephants |

## Stage 4 — Reusable masks, constraints and extension bounds

The script derives complete component slots before rendering. Whole supplied-function right-hand sides, calendar dates/time scalars, answer fragments and full aligned blocks are controlled slots; it never replaces isolated short expressions across prose/commands. Fixed prose and source-specific row omissions are retained. Optional endpoint-pattern context and missing blank presentation are separately recorded repairs. π spacing in the factory row is notation normalization; no stage is dropped.

Easy stock h uses integer divisor 2…5 and square weeks 2²…12²; g retains divisor1 and square weeks 2²…20², giving exactly19 mathematical tasks. These bounds preserve one familiar square-root evaluation and avoid invalid domains. Single base-exponential rates use bases2…5, positive coefficients, familiar integer exponents; the drug decay also uses half-integer exponents and rounding. Muon decay uses coefficients2…15, negative exponent coefficients1…4, elapsed times0.5…2 and three-decimal rounding. Battery initial percentage remains100. Growth/decay signs are enforced.

Moderate pool samples positive coefficients and t3…8 with leaking coefficient 1/4,1/2,3/4; all supplied rates must be nonnegative. Crocodiles sample positive birth/death coefficients with k1/4 and t4,8,12,16. Elephants retain familiar base2…4 and exponent1 or2 at a positive shifted year; signs of the resulting net rate vary. Factory samples whole-period times (sine zero), positive order coefficient, completion baseline greater than oscillation amplitude, negative exponential coefficient −0.1 or −0.2, and nearest-integer rounding.

Hard clock_factory samples period2,6,10,14 and quarter/three-quarter periods, so elapsed time is a noninteger half hour and sine is ±1. Work starts8:00; requested time is explicitly24-hour notation. Nonzero amplitude and half-hour/familiar-angle requirements apply to explicit inputs. The formal relation, substitution, distribution, trig reduction and rounding stages match the source method.

Authored default single-rate bank: correct, double coefficient, halve coefficient, omit exponential, replace exponential by elapsed time. Authored default net-rate bank: correct, add exit, reverse subtraction, omit exit, omit entry. Complete banks must be finite, inequivalent and eligible; the whole instance is rejected when any operation collides. Positive-magnitude single-rate defaults reject negative distractors. Net-rate signs are meaningful. All banks contain five options.

Explicit observed banks are opt-in because multiple scalar values cannot uniquely identify error operations. Coefficient scaling is an honest constrained replay pattern, not a polynomial fit or recovered authoring mechanism. Changed-parameter bank examples appear in review.md. Mathematical task fingerprints exclude banks, profile and source/calendar aliases; presentation identity includes actual prompt, complete fixed solution and every displayed choice.

## Plot extraction / generation

No original prompt, bank or solution in this KP has a mathematical plot or diagram. Steps5 and7 have plot rating none; no renderer required.

## Parent QA correction

The drug, battery and elephant solution introductions now use the complete generated elapsed-time slot rather than fixed original 5/8 values; the krill origin year also uses its supplied slot. Original-parameter prose remains unchanged. Validation reads these actual prose substitutions in changed-parameter questions.
