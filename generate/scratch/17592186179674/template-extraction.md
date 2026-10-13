# Four-stage extraction

## 1. Describe every source before generalizing

All responses are delimiter-free scalar mathematical values in a single five-option radio field named selection. Each source starts with an explicit Cartesian curve and two oriented endpoints, then parameterization, derivative and a fixed line-integral calculation. Exact arithmetic only. The source-specific extraction below retains all options and all mathematical stages; the raw source.json preserves full prose and original IDs.

### q-39344 / parabola_xy

If the path $C$ is a part of the parabola $y={x}^{2}$ traversed from the point $A(0,0)$ to point $B(2,4),$ then ${\int }_{C}x\,dx+y\,dy=$

Observed base parameters: `{"a": 1, "b": 1, "c": 1, "u": 0, "v": 2}`.

Correct scalar fragment: `10`.

Ordered evaluation stages:

1. `{\int }_{0}^{2}x\frac{\text{d}x}{\text{d}t}\,\text{d}t+y\frac{\text{d}y}{\text{d}t}\,\text{d}t`

2. `{\int }_{0}^{2}(x\frac{\text{d}x}{\text{d}t}+y\frac{\text{d}y}{\text{d}t})\,\text{d}t`

3. `{\int }_{0}^{2}t\cdot 1+{t}^{2}\cdot 2t\,dt`

4. `{\int }_{0}^{2}t+2{t}^{3}\,dt`

5. `{[\frac{{t}^{2}}{2}+\frac{{t}^{4}}{2}]}_{0}^{2}`

6. `[\frac{{2}^{2}}{2}+\frac{{2}^{4}}{2}]-[0]`

7. `2+8`

8. `10`

Complete original bank/profile:

- `6`; recipe `scale × (6)`; designation incorrect.

- `12`; recipe `scale × (12)`; designation incorrect.

- `8`; recipe `scale × (8)`; designation incorrect.

- `14`; recipe `scale × (14)`; designation incorrect.

- `10`; recipe `scale × (10)`; designation correct.

The wrong scalar values alone do not identify a unique source mistake. Their complete expression patterns are preserved under uniform scaling of the entire one-form; this does not claim a recovered error intent. These explicit profiles are replay-only.

### q-81178 / shift_log

If the path $C$ is a part of the parabola $y=(x+1)^{2}$ traversed from the point $P(0,1)$ to point $Q(1,4),$ then ${\int }_{C}\frac{dx+dy}{y}=$

Observed base parameters: `{"a": 1, "b": 1, "h": 1, "u": 0, "v": 1}`.

Correct scalar fragment: `2\operatorname{ln}⁡2+\frac{1}{2}`.

Ordered evaluation stages:

1. `{\int }_{0}^{1}\frac{1}{y}(\frac{\text{d}x}{\text{d}t}\,\text{d}t+\frac{\text{d}y}{\text{d}t}\,\text{d}t)`

2. `{\int }_{0}^{1}\frac{1}{y}(\frac{\text{d}x}{\text{d}t}+\frac{\text{d}y}{\text{d}t})\text{d}t`

3. `{\int }_{0}^{1}\frac{1+2(t+1)}{(t+1)^{2}}\,dt`

4. `{\int }_{0}^{1}\frac{1}{(t+1)^{2}}+\frac{2}{t+1}\,dt`

5. `{[-\frac{1}{t+1}+2\operatorname{ln}⁡(t+1)]}_{0}^{1}`

6. `[-\frac{1}{1+1}+2\operatorname{ln}⁡(1+1)]-[-\frac{1}{0+1}+2\operatorname{ln}⁡(0+1)]`

7. `[-\frac{1}{2}+2\operatorname{ln}⁡2]-[-1+0]`

8. `2\operatorname{ln}⁡2+\frac{1}{2}`

Complete original bank/profile:

- `3\operatorname{ln}⁡2-\frac{1}{2}`; recipe `scale × (3\operatorname{ln}⁡2-\frac{1}{2})`; designation incorrect.

- `2\operatorname{ln}⁡2+\frac{1}{2}`; recipe `scale × (2\operatorname{ln}⁡2+\frac{1}{2})`; designation correct.

