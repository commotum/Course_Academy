# Template extraction

Capture provenance: math / basis 1356 / lineage 01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1. This follows the four extraction stages; raw evidence is retained separately.

## 1. Describe each observed source

| Source | Original forms, variable roles, layout and ordered solution stages |

|---|---|

| q-48707 | Museum occupancy N(t), entries E(t), exits L(t), minutes after opening. Three adjacent bullets and relationship request. Unrated; five radio equations; missing solution/correct designation. Supported solution uses canonical convention prose with museum substitution. |

| q-72004 | Bacteria count N(t), growth r(t), hours. Two spaced bullets. Radio, five equations. Solution: amount description → formal N′=dN/dt=Change N/Change t → growth meaning → equality N′=r in prose. |

| q-112509 | Height H(t), centimeters, growth r(t), years since planting. Two spaced bullets; field absent. Solution has the same four ordered stages as bacteria, with ASCII prime notation. |

| q-48923 | Park occupancy N(t), entry E(t), exit L(t), minutes after opening. Three spaced bullets; field absent. Solution: occupancy description → formal derivative ratio → instantaneous occupancy-change meaning → entry-minus-exit explanation → displayed N′=E−L. |

| q-72109 | Wall brick count B(t), growth r(t), hours. Two spaced bullets; field absent. Same four single-growth stages with ASCII prime notation. |

| q-112518 | Fence panel count P(t), growth r(t), hours. Two spaced bullets; radio. Reciprocal/square/one-minus-rate bank. Same four single-growth stages with Unicode prime notation. |

| q-112519 | Playground child count N(t), entries E(t), exits L(t), hours after opening. Three spaced bullets; radio. Same five net stages; first sentence incorrectly mentions park/minutes and is repaired. |

| q-112522 | Account count N(t), openings O(t), cancellations C(t), days. Three spaced bullets; radio. Five net stages, using open/cancel rates and Unicode prime notation. |

| q-72105 | Plane altitude A(t), growth r(t), minutes after takeoff. Two spaced bullets (second lacks separator dash). Radio sign bank. Four single-growth stages; first sentence hours is corrected to minutes. |

All supplied functions are modeled smooth quantities/rates over nonnegative observation time. Rates are at the same time argument; no numerical formula, time substitution, derivative calculation or unit conversion occurs. Counts/heights/amounts are modeled nonnegative. Entry/removal magnitudes are nonnegative; the bank relationship is a universal model identity, so an accidental equality at one special time does not make a distractor correct.

## 2. Generalized shared pattern

Single growth: the derivative of the accumulated quantity is the supplied positive growth rate. Net flow: the derivative of occupancy/account count is the positive incoming rate minus the positive outgoing rate. The assessed response is a complete functional equation. Five radio options mix derivative versus amount, rate versus rate derivative, and sign/operation errors. Existing source labels overlap in workload; source labels are preserved.

## 3. Components and every source choice

The formal ratio, interpretation sentence and final equation retain the exact source sequence. Complete source fields and their IDs are in source.json. The following tables map every original displayed value to its exact operation; no inferred original authoring code or error intention is claimed. Formulas are defensible parameterized expression patterns and complete banks are selected together.

### q-48707 — museum_net

Parameters: `{"Q": "N", "T": "t", "unit": "minutes", "I": "E", "L": "L"}`. Field origin: observed.

| Source field / correct designation | Exact displayed choice | Parameterized operation |

|---|---|---|

| `9ec4ed13-bf56-57c0-afef-d9dca073a67b` / wrong | $N(t) = E(t) + L(t)$ | `stock_sum` |

| `9ec4ed13-bf56-57c0-afef-d9dca073a67b` / missing designation; mathematically correct | $N^{′}(t) = E(t) - L(t)$ | `correct` |

| `9ec4ed13-bf56-57c0-afef-d9dca073a67b` / wrong | $N^{′}(t) = E(t) \cdot L(t)$ | `product` |

| `9ec4ed13-bf56-57c0-afef-d9dca073a67b` / wrong | $N^{′}(t) = E(t) + L(t)$ | `sum` |

| `9ec4ed13-bf56-57c0-afef-d9dca073a67b` / wrong | $N(t) = E(t) - L(t)$ | `stock_difference` |

