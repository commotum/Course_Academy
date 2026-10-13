# Four-stage template extraction

## 1. Describe individual source questions

### q-105890 — hard (observed)

Parameters `{"a": 500, "k": 2, "below": 400, "above": 600}`. Positive exact integers except the terminating decimal rate 0.002 in q-15591. Variable y is the quantity; t is time. Relation is first-order dy/dt = RHS, with y(0) supplied only for IVPs. Prompt: Which of the following initial value problems is an inhibited decay problem?

Field: selection/radio; five delimiter-free math values; complete ODE and initial condition. Solution sequence: IVP definition → identify → rate/equilibrium/initial values → above-equilibrium test → contrast below-equilibrium IVP. Every shared sentence and paragraph is preserved exactly.

### q-105893 — moderate (authored repair; structurally matches rated moderate sources)

Parameters `{"a": 40, "k": 20}`. Positive exact integers except the terminating decimal rate 0.002 in q-15591. Variable y is the quantity; t is time. Relation is first-order dy/dt = RHS, with y(0) supplied only for IVPs. Prompt: Given that $y > 40$ and $t > 0$, which of the following is an inhibited decay equation?

Field: selection/radio; five delimiter-free math values; complete ODE. Solution sequence: definition → identify → factor → constants and inequality. No original worked solution: repaired from the two expanded sources.

### q-105898 — easy (observed)

Parameters `{"a": 20, "k": 80}`. Positive exact integers except the terminating decimal rate 0.002 in q-15591. Variable y is the quantity; t is time. Relation is first-order dy/dt = RHS, with y(0) supplied only for IVPs. Prompt: Given that $y>20$ and $t>0,$ which of the following is an inhibited decay equation?

Field: selection/radio; five delimiter-free math values; complete ODE. Solution sequence: definition → identify → constants and inequality. Every shared sentence and paragraph is preserved exactly.

### q-106647 — easy (observed)

Parameters `{"a": 9, "k": 5}`. Positive exact integers except the terminating decimal rate 0.002 in q-15591. Variable y is the quantity; t is time. Relation is first-order dy/dt = RHS, with y(0) supplied only for IVPs. Prompt: Given that $y>9$ and $t>0,$ which of the following is an inhibited decay equation?

Field: selection/radio; five delimiter-free math values; complete ODE. Solution sequence: definition → identify → constants and inequality. Every shared sentence and paragraph is preserved exactly.

### q-106651 — moderate (observed)

Parameters `{"a": 8, "k": 22}`. Positive exact integers except the terminating decimal rate 0.002 in q-15591. Variable y is the quantity; t is time. Relation is first-order dy/dt = RHS, with y(0) supplied only for IVPs. Prompt: Given that $y>8$ and $t>0,$ which of the following is an inhibited decay equation?

Field: selection/radio; five delimiter-free math values; complete ODE. Solution sequence: definition → identify → factor → constants and inequality. Every shared sentence and paragraph is preserved exactly.

### q-15591 — hard (observed)

Parameters `{"a": 1500, "k": "0.002", "below": 1000, "above": 3000}`. Positive exact integers except the terminating decimal rate 0.002 in q-15591. Variable y is the quantity; t is time. Relation is first-order dy/dt = RHS, with y(0) supplied only for IVPs. Prompt: Which of the following initial value problems is an inhibited decay problem?

Field: selection/radio; five delimiter-free math values; complete ODE and initial condition. Solution sequence: IVP definition → identify → rate/equilibrium/initial values → above-equilibrium test → contrast below-equilibrium IVP. Every shared sentence and paragraph is preserved exactly.

### q-106654 — moderate (observed)

Parameters `{"a": 30, "k": 28}`. Positive exact integers except the terminating decimal rate 0.002 in q-15591. Variable y is the quantity; t is time. Relation is first-order dy/dt = RHS, with y(0) supplied only for IVPs. Prompt: Given that $y>30$ and $t>0,$ which of the following is an inhibited decay equation?

Field: selection/radio; five delimiter-free math values; complete ODE. Solution sequence: definition → identify → factor → constants and inequality. Every shared sentence and paragraph is preserved exactly.

## 2. Generalize the shared patterns

Easy identifies a constant negative multiple of the linear difference y−a from already factored options, given y>a. Moderate checks the same model after factoring the negative y coefficient in a constant-first expanded expression. Hard checks the same factor structure AND the initial inequality y₀>a in five complete IVPs. All questions ask for recognition; none asks for integration, long-time calculation, physical modeling, or nonlinear-model analysis. Nonlinear options serve only as exclusion alternatives.

## 3. Component map: every option and complete bank

