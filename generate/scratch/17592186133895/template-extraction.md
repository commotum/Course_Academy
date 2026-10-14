# Four-stage template extraction

## Stage 1 — specific source descriptions

Each source uses the same simple/piecewise-smooth/closed/positive curve premise and a circulation equal to area for **any** such curve in R². Easy prints P,Q pairs and moderate prints F vectors. All sources have three candidates, five text choices and an explanatory Green's theorem opening, area/circulation equality chain, three held partial derivative checks, three collected curls and one concluding response-set sentence. Bullet versus Roman-number list, missing/retained thin space in the area identity, per-pair wording and mathematical spellings are fixed separately for each source.

### q-125852 (easy)

Observed parameters: `{"a": 1, "n": 2}`.

- I: P = $y$, Q = $- x$; held P_y = $1$, held Q_x = $-1$; curl = $-2$.
- II: P = $\frac{x}{2} + \cos{\left(y^{2} \right)}$, Q = $\frac{y}{2}$; held P_y = $- 2 y \sin{\left(y^{2} \right)}$, held Q_x = $0$; curl = $2 y \sin{\left(y^{2} \right)}$.
- III: P = $0$, Q = $x$; held P_y = $0$, held Q_x = $1$; curl = $1$.

### q-125853 (moderate)

Observed parameters: `{"a": 1, "n": 2, "d": 4}`.

- I: P = $- y$, Q = $x^{2} + x$; held P_y = $-1$, held Q_x = $2 x + 1$; curl = $2 x + 2$.
- II: P = $x - \frac{y}{4}$, Q = $\frac{3 x}{4}$; held P_y = $- \frac{1}{4}$, held Q_x = $\frac{3}{4}$; curl = $1$.
- III: P = $- y$, Q = $0$; held P_y = $-1$, held Q_x = $0$; curl = $1$.

### q-126560 (easy)

Observed parameters: `{"a": 1, "d": 2}`.

- I: P = $- \frac{y}{2} + e^{x + y}$, Q = $\frac{x}{2} + e^{x + y}$; held P_y = $e^{x + y} - \frac{1}{2}$, held Q_x = $e^{x + y} + \frac{1}{2}$; curl = $1$.
- II: P = $\sin{\left(y \right)}$, Q = $\cos{\left(x \right)}$; held P_y = $\cos{\left(y \right)}$, held Q_x = $- \sin{\left(x \right)}$; curl = $- \sin{\left(x \right)} - \cos{\left(y \right)}$.
- III: P = $x$, Q = $x$; held P_y = $0$, held Q_x = $1$; curl = $1$.

### q-126571 (moderate)

Observed parameters: `{"a": 1, "d": 5}`.

- I: P = $0$, Q = $x$; held P_y = $0$, held Q_x = $1$; curl = $1$.
- II: P = $e^{y}$, Q = $y$; held P_y = $e^{y}$, held Q_x = $0$; curl = $- e^{y}$.
- III: P = $- \frac{y}{5} + \operatorname{atan}{\left(x \right)}$, Q = $\frac{4 x}{5}$; held P_y = $- \frac{1}{5}$, held Q_x = $\frac{4}{5}$; curl = $1$.

### q-126577 (moderate)

Observed parameters: `{"a": 1, "d": 7}`.

- I: P = $y$, Q = $y$; held P_y = $1$, held Q_x = $0$; curl = $-1$.
- II: P = $\frac{y}{7}$, Q = $\frac{6 x}{7}$; held P_y = $\frac{1}{7}$, held Q_x = $\frac{6}{7}$; curl = $\frac{5}{7}$.
- III: P = $e^{x} - e^{- y}$, Q = $x + x e^{- y}$; held P_y = $e^{- y}$, held Q_x = $1 + e^{- y}$; curl = $1$.

### q-126574 (moderate)

Observed parameters: `{"a": 1, "d": 3}`.