Prompt/solution masks: `templates.json` → `q_48707`. Repairs: missing correct designation inferred from inflow minus outflow; missing solution authored from canonical example; unrated assigned moderate.

### q-72004 — single_sign

Parameters: `{"Q": "N", "T": "t", "unit": "hours", "R": "r"}`. Field origin: observed.

| Source field / correct designation | Exact displayed choice | Parameterized operation |

|---|---|---|

| `874c5434-9157-538e-be59-176244d35d61` / wrong | $N(t)=r(t)$ | `stock_rate` |

| `874c5434-9157-538e-be59-176244d35d61` / wrong | $N(t)={r}^{′}(t)$ | `stock_rate_derivative` |

| `874c5434-9157-538e-be59-176244d35d61` / correct observed | ${N}^{′}(t)=r(t)$ | `correct` |

| `874c5434-9157-538e-be59-176244d35d61` / wrong | $N(t)=-{r}^{′}(t)$ | `stock_negative_rate_derivative` |

| `874c5434-9157-538e-be59-176244d35d61` / wrong | ${N}^{′}(t)=-r(t)$ | `negative_derivative_rate` |

Prompt/solution masks: `templates.json` → `q_72004`. Repairs: none before instantaneous-rate clarification.

### q-112509 — single_sign

Parameters: `{"Q": "H", "T": "t", "unit": "years", "R": "r"}`. Field origin: authored supported radio.

| Source field / correct designation | Exact displayed choice | Parameterized operation |

|---|---|---|

No observed field or bank exists. Supported authored peer profile (does not count toward observed-bank coverage):

- `stock_rate`: $H(t)=r(t)$
- `stock_rate_derivative`: $H(t)={r}^{′}(t)$
- `correct`: ${H}^{′}(t)=r(t)$
- `stock_negative_rate_derivative`: $H(t)=-{r}^{′}(t)$
- `negative_derivative_rate`: ${H}^{′}(t)=-r(t)$

Prompt/solution masks: `templates.json` → `q_112509`. Repairs: none before instantaneous-rate clarification.

### q-48923 — net_standard

Parameters: `{"Q": "N", "T": "t", "unit": "minutes", "I": "E", "L": "L"}`. Field origin: authored supported radio.

| Source field / correct designation | Exact displayed choice | Parameterized operation |

|---|---|---|

No observed field or bank exists. Supported authored peer profile (does not count toward observed-bank coverage):

- `sum`: ${N}^{′}(t)=E(t)+L(t)$
- `correct`: ${N}^{′}(t)=E(t)-L(t)$
- `stock_sum`: $N(t)=E(t)+L(t)$
- `stock_difference`: $N(t)=E(t)-L(t)$
- `product`: ${N}^{′}(t)=E(t)\cdot L(t)$

Prompt/solution masks: `templates.json` → `q_48923`. Repairs: none before instantaneous-rate clarification.

### q-72109 — single_sign

Parameters: `{"Q": "B", "T": "t", "unit": "hours", "R": "r"}`. Field origin: authored supported radio.

| Source field / correct designation | Exact displayed choice | Parameterized operation |

|---|---|---|

No observed field or bank exists. Supported authored peer profile (does not count toward observed-bank coverage):

- `stock_rate`: $B(t)=r(t)$
- `stock_rate_derivative`: $B(t)={r}^{′}(t)$
- `correct`: ${B}^{′}(t)=r(t)$
- `stock_negative_rate_derivative`: $B(t)=-{r}^{′}(t)$
- `negative_derivative_rate`: ${B}^{′}(t)=-r(t)$

Prompt/solution masks: `templates.json` → `q_72109`. Repairs: none before instantaneous-rate clarification.

### q-112518 — single_reciprocal

Parameters: `{"Q": "P", "T": "t", "unit": "hours", "R": "r"}`. Field origin: observed.

| Source field / correct designation | Exact displayed choice | Parameterized operation |

|---|---|---|

| `2bc9aea5-67df-59f8-abb7-e8249f8d9def` / wrong | ${P}^{′}(t)=\frac{1}{r(t)}$ | `reciprocal` |

| `2bc9aea5-67df-59f8-abb7-e8249f8d9def` / wrong | $P(t)={r}^{2}(t)$ | `square_rate` |