- `2\operatorname{ln}⁡3-1`; recipe `scale × (2\operatorname{ln}⁡3-1)`; designation incorrect.

- `\operatorname{ln}⁡3+1`; recipe `scale × (\operatorname{ln}⁡3+1)`; designation incorrect.

- `\operatorname{ln}⁡2-\frac{1}{2}`; recipe `scale × (\operatorname{ln}⁡2-\frac{1}{2})`; designation incorrect.

The wrong scalar values alone do not identify a unique source mistake. Their complete expression patterns are preserved under uniform scaling of the entire one-form; this does not claim a recovered error intent. These explicit profiles are replay-only.

### q-124664 / sqrt_linear

If the path $C$ is a part of the graph $y=2\sqrt{x}$ traversed from the point $P(1,2)$ to point $Q(4,4),$ then ${\int }_{C}(x-y)\,dx+(x+y)\,dy=$

Observed base parameters: `{"a": 1, "b": 1, "c": 2, "u": 1, "v": 2}`.

Correct scalar fragment: `\frac{53}{6}`.

Ordered evaluation stages:

1. `{\int }_{1}^{2}(x-y)\,\frac{\text{d}x}{\text{d}t}\,\text{d}t+(x+y)\,\frac{\text{d}y}{\text{d}t}\,\text{d}t`

2. `{\int }_{1}^{2}((x-y)\,\frac{\text{d}x}{\text{d}t}+(x+y)\,\frac{\text{d}y}{\text{d}t})\text{d}t`

3. `{\int }_{1}^{2}({t}^{2}-2t)\cdot 2t+({t}^{2}+2t)\cdot 2\,dt`

4. `2{\int }_{1}^{2}t({t}^{2}-2t)+({t}^{2}+2t)\,dt`

5. `2{\int }_{1}^{2}{t}^{3}-{t}^{2}+2t\,dt`

6. `2{[\frac{{t}^{4}}{4}-\frac{{t}^{3}}{3}+{t}^{2}]}_{1}^{2}`

7. `2[(\frac{{2}^{4}}{4}-\frac{{2}^{3}}{3}+{2}^{2})-(\frac{{1}^{4}}{4}-\frac{{1}^{3}}{3}+{1}^{2})]`

8. `2[4-\frac{8}{3}+4-\frac{1}{4}+\frac{1}{3}-1]`

9. `2\cdot \frac{53}{12}`

10. `\frac{53}{6}`

Complete original bank/profile:

- `8`; recipe `scale × (8)`; designation incorrect.

- `\frac{53}{6}`; recipe `scale × (\frac{53}{6})`; designation correct.

- `\frac{49}{8}`; recipe `scale × (\frac{49}{8})`; designation incorrect.

- `6`; recipe `scale × (6)`; designation incorrect.

- `\frac{42}{7}`; recipe `scale × (\frac{42}{7})`; designation incorrect.

The wrong scalar values alone do not identify a unique source mistake. Their complete expression patterns are preserved under uniform scaling of the entire one-form; this does not claim a recovered error intent. These explicit profiles are replay-only.

### q-124668 / cubic_recip

If the path $C$ is a part of the graph $y={x}^{3}$ traversed from the point $P(1,1)$ to point $Q(2,8),$ then ${\int }_{C}\frac{1}{y}\,dx+\frac{1}{{x}^{2}}\,dy=$

Observed base parameters: `{"a": 1, "b": 1, "c": 1, "u": 1, "v": 2}`.

Correct scalar fragment: `\frac{27}{8}`.

Ordered evaluation stages:

1. `{\int }_{1}^{2}\frac{1}{y}\,\frac{\text{d}x}{\text{d}t}\,\text{d}t+\frac{1}{{x}^{2}}\,\frac{\text{d}y}{\text{d}t}\,\text{d}t`

2. `{\int }_{1}^{2}(\frac{1}{y}\,\frac{\text{d}x}{\text{d}t}+\frac{1}{{x}^{2}}\,\frac{\text{d}y}{\text{d}t})\text{d}t`