The following equations are operation recipes in parameters a,k,below,above. They specify exact syntax/math transformations and reproduce the full observed bank. Their mathematical structure is observed; the historical learner misconception behind each option is not recoverable. Labels describe operations, not an asserted psychological intent. There are no unexplained scalar distractors or fitted constants. No option feedback is added to the learner content.

### q-105890 / ivp_integer

| Field | Recipe / complete mathematical object | Exact original value | Designation |

|---|---|---|---|

| selection | `(-k(y-a), below)` | `$\frac{dy}{dt}=-2(y-500),\,y(0)=400$` | wrong (observed designation) |

| selection | `(-k(y-a), above)` | `$\frac{dy}{dt}=-2(y-500),\,y(0)=600$` | correct (observed) |

| selection | `(-ky(y-a), below)` | `$\frac{dy}{dt}=-2y(y-500),\,y(0)=400$` | wrong (observed designation) |

| selection | `(ky(y-a), above)` | `$\frac{dy}{dt}=2y(y-500),\,y(0)=600$` | wrong (observed designation) |

| selection | `(k(y-a), above)` | `$\frac{dy}{dt}=2(y-500),\,y(0)=600$` | wrong (observed designation) |

Mapping: full 5/5 exact options. Source Pull option order is incidental; the profile retains the complete set. Each field is owned by its question; each answer belongs to that field.

### q-105893 / expanded_spaced

| Field | Recipe / complete mathematical object | Exact original value | Designation |

|---|---|---|---|

| selection | `kay-ky²` | `$\frac{dy}{dt} = 800y - 20y^{2}$` | wrong (independently inferred) |

| selection | `ky²-ka` | `$\frac{dy}{dt} = 20y^{2} - 800$` | wrong (independently inferred) |

| selection | `ka-ky²` | `$\frac{dy}{dt} = 800 - 20y^{2}$` | wrong (independently inferred) |

| selection | `ka+ky` | `$\frac{dy}{dt} = 800 + 20y$` | wrong (independently inferred) |

| selection | `ka-ky` | `$\frac{dy}{dt} = 800 - 20y$` | correct (independently inferred) |

Mapping: full 5/5 exact options. Source Pull option order is incidental; the profile retains the complete set. Each field is owned by its question; each answer belongs to that field.

### q-105898 / factored_signs

| Field | Recipe / complete mathematical object | Exact original value | Designation |

|---|---|---|---|

| selection | `k(y+a)` | `$\frac{dy}{dt}=80(y+20)$` | wrong (observed designation) |

| selection | `-ky(a-y)` | `$\frac{dy}{dt}=-80y(20-y)$` | wrong (observed designation) |

| selection | `-k(a-y)` | `$\frac{dy}{dt}=-80(20-y)$` | wrong (observed designation) |

| selection | `ky(y+a)` | `$\frac{dy}{dt}=80y(y+20)$` | wrong (observed designation) |

| selection | `-k(y-a)` | `$\frac{dy}{dt}=-80(y-20)$` | correct (observed) |

Mapping: full 5/5 exact options. Source Pull option order is incidental; the profile retains the complete set. Each field is owned by its question; each answer belongs to that field.

### q-106647 / factored_powers

| Field | Recipe / complete mathematical object | Exact original value | Designation |

|---|---|---|---|

| selection | `-ky(y+a)` | `$\frac{dy}{dt}=-5y(y+9)$` | wrong (observed designation) |

| selection | `-ky²(y-a)` | `$\frac{dy}{dt}=-5{y}^{2}(y-9)$` | wrong (observed designation) |

| selection | `-k(a-y)` | `$\frac{dy}{dt}=-5(9-y)$` | wrong (observed designation) |

| selection | `-k(y-a)` | `$\frac{dy}{dt}=-5(y-9)$` | correct (observed) |

| selection | `-k(y²-a)` | `$\frac{dy}{dt}=-5({y}^{2}-9)$` | wrong (observed designation) |

Mapping: full 5/5 exact options. Source Pull option order is incidental; the profile retains the complete set. Each field is owned by its question; each answer belongs to that field.

### q-106651 / expanded

| Field | Recipe / complete mathematical object | Exact original value | Designation |

|---|---|---|---|

| selection | `ka-ky²` | `$\frac{dy}{dt}=176-22{y}^{2}$` | wrong (observed designation) |

| selection | `kay-ky²` | `$\frac{dy}{dt}=176y-22{y}^{2}$` | wrong (observed designation) |

| selection | `ky²-ka` | `$\frac{dy}{dt}=22{y}^{2}-176$` | wrong (observed designation) |

| selection | `ka-ky` | `$\frac{dy}{dt}=176-22y$` | correct (observed) |

