# Template extraction

## 1. Specific original descriptions

Every original asks major first and minor second, using x and y as coordinates and a,b as horizontal/vertical radius labels. Positive integer squared radii determine the number-form workload; denominators are not radii. Radio answers are text containing two separate inline math fragments joined by “and”; blanks supply the axis-length sentences and expect delimiter-free math fragments. Source field order is retained even where field-2 precedes field-1. Per-original number forms, complete banks and solutions follow in review.md; the classification table records all exact squared-radius pairs and layouts.

## 2. Shared pattern

Identify a²=dx,b²=dy from the already normalized origin-centered standard equation. Take a=√dx,b=√dy. Choose the larger radius as semi-major and smaller as semi-minor; double each. The same complete fixed solution applies regardless of selected wrong answer. Blanks ask for the two scalar lengths; radios ask for an ordered pair.

## 3. Components and complete bank map

Notation: U=max(dx,dy), V=min(dx,dy), A=√U, B=√V. Each recipe below is a complete pair of mathematical expressions. Recipe number is the original bank position, not a correctness-independent random perturbation. All values reproduce literally at original inputs; complete banks are preserved together, and a collision rejects the entire changed instance. Original distractor intent cannot be recovered from scalar values alone. “Opaque” explicitly marks weak arithmetic evidence, retained only by an explicit observed replay profile. Other operations are explicit generalizations, with original intent still unverified. Authored defaults use correct(2A,2B), omit both doubles(A,B), omit minor double(2A,B), omit major double(A,2B), and use squared radii(U,V).

All source fields, values, designated correct values, presence/absence, parameter inputs and recipe expressions are mapped below.

### q-7598: dx=4, dy=16; radio_so

Horizontal radius: $2$; vertical radius: $4$. Major orientation: vertical. 0 nonsquare integer radicands.

Field `selection`: `:answer-field.type/radio`. Correct ref: $8$ and $4$.

|position|original value|parameterized pair|evidence status|
|---:|---|---|---|
|1|$6$ and $2$|`sqrt(U) + sqrt(V)`, `sqrt(V)`|explicit arithmetic generalization; original intent unverified|
|2|$8$ and $4$|`2*sqrt(U)`, `2*sqrt(V)`|explicit arithmetic generalization; original intent unverified|
|3|$6$ and $4$|`sqrt(U) + sqrt(V)`, `2*sqrt(V)`|explicit arithmetic generalization; original intent unverified|
|4|$4$ and $2$|`sqrt(U)`, `sqrt(V)`|explicit arithmetic generalization; original intent unverified|
|5|$8$ and $2$|`2*sqrt(U)`, `sqrt(V)`|explicit arithmetic generalization; original intent unverified|

Profile: `observed_q-7598`.

### q-7600: dx=10, dy=9; radio_unrated

Horizontal radius: $\sqrt{10}$; vertical radius: $3$. Major orientation: horizontal. 1 nonsquare integer radicands.

Field `selection`: `:answer-field.type/radio`. Correct ref: absent; inference separately recorded.

|position|original value|parameterized pair|evidence status|
|---:|---|---|---|
|1|$6$ and $5$|`2*sqrt(V)`, `5*sqrt(V)/3`|opaque numerical evidence|
|2|$2\sqrt{10}$ and $6$|`2*sqrt(U)`, `2*sqrt(V)`|explicit arithmetic generalization; original intent unverified|
|3|$6$ and $2$|`2*sqrt(V)`, `2*sqrt(V)/3`|opaque numerical evidence|
|4|$\sqrt{10}$ and $3$|`sqrt(U)`, `sqrt(V)`|explicit arithmetic generalization; original intent unverified|
|5|$5$ and $3$|`5*sqrt(V)/3`, `sqrt(V)`|opaque numerical evidence|

Profile: `observed_q-7600`.

### q-115132: dx=16, dy=7; radio_thus

Horizontal radius: $4$; vertical radius: $\sqrt{7}$. Major orientation: horizontal. 1 nonsquare integer radicands.

Field `selection`: `:answer-field.type/radio`. Correct ref: $8$ and $2\sqrt{7}$.

