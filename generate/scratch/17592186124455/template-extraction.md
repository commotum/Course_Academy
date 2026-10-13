# Template extraction

## 1. Describe each original

Each row below is a complete individual record. source.json retains all EDB attribute presence, identities, original banks, missing refs and errors. source-templates.json retains full sentence/row masks, coordinate factors and numeric spelling components; source-cases.json records original parameters. Original MA widgets for q36391/q65204 are saved in original-widgets.json.

### q-36391

Consider the plane curve $x^{2}y = xy + 4$. Find a tangent vector to that curve at the point $(2, 2)$.

Observed difficulty: unrated. Symbolic implicit expression: `x**2*y - x*y`. Point: `(2,2)`. Evaluated derivative pair: `[6, 2]`.

Field0: key `selection`; radio; source correct-ref present: False.

| Choice UUID | Full observed component | Correct designation | Mathematical tangent condition | Recipe interpretation |
|---|---|---|---|---|
| adfa4a9b-088c-5d4c-a06a-f83cff46387a | `6i + 2j` | unmarked | False | fixed opaque complete observed expression; no inferred error operation |
| bc43c78b-b71e-59cc-86a1-ed21b4906ff7 | `2i - 6j` | unmarked | True | computed f_y,-f_x with captured scalar spelling |
| 166843cc-f599-540c-a895-790beb61e4f8 | `6i` | unmarked | False | fixed opaque complete observed expression; no inferred error operation |
| 4c8d92ed-bd29-5e78-ac9c-40789085eb1c | `6i - j` | unmarked | False | fixed opaque complete observed expression; no inferred error operation |
| 75ba95d3-ccdd-5335-bc47-1bc87a3a2f26 | `3i + 2j` | unmarked | False | fixed opaque complete observed expression; no inferred error operation |

Full worked-solution string present: False. Ordered sentence and mathematical masks retain rearrangement, level definition, formula, formal partial-operator inputs, symbolic component derivatives, original coordinate-factor evaluation row, final collected vector and concluding sentence. q36391 has no observed solution and receives a separately authored completion.

### q-65204

Consider the plane curve $\operatorname{cos}⁡x\operatorname{cos}⁡y=\operatorname{sin}⁡(xy).$ Find a tangent vector to that curve at the point $(0,\frac{\pi }{2}).$

Observed difficulty: moderate. Symbolic implicit expression: `-sin(x*y) + cos(x)*cos(y)`. Point: `(0,pi/2)`. Evaluated derivative pair: `[-pi/2, -1]`.

Field0: key `selection`; radio; source correct-ref present: False.

| Choice UUID | Full observed component | Correct designation | Mathematical tangent condition | Recipe interpretation |
|---|---|---|---|---|
| cb45de19-662d-5d40-8c9f-bbab41e8b53e | `i + \frac{π}{2}j` | unmarked | False | fixed opaque complete observed expression; no inferred error operation |
| 2a2d68dc-8a02-5aaf-bc95-d03534713413 | `-\frac{π}{2}i + j` | unmarked | False | fixed opaque complete observed expression; no inferred error operation |
| 5a8566cd-85af-5590-bb6a-4011fa8ce372 | `-i - j` | unmarked | False | fixed opaque complete observed expression; no inferred error operation |
| 74712c7b-e3ca-5c16-8204-9da1f79907ba | `-i + \frac{π}{2}j` | unmarked | True | computed f_y,-f_x with captured scalar spelling |
| 78e79b08-e49f-5790-abb9-6e44dbd739b1 | `-\frac{π}{2}i - j` | unmarked | False | fixed opaque complete observed expression; no inferred error operation |
Field1: key `selection`; radio; source correct-ref present: True.

