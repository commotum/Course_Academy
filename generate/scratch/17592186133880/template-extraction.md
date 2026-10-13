# Template extraction: four stages

## 1. Source-specific description

Every original prompt, ordered full worked solution, complete fields and correct refs are retained in source.json. This table records every observed field and choice operation. Choices are finite **complete subsets of the four statements**, so no hidden numerical error recipe is inferred. I-only omits solenoidal status; IV-only omits zero divergence; II-and-IV and III-and-IV conflate nonzero divergence with solenoidal status; II-and-III is contradictory everywhere. None is the empty subset. The recipe is the exact stated subset, independent of field magnitude or letter.

| Source | Level | Qualitative plot M; drift; domain | Fields | Correct designation |

|---|---|---|---|---|

| q-105075 | moderate | `([[0, 0], [0, -1]], [0, 12], 'quadrant')` | 2 | ['MISSING', 'III only'] |

| q-105571 | easy | `([[0, 0], [0, 0]], [1, 2], 'quadrant')` | 2 | ['MISSING', 'I and IV only'] |

| q-105046 | easy | `([[0, 0], [0, 0]], [1, 0], 'plane')` | 1 | ['I and IV only'] |

| q-105573 | moderate | `([[0, 0], [0, 1]], [0, 0], 'quadrant')` | 1 | ['II only'] |

| q-105575 | moderate | `([[0, -1], [0, 0]], [0, 0], 'plane')` | 1 | ['I and IV only'] |

| q-105576 | easy | `([[0, 0], [0, 0]], [-1, -1], 'plane')` | 1 | ['I and IV only'] |

| q-105578 | moderate | `([[1, 0], [0, 1]], [0, 0], 'quadrant')` | 1 | ['II only'] |

| q-123245 | easy | `([[1, 0], [0, 1]], [0, 0], 'plane')` | 1 | ['II only'] |

| q-131192 | moderate | `([[0, 0], [0, 1]], [1, 0], 'quadrant')` | 1 | ['II only'] |

| q-131193 | easy | `([[0, 0], [0, 0]], [1, -1], 'plane')` | 1 | ['I and IV only'] |

| q-105577 | moderate | `([[0, 0], [-1, 0]], [0, 0], 'quadrant')` | 1 | ['I and IV only'] |

| q-105572 | moderate | `([[-1, 0], [0, -1]], [0, 0], 'quadrant')` | 1 | ['III only'] |

| q-131195 | hard | `([[0, 0], [0, 1]], [1, 0], 'plane')` | 1 | ['II only'] |

| q-131196 | hard | `([[-1, 0], [0, 0]], [0, 1], 'plane')` | 1 | ['III only'] |

## 2. Generalized pattern

Read a smooth vector-field picture: determine whether there is a local excess of outward/inward normal flow, or balance, throughout its domain; choose all corresponding sign statements and the everywhere-zero solenoidal definition. There is no need to calculate partial derivatives, interpret curl, or invoke the divergence theorem. A single fixed solution recalls the three sign rules, defines solenoidal, examines sign statements, examines IV, and gives the complete subset answer.

## 3. Components and complete bank mapping

### q-105075

Prompt notation: div F. Prompt plot: images/34/3411e11060b06a11c82ad677f50731faa31c6bc2e83ccb0d0d10931cf3d76592.png.

Field 1, `39063289-e948-5c53-bc32-a9e7fa1b008c`, radio key `selection`, whole-bank profile `bank-1`:

- `8a764f49-9edb-5020-9a41-bf5dac3e103e`: `I only` ← `subset_value(('I',))`

- `9d6d6769-d8ff-5808-9fdc-2c6a3c27f2ce`: `III only` ← `subset_value(('III',))`

- `e1924edf-bb90-519c-ad15-dc5c4909ac55`: `I and IV only` ← `subset_value(('I', 'IV'))`

- `080a320c-3361-5001-ab96-5c073de14d26`: `III and IV only` ← `subset_value(('III', 'IV'))`

