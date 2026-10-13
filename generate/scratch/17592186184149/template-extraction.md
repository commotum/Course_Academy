# Template extraction: four stages

## 1. Source-specific descriptions

Each practice source uses a known positive B, a constant C restricted to the open principal interval, a graph with three π-coordinate labels and a five-choice scalar radio field. B is supplied; the only assessed unknown is C. All statements, field keys, choices, correct designation and fixed worked prose are frozen in source.json.

| Source | Level | Family B | C | Zero | Poles | Bank |
|---|---|---|---|---|---|---|
| q-65570 | moderate | tan 1/2 | $\frac{\pi }{8}$ | $-\frac{\pi }{4}$ | $-\frac{5\pi }{4}$, $\frac{3\pi }{4}$ | $-\frac{\pi }{4}$, $1$, $-\frac{1}{8}$, $\frac{\pi }{4}$, $\frac{\pi }{8}$ |
| q-79194 | moderate | tan 2 | $-\frac{\pi }{3}$ | $\frac{\pi }{6}$ | $-\frac{\pi }{12}$, $\frac{5\pi }{12}$ | $\frac{\pi }{12}$, $-\frac{\pi }{6}$, $\frac{\pi }{6}$, $\frac{\pi }{3}$, $-\frac{\pi }{3}$ |
| q-117888 | moderate | tan 3 | $-\frac{\pi }{7}$ | $\frac{\pi }{21}$ | $-\frac{5\pi }{42}$, $\frac{3\pi }{14}$ | $-\frac{\pi }{14}$, $\frac{\pi }{14}$, $\frac{\pi }{7}$, $-\frac{2\pi }{7}$, $-\frac{\pi }{7}$ |
| q-117890 | moderate | tan 1/4 | $\frac{\pi }{8}$ | $-\frac{\pi }{2}$ | $-\frac{5\pi }{2}$, $\frac{3\pi }{2}$ | $-\frac{\pi }{4}$, $\frac{\pi }{8}$, $-\frac{\pi }{2}$, $\frac{\pi }{4}$, $\frac{\pi }{2}$ |
| q-117891 | moderate | tan 2 | $\frac{\pi }{6}$ | $-\frac{\pi }{12}$ | $-\frac{\pi }{3}$, $\frac{\pi }{6}$ | $\frac{\pi }{12}$, $\frac{\pi }{6}$, $-\frac{\pi }{3}$, $-\frac{\pi }{12}$, $-\frac{\pi }{6}$ |
| q-143670 | moderate | cot 1/3 | $-\frac{\pi }{12}$ | $\frac{7\pi }{4}$ | $\frac{\pi }{4}$, $\frac{13\pi }{4}$ | $-\frac{\pi }{12}$, $-\frac{3\pi }{4}$, $3$, $\frac{\pi }{4}$, $\frac{\pi }{3}$ |
| q-143671 | moderate | cot 2 | $-\frac{\pi }{3}$ | $\frac{5\pi }{12}$ | $\frac{\pi }{6}$, $\frac{2\pi }{3}$ | $\frac{\pi }{6}$, $-\frac{\pi }{12}$, $\frac{\pi }{3}$, $-\frac{\pi }{4}$, $-\frac{\pi }{3}$ |
| q-143672 | moderate | cot 1/2 | $\frac{\pi }{4}$ | $\frac{\pi }{2}$ | $-\frac{\pi }{2}$, $\frac{3\pi }{2}$ | $-\frac{\pi }{8}$, $\frac{\pi }{4}$, $\frac{3\pi }{4}$, $\frac{\pi }{2}$, $-\frac{\pi }{3}$ |
| q-143674 | moderate | cot 3 | $\frac{\pi }{4}$ | $\frac{\pi }{12}$ | $-\frac{\pi }{12}$, $\frac{\pi }{4}$ | $-\frac{\pi }{3}$, $\frac{\pi }{4}$, $-\frac{\pi }{4}$, $-\frac{\pi }{12}$, $\frac{\pi }{6}$ |
| q-143675 | moderate | cot 4 | $-\frac{2\pi }{5}$ | $\frac{9\pi }{40}$ | $\frac{\pi }{10}$, $\frac{7\pi }{20}$ | $\frac{\pi }{10}$, $\frac{\pi }{5}$, $-\frac{\pi }{4}$, $-\frac{\pi }{10}$, $-\frac{2\pi }{5}$ |
| q-143676 | hard | cot 2/5 | $-\frac{\pi }{5}$ | $\frac{7\pi }{4}$ | $\frac{\pi }{2}$, $3\pi$ | $\frac{4\pi }{5}$, $-\frac{2\pi }{5}$, $\frac{\pi }{2}$, $-\frac{\pi }{5}$, $-\frac{\pi }{4}$ |
| q-143677 | hard | cot 2/3 | $\frac{\pi }{6}$ | $\frac{\pi }{2}$ | $-\frac{\pi }{4}$, $\frac{5\pi }{4}$ | $-\frac{\pi }{4}$, $\frac{\pi }{6}$, $-\frac{3\pi }{8}$, $\frac{\pi }{3}$, $\frac{\pi }{8}$ |
| q-65571 | hard | tan 3/5 | $-\frac{\pi }{5}$ | $\frac{\pi }{3}$ | $-\frac{\pi }{2}$, $\frac{7\pi }{6}$ | $\frac{\pi }{10}$, $-\frac{\pi }{5}$, $-\frac{\pi }{7}$, $\frac{\pi }{3}$, $\frac{\pi }{5}$ |
| q-79195 | moderate | tan 3 | $\frac{\pi }{4}$ | $-\frac{\pi }{12}$ | $-\frac{\pi }{4}$, $\frac{\pi }{12}$ | $\frac{\pi }{6}$, $\frac{\pi }{4}$, $\frac{-\pi }{4}$, $\frac{\pi }{3}$, $-\frac{\pi }{6}$ |