| selection | `ka+ky` | `$\frac{dy}{dt}=176+22y$` | wrong (observed designation) |

Mapping: full 5/5 exact options. Source Pull option order is incidental; the profile retains the complete set. Each field is owned by its question; each answer belongs to that field.

### q-15591 / ivp_decimal_grouped

| Field | Recipe / complete mathematical object | Exact original value | Designation |

|---|---|---|---|

| selection | `(-ky(y-a), below)` | `$\frac{dy}{dt}=-0.002y(y-1\,500),\,y(0)=1\,000$` | wrong (observed designation) |

| selection | `(-k(y-a), above)` | `$\frac{dy}{dt}=-0.002(y-1\,500),\,y(0)=3\,000$` | correct (observed) |

| selection | `(ky(y-a), above)` | `$\frac{dy}{dt}=0.002y(y-1\,500),\,y(0)=3\,000$` | wrong (observed designation) |

| selection | `(k(y-a), above)` | `$\frac{dy}{dt}=0.002(y-1\,500),\,y(0)=3\,000$` | wrong (observed designation) |

| selection | `(-k(y-a), below)` | `$\frac{dy}{dt}=-0.002(y-1\,500),\,y(0)=1\,000$` | wrong (observed designation) |

Mapping: full 5/5 exact options. Source Pull option order is incidental; the profile retains the complete set. Each field is owned by its question; each answer belongs to that field.

### q-106654 / expanded

| Field | Recipe / complete mathematical object | Exact original value | Designation |

|---|---|---|---|

| selection | `ka-ky²` | `$\frac{dy}{dt}=840-28{y}^{2}$` | wrong (observed designation) |

| selection | `kay-ky²` | `$\frac{dy}{dt}=840y-28{y}^{2}$` | wrong (observed designation) |

| selection | `ky²-ka` | `$\frac{dy}{dt}=28{y}^{2}-840$` | wrong (observed designation) |

| selection | `ka-ky` | `$\frac{dy}{dt}=840-28y$` | correct (observed) |

| selection | `ka+ky` | `$\frac{dy}{dt}=840+28y$` | wrong (observed designation) |

Mapping: full 5/5 exact options. Source Pull option order is incidental; the profile retains the complete set. Each field is owned by its question; each answer belongs to that field.

## 4. Extract reusable templates and constraints

Fixed components: original question sentence, definition of inhibited decay, identification sentence, one fixed worked solution per instance, five-choice `selection` radio, derivative left side and complete answer shape. Variable components: positive equilibrium a, positive coefficient k, expanded constant ka, above/below initial values, all repeated occurrences and equation fragments. Conditional components: moderate inserts the original factoring paragraph and equation; hard inserts the initial-value explanation and below-equilibrium contrast. Profile controls full bank, thousands separators, spaces, and braced powers; it does not change the skill.

Exact calculations: linear correct RHS = −k(y−a) = ka−ky; derivative coefficient <0; equilibrium root a; hard initial above>a and the contrast below<a. Wrong operations are the complete objects listed above. The generator chooses a whole bank, computes exact mathematics, and rejects the entire instance if any two options are equivalent or more than one qualifies.

Observed domain: a,k>0, t>0, y>a. Hard: 0<below<a<above. Number samples are authored bounds: easy/moderate integer a∈[2,100], integer k∈[2,80]; hard a from {20,40,75,100,250,500,750,1000,1500,2000}, k from eleven terminating positive rates 0.001 through 5, independent four-value above/below gaps. Explicit replay admits every observed a,k including a=1500. Inputs are validated and never silently repaired. Decimal conversion is exact, not a floating rounding operation.

The 7,821 easy/moderate parameter pairs per profile and 1,760 hard rate/equilibrium/initial combinations per profile provide repeat practice. These are valid mathematical objects within the same categorical skill, not claims that number changes recover new templates. No additional authored template or missing-level extension is necessary because all levels have observed sources. Parameter variety changes equilibrium, coefficient, expanded constant, or initial inequalities while retaining the same within-level reasoning demand. Difficulty has no progression.

Content identity hashes template/domain/parameters, prompt, fixed solution and complete displayed bank. Option order and seed do not affect identity for fixed parameters/profile. Different displayed profiles have different content identities; the mathematical parameter fingerprint can deduplicate identical underlying tasks across profiles. Answer IDs are field-owned UUIDs. No parameter metadata leaks into learner prose.

Plot extraction/generation: none (steps 5 and 7). Source replay is performed through the same parameterized generator as authored samples. There is no source-ID switch returning question payloads and no correct-answer lookup. All seven source cases are explicit in source-cases.json.