- `1145c273-7eaa-577b-8a14-75a420c86885`: `II only` ← `subset_value(('II',))`

- Original correct designation absent; evidence only, not counted as matched.

Field 2, `2bcce67f-0a6c-5ff1-abd8-5204a040f9e5`, radio key `selection`, whole-bank profile `bank-1`:

- `4af00ead-cb31-51e6-9f21-869070b74a3b`: `I and IV only` ← `subset_value(('I', 'IV'))`

- `5e82f46c-d873-514d-bfa9-fcd50b8798f7`: `I only` ← `subset_value(('I',))`

- `57566773-e704-586b-bc5c-d48eca074e5b`: `III and IV only` ← `subset_value(('III', 'IV'))`

- `b43f392a-de66-542d-85c1-a5e456a297d9`: `III only` ← `subset_value(('III',))` **original CORRECT**

- `a163be0a-2b14-51bd-a9a8-1d4a4207b41d`: `II only` ← `subset_value(('II',))`

Complete source solution reproduced verbatim through masked field/axis components; exact source replay compares the entire string, ordered paragraphs, bullets and plot placement, not just opening phrases.

### q-105571

Prompt notation: div F. Prompt plot: images/86/864ce19530f022e52b7c9513c0cebc64e898f6e71ecf1066ab6aad92d6df40bf.png.

Field 1, `2e9d4ee0-42ea-53df-aa07-9fe9b51468fb`, radio key `selection`, whole-bank profile `bank-2`:

- `869bd612-bbbc-56b2-9d4d-f34bcb0e9062`: `III only` ← `subset_value(('III',))`

- `ef2bd30f-e9a9-5da5-b0ba-7117ab7d4fec`: `I and IV only` ← `subset_value(('I', 'IV'))`

- `1f5a8846-da94-5536-9acc-ee78e8bdaa34`: `I only` ← `subset_value(('I',))`

- `38261aa3-82a9-5fb1-abe8-0ecc0b4a52c4`: `II and IV only` ← `subset_value(('II', 'IV'))`

- `4fddf9c2-de5d-54e2-a6b1-6f255aed1e2d`: `II only` ← `subset_value(('II',))`

- Original correct designation absent; evidence only, not counted as matched.

Field 2, `221ebaf4-de8e-55b9-8386-ea7500ef7627`, radio key `selection`, whole-bank profile `bank-2`:

- `5f861ee0-c10a-55b7-b421-ea16180f7604`: `I and IV only` ← `subset_value(('I', 'IV'))` **original CORRECT**

- `1a3efe9f-6494-50ee-b7d8-97bd8f0b08a4`: `II and IV only` ← `subset_value(('II', 'IV'))`

- `d4611053-0c8f-5196-8404-73c9022f341f`: `I only` ← `subset_value(('I',))`

- `abcf06ba-2db2-5bee-b66a-0d860f76e3ce`: `III only` ← `subset_value(('III',))`

- `44e3ce89-0fb0-5271-8574-d381668934c8`: `II only` ← `subset_value(('II',))`

Complete source solution reproduced verbatim through masked field/axis components; exact source replay compares the entire string, ordered paragraphs, bullets and plot placement, not just opening phrases.

### q-105046

Prompt notation: ∇·F. Prompt plot: images/0b/0bc0e75bb577ca37b89568e14a4e0d03da7ce4f4853c4e8c57d9b2df79897b13.png.

Field 1, `86eda225-7e4d-5e5f-9ce8-78deff9e5db6`, radio key `selection`, whole-bank profile `bank-2`:

- `005c8e0e-15a2-595a-8bf4-9ff48deefe1b`: `II only` ← `subset_value(('II',))`

- `5a77fe81-e649-5e06-8e48-0a04dd7aa841`: `I only` ← `subset_value(('I',))`

