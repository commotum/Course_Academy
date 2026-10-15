# Classification and extraction refresh

Database `math`, basis 2740, lineage `01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1`. Current exact source evidence is in `reference/initial/kp.edn`; historical basis-1356 evidence remains in `source.json`. All 12 current practice questions were inspected. Canonical examples do not contribute to practice inventory.

Seven original mathematical families now use three checkbox fields (I, II, III), each with the complete `{false,true}` bank. Five additional families use one five-choice radio field. All are plot rating **none**. The generator retains its independently replayed historical radio response contract; current radio sources independently support that contract. Existing checkbox fields are preserved. Hard remains an authored workload extension with 11 nonzero derivative contributions; no current source has a hard annotation.

## Current source families

### q-125852 (easy)

Source EID 17592186134092. Parameters shown below are observed anchors; no new sampling domain is inferred for the five new families. Three supplied pairs, the universal positively oriented curve premise, the unit-curl identity criterion, three partial/curl checks and the full selected subset form the backbone.

- I: P = `y`; Q = `-x`; P_y = `1`; Q_x = `-1`; curl = `-2`.
- II: P = `x/2 + cos(y**2)`; Q = `y/2`; P_y = `-2*y*sin(y**2)`; Q_x = `0`; curl = `2*y*sin(y**2)`.
- III: P = `0`; Q = `x`; P_y = `0`; Q_x = `1`; curl = `1`.

- Field `I`, `:answer-field.type/checkbox`: complete bank `["false", "true"]`; correct `false`. Checkbox recipes are the explicit candidate truth value and its negation; radio recipes are the exact listed candidate subsets. No numeric error interpretation is inferred.
- Field `II`, `:answer-field.type/checkbox`: complete bank `["false", "true"]`; correct `false`. Checkbox recipes are the explicit candidate truth value and its negation; radio recipes are the exact listed candidate subsets. No numeric error interpretation is inferred.
- Field `III`, `:answer-field.type/checkbox`: complete bank `["false", "true"]`; correct `true`. Checkbox recipes are the explicit candidate truth value and its negation; radio recipes are the exact listed candidate subsets. No numeric error interpretation is inferred.

### q-125853 (moderate)

Source EID 17592186134093. Parameters shown below are observed anchors; no new sampling domain is inferred for the five new families. Three supplied pairs, the universal positively oriented curve premise, the unit-curl identity criterion, three partial/curl checks and the full selected subset form the backbone.

- I: P = `-y`; Q = `x**2 + x`; P_y = `-1`; Q_x = `2*x + 1`; curl = `2*x + 2`.
- II: P = `x - y/4`; Q = `3*x/4`; P_y = `-1/4`; Q_x = `3/4`; curl = `1`.
- III: P = `-y`; Q = `0`; P_y = `-1`; Q_x = `0`; curl = `1`.

- Field `I`, `:answer-field.type/checkbox`: complete bank `["false", "true"]`; correct `false`. Checkbox recipes are the explicit candidate truth value and its negation; radio recipes are the exact listed candidate subsets. No numeric error interpretation is inferred.
- Field `II`, `:answer-field.type/checkbox`: complete bank `["false", "true"]`; correct `true`. Checkbox recipes are the explicit candidate truth value and its negation; radio recipes are the exact listed candidate subsets. No numeric error interpretation is inferred.
- Field `III`, `:answer-field.type/checkbox`: complete bank `["false", "true"]`; correct `true`. Checkbox recipes are the explicit candidate truth value and its negation; radio recipes are the exact listed candidate subsets. No numeric error interpretation is inferred.

### q-126560 (easy)

Source EID 17592186369359. Parameters shown below are observed anchors; no new sampling domain is inferred for the five new families. Three supplied pairs, the universal positively oriented curve premise, the unit-curl identity criterion, three partial/curl checks and the full selected subset form the backbone.

- I: P = `-y/2 + exp(x + y)`; Q = `x/2 + exp(x + y)`; P_y = `exp(x + y) - 1/2`; Q_x = `exp(x + y) + 1/2`; curl = `1`.
- II: P = `sin(y)`; Q = `cos(x)`; P_y = `cos(y)`; Q_x = `-sin(x)`; curl = `-sin(x) - cos(y)`.
- III: P = `x`; Q = `x`; P_y = `0`; Q_x = `1`; curl = `1`.