| `2bc9aea5-67df-59f8-abb7-e8249f8d9def` / correct observed | ${P}^{′}(t)=r(t)$ | `correct` |

| `2bc9aea5-67df-59f8-abb7-e8249f8d9def` / wrong | $P(t)={r}^{′}(t)$ | `stock_rate_derivative` |

| `2bc9aea5-67df-59f8-abb7-e8249f8d9def` / wrong | ${P}^{′}(t)=1-r(t)$ | `one_minus_rate` |

Prompt/solution masks: `templates.json` → `q_112518`. Repairs: none before instantaneous-rate clarification.

### q-112519 — net_standard

Parameters: `{"Q": "N", "T": "t", "unit": "hours", "I": "E", "L": "L"}`. Field origin: observed.

| Source field / correct designation | Exact displayed choice | Parameterized operation |

|---|---|---|

| `23d223b5-bd3f-5c3b-89d6-23c60d550968` / wrong | ${N}^{′}(t)=E(t)+L(t)$ | `sum` |

| `23d223b5-bd3f-5c3b-89d6-23c60d550968` / correct observed | ${N}^{′}(t)=E(t)-L(t)$ | `correct` |

| `23d223b5-bd3f-5c3b-89d6-23c60d550968` / wrong | $N(t)=E(t)+L(t)$ | `stock_sum` |

| `23d223b5-bd3f-5c3b-89d6-23c60d550968` / wrong | $N(t)=E(t)-L(t)$ | `stock_difference` |

| `23d223b5-bd3f-5c3b-89d6-23c60d550968` / wrong | ${N}^{′}(t)=E(t)\cdot L(t)$ | `product` |

Prompt/solution masks: `templates.json` → `q_112519`. Repairs: worked-solution context/time repaired: park/minutes to playground/hours.

### q-112522 — net_accounts

Parameters: `{"Q": "N", "T": "t", "unit": "days", "I": "O", "L": "C"}`. Field origin: observed.

| Source field / correct designation | Exact displayed choice | Parameterized operation |

|---|---|---|

| `5637c519-0dcb-5ebf-8eff-71f832658838` / wrong | $N(t)=-O(t)-C(t)$ | `stock_negative_sum` |

| `5637c519-0dcb-5ebf-8eff-71f832658838` / wrong | $N(t)=O(t)+C(t)$ | `stock_sum` |

| `5637c519-0dcb-5ebf-8eff-71f832658838` / wrong | ${N}^{′}(t)=O(t)+C(t)$ | `sum` |

| `5637c519-0dcb-5ebf-8eff-71f832658838` / correct observed | ${N}^{′}(t)=O(t)-C(t)$ | `correct` |

| `5637c519-0dcb-5ebf-8eff-71f832658838` / wrong | $N(t)=O(t)-C(t)$ | `stock_difference` |

Prompt/solution masks: `templates.json` → `q_112522`. Repairs: none before instantaneous-rate clarification.

### q-72105 — single_sign

Parameters: `{"Q": "A", "T": "t", "unit": "minutes", "R": "r"}`. Field origin: observed.

| Source field / correct designation | Exact displayed choice | Parameterized operation |

|---|---|---|

| `27c52aef-834f-5c1c-9709-b11a313c17d7` / correct observed | ${A}^{′}(t)=r(t)$ | `correct` |

| `27c52aef-834f-5c1c-9709-b11a313c17d7` / wrong | $A(t)=-{r}^{′}(t)$ | `stock_negative_rate_derivative` |

| `27c52aef-834f-5c1c-9709-b11a313c17d7` / wrong | ${A}^{′}(t)=-r(t)$ | `negative_derivative_rate` |

| `27c52aef-834f-5c1c-9709-b11a313c17d7` / wrong | $A(t)={r}^{′}(t)$ | `stock_rate_derivative` |

| `27c52aef-834f-5c1c-9709-b11a313c17d7` / wrong | $A(t)=r(t)$ | `stock_rate` |

Prompt/solution masks: `templates.json` → `q_72105`. Repairs: worked-solution time repaired: hours to minutes.

### Recipe operations