| Choice UUID | Full observed component | Correct designation | Mathematical tangent condition | Recipe interpretation |
|---|---|---|---|---|
| 323ab6d8-7707-5cf4-a618-ba17b3923dd9 | `-i+\frac{\pi }{2}\,j` | marked | True | computed f_y,-f_x with captured scalar spelling |
| 043f0c6b-beee-5929-91a6-329b0aba6cab | `i+\frac{\pi }{2}\,j` | unmarked | False | fixed opaque complete observed expression; no inferred error operation |
| 6c7f3a73-6bb3-57e1-b890-8a39b32ac5a3 | `-\frac{\pi }{2}\,i+j` | unmarked | False | fixed opaque complete observed expression; no inferred error operation |
| b9bd5e2f-eea5-58c3-8f18-2c41ef884348 | `-i-j` | unmarked | False | fixed opaque complete observed expression; no inferred error operation |
| cb787b13-c2e5-5275-b510-4a2ee9675a16 | `-\frac{\pi }{2}\,i-j` | unmarked | False | fixed opaque complete observed expression; no inferred error operation |

Full worked-solution string present: True. Ordered sentence and mathematical masks retain rearrangement, level definition, formula, formal partial-operator inputs, symbolic component derivatives, original coordinate-factor evaluation row, final collected vector and concluding sentence. q36391 has no observed solution and receives a separately authored completion.

### q-130198

Consider the plane curve $x\operatorname{cos}⁡y=-y\operatorname{sin}⁡x+\frac{\pi }{2}.$ Find a tangent vector to that curve at the point $(\frac{\pi }{2},0).$

Observed difficulty: moderate. Symbolic implicit expression: `x*cos(y) + y*sin(x)`. Point: `(pi/2,0)`. Evaluated derivative pair: `[1, 1]`.

Field0: key `selection`; radio; source correct-ref present: True.

| Choice UUID | Full observed component | Correct designation | Mathematical tangent condition | Recipe interpretation |
|---|---|---|---|---|
| 0ab7ecfb-6837-5f43-a7dc-5de26787b651 | `i-j` | marked | True | computed f_y,-f_x with captured scalar spelling |
| 23c6bb01-4817-5934-b31c-f94122a313f8 | `-2\,i+j` | unmarked | False | fixed opaque complete observed expression; no inferred error operation |
| 4d97af51-08fe-5c7f-90df-c14d7845e35f | `\frac{\pi }{2}\,i+j` | unmarked | False | fixed opaque complete observed expression; no inferred error operation |
| 96b21983-40a1-5c92-8a77-84386b07a32d | `-i-\frac{\pi }{2}\,j` | unmarked | False | fixed opaque complete observed expression; no inferred error operation |
| eae56032-740f-556c-b1d0-0bf3c280086c | `i+2\,j` | unmarked | False | fixed opaque complete observed expression; no inferred error operation |

Full worked-solution string present: True. Ordered sentence and mathematical masks retain rearrangement, level definition, formula, formal partial-operator inputs, symbolic component derivatives, original coordinate-factor evaluation row, final collected vector and concluding sentence. q36391 has no observed solution and receives a separately authored completion.

### q-130200

Consider the plane curve $x{e}^{{y}^{2}+1}=e-y.$ Find a tangent vector to that curve at the point $(1,0).$

Observed difficulty: moderate. Symbolic implicit expression: `x*exp(y**2 + 1) + y`. Point: `(1,0)`. Evaluated derivative pair: `[E, 1]`.

Field0: key `selection`; radio; source correct-ref present: True.

| Choice UUID | Full observed component | Correct designation | Mathematical tangent condition | Recipe interpretation |
|---|---|---|---|---|
| 1db8855f-407d-543c-b41c-01ec8863c250 | `i+{e}^{2}\,j` | unmarked | False | fixed opaque complete observed expression; no inferred error operation |
| 310e7ac2-6457-50a9-b85b-62fe72227f50 | `i-e\,j` | marked | True | computed f_y,-f_x with captured scalar spelling |
| 313c22eb-142a-5e0a-bbf7-3e694214c7e6 | `2\,i` | unmarked | False | fixed opaque complete observed expression; no inferred error operation |
| 3ef9f166-57a7-581f-b069-feefd3a089a9 | `-j` | unmarked | False | fixed opaque complete observed expression; no inferred error operation |
| 66d4bf27-1916-5b14-ad54-71713514a6d7 | `2e\,i+j` | unmarked | False | fixed opaque complete observed expression; no inferred error operation |

