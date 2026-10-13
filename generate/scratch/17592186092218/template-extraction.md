# Template extraction

## Stage 1: specific observed questions

All numbers are exact. Radius is a positive integer except q-17124 (1/3); angles are familiar unit-circle values, expressed in degrees, radians, or zero. x/y are Cartesian output coordinates, P the described point, r/theta the interpreted polar quantities. Original punctuation and all worked-solution row prefixes/groupings are preserved by complete-component masks. Decoded-byte inspection shows no adjacent backslashes in answer commands; ord samples contain a single byte 92 before commands. JSON output escaping is not a TeX defect. Source row separators are genuine double-backslash TeX, retained.

### q-17133 / legacy_radian_radio

Original: Given that the distance from a point $P$ to the origin is $1$, and that $P$ makes an angle of $\frac{5π}{3}$ with the positive $x$-axis, what are the Cartesian coordinates of $P$?

Parameters: `{"radius": "1", "angle": "5/3", "unit": "radians"}`. Field attributes: `[{"key": "selection", "type": ":answer-field.type/radio", "answer_type": ":answer.type/math", "correct_present": false}]`.

### q-8522 / legacy_degree_radio

Original: Given that the distance from a point $P$ to the origin is $5$, and that $P$ makes an angle of $330^{∘}$ with the positive $x$-axis, what are the Cartesian coordinates of $P$?

Parameters: `{"radius": "5", "angle": "330", "unit": "degrees"}`. Field attributes: `[{"key": "selection", "type": ":answer-field.type/radio", "answer_type": ":answer.type/math", "correct_present": false}]`.

### q-120328 / degree_unrepeated_radio

Original: Given that the distance from a point $P$ to the origin is $6,$ and that $P$ makes an angle of ${315}^{∘}$ with the positive $x$-axis, what are the Cartesian coordinates of $P?$

Parameters: `{"radius": "6", "angle": "315", "unit": "degrees"}`. Field attributes: `[{"key": "selection", "type": ":answer-field.type/radio", "answer_type": ":answer.type/math", "correct_present": true}]`.

### q-17124 / radian_negative_fraction_radio

Original: Given that the distance from a point $P$ to the origin is $\frac{1}{3},$ and that $P$ makes an angle of $\frac{5\pi }{4}$ with the positive $x$-axis, what are the Cartesian coordinates of $P?$

Parameters: `{"radius": "1/3", "angle": "5/4", "unit": "radians"}`. Field attributes: `[{"key": "selection", "type": ":answer-field.type/radio", "answer_type": ":answer.type/math", "correct_present": true}]`.

### q-17126 / radian_mixed_radio

Original: Given that the distance from a point $P$ to the origin is $2,$ and that $P$ makes an angle of $\frac{7\pi }{4}$ with the positive $x$-axis, what are the Cartesian coordinates of $P?$

Parameters: `{"radius": "2", "angle": "7/4", "unit": "radians"}`. Field attributes: `[{"key": "selection", "type": ":answer-field.type/radio", "answer_type": ":answer.type/math", "correct_present": true}]`.

### q-17128 / axis_radian_radio

Original: Given that the distance from a point $P$ to the origin is $2,$ and that $P$ makes an angle of $\frac{3\pi }{2}$ with the positive $x$-axis, what are the Cartesian coordinates of $P?$

Parameters: `{"radius": "2", "angle": "3/2", "unit": "radians"}`. Field attributes: `[{"key": "selection", "type": ":answer-field.type/radio", "answer_type": ":answer.type/math", "correct_present": true}]`.

### q-17134 / radian_repeated_radio

Original: Given that the distance from a point $P$ to the origin is $4,$ and that $P$ makes an angle of $\frac{4\pi }{3}$ with the positive $x$-axis, what are the Cartesian coordinates of $P?$

Parameters: `{"radius": "4", "angle": "4/3", "unit": "radians"}`. Field attributes: `[{"key": "selection", "type": ":answer-field.type/radio", "answer_type": ":answer.type/math", "correct_present": true}]`.

### q-17137 / axis_zero_radio

Original: Given that the distance from a point $P$ to the origin is $7,$ and that $P$ makes an angle of $0$ with the positive $x$-axis, what are the Cartesian coordinates of $P?$

Parameters: `{"radius": "7", "angle": "0", "unit": "radians"}`. Field attributes: `[{"key": "selection", "type": ":answer-field.type/radio", "answer_type": ":answer.type/math", "correct_present": true}]`.