|position|original value|parameterized pair|evidence status|
|---:|---|---|---|
|1|$16$ and $7$|`U`, `V`|explicit arithmetic generalization; original intent unverified|
|2|$14$ and $8$|`2*V`, `2*sqrt(U)`|opaque numerical evidence|
|3|$8$ and $3.5$|`U/2`, `V/2`|explicit arithmetic generalization; original intent unverified|
|4|$4$ and $\sqrt{7}$|`sqrt(U)`, `sqrt(V)`|explicit arithmetic generalization; original intent unverified|
|5|$8$ and $2\sqrt{7}$|`2*sqrt(U)`, `2*sqrt(V)`|explicit arithmetic generalization; original intent unverified|

Profile: `observed_q-115132`.

### q-115135: dx=100, dy=25; radio_thus

Horizontal radius: $10$; vertical radius: $5$. Major orientation: horizontal. 0 nonsquare integer radicands.

Field `selection`: `:answer-field.type/radio`. Correct ref: $20$ and $10$.

|position|original value|parameterized pair|evidence status|
|---:|---|---|---|
|1|$20$ and $10$|`2*sqrt(U)`, `2*sqrt(V)`|explicit arithmetic generalization; original intent unverified|
|2|$5$ and $2.5$|`sqrt(U)/2`, `sqrt(V)/2`|explicit arithmetic generalization; original intent unverified|
|3|$50$ and $12.5$|`U/2`, `V/2`|explicit arithmetic generalization; original intent unverified|
|4|$100$ and $25$|`U`, `V`|explicit arithmetic generalization; original intent unverified|
|5|$10$ and $5$|`sqrt(U)`, `sqrt(V)`|explicit arithmetic generalization; original intent unverified|

Profile: `observed_q-115135`.

### q-16452: dx=4, dy=2; radio_so

Horizontal radius: $2$; vertical radius: $\sqrt{2}$. Major orientation: horizontal. 1 nonsquare integer radicands.

Field `selection`: `:answer-field.type/radio`. Correct ref: $4$ and $2\sqrt{2}$.

|position|original value|parameterized pair|evidence status|
|---:|---|---|---|
|1|$2\sqrt{2}$ and $\sqrt{2}$|`sqrt(2)*sqrt(U)`, `sqrt(V)`|explicit arithmetic generalization; original intent unverified|
|2|$4$ and $2\sqrt{2}$|`2*sqrt(U)`, `2*sqrt(V)`|explicit arithmetic generalization; original intent unverified|
|3|$8$ and $4$|`2*U`, `2*V`|explicit arithmetic generalization; original intent unverified|
|4|$4$ and $2$|`U`, `V`|explicit arithmetic generalization; original intent unverified|
|5|$2\sqrt{2}$ and $2$|`sqrt(2)*sqrt(U)`, `sqrt(U)`|explicit arithmetic generalization; original intent unverified|

Profile: `observed_q-16452`.

### q-16454: dx=3, dy=12; radio_so

Horizontal radius: $\sqrt{3}$; vertical radius: $2\sqrt{3}$. Major orientation: vertical. 2 nonsquare integer radicands.

Field `selection`: `:answer-field.type/radio`. Correct ref: $4\sqrt{3}$ and $2\sqrt{3}$.

|position|original value|parameterized pair|evidence status|
|---:|---|---|---|
|1|$4\sqrt{3}$ and $\sqrt{3}$|`2*sqrt(U)`, `sqrt(V)`|explicit arithmetic generalization; original intent unverified|
|2|$2\sqrt{3}$ and $\sqrt{3}$|`sqrt(U)`, `sqrt(V)`|explicit arithmetic generalization; original intent unverified|
|3|$12$ and $3$|`U`, `V`|explicit arithmetic generalization; original intent unverified|
|4|$4\sqrt{3}$ and $2\sqrt{3}$|`2*sqrt(U)`, `2*sqrt(V)`|explicit arithmetic generalization; original intent unverified|
|5|$6$ and $3$|`U/2`, `V`|opaque numerical evidence|

Profile: `observed_q-16454`.

### q-277923: dx=64, dy=81; blank_newline

Horizontal radius: $8$; vertical radius: $9$. Major orientation: vertical. 0 nonsquare integer radicands.

Field `field-1`: `:answer-field.type/blank`. Correct ref: 18.

Value `18`; recipe `2*sqrt(U)`.

