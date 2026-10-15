# Current source classification, basis 2715

Database math, lineage 01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1. Full source records are retained in initial/kp.edn and initial/kp.json. The basis-1356 draft remains immutable historical evidence. Current changes are formatting normalization, removal of the old duplicate selection membership on q-82874, and three additional source questions. Ten current source practices have ten radio fields, five math options each; nine are hard and one is unrated. No supplied .generated file exists.

| Source | Backbone | Observed level | Plot requirement | Bounded package treatment |

|---|---|---|---|---|

| q-38374 | unit shear, unshifted parabolic cap | unrated | none in source | simple; authored easy completion |

| q-82874 | quartic vs sloped line | hard | moderate, solution region | quartic; incorrect source factorization excluded from inventory |

| q-160885 | product hyperbola y±ax, two lower lines | hard | moderate, solution region | hyper_y |

| q-82878 | downward parabola with translated v | hard | moderate, solution region | down; incorrect inverse prose excluded from inventory |

| q-83943 | upward shifted parabola, horizontal cap | hard | moderate, solution region | up |

| q-83947 | upward shifted parabola, vertical cap | hard | moderate, solution region | vertical; source diagram misaligned, excluded from inventory |

| q-160710 | product hyperbola x±ay, two lower lines | hard | moderate, solution region | hyper_x |

| q-38132 | u=x+2y,v=x; v=u²−1 to v=1 | hard | moderate, solution region | source inventory validated; no sampler for this map orientation |

| q-83944 | u=x−y,v=y; v=3−u⁴ above v=2 | hard | moderate, solution region | not sampled; extra unmatched parenthesis in source integration row |

| q-82910 | u=x+y,v=y; cubic below quadratic on [0,1] | hard | moderate, solution region | not sampled; intersection system incorrectly states v=u as a general relation |



Ten distinct observed Markdown/value templates: seven historical families plus the new coefficient orientation q-38132, downward quartic q-83944, and cubic/quadratic q-82910. A map with a nonunit y coefficient and v=x is kept distinct from the historical v=x family because the determinant and inverse stages differ. New power combinations change primitive stages; they are not parameter slots of the existing parabola/quartic-versus-line families. All current source fields use selection/radio and math values. Each source remains its own complete bank profile; none is pooled.

## New template extraction and plots

q-38132 supplies u=x+2y,v=x, curve (x+2y)²−x−1=0 and line x=1. Domain −√2≤u≤√2,u²−1≤v≤1; inverse determinant −1/2 and area 4√2/3. Four stages retain substitution, intersections, determinant, reciprocal, inner integration and quadratic primitive endpoint arithmetic. Plot: red upward parabola v=u²−1, blue cap v=1, zero axes and dashed guides at ±√2; shaded bounded cap, vertical slice arrow. New plots would be required when bounds change.

q-83944 supplies u=x−y,v=y, curve y+(x−y)⁴=3 and line y=2. Domain −1≤u≤1,2≤v≤3−u⁴; determinant 1 and area 8/5. Four stages use a degree-five primitive u−u⁵/5, symmetric endpoints. Plot: red downward quartic v=3−u⁴, blue v=2, shaded cap, zero axes and guides at ±1. Preserve curve orientation; this is not the historical quartic-versus-line family. Extra closing parenthesis in the width row must be corrected in any future authored variant.

q-82910 supplies u=x+y,v=y and curves (x+y)³−y=0, (x+y)²−y=0. Domain 0≤u≤1,u³≤v≤u²; determinant 1, area 1/12. Intersection polynomial u²(u−1)=0 and two nonlinear bounds require cubic/quartic primitive terms. Plot: blue cubic lower boundary and red quadratic upper boundary, zero axes, endpoint guide at 1, shaded wedge and slice arrow. The source system’s v=u holds only at the two intersections; future variants must state the actual boundary relation.

## Capability scope

All easy, moderate and hard bands are supported by the eight existing, revalidated normal families. Easy and moderate remain authored curriculum assignments with reasons and bounds in classification.md. This replenishment does not implement samplers for the three newly captured templates: their source banks and representations are retained exactly below, with unresolved recipes explicitly unclaimed. This is a template capability exception, not a filled template or an unsupported difficulty. These omissions do not prevent the five-question reserve in any band. The supplied .generated file was absent.

Historical raw profiles replay 8/8 complete banks and 40/40 values with original omissions at basis 1356; that result is not claimed as replay of the newly captured banks or the current 10-field snapshot. Normal method banks remain explicitly authored extensions, with a complete profile selected before sampling. No source record or learner record is changed.

Inventory conservatively excludes source questions with known teaching/geometry defects and the unrated incomplete question. Four current sources (q-160885, q-83943, q-160710, q-38132) have independently checked displayed maps, transformed boundaries, positive region widths, exact integrals, canonical answers, distinct five-value banks and existing hashed assets. Their source diagrams were visually inspected. Native learner grading and shown/reserved exclusion are rerun at the locked preparation basis.

## Current complete banks

### q-38374

Using the change of variables

