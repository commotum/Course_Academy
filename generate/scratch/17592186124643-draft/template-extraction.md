# Template extraction

Current point-specialization constraint: for the monomial hard extension, the
target coordinate must differ from twice the held coordinate. Otherwise the
held-coordinate distractor has the same evaluated limit as the correct quotient.
This is enforced for explicit parameters and seeded sampling. See
reference/replenishment/hard-domain-limit-validation.json for an independent
check of every supported hard record's rendered limits.

## 1. Specific original descriptions

Every original is reproduced in review.md and source-replays.json. Raw records are in source.json and all sixty exact answer values, field ownership, designation presence and parameterized masks are in bank-map.json. Original display syntax, including the ASCII sqrt limit syntax and the source's f(x) versus f(x,y) prose mismatch, is retained by observed evidence profiles. Normalization uses the frozen shared math_format.py before IDs. No distractor diagnosis or feedback is fabricated.

### q-158412 — monomial

Given that $f(x,y)=3{x}^{2}y,$ then $\frac{∂f}{∂x}=$

Anchor parameter slots: `{"a": 3, "n": 2}`. Target `x`; the other independent input is held constant. One `selection` radio field, five complete limit-expression choices. The worked solution has exactly three display blocks: formal partial-derivative limit; actual shifted function; substituted quotient limit. Its shared opening says “The partial derivative”. All five mask expressions are listed below; complete banks are chosen together, not assembled from a pool.

- 1: `{lim}_{h\to 0}(\frac{@@a@@(x+h)^{@@n@@}y-@@a@@{x}^{@@n@@}y}{h})` (captured correct)
- 2: `{lim}_{h\to 0}(\frac{@@a@@{x}^{@@n@@}y-@@a@@{x}^{@@n@@}(y+h)}{h})`
- 3: `{lim}_{h\to 0}(\frac{@@a@@{x}^{@@n@@}(y+h)+@@a@@{x}^{@@n@@}y}{h})`
- 4: `{lim}_{h\to 0}(\frac{@@a@@(x+h)^{@@n@@}y+@@a@@{x}^{@@n@@}y}{h})`
- 5: `{lim}_{h\to 0}(\frac{@@a@@{x}^{@@n@@}(y+h)-@@a@@{x}^{@@n@@}y}{h})`
### q-158413 — root_product

Given that $f(x, y) = x\sqrt{y}$, then $\frac{∂f}{∂y} =$

Anchor parameter slots: `{}`. Target `y`; the other independent input is held constant. One `selection` radio field, five complete limit-expression choices. Difficulty, solution and correct designation are absent. The original MA widget confirms the five-choice layout but supplies no recovered key or solution. All five mask expressions are listed below; complete banks are chosen together, not assembled from a pool.

- 1: `lim_(h → 0)(\frac{x\sqrt{y + h} + x\sqrt{y}}{h})`
- 2: `lim_(h → 0)(((x + h)\sqrt{y} - x\sqrt{y + h})/(h))`
- 3: `lim_(h → 0)(((x + h)\sqrt{y} - x\sqrt{y})/(h))`
- 4: `lim_(h → 0)(\frac{x\sqrt{y + h} - x\sqrt{y}}{h})` (independently correct, captured key absent)
- 5: `lim_(h → 0)((x\sqrt{y + h} - (x + h)\sqrt{y})/(h))`
### q-159574 — exponential_linear

Given that $f(x,y)={2}^{x+2y},$ then $\frac{∂f}{∂x}=$

Anchor parameter slots: `{"b": 2, "c": 2}`. Target `x`; the other independent input is held constant. One `selection` radio field, five complete limit-expression choices. The worked solution has exactly three display blocks: formal partial-derivative limit; actual shifted function; substituted quotient limit. Its shared opening says “The partial derivative”. All five mask expressions are listed below; complete banks are chosen together, not assembled from a pool.

