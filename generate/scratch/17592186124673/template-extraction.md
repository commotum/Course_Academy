# Template extraction

## Stage1 — original instances

Exact prompt, source answer fields, complete choices, correct refs and entire solutions are preserved in source.json; source-cases.json declares actual parameter recipes. The mapping below enumerates every option of every source field, including the legacy field.


### q-106661 / factored_equation / observed_106661

Parameters: `{"a": 150, "k": "0.5"}`

Prompt: Given that $y < 150$ and $t \ge 0$, which of the following is an inhibited growth equation?

Field 0 id 79311994-ead5-5028-b4a4-de97196cfb35 /selection/radio

| Original value | Parameterized complete value recipe | Designation |
|---|---|---|
|`\frac{dy}{dt} =-0.5(y + 150)`|−k(y+a)|not designated|
|`\frac{dy}{dt} = 150(y + 0.5)`|a(y+k)|not designated|
|`\frac{dy}{dt} = 150(y - 0.5)`|a(y−k)|not designated|
|`\frac{dy}{dt} = 0.5(150 - y)`|k(a−y) correct|not designated|
|`\frac{dy}{dt} = 0.5(y - 150)`|k(y−a)|not designated|

Worked solution: ABSENT; raw replay keeps it absent.

### q-106662 / expanded_equation / observed_106662

Parameters: `{"a": 80, "k": 5}`

Prompt: Given that $y<80$ and $t\ge 0,$ which of the following is an inhibited growth equation?

Field 0 id b4164cc7-8b43-5b53-b800-89f7a6270478 /selection/radio

| Original value | Parameterized complete value recipe | Designation |
|---|---|---|
|`\frac{dy}{dt} = 5y^{2} - 400`|ky²−ka|not designated|
|`\frac{dy}{dt} = 5 - 400y`|k−ka·y|not designated|
|`\frac{dy}{dt} = 400 - 5y`|ka−ky correct|not designated|
|`\frac{dy}{dt} = 5y - 400`|ky−ka|not designated|
|`\frac{dy}{dt} = 400 - 5y^{2}`|ka−ky²|not designated|

Field 1 id 1b3476a6-1afc-5395-a095-cd169e19c687 /selection/radio

| Original value | Parameterized complete value recipe | Designation |
|---|---|---|
|`\frac{dy}{dt}=5-400y`|k−ka·y|wrong|
|`\frac{dy}{dt}=5y-400`|ky−ka|wrong|
|`\frac{dy}{dt}=400-5y`|ka−ky correct|correct|
|`\frac{dy}{dt}=5{y}^{2}-400`|ky²−ka|wrong|
|`\frac{dy}{dt}=400-5{y}^{2}`|ka−ky²|wrong|

Worked solution: An inhibited growth equation has the form

$$
\frac{dy}{dt}=k(a-y),
$$

where $k>0$ is a constant of proportionality, and $a>y$ for all $t\ge 0.$

From the given options, the only inhibited growth equation is

$$
\frac{dy}{dt}=400-5y.
$$

To see this, let's factor the right-hand side of the equation. This gives

$$
\frac{dy}{dt}=5(80-y).
$$

In this case, the constant of proportionality is $k=5,$ and $a=80.$ Note that for inhibited growth, we must have $y<80$ for all $t\ge 0.$

### q-106663 / factored_ivp / observed_106663

Parameters: `{"a": 250, "k": 3, "initials": [200, 400, 150, 50, 100]}`

Prompt: Which of the following initial value problems is an inhibited growth problem?

Field 0 id 177efa5e-2726-5c7f-b592-713face07fe6 /selection/radio

| Original value | Parameterized complete value recipe | Designation |
|---|---|---|
|`\frac{dy}{dt}=3(y-250),\,y(0)=200`|k(y−a),initials[0]|wrong|
|`\frac{dy}{dt}=3(250-y),\,y(0)=400`|k(a−y),initials[1]>a|wrong|
|`\frac{dy}{dt}=3(250-y),\,y(0)=150`|k(a−y),initials[2]<a correct|correct|
|`\frac{dy}{dt}=3y(y-250),\,y(0)=50`|ky(y−a),initials[3]|wrong|
|`\frac{dy}{dt}=-3(y+250),\,y(0)=100`|−k(y+a),initials[4]|wrong|

Worked solution: An inhibited growth initial value problem has the form

$$
\frac{dy}{dt}=k(a-y),\,y(0)={y}_{0}
$$