3. `{\int }_{1}^{2}\frac{1}{{t}^{3}}\cdot 1+\frac{1}{{t}^{2}}\cdot 3{t}^{2}\,\text{d}t`

4. `{\int }_{1}^{2}\frac{1}{{t}^{3}}+3\,\text{d}t`

5. `{[-\frac{1}{2{t}^{2}}+3t]}_{1}^{2}`

6. `[-\frac{1}{2({2}^{2})}+3(2)]-[-\frac{1}{2({1}^{2})}+3(1)]`

7. `-\frac{1}{8}+6+\frac{1}{2}-3`

8. `\frac{27}{8}`

Complete original bank/profile:

- `3`; recipe `scale × (3)`; designation incorrect.

- `2`; recipe `scale × (2)`; designation incorrect.

- `\frac{27}{8}`; recipe `scale × (\frac{27}{8})`; designation correct.

- `\frac{31}{6}`; recipe `scale × (\frac{31}{6})`; designation incorrect.

- `\frac{19}{4}`; recipe `scale × (\frac{19}{4})`; designation incorrect.

The wrong scalar values alone do not identify a unique source mistake. Their complete expression patterns are preserved under uniform scaling of the entire one-form; this does not claim a recovered error intent. These explicit profiles are replay-only.

### q-39679 / cuberoot_exp

If the path $C$ is a part of the curve $y=\sqrt[3]{x}$ traversed from the point $P(0,0)$ to point $Q(1,1),$ then ${\int }_{C}4y{e}^{xy}\,dx+dy=$

Observed base parameters: `{"a": 4, "b": 1, "c": 1, "u": 0, "v": 1}`.

Correct scalar fragment: `3e-2`.

Ordered evaluation stages:

1. `{\int }_{0}^{1}4y{e}^{xy}\,\frac{\text{d}x}{\text{d}t}\,\text{d}t+\frac{\text{d}y}{\text{d}t}\,\text{d}t`

2. `{\int }_{0}^{1}(4y{e}^{xy}\,\frac{\text{d}x}{\text{d}t}+\frac{\text{d}y}{\text{d}t})\text{d}t`

3. `{\int }_{0}^{1}4t\cdot {e}^{{t}^{3}\cdot t}\cdot 3{t}^{2}+1\,dt`

4. `{\int }_{0}^{1}12{t}^{3}{e}^{{t}^{4}}+1\,dt`

5. `{[3{e}^{{t}^{4}}+t]}_{0}^{1}`

6. `[3{e}^{(1)^{4}}+(1)]-[3{e}^{(0)^{4}}+(0)]`

7. `[3e+1]-[3]`

8. `3e-2`

Complete original bank/profile:

- `3e+4`; recipe `scale × (3e+4)`; designation incorrect.

- `5e+4`; recipe `scale × (5e+4)`; designation incorrect.

- `4e-3`; recipe `scale × (4e-3)`; designation incorrect.

- `3e-2`; recipe `scale × (3e-2)`; designation correct.

- `2e-3`; recipe `scale × (2e-3)`; designation incorrect.

The wrong scalar values alone do not identify a unique source mistake. Their complete expression patterns are preserved under uniform scaling of the entire one-form; this does not claim a recovered error intent. These explicit profiles are replay-only.

### q-80983 / sqrt_poly

If the path $C$ is a part of the graph $y=\sqrt{x}$ traversed from the point $A(0,0)$ to point $B(1,1),$ then  ${\int }_{C}({x}^{2}+y)\,dx+(3x+2y)\,dy=$

Observed base parameters: `{"a": 1, "b": 1, "c": 1, "d": 3, "e": 2, "u": 0, "v": 1}`.

Correct scalar fragment: `3`.

Ordered evaluation stages:

1. `{\int }_{0}^{1}({x}^{2}+y)\,\frac{\text{d}x}{\text{d}t}\,\text{d}t+(3x+2y)\,\frac{\text{d}y}{\text{d}t}\,\text{d}t`

2. `{\int }_{0}^{1}(({x}^{2}+y)\,\frac{\text{d}x}{\text{d}t}+(3x+2y)\,\frac{\text{d}y}{\text{d}t})\text{d}t`