- 1: `{lim}_{h\to 0}(\frac{{@@b@@}^{xh+@@c@@y}+{@@b@@}^{x+@@c@@y}}{h})`
- 2: `{lim}_{h\to 0}(\frac{{@@b@@}^{xh+@@c@@y}-{@@b@@}^{x+@@c@@y}}{h})`
- 3: `{lim}_{h\to 0}(\frac{{@@b@@}^{x+h+@@c@@y}-{@@b@@}^{x+@@c@@y}}{h})` (captured correct)
- 4: `{lim}_{h\to 0}(\frac{{@@b@@}^{x+@@c@@h+@@c@@y}-{@@b@@}^{x+@@c@@yy}}{h})`
- 5: `{lim}_{h\to 0}(\frac{{@@b@@}^{x+h+@@c@@y}+{@@b@@}^{x+@@c@@y}}{h})`
### q-159579 — log_linear

Given that $f(x,y)=\operatorname{log}⁡(x+3y),$ then $\frac{∂f}{∂x}=$

Anchor parameter slots: `{"c": 3}`. Target `x`; the other independent input is held constant. One `selection` radio field, five complete limit-expression choices. The worked solution has exactly three display blocks: formal partial-derivative limit; actual shifted function; substituted quotient limit. Its shared opening says “The partial derivative”. All five mask expressions are listed below; complete banks are chosen together, not assembled from a pool.

- 1: `{lim}_{h\to 0}(\frac{\operatorname{log}⁡(x-h+@@c@@y)+\operatorname{log}⁡(x+@@c@@y)}{h})`
- 2: `{lim}_{h\to 0}(\frac{h\operatorname{log}⁡(x+@@c@@y)-\operatorname{log}⁡(x+@@c@@y)}{h})`
- 3: `{lim}_{h\to 0}(\frac{\operatorname{log}⁡(x+@@c@@h+@@c@@y)-\operatorname{log}⁡(x+@@c@@y)}{h})`
- 4: `{lim}_{h\to 0}(\frac{\operatorname{log}⁡(x+h+@@c@@y)-\operatorname{log}⁡(x+@@c@@y)}{h})` (captured correct)
- 5: `{lim}_{h\to 0}(\frac{\operatorname{log}⁡(xh+@@c@@y)-\operatorname{log}⁡(x+@@c@@y)}{h})`
### q-159589 — rational

Given that $f(x,y)=\frac{{x}^{2}}{(y+2)^{3}},$ then $\frac{∂f}{∂y}=$

Anchor parameter slots: `{"p": 2, "q": 3, "a": 2}`. Target `y`; the other independent input is held constant. One `selection` radio field, five complete limit-expression choices. The worked solution has exactly three display blocks: formal partial-derivative limit; actual shifted function; substituted quotient limit. Its shared opening says “The derivative”. All five mask expressions are listed below; complete banks are chosen together, not assembled from a pool.

- 1: `{lim}_{h\to 0}[\frac{1}{h}(\frac{{x}^{@@p@@}}{(y-h+@@a@@)^{@@q@@}}+\frac{{x}^{@@p@@}}{(y+@@a@@)^{@@q@@}})]`
- 2: `{lim}_{h\to 0}[\frac{1}{h}(\frac{(x+h)^{@@p@@}}{(y+h+@@a@@)^{@@q@@}}-\frac{{x}^{@@p@@}}{(y+@@a@@)^{@@q@@}})]`
- 3: `{lim}_{h\to 0}[\frac{1}{h}(\frac{{x}^{@@p@@}}{(y+h+@@a@@)^{@@q@@}}-\frac{{x}^{@@p@@}}{(y+@@a@@)^{@@q@@}})]` (captured correct)
- 4: `{lim}_{h\to 0}[\frac{1}{h}(\frac{{x}^{@@p@@}}{(y+@@a@@h)^{@@q@@}}-\frac{{x}^{@@p@@}}{(y+@@a@@)^{@@q@@}})]`
- 5: `{lim}_{h\to 0}[\frac{1}{h}(\frac{(x+h)^{@@p@@}}{(y+@@a@@)^{@@q@@}}-\frac{{x}^{@@p@@}}{(y+@@a@@)^{@@q@@}})]`
### q-159593 — exponential_product