$u = x - y, v = y$,
calculate the area of the finite region $D$ bounded by the curve $(x - y)^{2} - y = 0$ and the line $y = 1$.

Field 3868bc82-87b4-5f23-bdbc-a27b10c54df7; selection/radio.

- `\frac{2}{3}`; key absent; source answer 9315f9a2-e02a-52a0-9b61-22998fdd4b41.

- `1`; key absent; source answer a2493839-f867-5e6b-86ab-21e93542af83.

- `2`; key absent; source answer aaf23205-9937-580f-9487-67df5e047e7e.

- `\frac{4}{3}`; key absent; source answer fbba71af-ed9d-5b0d-9f28-8c1f36bd3fcd.

- `\sqrt{2}`; key absent; source answer 176c442b-d740-5c8e-bae2-04e05f97f2e3.

### q-82874

Using the change of variables 

$$
u=x+y,\,v=x-y,
$$

calculate the area of the finite region $D$ bounded by the curve $(x+y)^{4}-x+y=0$ and  the line $y=0.$

Field a50d9972-aaca-5f8a-98d1-1ba9d85277f9; selection/radio.

- `\frac{1}{10}`; incorrect; source answer fcf7e1f1-fcf9-543c-97ee-b919265bfc35.

- `\frac{3}{20}`; correct; source answer c5bf893e-8435-5b7e-b5c4-19722cff781d.

- `\frac{2}{3}`; incorrect; source answer 4deced36-0d95-50f5-af94-23b1383c8b33.

- `\frac{1}{2}`; incorrect; source answer 3395c3cb-8544-536c-a34a-982908787158.

- `\frac{1}{3}`; incorrect; source answer 55a5789a-60d9-53af-abe8-31a45948a5e0.

### q-160885

Using the change of variables 

$$
u=y+2x,\,v=y-2x,
$$

calculate the area of the finite region $D$ bounded by the lines $y+2x=1,$ $y-2x=1$ and the curve ${y}^{2}-4{x}^{2}=4.$

Field 579f73d3-5ee3-5e3b-9cb0-45b6635a75cb; selection/radio.

- `\operatorname{ln}⁡4-\frac{3}{2}`; incorrect; source answer 33a307a4-5e3d-5e26-9870-e4654bb643c2.

- `\operatorname{ln}⁡4-\frac{3}{4}`; correct; source answer 9175a99b-56d0-595b-86db-511244542711.

- `2\operatorname{ln}⁡4-3`; incorrect; source answer 6ae05fa3-0d0d-5167-94c2-8ea479a334e8.

- `4\operatorname{ln}⁡4-\frac{3}{4}`; incorrect; source answer 222f9a03-a010-5d70-a31b-68c15b8ab921.

- `2\operatorname{ln}⁡4-\frac{3}{2}`; incorrect; source answer 86cdb592-c0ee-5680-989f-fa4c9b6fb697.

### q-82878

Using the change of variables 

$$
u=x-y,\,v=y+1,
$$

calculate the area of the finite region $D$ bounded by the curve $(x-y)^{2}+y=2$ and the line $y=0.$

Field 4e5a6329-2104-5c1b-84f2-ccc6d5d0b453; selection/radio.

- `\frac{2}{3}`; incorrect; source answer 9e834b2d-26ec-5a0b-b024-653762ca7f8f.

- `\frac{8\sqrt{2}}{3}`; correct; source answer 8232f0ab-a3f1-5a06-a6cb-8418ed7a1099.

- `\frac{8}{3}`; incorrect; source answer 36c18b51-d2d9-5561-b308-2fdc610bb877.

- `\frac{2\sqrt{2}}{3}`; incorrect; source answer 88c8bbb9-1718-53bf-8d76-f55389c1603f.

- `\frac{\sqrt{2}}{3}`; incorrect; source answer 29ff210b-32a3-59a3-9402-2b61a8d6a02a.

### q-83943

Using the change of variables 

$$
u=x-2y,\,v=y,
$$

calculate the area of the finite region $D$ bounded by the curve $y-(x-2y)^{2}=2$ and the line $y=3.$

Field d0492151-0ea1-564c-95ed-c1870ce912b6; selection/radio.

- `\frac{2}{3}`; incorrect; source answer 3e39adcf-f9fe-5dd8-8121-889b47f3e44f.

- `10`; incorrect; source answer eddeac90-01c0-5833-a667-85aceff8ed1b.

- `2`; incorrect; source answer 50017198-4384-5924-9339-b114ae17f28f.

- `\frac{4}{3}`; correct; source answer 2b3d1083-137d-51cd-af77-24049d080386.

- `\frac{1}{3}`; incorrect; source answer 19278225-d301-581a-a354-aa480305af42.

### q-83947

Using the change of variables 

$$
u=y+3x,\,v=x,
$$

calculate the area of the finite region $D$ bounded by the curve $(y+3x)^{2}-x=3$ and the line $x=1.$

Field b3452f16-065c-5d3f-b342-bf97b568f3a2; selection/radio.

- `-\frac{32}{3}`; incorrect; source answer b76d7d05-c899-566f-a267-b260f4f22494.