- `b9ee5d37-f557-5170-896e-a0186821d84e`: `III only` ← `subset_value(('III',))`

- `ed516192-424f-5a7a-a664-5896e5376a49`: `I and IV only` ← `subset_value(('I', 'IV'))` **original CORRECT**

- `f6e231ae-d734-5b35-81c3-81ff9183634d`: `II and IV only` ← `subset_value(('II', 'IV'))`

Complete source solution reproduced verbatim through masked field/axis components; exact source replay compares the entire string, ordered paragraphs, bullets and plot placement, not just opening phrases.

### q-105573

Prompt notation: div F. Prompt plot: images/30/3088d088689bbd0dfd33abe8240c6f02cceb257937fc1fccb8ba3df151dbfaab.png.

Field 1, `cb9b362c-341e-588a-98f7-56e59732034e`, radio key `selection`, whole-bank profile `bank-2`:

- `07a92cc1-113b-5b68-8eee-53888758e96c`: `I only` ← `subset_value(('I',))`

- `45f98056-476a-56c3-a387-1679af854fe6`: `III only` ← `subset_value(('III',))`

- `e226facb-7893-5854-8a55-7e51661183d1`: `II and IV only` ← `subset_value(('II', 'IV'))`

- `ef23eeaa-e349-5747-9c7d-4d499cf8c5dd`: `II only` ← `subset_value(('II',))` **original CORRECT**

- `fac16b79-d230-552c-b2c9-9227e7ed3b69`: `I and IV only` ← `subset_value(('I', 'IV'))`

Complete source solution reproduced verbatim through masked field/axis components; exact source replay compares the entire string, ordered paragraphs, bullets and plot placement, not just opening phrases.

### q-105575

Prompt notation: ∇·F. Prompt plot: images/11/11d38951b884f17616a61403d793322d0e2ea28910e806fe8f018251508352a1.png.

Field 1, `116238d5-19f2-50cb-9748-dd30cea9d39a`, radio key `selection`, whole-bank profile `bank-2`:

- `627918cc-4b21-5f54-b208-cb86d8a90fcf`: `III only` ← `subset_value(('III',))`

- `9f41d10b-f851-5d45-9827-61f7b022fc29`: `I and IV only` ← `subset_value(('I', 'IV'))` **original CORRECT**

- `d1e51c7e-db29-5f2f-8366-bcfa0cafd1d5`: `II and IV only` ← `subset_value(('II', 'IV'))`

- `dcb49dbb-7200-53b3-81d0-14d6d6fcc22b`: `I only` ← `subset_value(('I',))`

- `e21e0841-2d32-541f-bd4e-00d6bca599f2`: `II only` ← `subset_value(('II',))`

Complete source solution reproduced verbatim through masked field/axis components; exact source replay compares the entire string, ordered paragraphs, bullets and plot placement, not just opening phrases.

### q-105576

Prompt notation: ∇·F. Prompt plot: images/cf/cf932f4f02a216d5111da0748cb04f815a7d2e85af5db2f9282f5aefc359b816.png.

Field 1, `edb4b592-36f2-58e7-bc7b-d02442ac641b`, radio key `selection`, whole-bank profile `bank-3`:

- `36de03da-2578-5f05-876f-f54a0a9294f3`: `II only` ← `subset_value(('II',))`

- `7aaa08fe-4d2a-57c5-86e7-f6781940e81b`: `I and IV only` ← `subset_value(('I', 'IV'))` **original CORRECT**

- `80cdae6e-5c8b-5697-89ab-7480fc566987`: `I only` ← `subset_value(('I',))`

- `9056720e-3c5f-5cf9-a8ee-fb59548a6f75`: `II and IV only` ← `subset_value(('II', 'IV'))`

- `e1b392bc-be27-5e13-8e38-e3b0402b8388`: `IV only` ← `subset_value(('IV',))`

Complete source solution reproduced verbatim through masked field/axis components; exact source replay compares the entire string, ordered paragraphs, bullets and plot placement, not just opening phrases.