Given that $f(x,y)={3}^{xy},$ then $\frac{∂f}{∂y}=$

Anchor parameter slots: `{"b": 3}`. Target `y`; the other independent input is held constant. One `selection` radio field, five complete limit-expression choices. The worked solution has exactly three display blocks: formal partial-derivative limit; actual shifted function; substituted quotient limit. Its shared opening says “The derivative”. All five mask expressions are listed below; complete banks are chosen together, not assembled from a pool.

- 1: `{lim}_{h\to 0}(\frac{{@@b@@}^{xyh}-{@@b@@}^{xy}}{h})`
- 2: `{lim}_{h\to 0}(\frac{{@@b@@}^{xy+h}-{@@b@@}^{xy}}{h})`
- 3: `{lim}_{h\to 0}(\frac{{@@b@@}^{x(y+h)}-{@@b@@}^{xy}}{h})` (captured correct)
- 4: `{lim}_{h\to 0}(\frac{{@@b@@}^{x(y-h)}+{@@b@@}^{xy}}{h})`
- 5: `{lim}_{h\to 0}(\frac{{@@b@@}^{xy-h}+{@@b@@}^{xy}}{h})`
### q-159594 — cube_root

Given that $f(x,y)=\sqrt[3]{{x}^{2}-y},$ then $\frac{∂f}{∂y}=$

Anchor parameter slots: `{"p": 2}`. Target `y`; the other independent input is held constant. One `selection` radio field, five complete limit-expression choices. The worked solution has exactly three display blocks: formal partial-derivative limit; actual shifted function; substituted quotient limit. Its shared opening says “The derivative”. All five mask expressions are listed below; complete banks are chosen together, not assembled from a pool.

- 1: `{lim}_{h\to 0}(\frac{\sqrt[3]{{x}^{@@p@@}-yh}+\sqrt[3]{{x}^{@@p@@}-y}}{h})`
- 2: `{lim}_{h\to 0}(\frac{h\sqrt[3]{{x}^{@@p@@}-y}-\sqrt[3]{{x}^{@@p@@}-y}}{h})`
- 3: `{lim}_{h\to 0}(\frac{\sqrt[3]{{x}^{@@p@@}-(y-h)}+\sqrt[3]{{x}^{@@p@@}-y}}{h})`
- 4: `{lim}_{h\to 0}(\frac{\sqrt[3]{{x}^{@@p@@}-yh}-\sqrt[3]{{x}^{@@p@@}-y}}{h})`
- 5: `{lim}_{h\to 0}(\frac{\sqrt[3]{{x}^{@@p@@}-(y+h)}-\sqrt[3]{{x}^{@@p@@}-y}}{h})` (captured correct)
### q-159584 — log_product

Given that $f(x,y)=\operatorname{ln}⁡(7xy),$ then $\frac{∂f}{∂y}=$

Anchor parameter slots: `{"a": 7}`. Target `y`; the other independent input is held constant. One `selection` radio field, five complete limit-expression choices. The worked solution has exactly three display blocks: formal partial-derivative limit; actual shifted function; substituted quotient limit. Its shared opening says “The derivative”. All five mask expressions are listed below; complete banks are chosen together, not assembled from a pool.

- 1: `{lim}_{h\to 0}(\frac{\operatorname{ln}⁡(@@a@@x(y+h))-\operatorname{ln}⁡(@@a@@xy)}{h})` (captured correct)
- 2: `{lim}_{h\to 0}(\frac{\operatorname{ln}⁡(@@a@@x(y-h))+\operatorname{ln}⁡(@@a@@xy)}{h})`
- 3: `{lim}_{h\to 0}(\frac{\operatorname{ln}⁡(@@a@@(x+h)(y+h))-\operatorname{ln}⁡(@@a@@xy)}{h})`
- 4: `{lim}_{h\to 0}(\frac{h\operatorname{ln}⁡(@@a@@xy)-\operatorname{ln}⁡(@@a@@xy)}{h})`
- 5: `{lim}_{h\to 0}(\frac{\operatorname{ln}⁡(@@a@@xyh)-\operatorname{ln}⁡(@@a@@xy)}{h})`
### q-159592 — variable_power_exponent