- `\frac{16}{3}`; incorrect; source answer e610ef2b-0037-56d0-bead-5ff13607271a.

- `\frac{32}{3}`; correct; source answer 0ed3876d-8c80-5bc3-9185-9669f13f9f35.

- `-\frac{16}{3}`; incorrect; source answer 639ae9f3-3123-5bb0-aa7c-f883873eebe0.

- `\frac{47}{3}`; incorrect; source answer 8823d84a-4e7a-5110-b70c-63b3e1900363.

### q-160710

Using the change of variables 

$$
u=x-y,\,v=x+y,
$$

calculate the area of the finite region $D$ bounded by the lines $x+y=1,$ $x-y=1$ and the curve ${x}^{2}-{y}^{2}=2.$

Field 4e959dbb-ec9c-5316-8bef-b8459b6fb499; selection/radio.

- `\operatorname{ln}⁡2-1`; incorrect; source answer 5ea71a81-55b2-5821-a85d-2c2b860ef761.

- `\operatorname{ln}⁡2-\frac{1}{2}`; correct; source answer 68da978e-5392-5c13-80d0-e709f72c6da6.

- `2\operatorname{ln}⁡2-2`; incorrect; source answer 6e0953bd-cd3e-5daf-9baa-978871a2e773.

- `\operatorname{ln}⁡2-3`; incorrect; source answer 98fb62ce-1156-5b60-96a5-36d7a22956c9.

- `2\operatorname{ln}⁡2-\frac{3}{2}`; incorrect; source answer a31dfc4c-cfac-5c12-8881-aa0d90cb5c66.

### q-38132

Using the change of variables 

$$
u=x+2y,\,v=x,
$$

calculate the area of the finite region $D$ bounded by the curve $(x+2y)^{2}-x-1=0$ and the line $x=1.$

Field 9c1d39b3-e468-5801-801a-6497da6d4261; selection/radio.

- `\frac{4\sqrt{2}}{3}`; correct; source answer 26ffbc26-848e-5d04-abcc-6404b93bc783.

- `\frac{2}{3}`; incorrect; source answer 51513ac6-c10d-5428-81d7-fc0f9ff5e5a4.

- `\frac{1}{6}`; incorrect; source answer 8d66c296-5953-5fbe-8ee0-08a430a0fe71.

- `\frac{\sqrt{2}}{3}`; incorrect; source answer ab6be4c3-4f0a-5a3d-9787-10ec2aa91cac.

- `2\sqrt{2}`; incorrect; source answer df621dfa-555c-59a4-b00c-5eb1cda1d6b9.

### q-83944

Using the change of variables 

$$
u=x-y,\,v=y,
$$

calculate the area of the finite region $D$ bounded by the curve $y+(x-y)^{4}=3$ and the line $y=2.$

Field 462ba4b0-a9c1-5d72-894e-ca9fc93df274; selection/radio.

- `\frac{8}{5}`; correct; source answer 0e9418b6-f97a-56c0-a5f8-cb663c2070de.

- `-\frac{8}{5}`; incorrect; source answer 1e609f4f-6be3-5c74-b9cf-1200ed558b19.

- `-\frac{4}{5}`; incorrect; source answer 234a9c24-6945-5264-98b6-b6c065eb22c7.

- `\frac{2}{5}`; incorrect; source answer 74cdbe9e-bfc8-55b1-addc-c01619e14194.

- `\frac{12}{5}`; incorrect; source answer ba55a64c-3c7e-522a-800b-186dd45e7f5e.

### q-82910

Using the change of variables 

$$
u=x+y,\,v=y,
$$

calculate the area of the finite region $D$ bounded by the curves $(x+y)^{3}-y=0$ and $(x+y)^{2}-y=0.$

Field 06575685-8b6e-5313-b708-d919a2eb705b; selection/radio.

- `\frac{5}{12}`; incorrect; source answer 17418eda-e303-583e-abb8-8163f34cf65c.

- `\frac{1}{12}`; correct; source answer 3b1f2bf6-1e84-5da8-8223-f7a8617abe63.

- `\frac{1}{3}`; incorrect; source answer aaa17f5a-3932-5a85-be4a-9e7f8aca50c3.

- `\frac{1}{6}`; incorrect; source answer af9d5967-0e62-5e9c-80be-bb9563606efe.

- `\frac{1}{4}`; incorrect; source answer e507ffc4-50dc-56ba-8db0-2ce573a2305a.



## Distinctness and identity

Candidate comparison parses both supplied maps and all polynomial boundaries into exact SymPy objects (equations normalized to monic form), including existing source and canonical prompts. It ignores UUID, seed, option order, TeX spacing and solution wording. A changed supplied map or boundary is a mathematical task change; repeating only identity, ordering or rendering cannot enter this pool. The existing generator is unregistered: a deterministic UUID from the existing KP UUID is retained in freeze.json and the exact commit intent. Existing question/field/answer identities are never replaced. CLI sampling now skips repeated mathematical tasks and reports its finite catalog/bounded sampling limit.