Let Q denote amount, R its positive growth/loss magnitude, I positive inflow, L positive outflow (or signed outflow only in hard). All are evaluated at the displayed independent time. The correct derived relationship is Q′=R, Q′=−R, Q′=I−L or Q′=I+L according to the supplied definitions.

| Recipe | Complete equation |

|---|---|

| `stock_rate` | Q=R |

| `stock_rate_derivative` | Q=R′ |

| `stock_negative_rate_derivative` | Q=−R′ |

| `negative_derivative_rate` | Q′=−R |

| `positive_derivative_rate` | Q′=R |

| `stock_negative_rate` | Q=−R |

| `reciprocal` | Q′=1/R |

| `square_rate` | Q=R² |

| `one_minus_rate` | Q′=1−R |

| `stock_sum` | Q=I+L |

| `stock_difference` | Q=I−L |

| `stock_negative_sum` | Q=−I−L |

| `sum` | Q′=I+L |

| `difference` | Q′=I−L |

| `negative_sum` | Q′=−I−L |

| `product` | Q′=I L |

## 4. Reusable masks, conditions and calculations

Nine source masks have fixed full story sentences, list spacing and complete worked-solution prose. Only complete mathematical function names/derivative bases and the independent-variable components are slotted; prose words and TeX command names are protected. Source time units remain fixed. All masks independently replay original strings through the ordinary generate API. Supported missing-field source templates use exactly the listed complete peer bank, with authored origins.

The shared builder computes the correct derivative relationship first, builds all four wrong transformations from the same supplied-function components and rejects a whole bank when any two full equations are equivalent up to nonzero constant factor or when more than one follows identically from the prompt. It never randomly perturbs an answer or cherry-picks distractors. One fixed solution is independent of selected error.

Source full solution sequence is byte-compared after declared unit repairs, before appending the common instantaneous-limit clarification. Mathematical display blocks are also compared in order; generated changed-name blocks are read back and verified. All equations use the actual prompt names/argument. Identity includes actual prompt, fixed solution and complete bank; task fingerprint contains only the canonical meaningful relationship.

### Authored same-skill peer bounds

Default easy has positive growth or positive loss; default moderate has two positive flow magnitudes; hard adds only the signed-removal wording. The hard relation Q′=I+L prevents double negation. This hard level is an explicit design claim with no observed hard examples. The lesson’s meaning-of-derivative/signed-change narrative and canonical inflow/exit setup support this extension. No numerical rate-function evaluation or additional derivative rule appears. All levels stand alone; easy net source records remain accessible with their observed label.

Authored contexts: water volume (liters/minutes), grain mass (kilograms/hours), fuel volume (liters/seconds), inventory count (items/days). Distinct function names are single letters; time is t/u/s. Explicit inputs enforce the same bounds as sampling. Rates have amount/time units; amount itself is nonnegative on the modeled interval. Physical sign domains are positive single growth/loss or magnitude inflow/outflow, and hard positive inflow/negative removal. No domain-invalid scalar populations, times or option values are sampled.

There are exactly four meaningful response structures, and the mathematical fingerprint intentionally ignores context, physical units, function labels and time letters. All source single-growth items share one task fingerprint; all source positive-flow items share one. We do not claim unlimited mathematical diversity from cosmetic label changes. The four contexts and eligible names/time arguments supply repeated categorical peer practice.

### Repairs and separate fidelity denominators

Nine exact prompt strings; six observed banks, all 30/30 raw-exact mathematical option values; 5/5 existing correct designations. q-48707’s absent designation is a supported repair and cannot count as a matched observed designation. Three absent fields are supported authored fields and cannot count as recovered layouts. The museum solution is canonical-based authorship, not recovered source prose. Existing solution bodies: 6/8 raw-exact, 8/8 equal after the two declared physical-time/context corrections. All generated solutions then append the instantaneous-limit clarification, so full unchanged-solution fidelity is not claimed. Actual source bytes show single backslash TeX commands; there are no answer normalization repairs.

Plot extraction/spec: none. Original MA evidence confirms museum and bacteria radio layouts; it does not recover omitted fieldless questions or correct refs. `original-ma-evidence.json` retains relevant original items and provenance.

No unresolved choice mappings, invalid complete banks or grading findings remain.