### q-105578

Prompt notation: div F. Prompt plot: images/33/33f0353e3856fb2b458d17ed1959918e6a3dd96fd0a966d971575ffc212402f0.png.

Field 1, `2bea141b-d468-560c-9266-a844ba797d87`, radio key `selection`, whole-bank profile `bank-2`:

- `293fea52-e929-5811-afed-af97ddebf14a`: `II only` ← `subset_value(('II',))` **original CORRECT**

- `8cc29659-6ed2-5300-9382-238c0d2c4601`: `II and IV only` ← `subset_value(('II', 'IV'))`

- `9d34961c-bb25-5812-86f9-33a7d799bc19`: `I and IV only` ← `subset_value(('I', 'IV'))`

- `c71effce-e296-5a41-bbf5-5519f9760ea1`: `III only` ← `subset_value(('III',))`

- `f28361df-fd6a-50c5-8758-cfb0d1e00173`: `I only` ← `subset_value(('I',))`

Complete source solution reproduced verbatim through masked field/axis components; exact source replay compares the entire string, ordered paragraphs, bullets and plot placement, not just opening phrases.

### q-123245

Prompt notation: ∇·F. Prompt plot: images/b3/b315be9ba524ab538388fdaad31161c280d7d6e5ab71261345063ac6ffe819d5.png.

Field 1, `fe0c79f3-5071-5ae2-996b-25bb19951a62`, radio key `selection`, whole-bank profile `bank-4`:

- `336f3f9e-6053-5a86-b639-96673bb8f672`: `I and IV only` ← `subset_value(('I', 'IV'))`

- `39162a94-0d90-5b25-b209-24876a170a11`: `II only` ← `subset_value(('II',))` **original CORRECT**

- `5a8b15ca-d52d-531a-9f40-45fe63da8575`: `IV only` ← `subset_value(('IV',))`

- `5c64bab9-76fe-5d95-8daf-e8e1b620127c`: `III only` ← `subset_value(('III',))`

- `a0382c8f-1bdd-5f43-bb7f-8f4cbd016ed4`: `None of the statements are true.` ← `subset_value(())`

Complete source solution reproduced verbatim through masked field/axis components; exact source replay compares the entire string, ordered paragraphs, bullets and plot placement, not just opening phrases.

### q-131192

Prompt notation: div F. Prompt plot: images/e3/e30919dc7cc107bdda9872079b4dc0e59fe8e3e5767aa2d407b9d0af392803e0.png.

Field 1, `ea5cca5b-3f01-52ef-89bb-4b92a787b6ae`, radio key `selection`, whole-bank profile `bank-2`:

- `16ba8325-0de5-55e0-b591-b13e3cdf4ce5`: `III only` ← `subset_value(('III',))`

- `9a082c1d-14e4-53ff-92d2-66ed283dd413`: `I only` ← `subset_value(('I',))`

- `9fad71dc-b40f-5c4c-bb22-8e3334af0c4a`: `II only` ← `subset_value(('II',))` **original CORRECT**

- `c3e9170b-f2b7-5b98-8476-275056448f80`: `I and IV only` ← `subset_value(('I', 'IV'))`

- `c7d0c06d-23f7-52e0-b017-3b762a830f93`: `II and IV only` ← `subset_value(('II', 'IV'))`

Complete source solution reproduced verbatim through masked field/axis components; exact source replay compares the entire string, ordered paragraphs, bullets and plot placement, not just opening phrases.

### q-131193

Prompt notation: div F. Prompt plot: images/24/243496443c3878c90fb67888add6c6ad6d3e69aa20ba24f42ee89d58a2742534.png.

Field 1, `3d7511c4-3f39-553d-b99b-12a596c766ac`, radio key `selection`, whole-bank profile `bank-5`:

- `24e3d2fa-2512-5462-9398-2a405f6d7d67`: `II only` ← `subset_value(('II',))`