3. `{\int }_{0}^{1}({({t}^{2})}^{2}+t)\cdot 2t+(3{t}^{2}+2t)\cdot 1\,dt`

4. `{\int }_{0}^{1}({t}^{4}+t)\cdot 2t+3{t}^{2}+2t\,dt`

5. `{\int }_{0}^{1}2{t}^{5}+5{t}^{2}+2t\,dt`

6. `{[\frac{{t}^{6}}{3}+\frac{5{t}^{3}}{3}+{t}^{2}]}_{0}^{1}`

7. `[\frac{(1)^{6}}{3}+\frac{5(1)^{3}}{3}+(1)^{2}]-[0]`

8. `[\frac{1}{3}+\frac{5}{3}+1]-[0]`

9. `3`

Complete original bank/profile:

- `4`; recipe `scale × (4)`; designation incorrect.

- `5`; recipe `scale × (5)`; designation incorrect.

- `6`; recipe `scale × (6)`; designation incorrect.

- `2`; recipe `scale × (2)`; designation incorrect.

- `3`; recipe `scale × (3)`; designation correct.

The wrong scalar values alone do not identify a unique source mistake. Their complete expression patterns are preserved under uniform scaling of the entire one-form; this does not claim a recovered error intent. These explicit profiles are replay-only.

### q-81098 / shift_cross

If the path $C$ is a part of the parabola $y={x}^{2}-x$ traversed from the point $A(0,0)$ to point $B(2,2),$ then ${\int }_{C}2xy\,dx+x\,dy=$

Observed base parameters: `{"a": 2, "b": 1, "h": 1, "u": 0, "v": 2}`.

Correct scalar fragment: `6`.

Ordered evaluation stages:

1. `{\int }_{0}^{2}2xy\,\frac{\text{d}x}{\text{d}t}\,\text{d}t+x\,\frac{\text{d}y}{\text{d}t}\,\text{d}t`

2. `{\int }_{0}^{2}(2xy\,\frac{\text{d}x}{\text{d}t}+x\,\frac{\text{d}y}{\text{d}t})\text{d}t`

3. `{\int }_{0}^{2}2t({t}^{2}-t)\cdot 1+t(2t-1)\,dt`

4. `{\int }_{0}^{2}2{t}^{3}-t\,dt`

5. `{[\frac{{t}^{4}}{2}-\frac{{t}^{2}}{2}]}_{0}^{2}`

6. `[\frac{{2}^{4}}{2}-\frac{{2}^{2}}{2}]-[0]`

7. `8-2`

8. `6`

Complete original bank/profile:

- `12`; recipe `scale × (12)`; designation incorrect.

- `3`; recipe `scale × (3)`; designation incorrect.

- `6`; recipe `scale × (6)`; designation correct.

- `9`; recipe `scale × (9)`; designation incorrect.

- `15`; recipe `scale × (15)`; designation incorrect.

The wrong scalar values alone do not identify a unique source mistake. Their complete expression patterns are preserved under uniform scaling of the entire one-form; this does not claim a recovered error intent. These explicit profiles are replay-only.

### q-81180 / trig_sin

If the path $C$ is a part of the parabola $y=\pi {x}^{2}$ traversed from the point $A(1,\pi )$ to point $B(2,4\pi ),$ then ${\int }_{C}\operatorname{sin}⁡(\frac{y}{2{x}^{2}})\,dx+3x\,dy=$

Observed base parameters: `{"a": 3, "c": 1, "d": 2, "u": 1, "v": 2}`.

Correct scalar fragment: `1+14\pi `.

Ordered evaluation stages:

1. `{\int }_{1}^{2}\operatorname{sin}⁡(\frac{y}{2{x}^{2}})\frac{\text{d}x}{\text{d}t}\,\text{d}t+3x\,\frac{\text{d}y}{\text{d}t}\,\text{d}t`

2. `{\int }_{1}^{2}(\operatorname{sin}⁡(\frac{y}{2{x}^{2}})\frac{\text{d}x}{\text{d}t}+3x\,\frac{\text{d}y}{\text{d}t})\text{d}t`