Given that $f(x,y)={x}^{y},$ then $\frac{∂f}{∂y}=$

Anchor parameter slots: `{}`. Target `y`; the other independent input is held constant. One `selection` radio field, five complete limit-expression choices. The worked solution has exactly three display blocks: formal partial-derivative limit; actual shifted function; substituted quotient limit. Its shared opening says “The derivative”. All five mask expressions are listed below; complete banks are chosen together, not assembled from a pool.

- 1: `{lim}_{h\to 0}(\frac{{x}^{y-h}+{x}^{y}}{h})`
- 2: `{lim}_{h\to 0}(\frac{{x}^{yh}-{x}^{y}}{h})`
- 3: `{lim}_{h\to 0}(\frac{(x+h)^{y+h}-{x}^{y}}{h})`
- 4: `{lim}_{h\to 0}(\frac{{x}^{y+h}-{x}^{y}}{h})` (captured correct)
- 5: `{lim}_{h\to 0}(\frac{(x+h)^{y}-{x}^{y}}{h})`
### q-159575 — variable_power_base

Given that $f(x,y)={x}^{y},$ then $\frac{∂f}{∂x}=$

Anchor parameter slots: `{}`. Target `x`; the other independent input is held constant. One `selection` radio field, five complete limit-expression choices. The worked solution has exactly three display blocks: formal partial-derivative limit; actual shifted function; substituted quotient limit. Its shared opening says “The partial derivative”. All five mask expressions are listed below; complete banks are chosen together, not assembled from a pool.

- 1: `{lim}_{h\to 0}(\frac{(x+h)^{y}+{x}^{y}}{h})`
- 2: `{lim}_{h\to 0}(\frac{(x+h)^{y}-{x}^{y}}{h})` (captured correct)
- 3: `{lim}_{h\to 0}(\frac{{x}^{y+h}-{x}^{y}}{h})`
- 4: `{lim}_{h\to 0}(\frac{(x+h)^{y+h}-{x}^{y}}{h})`
- 5: `{lim}_{h\to 0}(\frac{{x}^{y+h}+{x}^{y}}{h})`
### q-159576 — cosine

Given that $f(x,y)=\operatorname{cos}⁡(x-{y}^{2}),$ then $\frac{∂f}{∂x}=$

Anchor parameter slots: `{"p": 2}`. Target `x`; the other independent input is held constant. One `selection` radio field, five complete limit-expression choices. The worked solution has exactly three display blocks: formal partial-derivative limit; actual shifted function; substituted quotient limit. Its shared opening says “The partial derivative”. All five mask expressions are listed below; complete banks are chosen together, not assembled from a pool.

- 1: `{lim}_{h\to 0}(\frac{\operatorname{cos}⁡(x+h-{y}^{@@p@@})-\operatorname{cos}⁡(x-{y}^{@@p@@})}{h})` (captured correct)
- 2: `{lim}_{h\to 0}(\frac{\operatorname{cos}⁡(xh-{y}^{@@p@@})-\operatorname{cos}⁡(x-{y}^{@@p@@})}{h})`
- 3: `{lim}_{h\to 0}(\frac{\operatorname{cos}⁡(x+h-{y}^{@@p@@})+\operatorname{cos}⁡(x-{y}^{@@p@@})}{h})`
- 4: `{lim}_{h\to 0}(\frac{\operatorname{cos}⁡(xh-{y}^{@@p@@})+\operatorname{cos}⁡(x-{y}^{@@p@@})}{h})`
- 5: `{lim}_{h\to 0}(\frac{h\operatorname{cos}⁡(x-{y}^{@@p@@})-\operatorname{cos}⁡(x-{y}^{@@p@@})}{h})`
### q-159572 — sine_product