## 2. Shared pattern

Factor Bx+C into B(x+C/B); compare the graph with y=tan(Bx) or y=cot(Bx); read horizontal displacement h=z-z0; solve C=-Bh, selecting the stated principal representative. Moderate integer/reciprocal B has one final equality; hard nonunit rational B shows C=(-h)B before collecting. The required answer is a scalar C, not a full equation or an unrestricted displacement.

## 3. Components and complete bank map

The prompt is a graph followed by the original function-and-bound sentence. Each worked solution retains its opening, formal two-row factorization, factor explanation, comparison plot, displacement sentence, equation chain, and optional final interval sentence. recipes.json stores source masks and one component descriptor per complete math slot, including punctuation, baseline spelling, subtraction form and display/inline layout. It is not an answer-selection lookup. Each choice is mapped below to its exact source field and a parameterized scalar pattern. Scalar wrong answers alone do not identify the original error operation; all observed error interpretations are unresolved and all observed profiles remain evidence-only.

### observed:q-65570

Field selection, `50abe121-f986-569c-96f5-0b825aa3ad90`, five-choice radio. Parameterized recipe is source-pattern value × c/c0; it reproduces every scalar value without asserting a learner error. Its use is limited to explicit ineligible evidence replay.

| Choice UUID | Source exact value | Recipe in C | Correct |
|---|---|---|---|
| 35078d74-667f-5d42-9d17-366be03c50b2 | $-\frac{\pi }{4}$ | `(-2) C` | False |
| a68ca484-4871-5d33-a32d-9c7dd67ecbc4 | $1$ | `(8/pi) C` | False |
| d31b1ea6-9889-5698-98e1-878acc489e07 | $-\frac{1}{8}$ | `(-1/pi) C` | False |
| e2dd2f79-e39a-58bc-aee5-01f3ef542729 | $\frac{\pi }{4}$ | `(2) C` | False |
| fc5bd80c-b257-5028-b120-1e6934062109 | $\frac{\pi }{8}$ | `(1) C` | True |
### observed:q-79194

Field selection, `1fc3c1af-059f-504a-97e2-7584a4073b63`, five-choice radio. Parameterized recipe is source-pattern value × c/c0; it reproduces every scalar value without asserting a learner error. Its use is limited to explicit ineligible evidence replay.

