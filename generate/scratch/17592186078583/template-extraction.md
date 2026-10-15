# Current template extraction

Source basis 2710. This supersedes the archived basis-1356 extraction. All parameters, source choice recipes and component masks are in templates.json and source-cases.json.

## Backbone and slots

Easy has one supplied ambient S and direct proportionality. Moderate has supplied initial I and ambient S, preserves the stated positive constant k, and identifies S rather than I in -k(T-S). Fixed: one complete-equation selection field, five options, generic Newton equation then numerical substitution. Changing operations, adding observed readings, fitting k or solving the ODE is outside the backbone.

S is an integer ambient: 10–40 Celsius or 50–85 Fahrenheit. These are conservative sampling bounds; all observed parameters remain replayable. I varies within context-specific bounds (thermometer 90–110 F, turkey 120–180 F, soup 140–212 F, water 40–99 C, straightener 200–450 F), with I>=S+10. I affects prompt and complete-bank recipes but is excluded from task identity because I alone does not change the assessed model. Scale/context remain tied to their source masks.

Distinct task key: ambient, scale and number of supplied temperatures. Context, initial reading alone, seed, choice order and distractor profile do not establish another task. Finite policy domains: easy 31, moderate 67 before excluding existing/seen/reserved content. Canonical ambient/role keys also exclude duplicates. No plots are present; steps 5 and 7 require no new assets.

## q-105917

Observed parameters: {"S": 25}. Unit C. All slots occur in the exact source prompt, shared worked solution and observed whole bank below.

### Prompt mask

The rate at which a liquid cools is proportional to the difference between its temperature and the temperature of its surroundings. Let $T(t)$ be the temperature of the liquid in degrees Celsius, and let $t>0$ be the time in minutes. If the temperature of the surroundings is ${@@S@@}^{∘}\text{C},$ which differential equation could be used to model the temperature of the liquid? Assume that $k>0$ is a constant of proportionality.

### Solution mask

Newton's law of cooling states that the rate at which the temperature $T(t)$ of a body changes is proportional to the difference between its temperature and its surroundings. Therefore, we have the differential equation

$$
\frac{\text{d}T}{\text{d}t}=-k(T-{T}_{S}),
$$

where ${T}_{S}$ is the temperature of the surroundings, and $k>0$ is a constant of proportionality.

In our case, ${T}_{S}={@@S@@}^{∘}\text{C},$ and we have

$$
\frac{\text{d}T}{\text{d}t}=-k(T-@@S@@).
$$

### Complete bank recipes

1. `{T}^{′}(t)=-k(T-@@S@@)`

2. `{T}^{′}(t)=-kT(T-@@S@@)`

3. `{T}^{′}(t)=k(T-@@S@@)`

4. `{T}^{′}(t)=kT(T+@@S@@)`

5. `{T}^{′}(t)=kT(T-@@S@@)`

Correct recipe: -k(T-S). The remaining recipes are retained as complete displayed expressions; source replay verifies their full mathematical values, not inferred labels. Raw doubled escapes are retained for replay and normalized for normal output.

## q-37365

Observed parameters: {"S": 64, "I": 100}. Unit F. All slots occur in the exact source prompt, shared worked solution and observed whole bank below.

### Prompt mask

A medical doctor records the temperature of ${@@I@@}^{∘}\text{F}$ using a thermometer. After the measurement is taken, the temperature reading $T(t)$ of the thermometer decreases at a rate that obeys Newton's law of cooling. Here, $T$ is measured in degrees Fahrenheit, and $t>0$ is the time in minutes. If the room temperature is ${@@S@@}^{∘}\text{F},$ which differential equation could be used to model the thermometer reading? Assume that $k>0$ is a constant of proportionality.

### Solution mask

Newton's law of cooling states that the rate at which the temperature $T(t)$ of a body changes is proportional to the difference between its temperature and its surroundings. Therefore, we have the differential equation

$$
\frac{\text{d}T}{\text{d}t}=-k(T-{T}_{S}),
$$

where ${T}_{S}$ is the temperature of the surroundings, and $k>0$ is a constant of proportionality.

In our case, ${T}_{S}={@@S@@}^{∘}\text{F},$ and we have

$$
\frac{\text{d}T}{\text{d}t}=-k(T-@@S@@).
$$

### Complete bank recipes

1. `\frac{\text{d}T}{\text{d}t}=-@@S@@(T-@@I@@)`

2. `\frac{\text{d}T}{\text{d}t}=-@@I@@(T-@@S@@)`

3. `\frac{\text{d}T}{\text{d}t}=-k(T-@@I@@)`