Field `field-2`: `:answer-field.type/blank`. Correct ref: 16.

Value `16`; recipe `2*sqrt(V)`.

### q-279165: dx=9, dy=4; blank

Horizontal radius: $3$; vertical radius: $2$. Major orientation: horizontal. 0 nonsquare integer radicands.

Field `field-2`: `:answer-field.type/blank`. Correct ref: 4.

Value `4`; recipe `2*sqrt(V)`.

Field `field-1`: `:answer-field.type/blank`. Correct ref: 6.

Value `6`; recipe `2*sqrt(U)`.

### q-279166: dx=36, dy=16; blank

Horizontal radius: $6$; vertical radius: $4$. Major orientation: horizontal. 0 nonsquare integer radicands.

Field `field-1`: `:answer-field.type/blank`. Correct ref: 12.

Value `12`; recipe `2*sqrt(U)`.

Field `field-2`: `:answer-field.type/blank`. Correct ref: 8.

Value `8`; recipe `2*sqrt(V)`.

### q-279169: dx=4, dy=25; blank

Horizontal radius: $2$; vertical radius: $5$. Major orientation: vertical. 0 nonsquare integer radicands.

Field `field-1`: `:answer-field.type/blank`. Correct ref: 10.

Value `10`; recipe `2*sqrt(U)`.

Field `field-2`: `:answer-field.type/blank`. Correct ref: 4.

Value `4`; recipe `2*sqrt(V)`.

### q-279172: dx=36, dy=5; blank

Horizontal radius: $6$; vertical radius: $\sqrt{5}$. Major orientation: horizontal. 1 nonsquare integer radicands.

Field `field-1`: `:answer-field.type/blank`. Correct ref: 12.

Value `12`; recipe `2*sqrt(U)`.

Field `field-2`: `:answer-field.type/blank`. Correct ref: 2\sqrt{5}.

Value `2\sqrt{5}`; recipe `2*sqrt(V)`.

### q-279174: dx=12, dy=9; blank

Horizontal radius: $2\sqrt{3}$; vertical radius: $3$. Major orientation: horizontal. 1 nonsquare integer radicands.

Field `field-2`: `:answer-field.type/blank`. Correct ref: 6.

Value `6`; recipe `2*sqrt(V)`.

Field `field-1`: `:answer-field.type/blank`. Correct ref: 4\sqrt{3}.

Value `4\sqrt{3}`; recipe `2*sqrt(U)`.

### q-279197: dx=12, dy=49; blank

Horizontal radius: $2\sqrt{3}$; vertical radius: $7$. Major orientation: vertical. 1 nonsquare integer radicands.

Field `field-2`: `:answer-field.type/blank`. Correct ref: 4\sqrt{3}.

Value `4\sqrt{3}`; recipe `2*sqrt(V)`.

Field `field-1`: `:answer-field.type/blank`. Correct ref: 14.

Value `14`; recipe `2*sqrt(U)`.

### q-69563: dx=4, dy=49; radio_so

Horizontal radius: $2$; vertical radius: $7$. Major orientation: vertical. 0 nonsquare integer radicands.

Field `selection`: `:answer-field.type/radio`. Correct ref: $14$ and $4$.

|position|original value|parameterized pair|evidence status|
|---:|---|---|---|
|1|$14$ and $4$|`2*sqrt(U)`, `2*sqrt(V)`|explicit arithmetic generalization; original intent unverified|
|2|$14\sqrt{2}$ and $4\sqrt{2}$|`2*sqrt(2)*sqrt(U)`, `2*sqrt(2)*sqrt(V)`|explicit arithmetic generalization; original intent unverified|
|3|$7$ and $4$|`sqrt(U)`, `2*sqrt(V)`|explicit arithmetic generalization; original intent unverified|
|4|$7$ and $2$|`sqrt(U)`, `sqrt(V)`|explicit arithmetic generalization; original intent unverified|
|5|$7\sqrt{2}$ and $2\sqrt{2}$|`sqrt(2)*sqrt(U)`, `sqrt(2)*sqrt(V)`|explicit arithmetic generalization; original intent unverified|

Profile: `observed_q-69563`.

### q-7595: dx=16, dy=9; radio_so_space

Horizontal radius: $4$; vertical radius: $3$. Major orientation: horizontal. 0 nonsquare integer radicands.