- I: P = $y e^{x}$, Q = $x - e^{x}$; held P_y = $e^{x}$, held Q_x = $1 - e^{x}$; curl = $1 - 2 e^{x}$.
- II: P = $2 y$, Q = $x$; held P_y = $2$, held Q_x = $1$; curl = $-1$.
- III: P = $- \frac{y}{3} + \cos{\left(x^{2} \right)}$, Q = $\frac{2 x}{3} + 1$; held P_y = $- \frac{1}{3}$, held Q_x = $\frac{2}{3}$; curl = $1$.

### q-126575 (moderate)

Observed parameters: `{"a": 1, "n": 3, "d": 2}`.

- I: P = $y^{3}$, Q = $x^{3} + 1$; held P_y = $3 y^{2}$, held Q_x = $3 x^{2}$; curl = $3 x^{2} - 3 y^{2}$.
- II: P = $\sqrt{2} x + \frac{y}{2}$, Q = $\frac{3 x}{2}$; held P_y = $\frac{1}{2}$, held Q_x = $\frac{3}{2}$; curl = $1$.
- III: P = $x$, Q = $x$; held P_y = $0$, held Q_x = $1$; curl = $1$.

## Stage 2 — shared mathematical pattern

Differentiate each Q with respect to x holding y fixed, and each P with respect to y holding x fixed. Subtract P_y from Q_x, retaining signs; a pair is admissible exactly when that function is identically 1 over the declared domain. Return the complete set. Fields whose curl only happens to equal 1 somewhere remain ineligible.

## Stage 3 — component and complete-bank map

The source strings and extracted complete expression slots are in source.json and extraction-components.json. Each option below is a full finite subset of {I,II,III}; its exact recipe is the indicated subset, independently compared with the derived admissible set. These historical choices contain no numeric distractor whose intent needs guessing. No source distractor diagnosis is added to learner prose.

### q-125852, bank 1, field `5d17d2d8-9928-5246-af09-a8de679c2edf`

- `99862250-7069-52b8-961c-43b2d6c3e458` → `III only`; recipe = subset [2]; designation absent in this legacy bank.
- `f68109da-5447-5289-9116-b22d249e0b40` → `I and II only`; recipe = subset [0, 1]; designation absent in this legacy bank.
- `5b193744-a5b0-5a56-a6c4-959a94a39569` → `II only`; recipe = subset [1]; designation absent in this legacy bank.
- `6b57aff0-91a2-5924-b717-b77009c0d3d6` → `I only`; recipe = subset [0]; designation absent in this legacy bank.
- `7be44107-414a-5573-bb82-9924ad37ebda` → `I and III only`; recipe = subset [0, 2]; designation absent in this legacy bank.

### q-125852, bank 2, field `633e4ab2-3db4-5baf-9514-75709128a17a`

- `4bbde3ea-51a4-5bb9-b415-15b081645f8b` → `I and III only`; recipe = subset [0, 2]; captured incorrect.
- `7503552f-1a3f-5846-a2bb-20c103b29664` → `I only`; recipe = subset [0]; captured incorrect.
- `8bb7ee7a-6e0f-5758-a561-9b3915b9f2e8` → `III only`; recipe = subset [2]; captured correct.
- `17bae066-3d20-59d8-b46d-cf1882d28b09` → `I and II only`; recipe = subset [0, 1]; captured incorrect.
- `902e9dbe-6cff-5089-8658-727ffe921b4a` → `II only`; recipe = subset [1]; captured incorrect.

### q-125853, bank 1, field `097d24ae-bf47-5570-8b59-107607077491`

- `acef05c6-00e1-5592-a1a0-889b8fae112b` → `I only`; recipe = subset [0]; designation absent in this legacy bank.
- `b7bd9e64-696c-51f2-9326-b4dd35e8d309` → `III only`; recipe = subset [2]; designation absent in this legacy bank.
- `033fba2e-49ef-5a43-86ee-97280d5189b6` → `II and III only`; recipe = subset [1, 2]; designation absent in this legacy bank.
- `06170a0b-5016-5c98-abd7-afe22178d627` → `I and II only`; recipe = subset [0, 1]; designation absent in this legacy bank.
- `4abc258a-2852-54fd-89be-f1ca43962d66` → `II only`; recipe = subset [1]; designation absent in this legacy bank.