3. `{\int }_{1}^{2}\operatorname{sin}⁡(\frac{\pi {t}^{2}}{2{t}^{2}})\cdot 1+3t\cdot 2\pi t\,dt`

4. `{\int }_{1}^{2}\operatorname{sin}⁡(\frac{\pi }{2})+6\pi {t}^{2}\,dt`

5. `{\int }_{1}^{2}1+6\pi {t}^{2}\,dt`

6. `[t+2\pi {t}^{3}]_{1}^{2}`

7. `[2+2\pi (2)^{3}]-[1+2\pi (1)^{3}]`

8. `[2+16\pi ]-[1+2\pi ]`

9. `1+14\pi`

Complete original bank/profile:

- `2+6\pi `; recipe `scale × (2+6\pi )`; designation incorrect.

- `2+10\pi `; recipe `scale × (2+10\pi )`; designation incorrect.

- `1+12\pi `; recipe `scale × (1+12\pi )`; designation incorrect.

- `1+14\pi `; recipe `scale × (1+14\pi )`; designation correct.

- `1+16\pi `; recipe `scale × (1+16\pi )`; designation incorrect.

The wrong scalar values alone do not identify a unique source mistake. Their complete expression patterns are preserved under uniform scaling of the entire one-form; this does not claim a recovered error intent. These explicit profiles are replay-only.

### q-90848 / hard_poly

If the path $C$ is a part of the parabola $y={x}^{2}-1$ traversed from the point $A(0,-1)$ to point $B(2,3),$ then ${\int }_{C}5{x}^{2}y\,dx+{x}^{2}(y+1)\,dy=$

Observed base parameters: `{"a": 5, "b": 1, "h": 1, "u": 0, "v": 2}`.

Correct scalar fragment: `40`.

Ordered evaluation stages:

1. `{\int }_{0}^{2}5{x}^{2}y\,\frac{\text{d}x}{\text{d}t}\,\text{d}t+{x}^{2}(y+1)\,\frac{\text{d}y}{\text{d}t}\,\text{d}t`

2. `{\int }_{0}^{2}(5{x}^{2}y\,\frac{\text{d}x}{\text{d}t}+{x}^{2}(y+1)\,\frac{\text{d}y}{\text{d}t})\text{d}t`

3. `{\int }_{0}^{2}5{t}^{2}({t}^{2}-1)\cdot 1+{t}^{2}({t}^{2}-1+1)\cdot 2t\,dt`

4. `{\int }_{0}^{2}5{t}^{4}-5{t}^{2}+2{t}^{5}\,dt`

5. `{[{t}^{5}-\frac{5}{3}{t}^{3}+\frac{{t}^{6}}{3}]}_{0}^{2}`

6. `[{2}^{5}-\frac{5}{3}(2)^{3}+\frac{{2}^{6}}{3}]-[0]`

7. `32-\frac{40}{3}+\frac{64}{3}`

8. `40`

Complete original bank/profile:

- `\frac{40}{3}`; recipe `scale × (\frac{40}{3})`; designation incorrect.

- `40`; recipe `scale × (40)`; designation correct.

- `\frac{4}{3}`; recipe `scale × (\frac{4}{3})`; designation incorrect.

- `60`; recipe `scale × (60)`; designation incorrect.

- `32`; recipe `scale × (32)`; designation incorrect.

The wrong scalar values alone do not identify a unique source mistake. Their complete expression patterns are preserved under uniform scaling of the entire one-form; this does not claim a recovered error intent. These explicit profiles are replay-only.

### q-90871 / trig_cos

If the path $C$ is a part of the parabola $y=\pi {x}^{2}$ traversed from the point $A(0,0)$ to point $B(1,\pi ),$ then ${\int }_{C}\operatorname{cos}⁡(\frac{y}{{x}^{2}})\,dx+4{x}^{2}\,dy=$

Observed base parameters: `{"a": 4, "c": 1, "d": 1, "u": 0, "v": 1}`.

Correct scalar fragment: `2\pi -1`.