- `5a0b785a-0eb8-57a0-825a-938a683bad1e`: `I and IV only` ← `subset_value(('I', 'IV'))` **original CORRECT**

- `8820c9da-a52e-5b7c-8e1b-89811eeef148`: `II and III only` ← `subset_value(('II', 'III'))`

- `8a9b9b35-f09b-5b88-9a8b-3096512d0b87`: `I only` ← `subset_value(('I',))`

- `b8a018d7-e9e5-5ca8-9567-308f5666fcc9`: `IV only` ← `subset_value(('IV',))`

Complete source solution reproduced verbatim through masked field/axis components; exact source replay compares the entire string, ordered paragraphs, bullets and plot placement, not just opening phrases.

### q-105577

Prompt notation: div F. Prompt plot: images/13/13b252e1f9a66836cbd72fbea9bb4c143a71344c923e2215a7718d75c9c42e26.png.

Field 1, `5d9f3218-acdd-54b1-9241-2a69def3fc05`, radio key `selection`, whole-bank profile `bank-6`:

- `8c43dc89-d798-5ee6-a608-13a523da7c67`: `I and IV only` ← `subset_value(('I', 'IV'))` **original CORRECT**

- `a046a076-8d56-592d-9d5e-dee188ac0368`: `II and IV only` ← `subset_value(('II', 'IV'))`

- `555d19b4-befb-5407-abf5-0647b07dd343`: `I only` ← `subset_value(('I',))`

- `19363938-2339-5a8d-9c88-ef7e16322d9b`: `III only` ← `subset_value(('III',))`

- `90dc64e8-45a9-5cb0-a0b9-7a2fc6081166`: `IV only` ← `subset_value(('IV',))`

Complete source solution reproduced verbatim through masked field/axis components; exact source replay compares the entire string, ordered paragraphs, bullets and plot placement, not just opening phrases.

### q-105572

Prompt notation: div F. Prompt plot: images/58/584016c88e5916984e181118d52caab95dba1fd0d861e0fd248a4e023d1b07da.png.

Field 1, `f0ff6b8b-be06-5d38-bc53-8c8fbff6866c`, radio key `selection`, whole-bank profile `bank-1`:

- `03e74b99-ee56-54e9-ae3f-42d5ee7c0a33`: `III only` ← `subset_value(('III',))` **original CORRECT**

- `5070438f-bcf7-51c2-8463-01a5c462b9d7`: `I and IV only` ← `subset_value(('I', 'IV'))`

- `67f8c8f5-44cd-5c0e-a53a-65de21b3fa5a`: `II only` ← `subset_value(('II',))`

- `803f938a-69cc-5cc9-9644-a563d2a7cf5f`: `I only` ← `subset_value(('I',))`

- `c3b2e55e-a370-570d-ba5a-e8f0f307eabf`: `III and IV only` ← `subset_value(('III', 'IV'))`

Complete source solution reproduced verbatim through masked field/axis components; exact source replay compares the entire string, ordered paragraphs, bullets and plot placement, not just opening phrases.

### q-131195

Prompt notation: ∇·F. Prompt plot: images/39/39dfec02c787141d8a728381f4093dfe9cbf3fdbf996177ba6f24d973015dc5f.png.

Field 1, `f8def5ae-54bc-5cde-af27-af1ce38db335`, radio key `selection`, whole-bank profile `bank-2`:

- `51328c89-8cdd-5ec3-96c7-541a1dd6496d`: `I only` ← `subset_value(('I',))`

- `53e20d90-4e62-516b-ae3d-39f75e6f0b26`: `III only` ← `subset_value(('III',))`

- `b1ea2773-828b-51a5-b56b-8c1ce5f3d0df`: `II only` ← `subset_value(('II',))` **original CORRECT**

- `c14c9ebe-eb84-5d9c-8dd2-5d0a1d71c120`: `I and IV only` ← `subset_value(('I', 'IV'))`