Full worked-solution string present: True. Ordered sentence and mathematical masks retain rearrangement, level definition, formula, formal partial-operator inputs, symbolic component derivatives, original coordinate-factor evaluation row, final collected vector and concluding sentence. q36391 has no observed solution and receives a separately authored completion.

### q-37516

Consider the plane curve $2x\operatorname{ln}⁡y=8xy+2-8e.$ Find a tangent vector to that curve at the point $(1,e).$

Observed difficulty: moderate. Symbolic implicit expression: `-8*x*y + 2*x*log(y)`. Point: `(1,E)`. Evaluated derivative pair: `[2 - 8*E, -8 + 2*exp(-1)]`.

Field0: key `selection`; radio; source correct-ref present: True.

| Choice UUID | Full observed component | Correct designation | Mathematical tangent condition | Recipe interpretation |
|---|---|---|---|---|
| 18cbb66c-c87e-532e-b215-79cebdd50220 | `(2e-8)\,i+(\frac{e}{2}-8)j` | unmarked | False | fixed opaque complete observed expression; no inferred error operation |
| 25737ab8-5934-517a-82e3-355f226249ae | `(1-4e)\,i+(\frac{2}{e}-8)j` | unmarked | False | fixed opaque complete observed expression; no inferred error operation |
| 569fd915-b891-5273-a763-b23c030c775d | `(2-8e)\,i+(2-8e)j` | unmarked | False | fixed opaque complete observed expression; no inferred error operation |
| 91bfacf0-e81a-591f-b5c7-eb843413fffc | `(\frac{2}{e}-8)i+(8e-2)\,j` | marked | True | computed f_y,-f_x with captured scalar spelling |
| e6c24a19-a0b8-5781-9f03-f3684c7d7f7c | `(8-2e)\,i+(\frac{8}{e}-2)j` | unmarked | False | fixed opaque complete observed expression; no inferred error operation |

Full worked-solution string present: True. Ordered sentence and mathematical masks retain rearrangement, level definition, formula, formal partial-operator inputs, symbolic component derivatives, original coordinate-factor evaluation row, final collected vector and concluding sentence. q36391 has no observed solution and receives a separately authored completion.

### q-72400

Consider the plane curve ${x}^{2}+{y}^{2}=2xy+9.$ Find a tangent vector to that curve at the point $(-1,2).$

Observed difficulty: moderate. Symbolic implicit expression: `x**2 - 2*x*y + y**2`. Point: `(-1,2)`. Evaluated derivative pair: `[-6, 6]`.

Field0: key `selection`; radio; source correct-ref present: True.

| Choice UUID | Full observed component | Correct designation | Mathematical tangent condition | Recipe interpretation |
|---|---|---|---|---|
| 5a7f7daf-eab5-5f09-9994-fb78510d1452 | `6\,i+6\,j` | marked | True | computed f_y,-f_x with captured scalar spelling |
| 5bdf6205-616a-5fe8-bae1-1eafc7069834 | `i-j` | unmarked | False | fixed opaque complete observed expression; no inferred error operation |
| 5f640f70-dd55-53af-a444-45f3d1013ded | `2\,i-j` | unmarked | False | fixed opaque complete observed expression; no inferred error operation |
| 6d1b9f33-c38c-59c8-99f2-2467570782ed | `i+6\,j` | unmarked | False | fixed opaque complete observed expression; no inferred error operation |
| 9f2d1ea8-f373-5f19-800d-34e70ba82c85 | `2\,i-6\,j` | unmarked | False | fixed opaque complete observed expression; no inferred error operation |

Full worked-solution string present: True. Ordered sentence and mathematical masks retain rearrangement, level definition, formula, formal partial-operator inputs, symbolic component derivatives, original coordinate-factor evaluation row, final collected vector and concluding sentence. q36391 has no observed solution and receives a separately authored completion.

### q-72463