### q-125853, bank 2, field `07c5c5c2-3396-52cb-9fba-4aead4b7e49a`

- `51032152-ac1c-5645-b519-4d9f91f449cc` → `II and III only`; recipe = subset [1, 2]; captured correct.
- `d548dfcc-afb7-5f57-ad90-cfdfdb29a3ba` → `I only`; recipe = subset [0]; captured incorrect.
- `0cc64ba0-9932-5ec8-a8c1-902a58b2e272` → `III only`; recipe = subset [2]; captured incorrect.
- `8c7ad01a-0f7e-5e8c-8299-0aee289f43aa` → `I and II only`; recipe = subset [0, 1]; captured incorrect.
- `9cfcd43c-0ace-5687-91b7-d1a23321bac2` → `II only`; recipe = subset [1]; captured incorrect.

### q-126560, bank 1, field `5a1e341d-7570-5f89-bb15-0d2fc13ee8fe`

- `1815869f-1306-5a7a-8a79-31aa7c3aed98` → `I, II, and III`; recipe = subset [0, 1, 2]; captured incorrect.
- `58993782-e81d-561a-8c2f-a709856b5298` → `I and III only`; recipe = subset [0, 2]; captured correct.
- `6c9bdb63-1c2c-5b12-a095-b34893ce6ab0` → `I only`; recipe = subset [0]; captured incorrect.
- `9cdced70-20f6-5c17-a5c6-34b0325d1ebf` → `I and II only`; recipe = subset [0, 1]; captured incorrect.
- `e393d19c-d776-50ae-81aa-fc2b967ef5f5` → `II only`; recipe = subset [1]; captured incorrect.

### q-126571, bank 1, field `9dea12d4-5756-5452-8729-3752e57f331e`

- `0df9c250-7ee0-5ece-be23-b462fd5a422f` → `II and III only`; recipe = subset [1, 2]; captured incorrect.
- `06a0083a-8cd7-5f98-9890-958e33d75b4d` → `I and III only`; recipe = subset [0, 2]; captured correct.
- `b520c185-893f-5860-8fa0-f1bb18583ae8` → `I only`; recipe = subset [0]; captured incorrect.
- `b812902c-4800-53c3-8754-8db8226bf6aa` → `I and II only`; recipe = subset [0, 1]; captured incorrect.
- `b3254e94-deb8-5a0b-aec5-298a58eed547` → `II only`; recipe = subset [1]; captured incorrect.

### q-126577, bank 1, field `e30dc9f1-8788-5cd6-85f2-29a70154514e`

- `1682494d-d524-5563-b569-856dbdf7297a` → `II and III only`; recipe = subset [1, 2]; captured incorrect.
- `e3d4788d-f0bc-5750-a40b-058b24c090d4` → `I only`; recipe = subset [0]; captured incorrect.
- `611ef7e9-ee73-5906-a42c-5c6fb21ca78b` → `III only`; recipe = subset [2]; captured correct.
- `77c2f880-1ea2-53a0-b72f-16fd1455fdbf` → `I and II only`; recipe = subset [0, 1]; captured incorrect.
- `e414b1b8-edc6-5c45-a972-64d39ae18795` → `II only`; recipe = subset [1]; captured incorrect.

### q-126574, bank 1, field `d3715f35-6d8a-57c2-a089-fd1bb9bddf47`

- `1f503e12-e11c-54c7-8ba7-5830ef6f73bd` → `I and II only`; recipe = subset [0, 1]; captured incorrect.
- `20a55ace-f5e1-5a5a-91ce-2c0b7d1404a1` → `I only`; recipe = subset [0]; captured incorrect.
- `4798dafc-c73d-5ec4-b12f-da6f6620e4dd` → `III only`; recipe = subset [2]; captured correct.
- `8a583e9f-a399-590a-ac83-6aef2ccb73c6` → `I, II, and III`; recipe = subset [0, 1, 2]; captured incorrect.
- `fac08602-5de8-5d47-96f6-859f484e607d` → `II only`; recipe = subset [1]; captured incorrect.