| Choice UUID | Source exact value | Recipe in C | Correct |
|---|---|---|---|
| 25efffe0-a97f-5bba-872f-819835e25610 | $\frac{\pi }{12}$ | `(-1/4) C` | False |
| 2d97bafb-5a87-5ba7-b763-927943b3e7cb | $-\frac{\pi }{6}$ | `(1/2) C` | False |
| 51ef6fff-f3d4-57ee-b1a4-d5aada807fc5 | $\frac{\pi }{6}$ | `(-1/2) C` | False |
| b12badcd-f45e-5665-aa07-1cbd839e3523 | $\frac{\pi }{3}$ | `(-1) C` | False |
| ddf326fc-b3ea-5f91-bf0c-6759d86b03a6 | $-\frac{\pi }{3}$ | `(1) C` | True |
### observed:q-117888

Field selection, `0dd471e5-3d02-59ea-ae43-9700669b6052`, five-choice radio. Parameterized recipe is source-pattern value × c/c0; it reproduces every scalar value without asserting a learner error. Its use is limited to explicit ineligible evidence replay.

| Choice UUID | Source exact value | Recipe in C | Correct |
|---|---|---|---|
| 1382a0da-6af2-58cd-a188-1d157bd20cd9 | $-\frac{\pi }{14}$ | `(1/2) C` | False |
| 255f49c4-fc05-50ed-8b6d-c7d105680f5a | $\frac{\pi }{14}$ | `(-1/2) C` | False |
| 70d6cf7f-09b3-54e7-91e5-21216ebc3505 | $\frac{\pi }{7}$ | `(-1) C` | False |
| 8f7c0e22-c4ef-5f16-9e47-d3a2ab3e0908 | $-\frac{2\pi }{7}$ | `(2) C` | False |
| 958902e2-d4fc-583d-abca-b3667fecc3aa | $-\frac{\pi }{7}$ | `(1) C` | True |
### observed:q-117890

Field selection, `5303117c-9cc9-5aa9-a8ac-5b23f63b8352`, five-choice radio. Parameterized recipe is source-pattern value × c/c0; it reproduces every scalar value without asserting a learner error. Its use is limited to explicit ineligible evidence replay.

| Choice UUID | Source exact value | Recipe in C | Correct |
|---|---|---|---|
| 08bb1537-d88e-5b3f-911a-ebda185d71d0 | $-\frac{\pi }{4}$ | `(-2) C` | False |
| 154d1a5b-94de-5332-826d-f7085ae1bbac | $\frac{\pi }{8}$ | `(1) C` | True |
| 6982de92-482e-5773-8de9-08b335a18349 | $-\frac{\pi }{2}$ | `(-4) C` | False |
| 8612ead4-47dc-5874-b6e3-9dfd76a3c1d7 | $\frac{\pi }{4}$ | `(2) C` | False |
| ad9bf3b6-8f0d-5e32-8900-ae60d369c4d7 | $\frac{\pi }{2}$ | `(4) C` | False |
### observed:q-117891

Field selection, `b8963d4e-4e20-5bae-a6bb-d591908baaca`, five-choice radio. Parameterized recipe is source-pattern value × c/c0; it reproduces every scalar value without asserting a learner error. Its use is limited to explicit ineligible evidence replay.

| Choice UUID | Source exact value | Recipe in C | Correct |
|---|---|---|---|
| 3bcb0260-5769-5c20-88aa-a4f01f0ed3e9 | $\frac{\pi }{12}$ | `(1/2) C` | False |
| 605d6a7a-183a-572b-88b6-7f2f4255e6ca | $\frac{\pi }{6}$ | `(1) C` | True |
| 645de680-5d7f-5ab0-a739-68065e200b35 | $-\frac{\pi }{3}$ | `(-2) C` | False |
| 9b5d31a5-d46b-5fe9-a177-ab14a5602ff0 | $-\frac{\pi }{12}$ | `(-1/2) C` | False |
| f1a9237f-441e-59ec-bbfc-da0afdb86299 | $-\frac{\pi }{6}$ | `(-1) C` | False |
### observed:q-143670