4. `\frac{\text{d}T}{\text{d}t}=-k(T-@@SUM@@)`

5. `\frac{\text{d}T}{\text{d}t}=-k(T-@@S@@)`

Correct recipe: -k(T-S). The remaining recipes are retained as complete displayed expressions; source replay verifies their full mathematical values, not inferred labels. Raw doubled escapes are retained for replay and normalized for normal output.

## q-106883

Observed parameters: {"S": 67, "I": 145}. Unit F. All slots occur in the exact source prompt, shared worked solution and observed whole bank below.

### Prompt mask

A turkey reaches ${@@I@@}^{∘}\text{F}$ in the oven. After removing the turkey from the oven, the turkey's temperature $T(t)$ decreases at a rate that obeys Newton's law of cooling. Here, $T$ is measured in degrees Fahrenheit, and $t>0$ is the time in minutes. If the room temperature is ${@@S@@}^{∘}\text{F},$ which differential equation could be used to model the temperature of the turkey? Assume that $k>0$ is a constant of proportionality.

### Solution mask

Newton's law of cooling states that the rate at which the temperature $T(t)$ of a body changes is proportional to the difference between its temperature and its surroundings. Therefore, we have the differential equation

$$
\frac{\text{d}T}{\text{d}t}=-k(T-{T}_{S}),
$$

where ${T}_{S}$ is the temperature of the surroundings, and $k>0$ is a constant of proportionality.

In our case, ${T}_{S}={@@S@@}^{∘}\text{F},$ and we have

$$
\frac{\text{d}T}{\text{d}t}=-k(T-@@S@@).
$$

### Complete bank recipes

1. `\frac{\text{d}T}{\text{d}t}=-@@S@@(T-@@I@@)`

2. `\frac{\text{d}T}{\text{d}t}=-@@I@@(T-@@S@@)`

3. `\frac{\text{d}T}{\text{d}t}=-kT(T-@@S@@)`

4. `\frac{\text{d}T}{\text{d}t}=-k(T-@@S@@)`

5. `\frac{\text{d}T}{\text{d}t}=-k(T-@@I@@)`

Correct recipe: -k(T-S). The remaining recipes are retained as complete displayed expressions; source replay verifies their full mathematical values, not inferred labels. Raw doubled escapes are retained for replay and normalized for normal output.

## q-106934

Observed parameters: {"S": 76, "I": 200}. Unit F. All slots occur in the exact source prompt, shared worked solution and observed whole bank below.

### Prompt mask

In a restaurant kitchen, a pot of soup reaches a temperature of ${@@I@@}^{∘}\text{F}.$ After turning off the stove, the temperature $T(t)$ of the soup decreases at a rate that obeys Newton's law of cooling. Here, $T$ is measured in degrees Fahrenheit, and $t>0$ is the time in minutes. If the kitchen temperature is ${@@S@@}^{∘}\text{F},$ which differential equation could be used to model the pot temperature? Assume that $k>0$ is a constant of proportionality.

### Solution mask

Newton's law of cooling states that the rate at which the temperature $T(t)$ of a body changes is proportional to the difference between its temperature and its surroundings. Therefore, we have the differential equation

$$
\frac{\text{d}T}{\text{d}t}=-k(T-{T}_{S}),
$$

where ${T}_{S}$ is the temperature of the surroundings, and $k>0$ is a constant of proportionality.

In our case, ${T}_{S}={@@S@@}^{∘}\text{F},$ and we have

$$
\frac{\text{d}T}{\text{d}t}=-k(T-@@S@@).
$$

### Complete bank recipes

1. `\frac{\text{d}T}{\text{d}t}=-@@S@@k(T-@@I@@)`

2. `\frac{\text{d}T}{\text{d}t}=-k(T-@@I@@)`

3. `\frac{\text{d}T}{\text{d}t}=-k(T-@@S@@)`

4. `\frac{\text{d}T}{\text{d}t}=-@@I@@(T-@@S@@)`

5. `\frac{\text{d}T}{\text{d}t}=@@I@@k(T-@@S@@)`

Correct recipe: -k(T-S). The remaining recipes are retained as complete displayed expressions; source replay verifies their full mathematical values, not inferred labels. Raw doubled escapes are retained for replay and normalized for normal output.

## q-106935

Observed parameters: {"S": 19, "I": 90}. Unit C. All slots occur in the exact source prompt, shared worked solution and observed whole bank below.

### Prompt mask

A container of water at a temperature of ${@@I@@}^{∘}\text{C}$ is placed in a room. The temperature $T(t)$ of the water decreases at a rate that obeys Newton's law of cooling. Here, $T$ is measured in degrees Celsius, and $t>0$ is the time in minutes. If the room temperature is ${@@S@@}^{∘}\text{C},$ which differential equation could be used to model the water temperature? Assume that $k>0$ is a constant of proportionality.