### q-276786 / radian_blank

Original: If the distance from a point $P$ to the origin is $8,$ and that $P$ makes an angle of $\frac{7\pi }{4}$ with the positive $x$-axis, then the Cartesian coordinates of $P$ are$\,(${{field-1}}$,$
{{field-2}}$).$

Parameters: `{"radius": "8", "angle": "7/4", "unit": "radians"}`. Field attributes: `[{"key": "field-1", "type": ":answer-field.type/blank", "answer_type": ":answer.type/math", "correct_present": true}, {"key": "field-2", "type": ":answer-field.type/blank", "answer_type": ":answer.type/math", "correct_present": true}]`.

### q-276791 / degree_blank

Original: If the distance from a point $P$ to the origin is $12,$ and that $P$ makes an angle of ${60}^{∘}$ with the positive $x$-axis, then the Cartesian coordinates of $P$ are$\,(${{field-1}}$,$
{{field-2}}$).$

Parameters: `{"radius": "12", "angle": "60", "unit": "degrees"}`. Field attributes: `[{"key": "field-1", "type": ":answer-field.type/blank", "answer_type": ":answer.type/math", "correct_present": true}, {"key": "field-2", "type": ":answer-field.type/blank", "answer_type": ":answer.type/math", "correct_present": true}]`.

### q-276798 / degree_signed_blank

Original: If the distance from a point $P$ to the origin is $3,$ and that $P$ makes an angle of ${240}^{∘}$ with the positive $x$-axis, then the Cartesian coordinates of $P$ are$\,(${{field-1}}$,$
{{field-2}}$).$

Parameters: `{"radius": "3", "angle": "240", "unit": "degrees"}`. Field attributes: `[{"key": "field-1", "type": ":answer-field.type/blank", "answer_type": ":answer.type/math", "correct_present": true}, {"key": "field-2", "type": ":answer-field.type/blank", "answer_type": ":answer.type/math", "correct_present": true}]`.

### q-8516 / degree_signed_radio

Original: Given that the distance from a point $P$ to the origin is $8,$ and that $P$ makes an angle of ${150}^{∘}$ with the positive $x$-axis, what are the Cartesian coordinates of $P?$

Parameters: `{"radius": "8", "angle": "150", "unit": "degrees"}`. Field attributes: `[{"key": "selection", "type": ":answer-field.type/radio", "answer_type": ":answer.type/math", "correct_present": true}]`.

## Stage 2: shared mathematical pattern

Read the given distance as r and the given angle from the positive x-axis as theta. Compute x=r cos(theta) and y=r sin(theta), returning a complete coordinate tuple (radio) or its two scalar fragments (paired blanks). The solution states the interpreted polar coordinates, the conversion formulas, then four rows for x and four for y: formal component, substituted trigonometric expression, evaluated trigonometric product, simplified coordinate. It finishes with the complete Cartesian tuple. Source-specific punctuation, repeated x/y row prefixes, multiplication-dot/grouping choices and omitted words remain separate masks.

## Stage 3: component and complete-bank map

R is the radius; X=R cos(theta), Y=R sin(theta). Each expression below computes a complete displayed tuple from those quantities. Scalar-factor patterns in opaque historical banks are evidence component patterns, not recovered learner mistakes. No independent random perturbation or polynomial fitting is used. All nine historical banks remain public raw profiles and evidence only, including the banks also used in eligible normal variants. The four defensible bank shapes (sign/root substitution, sign/half-factor, down-axis, right-axis) are separately identified as source profiles in normal generation; their original-angle constraints and whole-bank collision checks apply. The remaining radio masks receive a separately authored method-sign-scale bank for normal practice.

### Complete bank raw-q-17133