### q-126575, bank 1, field `fd054105-4a4d-5e12-a937-81dcca4212b8`

- `0de6da70-c426-566d-b3d0-dce7471f5600` → `II only`; recipe = subset [1]; captured incorrect.
- `576c0bfb-effc-5ce5-827d-af6530c65e4e` → `II and III only`; recipe = subset [1, 2]; captured correct.
- `a5d96a71-7dc4-568f-af4e-fef495f9c448` → `I and II only`; recipe = subset [0, 1]; captured incorrect.
- `cd786957-3ffe-55c0-a40e-e21f738990d5` → `III only`; recipe = subset [2]; captured incorrect.
- `fcb13b39-dc15-5bed-8347-e772308dd574` → `I only`; recipe = subset [0]; captured incorrect.

## Stage 4 — reusable template and constraints

Public API templates are the seven source IDs plus `mixed`. Prompt masks replace only six complete component RHS slots (never incidental x in prose). Solution masks replace every complete held partial and each complete curl RHS. Original spellings are selected by mathematical expression equality, not a whole-source literal return. Changed components use exact SymPy LaTeX. The public raw profile preserves the original three collected curl rows with no added rows; normal solutions retain the same prose and sequence and add grouped subtraction and individually signed distribution before each collection. The final sentence is generated from all three admissibility checks, including hard candidate permutations.

Parameters and workload guards apply to samplers and explicit calls: a ∈ {1,…,5}; d ∈ {2,…,8}; n ∈ {2,3,4}; authored hard b,k ∈ {1,2,3}; order ∈ {0,…,5} denotes a permutation of the three candidates. Sources retain their original parameter sets; unused keys reject. Every hard instance keeps exactly 11 nonzero additive contributions across the six held partials; observed families have at most 7. This distinguishes the authored level without a new method. These small integers/fractions preserve the familiar source number forms. n remains a single power-rule/chain-rule operation, not a progression. Held-only arctan x, cos x², x, √2x and y components remain globally smooth on R² even though their assessed held derivatives vanish. No logarithms or singular trigonometric fields are permitted.

The default source profile reproduces the complete active historical bank; its operation recipes remain valid over every allowed parameter. Each observed subset T is implemented as the complete eligibility-flip operation S symmetric-difference (S_anchor symmetric-difference T), selected as a whole bank before parameters. This derives each response from the actual assessed decisions instead of looking up source strings. The family/profile is chosen before parameters and any missing/duplicate response rejects the whole bank. `method_toggle` is an authored five-member complete bank: correct set S, S symmetric-difference {I}, S symmetric-difference {II}, S symmetric-difference {III}, and complement(S). These represent individual eligibility decision mistakes and complete reversal. The raw profile retains every captured bank together, including the two absent legacy references, and is evidence-only. Normal defaults cover all source families; hard uses the method bank. No first-valid distractor pooling occurs.

Content identity hashes actual difficulty, prompt, fixed solution and complete displayed bank. Original raw anchors preserve source UUIDs; changed raw records receive owned IDs derived from their actual content. Seed/answer order cannot change normal content identity. Mathematical task fingerprints remove held-only components and identical nonconstant terms canceled from both derivatives, sort candidate derivative pairs to exclude Roman-label permutations, and exclude bank aliases. Shared gradient decorations, hard n/b changes that only cancel and answer order are not counted as meaningful variety. Finite enumeration uses only parameters affecting the retained assessed derivatives; the resulting counts appear in validation.json.

No mathematical source error was found in the seven practice prompts, partials, curls or active keys. Raw equality statements with `≠1` mean “not identically one” in this universal-curve context, not “unequal at every point.” For example q-126575's polynomial curl can equal one at individual points but is not eligible.