Field `selection`: `:answer-field.type/radio`. Correct ref: $8$ and $6$.

|position|original value|parameterized pair|evidence status|
|---:|---|---|---|
|1|$4$ and $3$|`sqrt(U)`, `sqrt(V)`|explicit arithmetic generalization; original intent unverified|
|2|$6$ and $4$|`2*sqrt(V)`, `sqrt(U)`|explicit arithmetic generalization; original intent unverified|
|3|$12$ and $8$|`4*sqrt(V)`, `2*sqrt(U)`|explicit arithmetic generalization; original intent unverified|
|4|$8$ and $6$|`2*sqrt(U)`, `2*sqrt(V)`|explicit arithmetic generalization; original intent unverified|
|5|$8$ and $3$|`2*sqrt(U)`, `sqrt(V)`|explicit arithmetic generalization; original intent unverified|

Profile: `observed_q-7595`.

### q-7601: dx=16, dy=25; radio_so

Horizontal radius: $4$; vertical radius: $5$. Major orientation: vertical. 0 nonsquare integer radicands.

Field `selection`: `:answer-field.type/radio`. Correct ref: $10$ and $8$.

|position|original value|parameterized pair|evidence status|
|---:|---|---|---|
|1|$5$ and $4$|`sqrt(U)`, `sqrt(V)`|explicit arithmetic generalization; original intent unverified|
|2|$25$ and $16$|`U`, `V`|explicit arithmetic generalization; original intent unverified|
|3|$\sqrt{5}$ and $2$|`U**(1/4)`, `V**(1/4)`|explicit arithmetic generalization; original intent unverified|
|4|$10$ and $8$|`2*sqrt(U)`, `2*sqrt(V)`|explicit arithmetic generalization; original intent unverified|
|5|$50$ and $32$|`2*U`, `2*V`|explicit arithmetic generalization; original intent unverified|

Profile: `observed_q-7601`.

### q-279198: dx=8, dy=24; blank

Horizontal radius: $2\sqrt{2}$; vertical radius: $2\sqrt{6}$. Major orientation: vertical. 2 nonsquare integer radicands.

Field `field-2`: `:answer-field.type/blank`. Correct ref: 4\sqrt{2}.

Value `4\sqrt{2}`; recipe `2*sqrt(V)`.

Field `field-1`: `:answer-field.type/blank`. Correct ref: 4\sqrt{6}.

Value `4\sqrt{6}`; recipe `2*sqrt(U)`.

### q-7596: dx=9, dy=18; radio_so

Horizontal radius: $3$; vertical radius: $3\sqrt{2}$. Major orientation: vertical. 1 nonsquare integer radicands.

Field `selection`: `:answer-field.type/radio`. Correct ref: $6\sqrt{2}$ and $6$.

|position|original value|parameterized pair|evidence status|
|---:|---|---|---|
|1|$6\sqrt{2}$ and $3$|`2*sqrt(U)`, `sqrt(V)`|explicit arithmetic generalization; original intent unverified|
|2|$3\sqrt{2}$ and $3$|`sqrt(U)`, `sqrt(V)`|explicit arithmetic generalization; original intent unverified|
|3|$6$ and $3$|`2*sqrt(V)`, `sqrt(V)`|explicit arithmetic generalization; original intent unverified|
|4|$18$ and $9$|`U`, `V`|explicit arithmetic generalization; original intent unverified|
|5|$6\sqrt{2}$ and $6$|`2*sqrt(U)`, `2*sqrt(V)`|explicit arithmetic generalization; original intent unverified|

Profile: `observed_q-7596`.

### q-7597: dx=20, dy=16; radio_so

Horizontal radius: $2\sqrt{5}$; vertical radius: $4$. Major orientation: horizontal. 1 nonsquare integer radicands.

Field `selection`: `:answer-field.type/radio`. Correct ref: $4\sqrt{5}$ and $8$.