- Field `selection`, choice `83908dd0-d198-52b3-8826-afa1429dbb50`: `(-\frac{1}{2}, \frac{\sqrt{3}}{2})` -> `(-R/2,R*sqrt(3)/2)`; original designation absent.
- Field `selection`, choice `9ae2cd5b-f109-5dbb-bf75-ab22f3567103`: `(\frac{1}{2},-\frac{\sqrt{3}}{2})` -> `(R/2,-R*sqrt(3)/2)`; original designation absent.
- Field `selection`, choice `0c3da346-d7d9-5148-b044-6261a6a7a773`: `(-\frac{\sqrt{3}}{2},-\frac{\sqrt{3}}{2})` -> `(-R*sqrt(3)/2,-R*sqrt(3)/2)`; original designation absent.
- Field `selection`, choice `46f644a7-41c7-575e-90ea-b0bdf7907385`: `(-\frac{\sqrt{3}}{2}, \frac{1}{2})` -> `(-R*sqrt(3)/2,R/2)`; original designation absent.
- Field `selection`, choice `4e49a3e0-69dd-5cc5-8e4e-d960cd9640b6`: `(\frac{1}{2},-\frac{1}{2})` -> `(R/2,-R/2)`; original designation absent.
### Complete bank raw-q-8522

- Field `selection`, choice `a09efa26-c8e0-5412-ab88-3198ac483f85`: `(-\frac{5\sqrt{2}}{2}, 5)` -> `(-R*sqrt(2)/2,R)`; original designation absent.
- Field `selection`, choice `b4663627-6e87-5b9e-ad2a-b45c4d9efc23`: `(\frac{5\sqrt{2}}{2},-\frac{5}{2})` -> `(R*sqrt(2)/2,-R/2)`; original designation absent.
- Field `selection`, choice `c31e9187-659c-536b-a14a-1ed24aef0f88`: `(\frac{5\sqrt{3}}{2},-5)` -> `(R*sqrt(3)/2,-R)`; original designation absent.
- Field `selection`, choice `5fc26997-f5ab-5e99-9de1-52c2d410ae79`: `(5, \frac{5\sqrt{2}}{2})` -> `(R,R*sqrt(2)/2)`; original designation absent.
- Field `selection`, choice `79adfbc5-24f9-5b5d-b471-2c462b1283f3`: `(\frac{5\sqrt{3}}{2},-\frac{5}{2})` -> `(R*sqrt(3)/2,-R/2)`; original designation absent.
### Complete bank raw-q-120328

- Field `selection`, choice `48fc86a1-f2ca-5fb6-98bb-2ba50587b6e1`: `(3\sqrt{2},-3\sqrt{2})` -> `(X,Y)`; original designation correct.
- Field `selection`, choice `6e2e5dea-eb32-5ef7-b053-292457b74c17`: `(\frac{3\sqrt{2}}{2},-\frac{3\sqrt{2}}{2})` -> `(X/2,Y/2)`; original designation incorrect.
- Field `selection`, choice `a8e86342-c856-59b9-acc7-8c16b2779f05`: `(2\sqrt{3},-2\sqrt{3})` -> `(R*sqrt(3)/3,-R*sqrt(3)/3)`; original designation incorrect.
- Field `selection`, choice `bceb10bc-923e-5dff-8dfb-386a60cdb562`: `(-6\sqrt{2},6\sqrt{2})` -> `(-R*sqrt(2),R*sqrt(2))`; original designation incorrect.
- Field `selection`, choice `cd3e4f69-01dd-5d42-b6e1-f9b19a563b4f`: `(\frac{2\sqrt{3}}{3},-\frac{2\sqrt{3}}{3})` -> `(R*sqrt(3)/9,-R*sqrt(3)/9)`; original designation incorrect.
### Complete bank raw-q-17124

- Field `selection`, choice `753543d7-b063-5cf6-b128-a80a7409bfa6`: `(-\frac{\sqrt{2}}{4},-\frac{\sqrt{2}}{4})` -> `(-sqrt(2)/(1/R+1),-sqrt(2)/(1/R+1))`; original designation incorrect.
- Field `selection`, choice `76d18bf0-adc0-56ad-a666-eb6830554a32`: `(-\frac{\sqrt{2}}{2},-\frac{\sqrt{2}}{2})` -> `(-sqrt(2)/2,-sqrt(2)/2)`; original designation incorrect.
- Field `selection`, choice `9e0cfff2-f165-5112-84b4-84ef6d0d16d8`: `(-\frac{\sqrt{2}}{3},-\frac{\sqrt{2}}{3})` -> `(-R*sqrt(2),-R*sqrt(2))`; original designation incorrect.
- Field `selection`, choice `b46da797-d4b1-5e93-b5d2-956b71f67813`: `(-\frac{\sqrt{2}}{6},-\frac{\sqrt{2}}{6})` -> `(X,Y)`; original designation correct.
- Field `selection`, choice `e9302e03-d1d5-5540-a03c-b0e2ce178144`: `(-\frac{\sqrt{2}}{5},-\frac{\sqrt{2}}{5})` -> `(-sqrt(2)/(1/R+2),-sqrt(2)/(1/R+2))`; original designation incorrect.
### Complete bank raw-q-17126