Consider the plane curve $2{x}^{3}{y}^{2}-4xy=1-3x.$ Find a tangent vector to that curve at the point $(1,1).$

Observed difficulty: moderate. Symbolic implicit expression: `2*x**3*y**2 - 4*x*y + 3*x`. Point: `(1,1)`. Evaluated derivative pair: `[5, 0]`.

Field0: key `selection`; radio; source correct-ref present: True.

| Choice UUID | Full observed component | Correct designation | Mathematical tangent condition | Recipe interpretation |
|---|---|---|---|---|
| 2a24f4b8-a184-5828-8c72-dcc5b94e5943 | `5\,i-5\,j` | unmarked | False | fixed opaque complete observed expression; no inferred error operation |
| 2afed586-1f6a-50fd-ad21-c54f17e514f5 | `i` | unmarked | False | fixed opaque complete observed expression; no inferred error operation |
| af297190-71a7-5741-8317-95edf63e83e2 | `i+5\,j` | unmarked | False | fixed opaque complete observed expression; no inferred error operation |
| be71b2b4-857d-5122-ac95-bc07fb632330 | `5\,i-j` | unmarked | False | fixed opaque complete observed expression; no inferred error operation |
| c71d302c-3c74-5be4-b48a-d3f52171a59d | `-5\,j` | marked | True | computed f_y,-f_x with captured scalar spelling |

Full worked-solution string present: True. Ordered sentence and mathematical masks retain rearrangement, level definition, formula, formal partial-operator inputs, symbolic component derivatives, original coordinate-factor evaluation row, final collected vector and concluding sentence. q36391 has no observed solution and receives a separately authored completion.

### q-130201

Consider the plane curve $xy=3-{x}^{2}-{y}^{3}.$ Find a tangent vector to that curve at the point $(-1,-1).$

Observed difficulty: moderate. Symbolic implicit expression: `x**2 + x*y + y**3`. Point: `(-1,-1)`. Evaluated derivative pair: `[-3, 2]`.

Field0: key `selection`; radio; source correct-ref present: True.

| Choice UUID | Full observed component | Correct designation | Mathematical tangent condition | Recipe interpretation |
|---|---|---|---|---|
| 29f3795a-9c5d-564b-99c5-8234a8f8adae | `3\,j` | unmarked | False | fixed opaque complete observed expression; no inferred error operation |
| 17117ea5-c48d-5a75-87dd-44fd4b306516 | `i-2\,j` | unmarked | False | fixed opaque complete observed expression; no inferred error operation |
| a1a1d040-84f6-5093-b8b7-a02c512a3ef2 | `3\,i-2\,j` | unmarked | False | fixed opaque complete observed expression; no inferred error operation |
| afb47ff5-03cb-5158-9e15-6ff6eeca5436 | `-2\,i` | unmarked | False | fixed opaque complete observed expression; no inferred error operation |
| 0c788786-b66b-5944-b4ad-21c56064f8a1 | `2\,i+3\,j` | marked | True | computed f_y,-f_x with captured scalar spelling |

Full worked-solution string present: True. Ordered sentence and mathematical masks retain rearrangement, level definition, formula, formal partial-operator inputs, symbolic component derivatives, original coordinate-factor evaluation row, final collected vector and concluding sentence. q36391 has no observed solution and receives a separately authored completion.

### q-72388

Consider the plane curve $x+1={x}^{2}y.$ Find a tangent vector to that curve at the point $(1,2).$

Observed difficulty: moderate. Symbolic implicit expression: `x**2*y - x`. Point: `(1,2)`. Evaluated derivative pair: `[3, 1]`.

Field0: key `selection`; radio; source correct-ref present: True.