where $k>0$ is a constant of proportionality, and $a>y$ for all $t\ge 0.$

From the given options, the only inhibited growth problem is

$$
\frac{dy}{dt}=3(250-y),\,y(0)=150.
$$

In this case, $k=3,a=250,$ and ${y}_{0}=150.$ Notice that $a>{y}_{0},$ which is required for inhibited growth. 

The other options do not represent inhibited growth. In particular, the initial value problem

$$
\frac{dy}{dt}=3(250-y),\,y(0)=400,
$$

does *not* represent inhibited growth model because ${y}_{0}=400>a=250.$

### q-37176 / expanded_ivp / observed_37176

Parameters: `{"options": [{"c": "5700", "b": "-0.8", "initial": "7200"}, {"c": "-875", "b": "0.02", "initial": "47500"}, {"c": "-19734", "b": "22", "initial": "20000"}, {"c": "690", "b": "-0.003", "initial": "200000"}, {"c": "1250", "b": "-0.005", "initial": "270000"}]}`

Prompt: Which of the following initial value problems is an inhibited growth problem?

Field 0 id 6bac56d3-4bd4-55bb-aa6f-dc8f9891aec6 /selection/radio

| Original value | Parameterized complete value recipe | Designation |
|---|---|---|
|`\frac{dP}{dt}=5\,700-0.8P,\,P(0)=7\,200`|Independent affine object options[0]: c+bP, P(0)=initial; k=−b, a=−c/b|wrong|
|`\frac{dP}{dt}=0.02P-875,\,P(0)=47\,500`|Independent affine object options[1]: c+bP, P(0)=initial; k=−b, a=−c/b|wrong|
|`\frac{dP}{dt}=22P-19\,734,\,P(0)=20\,000`|Independent affine object options[2]: c+bP, P(0)=initial; k=−b, a=−c/b|wrong|
|`\frac{dP}{dt}=690-0.003P,\,P(0)=200\,000`|Independent affine object options[3]: c+bP, P(0)=initial; k=−b, a=−c/b|correct|
|`\frac{dP}{dt}=1\,250-0.005P,\,P(0)=270\,000`|Independent affine object options[4]: c+bP, P(0)=initial; k=−b, a=−c/b|wrong|

Worked solution: An inhibited growth initial value problem has the form

$$
\frac{dy}{dt}=k(a-y),\,y(0)={y}_{0}
$$

where $k>0$ is a constant of proportionality, and $a>y$ for all $t\ge 0.$

From the given options, the only inhibited growth problem is

$$
\frac{dP}{dt}=690-0.003P,\,P(0)=200\,000,
$$

since

$$
\frac{dP}{dt}=690-0.003P=0.003(230\,000-P).
$$

In this case, $k=0.003,a=230\,000,$ and ${y}_{0}=200\,000.$ Notice that $a>{y}_{0},$ which is required for inhibited growth. 

The other options do not represent inhibited growth. In particular, the initial value problems

$$
\frac{dP}{dt}=1\,250-0.005P=0.005(250\,000-P),\,P(0)=270\,000,
$$

and

$$
\frac{dP}{dt}=5\,700-0.8P=0.8(7\,125-P),\,P(0)=7\,200
$$

do *not* represent an inhibited growth model because ${y}_{0}=270\,000>a=250\,000,$ and ${y}_{0}=7\,200>a=7\,125.$

### q-37177 / expanded_ivp / observed_37177

Parameters: `{"options": [{"c": "7", "b": "-0.0002", "initial": "38000"}, {"c": "8200", "b": "-40", "initial": "210"}, {"c": "-321", "b": "3", "initial": "120"}, {"c": "450", "b": "-0.03", "initial": "16000"}, {"c": "830", "b": "-0.8", "initial": "1000"}]}`

Prompt: Which of the following initial value problems is an inhibited growth problem?

Field 0 id 29089e7f-1a1a-5390-8184-20fce54bffdd /selection/radio