Ordered evaluation stages:

1. `{\int }_{0}^{1}\operatorname{cos}⁡(\frac{y}{{x}^{2}})\frac{\text{d}x}{\text{d}t}\,\text{d}t+4{x}^{2}\,\frac{\text{d}y}{\text{d}t}\,\text{d}t`

2. `{\int }_{0}^{1}(\operatorname{cos}⁡(\frac{y}{{x}^{2}})\frac{\text{d}x}{\text{d}t}+4{x}^{2}\,\frac{\text{d}y}{\text{d}t})\text{d}t`

3. `{\int }_{0}^{1}\operatorname{cos}⁡(\frac{\pi {t}^{2}}{{t}^{2}})\cdot 1+4{t}^{2}\cdot 2\pi t\,dt`

4. `{\int }_{0}^{1}\operatorname{cos}⁡\pi +8\pi {t}^{3}\,dt`

5. `{\int }_{0}^{1}8\pi {t}^{3}-1\,dt`

6. `[2\pi {t}^{4}-t]_{0}^{1}`

7. `[2\pi (1)^{4}-1]-[0]`

8. `2\pi -1`

Complete original bank/profile:

- `2\pi `; recipe `scale × (2\pi )`; designation incorrect.

- `2\pi -1`; recipe `scale × (2\pi -1)`; designation correct.

- `\pi -1`; recipe `scale × (\pi -1)`; designation incorrect.

- `2\pi +1`; recipe `scale × (2\pi +1)`; designation incorrect.

- `4\pi +3`; recipe `scale × (4\pi +3)`; designation incorrect.

The wrong scalar values alone do not identify a unique source mistake. Their complete expression patterns are preserved under uniform scaling of the entire one-form; this does not claim a recovered error intent. These explicit profiles are replay-only.

### q-124666 / square_cancel

If the path $C$ is a part of the graph $y={x}^{2}-1$ traversed from the point $P(1,0)$ to point $Q(2,3),$ then ${\int }_{C}{y}^{2}\,dx+x\,dy=$

Observed base parameters: `{"a": 1, "b": 1, "h": 1, "u": 1, "v": 2}`.

Correct scalar fragment: `\frac{36}{5}`.

Ordered evaluation stages:

1. `{\int }_{1}^{2}{y}^{2}\,\frac{\text{d}x}{\text{d}t}\,\text{d}t+x\,\frac{\text{d}y}{\text{d}t}\,\text{d}t`

2. `{\int }_{1}^{2}({y}^{2}\,\frac{\text{d}x}{\text{d}t}+x\,\frac{\text{d}y}{\text{d}t})\text{d}t`

3. `{\int }_{1}^{2}{({t}^{2}-1)}^{2}\cdot 1+t\cdot 2t\,dt`

4. `{\int }_{1}^{2}{t}^{4}-2{t}^{2}+1+2{t}^{2}\,dt`

5. `{\int }_{1}^{2}{t}^{4}+1\,dt`

6. `{[\frac{{t}^{5}}{5}+t]}_{1}^{2}`

7. `[\frac{{2}^{5}}{5}+2]-[\frac{{1}^{5}}{5}+1]`

8. `\frac{32}{5}+2-\frac{1}{5}-1`

9. `\frac{36}{5}`

Complete original bank/profile:

- `\frac{27}{5}`; recipe `scale × (\frac{27}{5})`; designation incorrect.

- `\frac{22}{3}`; recipe `scale × (\frac{22}{3})`; designation incorrect.

- `\frac{19}{5}`; recipe `scale × (\frac{19}{5})`; designation incorrect.

- `\frac{14}{3}`; recipe `scale × (\frac{14}{3})`; designation incorrect.

- `\frac{36}{5}`; recipe `scale × (\frac{36}{5})`; designation correct.

The wrong scalar values alone do not identify a unique source mistake. Their complete expression patterns are preserved under uniform scaling of the entire one-form; this does not claim a recovered error intent. These explicit profiles are replay-only.

## 2. Shared pattern