| Choice UUID | Full observed component | Correct designation | Mathematical tangent condition | Recipe interpretation |
|---|---|---|---|---|
| 4b63d502-5d59-57aa-8402-34f229d7c402 | `i-j` | unmarked | False | fixed opaque complete observed expression; no inferred error operation |
| d929314d-5095-5284-a04d-ed11a462fa9c | `i-3\,j` | marked | True | computed f_y,-f_x with captured scalar spelling |
| 47b22ede-a70a-5c2c-93d8-02196b170ae3 | `3\,i-2\,j` | unmarked | False | fixed opaque complete observed expression; no inferred error operation |
| 18da3830-6440-532f-9cfa-3f5d7f38caec | `2\,i+j` | unmarked | False | fixed opaque complete observed expression; no inferred error operation |
| 41a6476e-7908-5df0-9348-8c27d17118c4 | `2\,i+3\,j` | unmarked | False | fixed opaque complete observed expression; no inferred error operation |

Full worked-solution string present: True. Ordered sentence and mathematical masks retain rearrangement, level definition, formula, formal partial-operator inputs, symbolic component derivatives, original coordinate-factor evaluation row, final collected vector and concluding sentence. q36391 has no observed solution and receives a separately authored completion.

### q-130192

Consider the plane curve ${x}^{2}y={y}^{2}+3.$ Find a tangent vector to that curve at the point $(2,1).$

Observed difficulty: moderate. Symbolic implicit expression: `x**2*y - y**2`. Point: `(2,1)`. Evaluated derivative pair: `[4, 2]`.

Field0: key `selection`; radio; source correct-ref present: True.

| Choice UUID | Full observed component | Correct designation | Mathematical tangent condition | Recipe interpretation |
|---|---|---|---|---|
| b36ad97d-7477-5e7d-8ba7-295eb688f029 | `2\,j` | unmarked | False | fixed opaque complete observed expression; no inferred error operation |
| 118ee41d-f5a0-5dff-b95c-7ca94836bc57 | `3\,i` | unmarked | False | fixed opaque complete observed expression; no inferred error operation |
| 19b66868-06fe-5184-957b-7342b00b0910 | `2\,i-4\,j` | marked | True | computed f_y,-f_x with captured scalar spelling |
| bd3d37cc-037a-5d75-8a4d-47c54303cb93 | `2\,i-j` | unmarked | False | fixed opaque complete observed expression; no inferred error operation |
| 0ff73071-c5ea-582c-baaf-95b7a73e5652 | `i+2\,j` | unmarked | False | fixed opaque complete observed expression; no inferred error operation |

Full worked-solution string present: True. Ordered sentence and mathematical masks retain rearrangement, level definition, formula, formal partial-operator inputs, symbolic component derivatives, original coordinate-factor evaluation row, final collected vector and concluding sentence. q36391 has no observed solution and receives a separately authored completion.

### q-130194

Consider the plane curve $x\operatorname{ln}⁡y={x}^{2}-1.$ Find a tangent vector to that curve at the point $(-1,1).$

Observed difficulty: moderate. Symbolic implicit expression: `-x**2 + x*log(y)`. Point: `(-1,1)`. Evaluated derivative pair: `[2, -1]`.

Field0: key `selection`; radio; source correct-ref present: True.

| Choice UUID | Full observed component | Correct designation | Mathematical tangent condition | Recipe interpretation |
|---|---|---|---|---|
| 911d7e42-cfcf-516f-9283-caa49f997f72 | `2i` | unmarked | False | fixed opaque complete observed expression; no inferred error operation |
| 0e521a0c-e2f8-593e-ac64-9ff0e485a18b | `-i+j` | unmarked | False | fixed opaque complete observed expression; no inferred error operation |
| 35594e4f-af9b-5a65-8a40-4f8e1ea611be | `-i-2\,j` | marked | True | computed f_y,-f_x with captured scalar spelling |
| 2593f5c0-8a74-5dbd-9a7a-90d0d2eee839 | `j` | unmarked | False | fixed opaque complete observed expression; no inferred error operation |
| 99b82f0f-6ffa-5c51-818b-49987fd97f69 | `2i+j` | unmarked | False | fixed opaque complete observed expression; no inferred error operation |

Full worked-solution string present: True. Ordered sentence and mathematical masks retain rearrangement, level definition, formula, formal partial-operator inputs, symbolic component derivatives, original coordinate-factor evaluation row, final collected vector and concluding sentence. q36391 has no observed solution and receives a separately authored completion.