- Field `I`, `:answer-field.type/checkbox`: complete bank `["false", "true"]`; correct `true`. Checkbox recipes are the explicit candidate truth value and its negation; radio recipes are the exact listed candidate subsets. No numeric error interpretation is inferred.
- Field `II`, `:answer-field.type/checkbox`: complete bank `["false", "true"]`; correct `false`. Checkbox recipes are the explicit candidate truth value and its negation; radio recipes are the exact listed candidate subsets. No numeric error interpretation is inferred.
- Field `III`, `:answer-field.type/checkbox`: complete bank `["false", "true"]`; correct `true`. Checkbox recipes are the explicit candidate truth value and its negation; radio recipes are the exact listed candidate subsets. No numeric error interpretation is inferred.

### q-126571 (moderate)

Source EID 17592186369366. Parameters shown below are observed anchors; no new sampling domain is inferred for the five new families. Three supplied pairs, the universal positively oriented curve premise, the unit-curl identity criterion, three partial/curl checks and the full selected subset form the backbone.

- I: P = `0`; Q = `x`; P_y = `0`; Q_x = `1`; curl = `1`.
- II: P = `exp(y)`; Q = `y`; P_y = `exp(y)`; Q_x = `0`; curl = `-exp(y)`.
- III: P = `-y/5 + atan(x)`; Q = `4*x/5`; P_y = `-1/5`; Q_x = `4/5`; curl = `1`.

- Field `I`, `:answer-field.type/checkbox`: complete bank `["false", "true"]`; correct `true`. Checkbox recipes are the explicit candidate truth value and its negation; radio recipes are the exact listed candidate subsets. No numeric error interpretation is inferred.
- Field `II`, `:answer-field.type/checkbox`: complete bank `["false", "true"]`; correct `false`. Checkbox recipes are the explicit candidate truth value and its negation; radio recipes are the exact listed candidate subsets. No numeric error interpretation is inferred.
- Field `III`, `:answer-field.type/checkbox`: complete bank `["false", "true"]`; correct `true`. Checkbox recipes are the explicit candidate truth value and its negation; radio recipes are the exact listed candidate subsets. No numeric error interpretation is inferred.

### q-126577 (moderate)

Source EID 17592186369373. Parameters shown below are observed anchors; no new sampling domain is inferred for the five new families. Three supplied pairs, the universal positively oriented curve premise, the unit-curl identity criterion, three partial/curl checks and the full selected subset form the backbone.

- I: P = `y`; Q = `y`; P_y = `1`; Q_x = `0`; curl = `-1`.
- II: P = `y/7`; Q = `6*x/7`; P_y = `1/7`; Q_x = `6/7`; curl = `5/7`.
- III: P = `exp(x) - exp(-y)`; Q = `x + x*exp(-y)`; P_y = `exp(-y)`; Q_x = `1 + exp(-y)`; curl = `1`.

- Field `I`, `:answer-field.type/checkbox`: complete bank `["false", "true"]`; correct `false`. Checkbox recipes are the explicit candidate truth value and its negation; radio recipes are the exact listed candidate subsets. No numeric error interpretation is inferred.
- Field `II`, `:answer-field.type/checkbox`: complete bank `["false", "true"]`; correct `false`. Checkbox recipes are the explicit candidate truth value and its negation; radio recipes are the exact listed candidate subsets. No numeric error interpretation is inferred.
- Field `III`, `:answer-field.type/checkbox`: complete bank `["false", "true"]`; correct `true`. Checkbox recipes are the explicit candidate truth value and its negation; radio recipes are the exact listed candidate subsets. No numeric error interpretation is inferred.

### q-126574 (moderate)

Source EID 17592186431048. Parameters shown below are observed anchors; no new sampling domain is inferred for the five new families. Three supplied pairs, the universal positively oriented curve premise, the unit-curl identity criterion, three partial/curl checks and the full selected subset form the backbone.

- I: P = `y*exp(x)`; Q = `x - exp(x)`; P_y = `exp(x)`; Q_x = `1 - exp(x)`; curl = `1 - 2*exp(x)`.
- II: P = `2*y`; Q = `x`; P_y = `2`; Q_x = `1`; curl = `-1`.
- III: P = `-y/3 + cos(x**2)`; Q = `2*x/3 + 1`; P_y = `-1/3`; Q_x = `2/3`; curl = `1`.