| Original value | Parameterized complete value recipe | Designation |
|---|---|---|
|`\frac{dP}{dt}=7-0.000\,2P,\,P(0)=38\,000`|Independent affine object options[0]: c+bP, P(0)=initial; k=−b, a=−c/b|wrong|
|`\frac{dP}{dt}=8\,200-40P,\,P(0)=210`|Independent affine object options[1]: c+bP, P(0)=initial; k=−b, a=−c/b|wrong|
|`\frac{dP}{dt}=3P-321,\,P(0)=120`|Independent affine object options[2]: c+bP, P(0)=initial; k=−b, a=−c/b|wrong|
|`\frac{dP}{dt}=450-0.03P,\,P(0)=16\,000`|Independent affine object options[3]: c+bP, P(0)=initial; k=−b, a=−c/b|wrong|
|`\frac{dP}{dt}=830-0.8P,\,P(0)=1\,000`|Independent affine object options[4]: c+bP, P(0)=initial; k=−b, a=−c/b|correct|

Worked solution: An inhibited growth initial value problem has the form

$$
\frac{dy}{dt}=k(a-y),\,y(0)={y}_{0}
$$

where $k>0$ is a constant of proportionality, and $a>y$ for all $t\ge 0.$

From the given options, the only inhibited growth problem is

$$
\frac{dP}{dt}=830-0.8P,\,P(0)=1\,000,
$$

since

$$
\frac{dP}{dt}=830-0.8P=0.8(1\,037.5-P).
$$

In this case, $k=0.8,a=1\,037.5,$ and ${y}_{0}=1\,000.$ Notice that $a>{y}_{0},$ which is required for inhibited growth. 

The other options do not represent inhibited growth. In particular, the initial value problems

$$
\frac{dP}{dt}=7-0.000\,2P=0.000\,2(35\,000-P),\,P(0)=38\,000,
$$

$$
\frac{dP}{dt}=450-0.03P=0.03(15\,000-P),\,P(0)=16\,000,
$$

and

$$
\frac{dP}{dt}=8\,200-40P=40(205-P),\,P(0)=210
$$

do *not* represent an inhibited growth model because ${y}_{0}=38\,000>a=35\,000,$ ${y}_{0}=16\,000>a=15\,000,$ and ${y}_{0}=210>a=205.$

### q-37180 / expanded_ivp / observed_37180

Parameters: `{"options": [{"c": "12510", "b": "-18", "initial": "690"}, {"c": "-123", "b": "0.5", "initial": "2500"}, {"c": "-6066", "b": "9", "initial": "680"}, {"c": "2580", "b": "-0.6", "initial": "4400"}, {"c": "16256", "b": "-4", "initial": "4070"}]}`

Prompt: Which of the following initial value problems is an inhibited growth problem?

Field 0 id f34c38b1-0c67-5df9-bd25-f72ef39097ba /selection/radio

| Original value | Parameterized complete value recipe | Designation |
|---|---|---|
|`\frac{dP}{dt}=12\,510-18P,\,P(0)=690`|Independent affine object options[0]: c+bP, P(0)=initial; k=−b, a=−c/b|correct|
|`\frac{dP}{dt}=0.5P-1\,23,\,P(0)=2\,500`|Independent affine object options[1]: c+bP, P(0)=initial; k=−b, a=−c/b|wrong|
|`\frac{dP}{dt}=9P-6\,066,\,P(0)=680`|Independent affine object options[2]: c+bP, P(0)=initial; k=−b, a=−c/b|wrong|
|`\frac{dP}{dt}=2\,580-0.6P,\,P(0)=4\,400`|Independent affine object options[3]: c+bP, P(0)=initial; k=−b, a=−c/b|wrong|
|`\frac{dP}{dt}=16\,256-4P,\,P(0)=4\,070`|Independent affine object options[4]: c+bP, P(0)=initial; k=−b, a=−c/b|wrong|

Worked solution: An inhibited growth initial value problem has the form

$$
\frac{dy}{dt}=k(a-y),\,y(0)={y}_{0}
$$

where $k>0$ is a constant of proportionality, and $a>y$ for all $t\ge 0.$

From the given options, the only inhibited growth problem is

$$
\frac{dP}{dt}=12\,510-18P,\,P(0)=690,
$$

since

$$
\frac{dP}{dt}=12\,510-18P=18(695-P).
$$

In this case, $k=18,a=695,$ and ${y}_{0}=690.$ Notice that $a>{y}_{0},$ which is required for inhibited growth. 

The other options do not represent inhibited growth. In particular, the initial value problems

$$
\frac{dP}{dt}=16\,256-4P=4(4\,064-P),\,P(0)=4\,070,
$$

and

$$
\frac{dP}{dt}=2\,580-0.6P=0.6(4\,300-P),\,P(0)=4\,400
$$

do *not* represent an inhibited growth model because ${y}_{0}=4\,070>a=4\,064,$ and ${y}_{0}=4\,400>a=4\,300.$