- `cd47d87e-fdba-55d2-b443-02e11d1f6d93`: `II and IV only` ← `subset_value(('II', 'IV'))`

Complete source solution reproduced verbatim through masked field/axis components; exact source replay compares the entire string, ordered paragraphs, bullets and plot placement, not just opening phrases.

### q-131196

Prompt notation: ∇·F. Prompt plot: images/4b/4bf8de7e8719545b3d8abf5dc9fb4bc0c5f71034dba7186b7d9822d9e8be044d.png.

Field 1, `7fd542c0-4d3b-584d-9d7b-3c0d0b5750ae`, radio key `selection`, whole-bank profile `bank-7`:

- `18f86bf7-5c17-5cb6-8c9a-25e3a30c5a86`: `III only` ← `subset_value(('III',))` **original CORRECT**

- `26003085-8363-5ee2-8473-69f3ba602654`: `II only` ← `subset_value(('II',))`

- `4452f92a-63c8-5376-8e98-947775e29e69`: `I only` ← `subset_value(('I',))`

- `4bd6eba8-c859-5a8d-b522-f2c3b0ee5a65`: `I and IV only` ← `subset_value(('I', 'IV'))`

- `8aff9788-bb7e-5bb2-9074-85e6460dae3e`: `IV only` ← `subset_value(('IV',))`

Complete source solution reproduced verbatim through masked field/axis components; exact source replay compares the entire string, ordered paragraphs, bullets and plot placement, not just opening phrases.

## 4. Reusable templates and constraints

Raw observed template names are `observed-q-*`, selected with `raw-q-*` profile. All original attribute presence and IDs remain evidence. The engine enum/reference shapes are normalized without changing meaning. Prompt and entire solution are masked only at complete math symbols and plot components; coordinate exchange swaps the complete qualitative graph, math x/y and matching directional prose clauses. `field_symbol` is F/G/H; `swap_axes` is boolean; `scale` is a positive integer 1–3. Raw profile eligibility is false because original bullet labels and legacy missing refs are preserved. This prevents source evidence from silently becoming normal learner output.

Normal `visual-sign` uses seven full five-option banks from stage 3, interpreted as literal response subsets. Choose a whole bank first, then a complete eligible reduced object whose correct subset belongs to it. Reject the entire explicit object or sampled instance if it violates catalog bounds, any choice collides, more than one choice equals the requested truth subset, or the correct answer is absent. No pooled first-valid distractors are used.

Each normal level has independent catalog guards: easy uniform axial/diagonal fields or radial ±identity; moderate exactly one same-coordinate ±1 component with perpendicular unit drift, or one cross-coordinate ±1 shear with perpendicular unit drift, on the positive open square; hard nonzero transverse shear plus same-coordinate ±1 change, or two nonzero cross-coordinate components, with unit drift and signed plane. Quarter-turn orientations are enumerated, reduced duplicate objects removed. Arbitrary matrix parameters are disallowed. Magnitude bounds also apply to explicit parameters.

Finite visual object counts: easy 10, moderate 16, hard 24. Semantic response classes per level: positive, negative, zero. Visual geometry/orientation affects arrow reading; aliases and positive global magnitude do not create new tasks. The fingerprint contains the reduced matrix, reduced drift orientation and domain, excluding family names, bank profile, correct position, field letter and magnitude. Full content identity hashes version, actual prompt including canonical plot asset, exact fixed solution and complete sorted bank.

Source-format repairs are independent from exact fidelity: explicit Roman labels in every normal prompt; one active field for each duplicated source widget; no fabricated designation for either missing legacy ref. Normal prose includes direction or matching normal-component reasoning, avoiding an unsupported inference from vector length alone. Source correct refs agree with normalized qualitative sign patterns; no mathematical repair is asserted.

Plot extraction/specification is in plot-spec.md. All plots are heavy for fidelity; normal plots are generated by private Matplotlib render.py.