- Field `I`, `:answer-field.type/checkbox`: complete bank `["false", "true"]`; correct `false`. Checkbox recipes are the explicit candidate truth value and its negation; radio recipes are the exact listed candidate subsets. No numeric error interpretation is inferred.
- Field `II`, `:answer-field.type/checkbox`: complete bank `["false", "true"]`; correct `false`. Checkbox recipes are the explicit candidate truth value and its negation; radio recipes are the exact listed candidate subsets. No numeric error interpretation is inferred.
- Field `III`, `:answer-field.type/checkbox`: complete bank `["false", "true"]`; correct `true`. Checkbox recipes are the explicit candidate truth value and its negation; radio recipes are the exact listed candidate subsets. No numeric error interpretation is inferred.

### q-126575 (moderate)

Source EID 17592186431050. Parameters shown below are observed anchors; no new sampling domain is inferred for the five new families. Three supplied pairs, the universal positively oriented curve premise, the unit-curl identity criterion, three partial/curl checks and the full selected subset form the backbone.

- I: P = `y**3`; Q = `x**3 + 1`; P_y = `3*y**2`; Q_x = `3*x**2`; curl = `3*x**2 - 3*y**2`.
- II: P = `sqrt(2)*x + y/2`; Q = `3*x/2`; P_y = `1/2`; Q_x = `3/2`; curl = `1`.
- III: P = `x`; Q = `x`; P_y = `0`; Q_x = `1`; curl = `1`.

- Field `I`, `:answer-field.type/checkbox`: complete bank `["false", "true"]`; correct `false`. Checkbox recipes are the explicit candidate truth value and its negation; radio recipes are the exact listed candidate subsets. No numeric error interpretation is inferred.
- Field `II`, `:answer-field.type/checkbox`: complete bank `["false", "true"]`; correct `true`. Checkbox recipes are the explicit candidate truth value and its negation; radio recipes are the exact listed candidate subsets. No numeric error interpretation is inferred.
- Field `III`, `:answer-field.type/checkbox`: complete bank `["false", "true"]`; correct `true`. Checkbox recipes are the explicit candidate truth value and its negation; radio recipes are the exact listed candidate subsets. No numeric error interpretation is inferred.

### q-126568 (easy)

Source EID 17592186511504. Parameters shown below are observed anchors; no new sampling domain is inferred for the five new families. Three supplied pairs, the universal positively oriented curve premise, the unit-curl identity criterion, three partial/curl checks and the full selected subset form the backbone.

- I: P = `-y - cos(y)`; Q = `x*sin(y)`; P_y = `sin(y) - 1`; Q_x = `sin(y)`; curl = `1`.
- II: P = `x`; Q = `y`; P_y = `0`; Q_x = `0`; curl = `0`.
- III: P = `-y`; Q = `6*y**2`; P_y = `-1`; Q_x = `0`; curl = `1`.

- Field `selection`, `:answer-field.type/radio`: complete bank `["III only", "II and III only", "I only", "II only", "I and III only"]`; correct `I and III only`. Checkbox recipes are the explicit candidate truth value and its negation; radio recipes are the exact listed candidate subsets. No numeric error interpretation is inferred.

This newly observed source family is conservatively excluded from generator sampling. Its printed parameter values are not a validated sampling domain. Its full bank, solution stages and actual grader behavior were inspected.

### q-126572 (moderate)

Source EID 17592186560984. Parameters shown below are observed anchors; no new sampling domain is inferred for the five new families. Three supplied pairs, the universal positively oriented curve premise, the unit-curl identity criterion, three partial/curl checks and the full selected subset form the backbone.

- I: P = `-y + exp(y)`; Q = `x*exp(y)`; P_y = `exp(y) - 1`; Q_x = `exp(y)`; curl = `1`.
- II: P = `exp(y)`; Q = `0`; P_y = `exp(y)`; Q_x = `0`; curl = `-exp(y)`.
- III: P = `x**7 - y/5`; Q = `6*x/5`; P_y = `-1/5`; Q_x = `6/5`; curl = `7/5`.

- Field `selection`, `:answer-field.type/radio`: complete bank `["I only", "III only", "II only", "I and III only", "II and III only"]`; correct `I only`. Checkbox recipes are the explicit candidate truth value and its negation; radio recipes are the exact listed candidate subsets. No numeric error interpretation is inferred.

**Source error:** Candidate II supplies P=e^y, Q=0 but prints P_y=-e^y and curl=e^y. The correct derivative is e^y and curl=-e^y. Neither is identically one, so the selected set {I} remains correct. The two corrected expressions were checked in memory; the original is preserved and excluded from validated inventory and generator sampling.