Field selection, `b21fc2a6-944a-50a1-a0fa-69bde4da9e7f`, five-choice radio. Parameterized recipe is source-pattern value × c/c0; it reproduces every scalar value without asserting a learner error. Its use is limited to explicit ineligible evidence replay.

| Choice UUID | Source exact value | Recipe in C | Correct |
|---|---|---|---|
| 27dd6c2e-56f6-5224-a92d-a900e47fbf5d | $-\frac{\pi }{12}$ | `(1) C` | True |
| 4d20665a-d072-5d38-bc2e-83cd6ab4dfd7 | $-\frac{3\pi }{4}$ | `(9) C` | False |
| 69b8a942-cc3f-5887-9b9a-88358ec6410d | $3$ | `(-36/pi) C` | False |
| a7e2122f-6484-54b6-b0a8-b983751ab3ed | $\frac{\pi }{4}$ | `(-3) C` | False |
| dc531f8c-0ec3-5820-905b-629562f0fa99 | $\frac{\pi }{3}$ | `(-4) C` | False |
### observed:q-143671

Field selection, `20a1e721-de4b-5fc5-9f28-757e2e6b70a8`, five-choice radio. Parameterized recipe is source-pattern value × c/c0; it reproduces every scalar value without asserting a learner error. Its use is limited to explicit ineligible evidence replay.

| Choice UUID | Source exact value | Recipe in C | Correct |
|---|---|---|---|
| 31a8036f-17ff-55a2-804a-9b2f935b3eb5 | $\frac{\pi }{6}$ | `(-1/2) C` | False |
| 872ba577-0336-51a3-a330-83ebd6f756ab | $-\frac{\pi }{12}$ | `(1/4) C` | False |
| 9b9681ec-7818-50c5-b8e6-16783c330ca1 | $\frac{\pi }{3}$ | `(-1) C` | False |
| c7309cde-90ce-5d0e-b0e2-2d1526e4f905 | $-\frac{\pi }{4}$ | `(3/4) C` | False |
| fd64378f-da19-5467-a8d4-3c79f815b9c8 | $-\frac{\pi }{3}$ | `(1) C` | True |
### observed:q-143672

Field selection, `b42dc950-3ab6-53ee-bb79-c0cd1d57e61e`, five-choice radio. Parameterized recipe is source-pattern value × c/c0; it reproduces every scalar value without asserting a learner error. Its use is limited to explicit ineligible evidence replay.

| Choice UUID | Source exact value | Recipe in C | Correct |
|---|---|---|---|
| 0fb8c6d5-62f2-5f9e-9dff-a6c6cf210773 | $-\frac{\pi }{8}$ | `(-1/2) C` | False |
| 3d8111fb-6012-56e0-a9b6-3275417d9a31 | $\frac{\pi }{4}$ | `(1) C` | True |
| 8340b495-0e27-5ab2-8265-89b8a8f42f44 | $\frac{3\pi }{4}$ | `(3) C` | False |
| ceceedd5-348a-5f86-9a42-9b4e036292b7 | $\frac{\pi }{2}$ | `(2) C` | False |
| ed397ac8-10b1-54c0-9046-d661bdad85ca | $-\frac{\pi }{3}$ | `(-4/3) C` | False |
### observed:q-143674

Field selection, `7b65d7ea-f125-581a-a2df-c1111f4277a8`, five-choice radio. Parameterized recipe is source-pattern value × c/c0; it reproduces every scalar value without asserting a learner error. Its use is limited to explicit ineligible evidence replay.

| Choice UUID | Source exact value | Recipe in C | Correct |
|---|---|---|---|
| 07c6a391-2c92-5813-ba67-4345a362e8af | $-\frac{\pi }{3}$ | `(-4/3) C` | False |
| 4770e5d3-4587-5515-9152-939b65d37b5a | $\frac{\pi }{4}$ | `(1) C` | True |
| 5cbb6915-a1c8-5fc7-a06e-af95c679745f | $-\frac{\pi }{4}$ | `(-1) C` | False |
| 88b96039-922d-5b50-8541-b48f2cbcf322 | $-\frac{\pi }{12}$ | `(-1/3) C` | False |
| 8ab7af29-dc13-5490-8ec4-2b37032e3d65 | $\frac{\pi }{6}$ | `(2/3) C` | False |
### observed:q-143675