Parameterize the same Cartesian graph using its convenient coordinate, compute x′ and y′, evaluate ∫[P(x(t),y(t))x′(t)+Q(x(t),y(t))y′(t)]dt. Square/cube roots use x=t² or t³ to avoid differentiating a singular graph at the origin. The hard families add familiar trig simplification or polynomial products; none add a new line-integral theorem.

## 3. Components and bank accounting

Every original option is mapped above to its original field, exact value, designation, original parameters, complete source profile and explicit scaling operation. Prompt curve/endpoints, source parameterization and derivative stay fixed in replay; the complete assessed one-form and every evaluation stage scale together by an integer 1..6. k=1 yields all 11 exact raw prompts, all 11 exact raw solutions and all 55 exact raw choice strings. Raw q-124664 retains one wrong/wrong equivalence and is evidence-only. Normal observed replay minimally changes that one option; its other 54 values match their sources mathematically, and all 11 repaired profiles are valid.

## 4. Reusable templates and constraints

Source templates are extracted as complete mathematical component masks, with preserved literal prose/layout and ordered aligned rows, rather than replacing short numerals or variable letters across text. k multiplies each complete line-integral expression, antiderivative and endpoint arithmetic expression. Source row counts differ and remain source-specific; k does not insert or delete a step. k=1 rendering is the ordinary multiplicative-identity case, not a source-payload return branch.

Normal authored practice varies coefficients, curve scales/shifts and limits within each original family. Positive integer coefficients are 1..3, except designated a=1..5 for hard polynomial, exponential and hard trig families. All domains use 0≤u<v≤3; reciprocal cubic uses u=1; log graph x+h is strictly positive. Exponential root retains c=1,[0,1] for familiar e powers. Moderate root polynomial and hard polynomial upper limit is at most2. Sine retains c∈{1,3},d=2,u=1 and cosine d=1,c∈{1,2,3}, so trig constants are familiar and nonzero. These guards apply to explicit parameters. Every level contains unordered same-method families, with no within-level progression.

The authored complete bank, chosen as one profile before computation, is I, I_dx, I_dy, −I, I_dx−I_dy: correct, omit the other contribution, reverse traversal, or reverse the dy sign. All are derived by complete mathematical operations. If any two are equivalent, the whole sampled instance is rejected; explicit invalid instances raise ValueError. There is no random offset, answer-value lookup, mixed first-valid recipe pool, or learner-facing distractor diagnosis.

Authored solutions preserve the source shared method prose, explicit parameterization and derivative, two symbolic change-of-variable rows, unevaluated coordinate substitution/products, separate first distributed dx/dy sum, collection, component antiderivative, unevaluated endpoint powers, endpoint component sum and final collection. Exact SymPy values are simplified only for mathematically appropriate final expressions; ordered rendering masks prevent CAS from removing endpoint arithmetic.

## Repairs and interpretation

q-124664 duplicate wrong option: the original 42/7 and 6 are equal, so one raw bank is invalid; replace only 42/7 with I/2=53/12, a supported omission of the explicit factor2. q-90871 endpoint: compose before taking the right-hand limit; cos(πt²/t²)→cosπ and the polynomial term is finite, yielding2π−1. The normal problem states the one-sided composed extension; no interior pole is allowed. Cube-root curves use the regular supported parameterization x=t³,y=t rather than the infinite derivative of y=x^(1/3) at x=0. Notation repairs remove overescaped bank TeX and format natural logs as ln; they are separate from the duplicate-bank correction.

## Identity

Content UUID depends on version and actual printed prompt, fixed solution, full displayed bank and correct mathematical fragment; seed/shuffle/profile labels/unused parameters do not enter. Mathematical-task fingerprint uses the actual Cartesian relation, one-form and oriented x endpoint limits; banks/profile names do not enter. Parameterization is a solution tool; the assessed graph and traversal identify the task.

## Original widget inspection

Original MA3703 widgets q39344/q81178 confirm five-option multiple-choice layout and captured values. Other assigned question widgets are absent from the local six-question lesson snapshot; fixed-basis source capture remains their evidence. widget-evidence.json preserves those checks and the explicit linked curriculum order.