## 2. Shared pattern

Write the implicit curve as f(x,y)=k; evaluate f_y and-f_x at the specified point; select a nonzero vector tangent to the actual curve. Validity means ∇F(point)·v=0, so vectors proportional to the displayed formula are also mathematically correct. The bank audit checks all options by that criterion, including every source correct designation that exists. No source bank has a second tangent direction. q130201's specified point fails membership in the source curve, an independent prompt error.

## 3. Components and profiles

The per-source tables above map every field and choice. Twelve observed complete banks stay separate. Correct components are regenerated from actual symbolic derivatives; source scalar spelling masks preserve original notation at the original parameters. Incorrect opaque components remain explicit fixed expressions under the public raw/completed profile. They are not numerical fits and are not promoted as recovered historical error recipes. Their changed-point banks may have new mathematical ambiguities; the evidence record reports this limitation and stays ineligible for learning.

Authored method-bank has exactly five fixed operations: (f_y,-f_x); gradient (f_x,f_y); omit the rotation minus (f_y,f_x); reverse derivative roles with the same sign pattern(-f_x,f_y); omit the first family-defining summand before differentiation. All operations use actual displayed F and point. This bank is selected as a whole before sampling, and collisions reject the whole instance. No unused pool replacements or unrelated random perturbations occur.

## 4. Reusable masks and restrictions

Source masks preserve complete raw prose and ordered blocks, including omission of redundant numerical rows. The level constant, point tuple, every complete numeric coordinate factor and computed vector component are slots. Symbolic operator inputs and derivatives retain each source's own function structure. Authored templates derive F, its level, both partials, substituted-coordinate masks, individual evaluated coefficients and the final vector from exact SymPy data. Changed coordinates must remain within finite familiar forms and the actual arithmetic ceiling; logarithms require y>0. Raw malformed presentation is never silently called learner-ready.

## Source errors, repairs and limitations

- q36391: absent difficulty, worked solution and correct ref. Original MA1940 widget confirms one five-choice radio demand. Independent F_x=6,F_y=2 uniquely supports2i-6j. Completion adds that inferred ref, authored moderate label and full method solution. These are not matched observed attributes.
- q65204: two EDB fields share selection key; original MA1940 widget has one five-choice demand. Later field has correct ref and the same complete mathematical bank. Completion removes the earlier legacy field; both raw banks remain exact evidence. Decoded answer strings have only single-backslash runs. Additional slashes in JSON or tool output are serialization escaping, not a source-format anomaly. No backslash presentation repair is counted; source-format-audit.json records the decoded run lengths.
- q72463: rearrangement gives f=1 but level prose says f=0. Raw solution remains exact; completion corrects only the stated level.
- q130201: point(-1,-1) gives xy+x²+y³=1, while source constant is3. Completion changes the curve and its level/rearrangement constant to1, retaining the derivative/vector method. Correct vector values alone do not establish raw prompt correctness.

Raw exact denominators:11 prompts/key-presence layouts;12 banks/60 values;10 existing correct designations;10 full solution strings. Completions are counted separately. Authored easy/hard labels are design claims. Every historical profile, even repaired, remains evidence-only because distractor intent was not recovered.

Changed-point opaque evidence includes complete-bank ambiguity diagnostics in validation.json. For example q130192 at(-2,1) has both the regenerated vector2i+4j and historical choicei+2j as valid tangents. Both remain visible in evidence and the record is ineligible for learning. Native grader ID rejection of the second vector does not resolve that mathematical ambiguity.

## Conclusion-mask repair

Root independent readback found that q37516's final aligned vector and concluding prose used different comma-spacing notation. A global replacement of the aligned vector left the changed-point prose stale. Every source conclusion now has a separate complete vector component mask. Original inputs preserve the exact captured conclusion spelling; changed inputs recompute both components. Validation independently parses the concluding vector and the prose f(x,y) definition, and rejects the former stale-conclusion example. Runtime dependency/domain metadata does not participate in question identity; the corrected changed question does receive the identity of its corrected content.