### Solution mask

Newton's law of cooling states that the rate at which the temperature $T(t)$ of a body changes is proportional to the difference between its temperature and its surroundings. Therefore, we have the differential equation

$$
\frac{\text{d}T}{\text{d}t}=-k(T-{T}_{S}),
$$

where ${T}_{S}$ is the temperature of the surroundings, and $k>0$ is a constant of proportionality.

In our case, ${T}_{S}={@@S@@}^{∘}\text{C},$ and we have

$$
\frac{\text{d}T}{\text{d}t}=-k(T-@@S@@).
$$

### Complete bank recipes

1. `\frac{\text{d}T}{\text{d}t}=-k(T-@@S@@)`

2. `\frac{\text{d}T}{\text{d}t}=-@@I@@(T-@@S@@)`

3. `\frac{\text{d}T}{\text{d}t}=-@@I@@k(T-@@S@@)`

4. `\frac{\text{d}T}{\text{d}t}=-@@S@@k(T-@@I@@)`

5. `\frac{\text{d}T}{\text{d}t}=-k(T-@@I@@)`

Correct recipe: -k(T-S). The remaining recipes are retained as complete displayed expressions; source replay verifies their full mathematical values, not inferred labels. Raw doubled escapes are retained for replay and normalized for normal output.

## q-106936

Observed parameters: {"S": 30}. Unit C. All slots occur in the exact source prompt, shared worked solution and observed whole bank below.

### Prompt mask

The rate at which a pot of hot oil cools is proportional to the difference between its temperature and the temperature of its surroundings. Let $T(t)$ be the temperature of the liquid in degrees Celsius, and let $t>0$ be the time in minutes. If the temperature of the surroundings is ${@@S@@}^{∘}\text{C},$ which differential equation could be used to model the temperature of the oil? Assume that $k>0$ is a constant of proportionality.

### Solution mask

Newton's law of cooling states that the rate at which the temperature $T(t)$ of a body changes is proportional to the difference between its temperature and its surroundings. Therefore, we have the differential equation

$$
\frac{\text{d}T}{\text{d}t}=-k(T-{T}_{S}),
$$

where ${T}_{S}$ is the temperature of the surroundings, and $k>0$ is a constant of proportionality.

In our case, ${T}_{S}={@@S@@}^{∘}\text{C},$ and we have

$$
\frac{\text{d}T}{\text{d}t}=-k(T-@@S@@).
$$

### Complete bank recipes

1. `\frac{\text{d}T}{\text{d}t}=k(T-@@S@@)`

2. `\frac{\text{d}T}{\text{d}t}=-kT(T-@@S@@)`

3. `\frac{\text{d}T}{\text{d}t}=-k(@@S@@-T)`

4. `\frac{\text{d}T}{\text{d}t}=-k(T+@@S@@)`

5. `\frac{\text{d}T}{\text{d}t}=-k(T-@@S@@)`

Correct recipe: -k(T-S). The remaining recipes are retained as complete displayed expressions; source replay verifies their full mathematical values, not inferred labels. Raw doubled escapes are retained for replay and normalized for normal output.

## q-106937

Observed parameters: {"S": 75, "I": 450}. Unit F. All slots occur in the exact source prompt, shared worked solution and observed whole bank below.

### Prompt mask

A hair straightener reaches a temperature of ${@@I@@}^{∘}\text{F}.$ After turning it off, the temperature $T(t)$ of the straightener decreases at a rate that obeys Newton's law of cooling. Here, $T$ is measured in degrees Fahrenheit, and $t>0$ is the time in minutes. If the room temperature is ${@@S@@}^{∘}\text{F},$ which differential equation could be used to model the straightener temperature? Assume that $k>0$ is a constant of proportionality.

### Solution mask

Newton's law of cooling states that the rate at which the temperature $T(t)$ of a body changes is proportional to the difference between its temperature and its surroundings. Therefore, we have the differential equation

$$
\frac{\text{d}T}{\text{d}t}=-k(T-{T}_{S}),
$$

where ${T}_{S}$ is the temperature of the surroundings, and $k>0$ is a constant of proportionality.

In our case, ${T}_{S}={@@S@@}^{∘}\text{F},$ and we have

$$
\frac{\text{d}T}{\text{d}t}=-k(T-@@S@@).
$$

### Complete bank recipes

1. `\frac{\text{d}T}{\text{d}t}=-@@S@@k(T-@@I@@)`