- Field `selection`, choice `6579eacc-068b-5cac-8c3b-3d0005500a11`: `(-\sqrt{2},\sqrt{2})` -> `(-X,-Y)`; original designation incorrect.
- Field `selection`, choice `77f0a4c2-79c0-54cd-8fc3-9692d5df1551`: `(\sqrt{2},\sqrt{2})` -> `(X,-Y)`; original designation incorrect.
- Field `selection`, choice `88c83019-e455-582f-ae36-d2343335742f`: `(\sqrt{2},-\sqrt{3})` -> `(X,-R*sqrt(3)/2)`; original designation incorrect.
- Field `selection`, choice `9919d5ba-4b95-5580-84fc-627c631faff2`: `(-\sqrt{2},-\sqrt{2})` -> `(-X,Y)`; original designation incorrect.
- Field `selection`, choice `baa4a7a7-5652-5d2b-84aa-4fd087f99b43`: `(\sqrt{2},-\sqrt{2})` -> `(X,Y)`; original designation correct.
### Complete bank raw-q-17128

- Field `selection`, choice `359a8b1a-2e90-5221-b6b6-45c8e9ae12e9`: `(0,2)` -> `(0,R)`; original designation incorrect.
- Field `selection`, choice `5b3df71b-aee2-5f35-9b12-53d884eac1df`: `(0,1)` -> `(0,1)`; original designation incorrect.
- Field `selection`, choice `65df5433-d222-576b-bdee-9211bd3a1f8b`: `(0,-2)` -> `(0,-R)`; original designation correct.
- Field `selection`, choice `6d834bc3-a336-5730-9fdf-30a9b3c13603`: `(2,0)` -> `(R,0)`; original designation incorrect.
- Field `selection`, choice `fba3c6d5-e0fb-5390-90be-e8ccc191e99a`: `(-2,0)` -> `(-R,0)`; original designation incorrect.
### Complete bank raw-q-17134

- Field `selection`, choice `1f7d1dc9-08a0-5c97-af85-8958c4f26edc`: `(2,-2\sqrt{3})` -> `(-X,Y)`; original designation incorrect.
- Field `selection`, choice `630c3a59-ef83-541f-b9f3-e86f0db79abb`: `(-2,\sqrt{3})` -> `(X,-Y/2)`; original designation incorrect.
- Field `selection`, choice `6d760ce6-7b53-5b17-95f0-2a701da851f0`: `(2,\sqrt{3})` -> `(-X,-Y/2)`; original designation incorrect.
- Field `selection`, choice `6fda8237-6723-59bd-aa75-aa04c8fefcec`: `(-2,-2\sqrt{3})` -> `(X,Y)`; original designation correct.
- Field `selection`, choice `8297ba5c-921d-5ae0-bd90-2ee58b877b3a`: `(2,2\sqrt{3})` -> `(-X,-Y)`; original designation incorrect.
### Complete bank raw-q-17137

- Field `selection`, choice `0068e4a5-cb28-5519-9eed-397f1fd495ba`: `(0,7)` -> `(0,R)`; original designation incorrect.
- Field `selection`, choice `24c5f2d9-5d73-5dfb-8877-22831e9dfcc2`: `(7,1)` -> `(R,1)`; original designation incorrect.
- Field `selection`, choice `2fc39e53-d504-5253-a096-83f4724ee131`: `(7,0)` -> `(R,0)`; original designation correct.
- Field `selection`, choice `62a281e2-ead9-5741-8c03-34eb83922464`: `(1,0)` -> `(1,0)`; original designation incorrect.
- Field `selection`, choice `eba4daee-0b6f-57bd-8eb5-6f8a3b202d40`: `(-7,0)` -> `(-R,0)`; original designation incorrect.
### Complete bank raw-q-276786

- Field `field-1`, choice `4ac03d3b-2532-57c0-b9b4-500023e08f39`: `4\sqrt{2}` -> `X`; original designation correct.
- Field `field-2`, choice `bad2a675-9325-5f9e-98e8-a2644c41a27d`: `-4\sqrt{2}` -> `Y`; original designation correct.
### Complete bank raw-q-276791