## Stage2 — generalized pattern

An inhibited growth model is a negative-slope linear RHS with the stated limiting level, k(a−y), k>0. When a bound y<a is supplied, the correct candidate must grow throughout that declared range; a different equilibrium cannot establish that. For an IVP, additionally initial<a. Factored recognition is easy (inferred); expanded integer coefficients require factoring (observed moderate); factored or heterogeneous expanded IVPs add initial-condition discrimination (observed hard). Every variation at a level has the same assessed demands; there is no staged progression and no new solving skill.

## Stage3 — complete components and bank accounting

Every source choice above is an entire equation or entire IVP, not separately compared equation sides. Factored bank sign/reversal/swap/nonlinearity operations are defensible actual-method distractors. Expanded-equation swap k−ka·y has negative slope but its cap1/a differs from the declared a; it is ineligible under the stated range. Heterogeneous hard original banks hold five independent affine triples (intercept c, slope b, initial) with exactly one negative-slope below-cap model, two or three negative-slope above-cap objects and the remaining reversed-slope objects. Their independent intercept/rate numbers are not evidence of an inferred scalar-error algorithm. They are publicly replayable with new complete parameters and fixed role positions; raw evidence profiles are not weighted as normal defaults.

There are7/7 exact complete raw banks and35/35 exact options. Present wrong-designation count20/20 corresponds to the five source banks with correct refs; the other10 choices cannot be called observed distractors without inferring their missing designation. Independent mathematics identifies4 wrong choices in each of those2 missing-ref banks for normal completion, separately labeled authored/inferred. Source solutions:5/5 exact whole prose and display-stage sequences; absent1 is not an exact solution match.

## Stage4 — reusable templates, conditions and workload

Fixed components: original instructional sentences and formal k(a−y) definition; prompt question relation; five radio choices; one fixed worked solution. Variable components: complete numerical coefficients/caps/initial values everywhere in math and prose. Optional source attributes: q106661 difficulty, correct and solution are absent; q106662 legacy field is raw-only. Conditional components: expanded equation factoring paragraph; hard affine correct-factor row and two/three explicit excluded above-cap model rows; normal P teaching row uses P throughout while raw source preserves the original generic y definition. Nonstandard1\,23 grouping is raw-only. Formula arguments/variable names are built as complete components, not blind scalar replacements.

Domains enforced on sampling AND explicit inputs: factored equation/factored IVP2≤a≤500 and0.1≤k≤20; distinct a,k in easy prevents a swap collision. Moderate uses integer a,k withka≤10000. Factored-IVP five nonnegative initials≤1000 with second initial>a and third initial<a. Hard affine |c|≤100000,0.0001≤|b|≤40,0≤initial≤500000, c and b opposite signs, capacity1..500000, all rates/caps/initials have at most4 decimal places and terminating decimal form. Exactly one below-cap negative-slope candidate; complete fixed profile slope counts and raw role positions; reject duplicate whole IVPs. Bounds preserve source workload of one linear factor or at most one rational division per considered affine model, followed by initial comparison; no arbitrary transcendental evaluation is introduced.

Normal parameter samplers: easy50 caps×6 rates=300 substantive model pairs; moderate20 caps×9 rates=180 pairs; factored hard9 caps×8 rates=72 correct-model/initial tasks; heterogeneous hard16 rates, capacity multiples of100 from200 through min(100000,100000/rate), optional half-unit caps, and10 positive gaps per candidate. This enumerates205300 distinct correct rate/cap/initial triples per below-cap role after clamped-endpoint deduplication; only substantive recovered-cap/initial triples count, and distractor variation does not inflate that count. Wrong-bank variation and variable aliases do not inflate canonical mathematical-task counts. None of these finite counts claim recovery of the original sampler. Normal hard chooses factored or heterogeneous families; profiles2/3 denote fixed comparison count, not progression.

Identity: actual prompt, full fixed solution, complete banks and designation presence plus version determine content UUID/hash. Seed/order cannot change it. Canonical mathematical fingerprint uses exact reduced assessed model/cap/initial rather than number spelling, source id, profile, bank or seed. Owned answer UUIDs are field scoped. No database/Math Academy identities are fabricated. The CLI and public API permit explicit parameter/profile raw replay and handle absent solutions/difficulty/correct refs.

No plots were found; steps5/7 complete as none. No plotted-source extraction or image renderer is needed. Stop before database preparation.