This newly observed source family is conservatively excluded from generator sampling. Its printed parameter values are not a validated sampling domain. Its full bank, solution stages and actual grader behavior were inspected.

### q-126570 (easy)

Source EID 17592186561018. Parameters shown below are observed anchors; no new sampling domain is inferred for the five new families. Three supplied pairs, the universal positively oriented curve premise, the unit-curl identity criterion, three partial/curl checks and the full selected subset form the backbone.

- I: P = `-y/3`; Q = `x/3`; P_y = `-1/3`; Q_x = `1/3`; curl = `2/3`.
- II: P = `y*sin(x)`; Q = `x - cos(x)`; P_y = `sin(x)`; Q_x = `sin(x) + 1`; curl = `1`.
- III: P = `y**2`; Q = `x**2`; P_y = `2*y`; Q_x = `2*x`; curl = `2*x - 2*y`.

- Field `selection`, `:answer-field.type/radio`: complete bank `["I only", "II only", "III only", "I, II, and III", "II and III only"]`; correct `II only`. Checkbox recipes are the explicit candidate truth value and its negation; radio recipes are the exact listed candidate subsets. No numeric error interpretation is inferred.

This newly observed source family is conservatively excluded from generator sampling. Its printed parameter values are not a validated sampling domain. Its full bank, solution stages and actual grader behavior were inspected.

### q-126561 (easy)

Source EID 17592186561062. Parameters shown below are observed anchors; no new sampling domain is inferred for the five new families. Three supplied pairs, the universal positively oriented curve premise, the unit-curl identity criterion, three partial/curl checks and the full selected subset form the backbone.

- I: P = `exp(y)`; Q = `exp(x)`; P_y = `exp(y)`; Q_x = `exp(x)`; curl = `exp(x) - exp(y)`.
- II: P = `atan(y)`; Q = `y`; P_y = `1/(y**2 + 1)`; Q_x = `0`; curl = `-1/(y**2 + 1)`.
- III: P = `-y`; Q = `y`; P_y = `-1`; Q_x = `0`; curl = `1`.

- Field `selection`, `:answer-field.type/radio`: complete bank `["I and II only", "II only", "I and III only", "III only", "I only"]`; correct `III only`. Checkbox recipes are the explicit candidate truth value and its negation; radio recipes are the exact listed candidate subsets. No numeric error interpretation is inferred.

This newly observed source family is conservatively excluded from generator sampling. Its printed parameter values are not a validated sampling domain. Its full bank, solution stages and actual grader behavior were inspected.

### q-126559 (easy)

Source EID 17592186561063. Parameters shown below are observed anchors; no new sampling domain is inferred for the five new families. Three supplied pairs, the universal positively oriented curve premise, the unit-curl identity criterion, three partial/curl checks and the full selected subset form the backbone.

- I: P = `y`; Q = `x`; P_y = `1`; Q_x = `1`; curl = `0`.
- II: P = `-y`; Q = `0`; P_y = `-1`; Q_x = `0`; curl = `1`.
- III: P = `y + exp(x)`; Q = `y/3`; P_y = `1`; Q_x = `0`; curl = `-1`.

- Field `selection`, `:answer-field.type/radio`: complete bank `["II and III only", "I only", "I and III only", "II only", "III only"]`; correct `II only`. Checkbox recipes are the explicit candidate truth value and its negation; radio recipes are the exact listed candidate subsets. No numeric error interpretation is inferred.

This newly observed source family is conservatively excluded from generator sampling. Its printed parameter values are not a validated sampling domain. Its full bank, solution stages and actual grader behavior were inspected.

## Reused generator and distinctness

The historical templates, parameter constraints, operation banks, original replay evidence, and authored hard family remain described by `template-extraction.md` and `validation.json`. `capabilities.json` records supported levels and finite task counts. The current source refresh does not invent new operations or expand sampling based solely on new anchors.

Replenishment parses every displayed component independently, differentiates it, validates each partial/curl stage and the complete selected subset, and runs every answer choice through the actual application grader. The candidate identity used for deduplication excludes level, response format, seed, UUID, option order, candidate permutations, held-only terms, and shared matching gradient contributions. Source/canonical tasks are excluded even when previously served. No assets are required.

Every submission uses the application contributor and installed native ensure predicates. Under api.lock it rechecks the live basis, current source evidence, history/reservations, distinct available inventory, generator UUID/path and content identities. Exact requests, previews, immutable-lineage receipts and exact-db-after readback remain under `reference/replenishment/`.