- Field `field-1`, choice `c8687607-80ff-5873-a6e5-4e7b5b0a8602`: `6` -> `X`; original designation correct.
- Field `field-2`, choice `9f01dce6-e066-51e9-8e04-c9e737fc1a0f`: `6\sqrt{3}` -> `Y`; original designation correct.
### Complete bank raw-q-276798

- Field `field-1`, choice `76b9b4bb-41ee-5123-9c9a-81ee28b29a2c`: `-\frac{3}{2}` -> `X`; original designation correct.
- Field `field-2`, choice `3e8a5a4c-630b-516e-b8e0-968782ed3ec0`: `-\frac{3\sqrt{3}}{2}` -> `Y`; original designation correct.
### Complete bank raw-q-8516

- Field `selection`, choice `040aa995-2a95-5978-ae2e-5bf3e64df54b`: `(4\sqrt{3},2\sqrt{3})` -> `(-X,R*sqrt(3)/4)`; original designation incorrect.
- Field `selection`, choice `327eef0b-6d33-56b7-b7fa-65647e6064b0`: `(4\sqrt{3},4)` -> `(-X,Y)`; original designation incorrect.
- Field `selection`, choice `8813249a-4b08-5911-ab6e-9dfd026fab0b`: `(-4\sqrt{3},4\sqrt{2})` -> `(X,R*sqrt(2)/2)`; original designation incorrect.
- Field `selection`, choice `d6f4b322-8686-56b2-9216-36cb838b3f08`: `(-4\sqrt{3},4)` -> `(X,Y)`; original designation correct.
- Field `selection`, choice `dcf46c88-e2c1-5c74-915f-85de76f4b18a`: `(-4\sqrt{3},8\sqrt{3})` -> `(X,R*sqrt(3))`; original designation incorrect.

## Stage 4: reusable masks, domains, and repairs

recipes.json records all complete prompt/solution masks, fields and attribute-presence bits. build_extraction.py creates slots only for the complete radius, angle, tuple, substituted component, evaluated product and final coordinate; it never globally replaces short numerals. The historical option rendering retains per-source comma spaces. The normal solution masks use the source trigonometric notation and fixed full sentences, independent of selected mistake.

For nonunit nonaxis defaults, the complete authored method bank is (X,Y), (-X,Y), (X,-Y), (-X,-Y), (cos(theta),sin(theta)): reverse one or both quadrant signs and omit radius scaling. At authored unit-radius easy, omitting the radius would duplicate the correct tuple, so the final distractor interchanges sine/cosine; equal-magnitude angles instead use the explicitly eligible doubled-radius product (2X,2Y). The complete bank is selected by this mathematical condition before construction; no first-valid replacement pool is used. These easy bank shapes are authored method mistakes, not recovered historical recipes.

Source-normal profiles: q-17126 reverses signs or substitutes sqrt(3)/2 for the negative sine at 315 degrees; q-17134 reverses signs and halves the y scaling at 240 degrees; q-17128 interchanges the axes, reverses direction, or omits radius in the positive-axis distractor; q-17137 interchanges axes, replaces zero by one, omits radius, or reverses x. Profiles stay intact; duplicates reject the entire instance.

Unrated q-17133 and q-8522 have mathematically unique correct options (1/2,-sqrt(3)/2) and (5sqrt(3)/2,-5/2), independently derived; raw replay leaves absent refs/difficulty/solution absent and marks evidence_only. They cannot enter native grading fixtures without authored refs, so no native pass is claimed for these original records. An authored evidence level assignment moderate indexes their replay only; it is not a recovered label.

q-17128's second heading says x-coordinate although every y-stage equation and conclusion are correct. Raw replay preserves that original wording; normal output changes only that heading to y-coordinate. This is a prose repair, not a mathematical or TeX repair. Exact raw solution count and normal repaired prose are reported separately. No other source error was found.

Profiles require source angles in raw evidence replay but radius varies exactly; the complete bank components are recomputed. No raw branch returns a captured question or answer lookup payload. Normal sampling includes the legacy degree/radian prompt masks with explicitly authored solutions and inferred correct references, while raw omissions stay intact. It selects every eligible source-shaped family at each level before radius sampling, with opaque historical profiles excluded from learner defaults. All output is local review JSON, never transaction EDN.