Field selection, `3f5fe593-1589-5c40-aac0-bfffbafcf416`, five-choice radio. Parameterized recipe is source-pattern value × c/c0; it reproduces every scalar value without asserting a learner error. Its use is limited to explicit ineligible evidence replay.

| Choice UUID | Source exact value | Recipe in C | Correct |
|---|---|---|---|
| 24bcd966-4d0a-58d0-943e-8cf4e9c4e1ad | $\frac{\pi }{10}$ | `(-1/4) C` | False |
| 6674d189-d413-5051-9da8-54c2f39014d0 | $\frac{\pi }{5}$ | `(-1/2) C` | False |
| a0591c4c-0b63-5e56-a640-94f5dfe3dd67 | $-\frac{\pi }{4}$ | `(5/8) C` | False |
| cb64e6cc-c9ba-5473-982d-43077a936e0d | $-\frac{\pi }{10}$ | `(1/4) C` | False |
| d7774e07-5f8a-5b18-ad81-f5efc8beffbc | $-\frac{2\pi }{5}$ | `(1) C` | True |
### observed:q-143676

Field selection, `0189c09e-e677-5254-a0fb-54a417d40114`, five-choice radio. Parameterized recipe is source-pattern value × c/c0; it reproduces every scalar value without asserting a learner error. Its use is limited to explicit ineligible evidence replay.

| Choice UUID | Source exact value | Recipe in C | Correct |
|---|---|---|---|
| 03bc168c-f11d-51c2-bcec-43e2f2c594d8 | $\frac{4\pi }{5}$ | `(-4) C` | False |
| 1d2a9ebc-fa26-5fa6-bfe6-f8b5ba052e2f | $-\frac{2\pi }{5}$ | `(2) C` | False |
| 24d9abd2-8f95-581f-a159-19f44168c652 | $\frac{\pi }{2}$ | `(-5/2) C` | False |
| af303134-44b2-56cd-975a-36c2a314c7d1 | $-\frac{\pi }{5}$ | `(1) C` | True |
| d30c5ce1-6aae-525e-9853-2bf0d012d50c | $-\frac{\pi }{4}$ | `(5/4) C` | False |
### observed:q-143677

Field selection, `20a99701-dbbe-534f-a0ce-166bf09e58cf`, five-choice radio. Parameterized recipe is source-pattern value × c/c0; it reproduces every scalar value without asserting a learner error. Its use is limited to explicit ineligible evidence replay.

| Choice UUID | Source exact value | Recipe in C | Correct |
|---|---|---|---|
| 38f5df54-de20-581a-a052-687662bac099 | $-\frac{\pi }{4}$ | `(-3/2) C` | False |
| 59ea7cd8-2c89-5af6-9951-0c58c07e0a6f | $\frac{\pi }{6}$ | `(1) C` | True |
| 98bf869f-24f8-50f3-ac5e-4060bb11e000 | $-\frac{3\pi }{8}$ | `(-9/4) C` | False |
| b3d9faeb-5941-52e8-928f-04d747d92a64 | $\frac{\pi }{3}$ | `(2) C` | False |
| c58db38f-c8f1-5754-b80e-2298972c7447 | $\frac{\pi }{8}$ | `(3/4) C` | False |
### observed:q-65571

Field selection, `10496ff6-7779-5051-aba6-5bba4e7b9c2c`, five-choice radio. Parameterized recipe is source-pattern value × c/c0; it reproduces every scalar value without asserting a learner error. Its use is limited to explicit ineligible evidence replay.

| Choice UUID | Source exact value | Recipe in C | Correct |
|---|---|---|---|
| 21e5506f-4577-5036-ada5-dc6f9bc99169 | $\frac{\pi }{10}$ | `(-1/2) C` | False |
| 366585d6-d0fc-50e1-b496-79591f6c5405 | $-\frac{\pi }{5}$ | `(1) C` | True |
| 75f6de9c-83fb-55b9-9419-ef8f92a5ae22 | $-\frac{\pi }{7}$ | `(5/7) C` | False |
| e198d2ca-23db-5649-85de-6116093fd7d5 | $\frac{\pi }{3}$ | `(-5/3) C` | False |
| ee45bb2e-4cfb-5586-96b6-963f79e9e559 | $\frac{\pi }{5}$ | `(-1) C` | False |
### observed:q-79195