2. `\frac{\text{d}T}{\text{d}t}=-@@I@@k(T-@@S@@)`

3. `\frac{\text{d}T}{\text{d}t}=-k(T-@@I@@)`

4. `\frac{\text{d}T}{\text{d}t}=-k(T-@@S@@)`

5. `\frac{\text{d}T}{\text{d}t}=-k(T+@@S@@)`

Correct recipe: -k(T-S). The remaining recipes are retained as complete displayed expressions; source replay verifies their full mathematical values, not inferred labels. Raw doubled escapes are retained for replay and normalized for normal output.

## q-106878

Observed parameters: {"S": 21}. Unit C. All slots occur in the exact source prompt, shared worked solution and observed whole bank below.

### Prompt mask

The rate at which a body cools is proportional to the difference between its temperature and the temperature of its surroundings. Let $T(t)$ be the temperature of the body in degrees Celsius, and let $t>0$ be the time in minutes. If the temperature of the surroundings is ${@@S@@}^{∘}\text{C},$ which differential equation could be used to model the temperature of the liquid? Assume that $k>0$ is a constant of proportionality.

### Solution mask

Newton's law of cooling states that the rate at which the temperature $T(t)$ of a body changes is proportional to the difference between its temperature and its surroundings. Therefore, we have the differential equation

$$
\frac{\text{d}T}{\text{d}t}=-k(T-{T}_{S}),
$$

where ${T}_{S}$ is the temperature of the surroundings, and $k>0$ is a constant of proportionality.

In our case, ${T}_{S}={@@S@@}^{∘}\text{C},$ and we have

$$
\frac{\text{d}T}{\text{d}t}=-k(T-@@S@@).
$$

### Complete bank recipes

1. `{T}^{′}(t)=kT(T-@@S@@)`

2. `{T}^{′}(t)=-kT(T-@@S@@)`

3. `{T}^{′}(t)=-k(T-@@S@@)`

4. `{T}^{′}(t)=k(T+@@S@@)`

5. `{T}^{′}(t)=-k(T+@@S@@)`

Correct recipe: -k(T-S). The remaining recipes are retained as complete displayed expressions; source replay verifies their full mathematical values, not inferred labels. Raw doubled escapes are retained for replay and normalized for normal output.

## q-106932

Observed parameters: {"S": 16}. Unit C. All slots occur in the exact source prompt, shared worked solution and observed whole bank below.

### Prompt mask

The rate at which a cup of chocolate cools is proportional to the difference between its temperature and the temperature of its surroundings. Let $T(t)$ be the temperature of the chocolate in degrees Celsius, and let $t>0$ be the time in minutes. If the temperature of the surroundings is ${@@S@@}^{∘}\text{C},$ which differential equation could be used to model the temperature of the liquid? Assume that $k>0$ is a constant of proportionality.

### Solution mask

Newton's law of cooling states that the rate at which the temperature $T(t)$ of a body changes is proportional to the difference between its temperature and its surroundings. Therefore, we have the differential equation

$$
\frac{\text{d}T}{\text{d}t}=-k(T-{T}_{S}),
$$

where ${T}_{S}$ is the temperature of the surroundings, and $k>0$ is a constant of proportionality.

In our case, ${T}_{S}={@@S@@}^{∘}\text{C},$ and we have

$$
\frac{\text{d}T}{\text{d}t}=-k(T-@@S@@).
$$

### Complete bank recipes

1. `{T}^{′}(t)=kT(T+@@S@@)`

2. `{T}^{′}(t)=-k(T-@@S@@)`

3. `{T}^{′}(t)=-k(T+@@S@@)`

4. `{T}^{′}(t)=k(T-@@S@@)`

5. `{T}^{′}(t)=kT(T-@@S@@)`

Correct recipe: -k(T-S). The remaining recipes are retained as complete displayed expressions; source replay verifies their full mathematical values, not inferred labels. Raw doubled escapes are retained for replay and normalized for normal output.

## Supported corrections

For q-106936 normal output preserves the other four recipes and replaces the equivalent wrong -k(S-T) with -kT, retaining five unequal choices. This is an explicit bank correction. Other normal banks retain every observed complete recipe. Body/liquid, oil/liquid, soup/pot and chocolate/liquid slips are corrected with consistent object names.

## Source fidelity and variation

validate.py exactly replays all nine prompts, all nine complete banks (45/45 options), all keys and all worked solutions. Independent symbolic checks verify the displayed givens, complete equations, unique correct selection and the two rendered solution equations. All ambient values and initial boundary values are swept per template. Changed-ambient controls hold context and initial fixed; initial-only controls keep the same task key. review.md places every raw original alongside its normal counterpart and changed variants.