|position|original value|parameterized pair|evidence status|
|---:|---|---|---|
|1|$4\sqrt{5}$ and $8$|`2*sqrt(U)`, `2*sqrt(V)`|explicit arithmetic generalization; original intent unverified|
|2|$2\sqrt{5}$ and $4$|`sqrt(U)`, `sqrt(V)`|explicit arithmetic generalization; original intent unverified|
|3|$20$ and $16$|`U`, `V`|explicit arithmetic generalization; original intent unverified|
|4|$10$ and $8$|`U/2`, `V/2`|explicit arithmetic generalization; original intent unverified|
|5|$\sqrt{5}$ and $2$|`sqrt(U)/2`, `sqrt(V)/2`|explicit arithmetic generalization; original intent unverified|

Profile: `observed_q-7597`.

### q-115134: dx=49, dy=36; radio_thus

Horizontal radius: $7$; vertical radius: $6$. Major orientation: horizontal. 0 nonsquare integer radicands.

Field `selection`: `:answer-field.type/radio`. Correct ref: $14$ and $12$.

|position|original value|parameterized pair|evidence status|
|---:|---|---|---|
|1|$28$ and $24$|`4*sqrt(U)`, `4*sqrt(V)`|explicit arithmetic generalization; original intent unverified|
|2|$24.5$ and $18$|`U/2`, `V/2`|explicit arithmetic generalization; original intent unverified|
|3|$14$ and $12$|`2*sqrt(U)`, `2*sqrt(V)`|explicit arithmetic generalization; original intent unverified|
|4|$49$ and $36$|`U`, `V`|explicit arithmetic generalization; original intent unverified|
|5|$7$ and $6$|`sqrt(U)`, `sqrt(V)`|explicit arithmetic generalization; original intent unverified|

Profile: `observed_q-115134`.

### q-16455: dx=1, dy=8; radio_so

Horizontal radius: $1$; vertical radius: $2\sqrt{2}$. Major orientation: vertical. 1 nonsquare integer radicands.

Field `selection`: `:answer-field.type/radio`. Correct ref: $4\sqrt{2}$ and $2$.

|position|original value|parameterized pair|evidence status|
|---:|---|---|---|
|1|$8$ and $1$|`U`, `V`|explicit arithmetic generalization; original intent unverified|
|2|$2\sqrt{2}$ and $1$|`sqrt(U)`, `sqrt(V)`|explicit arithmetic generalization; original intent unverified|
|3|$4\sqrt{2}$ and $2$|`2*sqrt(U)`, `2*sqrt(V)`|explicit arithmetic generalization; original intent unverified|
|4|$4$ and $2$|`U/2`, `2*V`|opaque numerical evidence|
|5|$2\sqrt{2}$ and $2$|`sqrt(U)`, `2*sqrt(V)`|explicit arithmetic generalization; original intent unverified|

Profile: `observed_q-16455`.

## 4. Reusable templates and constraints

The Python script defines complete equation slots, each mathematical prose equality, optional simplified radical stages, major/minor variable names, and final doubling components. Neither answer strings nor worked prose are returned from source objects. Default equations retain `\frac{{x}^{2}}{DX}+\frac{{y}^{2}}{DY}=1`; the compact source profile spells `\frac{x^{2}}{DX} + \frac{y^{2}}{DY} = 1`. Blank placeholders exactly match field-1/field-2. Introductory/general-equation sentences, displayed block, variable roles, identification → square-root bullets → ordered semi-axes → double axes stage order remain fixed; redundant radius simplification is omitted precisely when its radical spelling is already simplest.

Positive unequal squared radii are mandatory. All radio instances require five distinct complete ordered pairs, exactly one correct pair and positive real lengths; there is no distractor replacement pool. Source decimals remain decimals for designated profile positions when values are integers/halves; other exact values use radical/fraction TeX. No plot assets or renderer are needed.

At raw replay the source's absent difficulty/solution/correct fields remain absent. Generated UUIDs replace original entity IDs, enum dictionaries become local enum strings and correct objects become field-owned lookup refs. These are representation changes, not learner-content changes. The fidelity normalization preserves question text, entire worked prose, field order/types/keys, every complete answer value/type, exact correct value and attribute presence. All practice originals, including the unrated record, are counted. All math identities are independently checked from actual displayed TeX, separate from exact source-content comparison and native grading.

Source q-7600's correct option is derivable as2√10,6, but no original designation exists. No mathematical errors or presentation repairs were found. Six opaque choice transformations remain an interpretation limit, not a fidelity failure. Moderate/hard remain authored design claims. This work stops at guide step7; no database data preparation occurs.