Field selection, `8571455f-3add-56cd-b95f-65d5a2eb936b`, five-choice radio. Parameterized recipe is source-pattern value × c/c0; it reproduces every scalar value without asserting a learner error. Its use is limited to explicit ineligible evidence replay.

| Choice UUID | Source exact value | Recipe in C | Correct |
|---|---|---|---|
| 2452d0e1-4362-5796-a78d-dd02a6585ca8 | $\frac{\pi }{6}$ | `(2/3) C` | False |
| 7cf12949-3c55-5003-9dd7-df558ba34624 | $\frac{\pi }{4}$ | `(1) C` | True |
| b0f87ce7-dd80-5709-99d0-ca3b27881647 | $\frac{-\pi }{4}$ | `(-1) C` | False |
| bbebdb1c-5559-5ac4-b7a7-c46f4dd61296 | $\frac{\pi }{3}$ | `(4/3) C` | False |
| f0deae7a-65de-5629-be07-d8599eee87d1 | $-\frac{\pi }{6}$ | `(-2/3) C` | False |

### Source anomalies and normal repairs

q-117890 displays -π/2 and π/2, representing the same tangent phase. Both are outside the stated strict representative interval. q-143670 displays -3π/4 and π/4, the same cotangent phase. q-143676 displays 4π/5 and -π/5, the same cotangent curve; -π/5 is the unique allowed principal answer. Even when outside-interval options are ineligible responses, duplicate equivalent curve equations reject the whole normal bank. Raw complete profiles retain these values with evidence_only=true and eligible_for_learning=false. Native radio grading distinguishes IDs; it cannot discover these phase aliases. Independent mathematics does so. All fourteen historical profiles are also opaque and therefore ineligible as normal generated learning banks. Normal presentation replaces the opaque complete bank with the authored assessed-method bank; this is labeled bank authoring, never claimed as recovered source error intent.

## 4. Reusable masks, constraints and authored extension

Normal complete bank operations are C (correct), -C (reverse displacement sign), C/B (treat phase as displacement: omit B), C/B² (invert B when converting displacement to phase), and C-sign(C)π/2 (mistake the zero for an asymptote, selecting that erroneous principal phase). All five operations apply together; any equal values or phase aliases modulo π reject the entire instance. No option is replaced from a pool. The geometric zero/asymptote confusion applies to both tan and cot. The solution is fixed, with no learner-facing distractor diagnosis.

Sampling/explicit bounds: easy B∈{2,3,1/2,1/3}; moderate integer B∈[2,5] or reciprocal 1/n for n∈[2,5]; hard reduced rational B with numerator 2…5 and denominator 2…7, both nonunit, B<2. B=1 and hidden unit reductions are excluded. C/π is a nonzero reduced signed fraction n/d with d∈{5,7,8,9,10,11,12}, 0<|n/d|<1/2. These familiar exact π-fractions extend the observed ±1/7, ±1/12, ±2/5, ±1/8 forms without another branch or arbitrary algebra. Source raw profiles preserve all originals separately, even where outside normal sampling bounds.

Easy is explicitly authored because no easy source exists: supply the displacement and overlay; arithmetic remains this same C=-Bh operation. Moderate reads signed zero coordinates from integer/reciprocal-scale graphs; cot zeros require comparing with π/(2B). Hard keeps the nonunit rational multiplier and a separate multiplication stage. Difficulty is assessed-information/workload, not a sequence within the level. Both families are unordered normal variations; the sampler selects the family before parameters and rejects whole invalid banks. Meaningful task counts enumerate family, reduced B, reduced principal C, and assessed-information level; choice order, profile, seed, function-name aliases and incidental layouts do not count. Content identity hashes version, difficulty, actual prompt, fixed solution and complete bank; mathematical identity excludes complete banks/profiles.