Given that $f(x,y)=\operatorname{sin}⁡(xy),$ then $\frac{∂f}{∂x}=$

Anchor parameter slots: `{}`. Target `x`; the other independent input is held constant. One `selection` radio field, five complete limit-expression choices. The worked solution has exactly three display blocks: formal partial-derivative limit; actual shifted function; substituted quotient limit. Its shared opening says “The partial derivative”. All five mask expressions are listed below; complete banks are chosen together, not assembled from a pool.

- 1: `{lim}_{h\to 0}(\frac{\operatorname{sin}⁡((x+h)(y+h))-\operatorname{sin}⁡(xy)}{h})`
- 2: `{lim}_{h\to 0}(\frac{\operatorname{sin}⁡(xy+h)-\operatorname{sin}⁡(xy)}{h})`
- 3: `{lim}_{h\to 0}(\frac{\operatorname{sin}⁡(xy+h)+\operatorname{sin}⁡(xy)}{h})`
- 4: `{lim}_{h\to 0}(\frac{\operatorname{sin}⁡((x+h)y)-\operatorname{sin}⁡(xy)}{h})` (captured correct)
- 5: `{lim}_{h\to 0}(\frac{\operatorname{sin}⁡(x(y+h))-\operatorname{sin}⁡(xy)}{h})`

## 2. General mathematical backbone

Given a two-input function and a requested partial derivative, replace only the target input by target+h. Hold the other input fixed. Subtract the original complete function value, group that numerator, divide the complete difference by the same h, and place it under lim h→0. The answer is the entire unevaluated limit expression. Expressions that both lack a finite limit are not interchangeable answers to a request for a particular defining difference quotient: banks are compared as full increment expressions before taking the limit. No derivative rule, cancellation, rationalization or limit-evaluation stage is added.

All observed normal families retain their original three operative display stages and shared sentences. Normal output minimally changes f(x) to f(x,y) in source prose, canonicalizes visible partial/limit notation, and adds one explicit h≠0 / held-variable sentence after the chain. Raw observed replay keeps the exact normalized original sentences and absent attributes. Source q-158413 normal completion uses the same three stages and labels them authored. One concrete solution depends only on the instance and never on the learner response.

## 3. Components and bank mapping

bank-map.json accounts for every source option one-to-one, including four wrong options in each keyed bank and all five unkeyed root-product options. templates.json holds extracted masks only, not completed question records or a source-payload return branch. Every ordinary and replay record runs through fill, role substitution, parameter validation, normalization and field-owned record assembly. Anchor replay is not a special case. Source difficulty, solution and correct-key presence are separate flags; the unkeyed record cannot count toward designation matches.

The malformed-looking `x+2yy` exponential distractor is algebraically readable as x+2y², but its pedagogical operation is underdetermined. Its exact full expression pattern is public ineligible observed evidence, with c replacing every coupled2. Normal method output uses a declared complete bank that replaces only that option by shifting the held coordinate y+h in b^(x+cy). This is an authored bank extension, not a recovered error intention. All other source banks use their complete parameterized expression patterns. Wrong options never have invented learner-facing explanations.

## 4. Reusable templates, slots and constraints

Fixed: two variables; one target and one held role; one five-option radio bank; subtraction/division/limit order; increment h; exactly the original three operative display blocks (except the source's absent solution); the family-specific operators and nested expression positions. Variable: each documented numeric slot and an optional simultaneous x↔y role relabeling. Function signatures always remain ordered f(x,y); after role exchange f(x+h,y) becomes f(x,y+h). Command names and ordinary prose words are protected. Coordinate entries are never globally replaced across prose. The role swap is exercised for correctness but is not counted as another meaningful mathematical task.

- `monomial`: {"a": [1, 9], "n": [2, 5]}. These slots occupy the existing coefficient, exponent, exponential base or shift components; the arithmetic is not evaluated in this symbolic setup task. 
- `root_product`: {}. These slots occupy the existing coefficient, exponent, exponential base or shift components; the arithmetic is not evaluated in this symbolic setup task. Its source backbone has no numeric slot; it is retained as a supported finite family and is not inflated by variable-letter aliases. 
- `exponential_linear`: {"b": [2, 9], "c": [2, 9]}. These slots occupy the existing coefficient, exponent, exponential base or shift components; the arithmetic is not evaluated in this symbolic setup task. 
- `log_linear`: {"c": [2, 9]}. These slots occupy the existing coefficient, exponent, exponential base or shift components; the arithmetic is not evaluated in this symbolic setup task. 
- `rational`: {"p": [2, 5], "q": [2, 5], "a": [1, 9]}. These slots occupy the existing coefficient, exponent, exponential base or shift components; the arithmetic is not evaluated in this symbolic setup task. 
- `exponential_product`: {"b": [2, 9]}. These slots occupy the existing coefficient, exponent, exponential base or shift components; the arithmetic is not evaluated in this symbolic setup task. 
- `cube_root`: {"p": [2, 5]}. These slots occupy the existing coefficient, exponent, exponential base or shift components; the arithmetic is not evaluated in this symbolic setup task. 
- `log_product`: {"a": [2, 9]}. These slots occupy the existing coefficient, exponent, exponential base or shift components; the arithmetic is not evaluated in this symbolic setup task. 
- `variable_power_exponent`: {}. These slots occupy the existing coefficient, exponent, exponential base or shift components; the arithmetic is not evaluated in this symbolic setup task. Its source backbone has no numeric slot; it is retained as a supported finite family and is not inflated by variable-letter aliases. 
- `variable_power_base`: {}. These slots occupy the existing coefficient, exponent, exponential base or shift components; the arithmetic is not evaluated in this symbolic setup task. Its source backbone has no numeric slot; it is retained as a supported finite family and is not inflated by variable-letter aliases. 
- `cosine`: {"p": [2, 5]}. These slots occupy the existing coefficient, exponent, exponential base or shift components; the arithmetic is not evaluated in this symbolic setup task. 
- `sine_product`: {}. These slots occupy the existing coefficient, exponent, exponential base or shift components; the arithmetic is not evaluated in this symbolic setup task. Its source backbone has no numeric slot; it is retained as a supported finite family and is not inflated by variable-letter aliases. 

Hard point_monomial preserves a·target²·held. Coordinates lie in {−3,−2,−1,1,2,3}; nonzero coefficient magnitude is at most5; enforce |a·target_coordinate²·held_coordinate|≤24 on explicit and sampled inputs. Every full signed function value is grouped before numerator subtraction, so negative source-point values cannot create ambiguous adjacent signs. The target-coordinate square is at most9 and absolute original complete value at most24; no high-power expansion or derivative evaluation is introduced. Hard point_sine preserves sin(xy), coordinates in {−3,−2,−1,1,2,3} with unequal entries, so their product has absolute value at most9 and both source-shaped increment errors remain distinct. Trigonometric values remain exact symbolic values, with no new trig evaluation skill. Both hard families retain formal quotient / concrete supplied-point substitution / final quotient stages. All bounds apply to public explicit calls. Equal sine coordinates reject the whole bank because target-only and other-only shifts collide; an individual option is never replaced after sampling.

Meaningful fingerprints canonicalize target/held roles and functions up to held-only additive terms (using symbolic derivatives only for internal deduplication, never learner solution steps) for symbolic tasks and the point-specialized increment expression for hard tasks. Variable-letter, seed and answer-order changes do not create another assessed task. Presentation identity includes difficulty, version, complete prompt, complete solution and full displayed bank; fields and answers own stable UUIDs. Distinct banks cannot share content identity. Runtime versions are recorded from the actual process.

No plots: plot-extraction.md records a none rating. No generation or validation step reaches EDB, a numeric registered script, shared caches, engine sources or the manifest.
