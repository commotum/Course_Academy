# Template extraction

## Stage 1: specific source descriptions

Each row below names the exact original parameter pattern and field. Prompts, UUIDs, every original bank and raw solutions remain in source.json and review.md; none are omitted. A blank always expects only the derivative RHS or scalar slope, because the left side and/or surrounding sentence already appears in the prompt.

| Source | Parameters | Outer / inner | Response / level |
|---|---|---|---|
| q-48730 | `{"a": 5, "b": -1}` | reciprocal; degree 1 | radio derivative RHS; moderate |
| q-48846 | `{"a": 4, "b": -3}` | sqrt; degree 1 | radio derivative RHS; moderate (authored unrated repair) |
| q-107291 | `{"a": -6, "b": 3}` | sqrt; degree 1 | radio derivative RHS; moderate |
| q-107360 | `{"a": -4, "b": 1, "t": -2}` | sqrt; degree 1 | radio scalar slope; easy |
| q-342764 | `{"a": 5, "b": 1}` | reciprocal; degree 1 | blank derivative RHS; moderate |
| q-314194 | `{"a": 2, "b": 7}` | reciprocal; degree 1 | blank derivative RHS; moderate |
| q-342680 | `{"a": 1, "b": -6, "c": 0}` | sqrt; degree 2 | blank derivative RHS; hard |
| q-342683 | `{"a": 3, "b": 6}` | sqrt; degree 1 | blank derivative RHS; hard |
| q-342802 | `{"a": 3, "b": 12, "c": 0, "t": 2}` | reciprocal; degree 2 | blank scalar slope; easy |

## Stage 2: generalized method and purpose

Write u as the radicand, express y as u^(1/2) or u^(−1/2), compute dy/du and du/dx separately, multiply, then substitute u back. Evaluated slope prompts additionally substitute the displayed x value. The hard quadratic blank retains the explicit factor-of-two cancellation stage; the hard linear blank retains the symbolic chain product followed by the numeric inner derivative. Reciprocal blanks retain a product row, a simplified u row and a substituted radicand row. These fixed stages are independent of chosen errors.

## Stage 3: components and complete banks

Fixed prose, paragraph separators, display blocks, final periods, field placement and source-specific punctuation are in templates.json. Variable components are the function, radicand, exponent rewrite, both derivatives, product rows and optional substitution rows. All these mathematical components are calculated. UUIDs below are raw evidence IDs; newly authored record IDs are field-owned UUIDv5 values.

Empirical source banks are explicit-only profiles. They retain an underdetermined expression shape without pretending it is a recovered cognitive error or authoring algorithm. In particular −3/u in q-48730 is a fixed empirical numerator over the varying radicand. The scalar shapes −5/√u(t), 1/√u(t), √u(t)/a and −a/2 in q-107360 reproduce its full bank; their intent is unknown. These parameterized recipes can generate variants through the normal API, but never enter default bank selection.

Observed operation shapes are also hypotheses about intent. `source_spaced` reverses the constant in two options, omits the inner derivative in two options and omits 1/2 in one option. `source_constfirst` uses −1/(2a√u), a/(2b√u), −a/√u and sign(a)/(2√u). The a/(2b√u) option is a parameterized constant-as-divisor shape; the original one example does not establish author intent.

Default radio bank is a separately labeled complete authored bank: correct result, omit du/dx, reverse derivative sign, omit the factor 1/2, and fail to lower the outer exponent. Formally, with e=±1/2, these four wrong operations yield e*u^(e−1), −e*u^(e−1)*u′, 2e*u^(e−1)*u′, e*u^e*u′, evaluated at t if required. Every member is selected together; if any collision or invalid member occurs, the entire instance is rejected. No first-valid distractor pool is used. Blank fragments have no distractor bank.

### Full original choice map

#### q-48730 / reciprocal_radio / source_reciprocal

Original field `14eebaf9-3e88-5f2b-82c3-330efcb42e3a`, key `selection`, type `:answer-field.type/radio`.

- `256d8104-e561-50d4-bb47-c84cda5f979d`: $-\frac{5}{2\sqrt{(5x-1{)}^{3}}}$ → `correct`; original correct; full expression matched.
- `92909c43-4d9f-55c2-9367-b2903d4d10f5`: $-\frac{3}{5x-1}$ → `empirical_minus_three_over_inner`; original incorrect; full expression matched.
- `b84fdb58-69a3-5339-b857-edeff32c5507`: $\frac{1}{2\sqrt{5x-1}}$ → `omit_inner_and_wrong_exponent`; original incorrect; full expression matched.
- `ccdb8149-860b-5213-8db1-d92c7a922a29`: $-\frac{5}{2\sqrt{5x-1}}$ → `keep_square_root_exponent`; original incorrect; full expression matched.
- `e32be03e-6bf9-5893-a620-899e6e49abe1`: $\frac{1}{2\sqrt{(5x-1{)}^{3}}}$ → `omit_inner_and_negative_sign`; original incorrect; full expression matched.

#### q-48846 / sqrt_spaced_radio / source_spaced

Original field `84ab9969-a822-5aa8-beea-30e48f66c60f`, key `selection`, type `:answer-field.type/radio`.

- `9d468059-f4b7-51ec-a214-229418cddeaf`: $\frac{4}{\sqrt{4x - 3}}$ → `omit_half`; original designation absent; full expression matched.
- `ce172954-02de-5948-98e6-063d373c04b1`: $\frac{2}{\sqrt{4x - 3}}$ → `correct`; original designation absent; full expression matched.
- `dd38fa2b-33de-5df5-aa85-ed357c5eb5e6`: $\frac{1}{2\sqrt{4x + 3}}$ → `reverse_constant_and_omit_inner`; original designation absent; full expression matched.
- `fd120f87-d6a9-56e7-ae4f-db302afd2580`: $\frac{2}{\sqrt{4x + 3}}$ → `reverse_constant`; original designation absent; full expression matched.
- `7f7778bb-8979-5802-bf93-4a409e6e58b7`: $\frac{1}{2\sqrt{4x - 3}}$ → `omit_inner`; original designation absent; full expression matched.

#### q-107291 / sqrt_constfirst_radio / source_constfirst

Original field `beb44a20-d166-5fe6-a7bc-aa72ceec3cb9`, key `selection`, type `:answer-field.type/radio`.

- `27cec937-8f89-509c-89d8-cac2418dad31`: $\frac{1}{12\sqrt{3-6x}}$ → `divide_by_inner_magnitude`; original incorrect; full expression matched.
- `48530683-52e3-5b2d-b80c-52c96ea80021`: $-\frac{1}{\sqrt{3-6x}}$ → `use_constant_as_divisor`; original incorrect; full expression matched.
- `6ea096e1-e11d-5b2f-9a38-2f0713ebe775`: $\frac{6}{\sqrt{3-6x}}$ → `omit_half_and_reverse_sign`; original incorrect; full expression matched.
- `afef1e77-e7bb-55d4-85fd-246b46e4f2ed`: $-\frac{3}{\sqrt{3-6x}}$ → `correct`; original correct; full expression matched.
- `eb52bd30-42b5-564a-b65a-5b27e7b61017`: $-\frac{1}{2\sqrt{3-6x}}$ → `omit_inner_magnitude`; original incorrect; full expression matched.

#### q-107360 / slope_sqrt_radio / source_slope

Original field `19320ca1-b053-535e-b992-542e4931ff17`, key `selection`, type `:answer-field.type/radio`.

- `0b523831-f11c-5631-b1d0-55d429e9b570`: $-\frac{5}{3}$ → `empirical_minus_five_over_root`; original incorrect; full expression matched.
- `321ef9b3-dc8b-5b99-b689-dfe8d1c4cf58`: $\frac{1}{3}$ → `empirical_one_over_root`; original incorrect; full expression matched.
- `501d0fb0-7ccb-548e-bb3a-b18b59d46b6f`: $-\frac{2}{3}$ → `correct`; original correct; full expression matched.
- `8cf3df5e-c66f-522b-838e-722473ef4ed3`: $-\frac{3}{4}$ → `empirical_root_over_linear_coefficient`; original incorrect; full expression matched.
- `99c71189-09eb-555b-8519-9b447439afc6`: $2$ → `empirical_negative_half_coefficient`; original incorrect; full expression matched.

#### q-342764 / reciprocal_blank / blank

Original field `cae0bf8f-009f-5cd9-a958-5250470d215a`, key `field-1`, type `:answer-field.type/blank`.

- `ea0b074e-9124-53da-b940-4a0beab23775`: $-\frac{5}{2\sqrt{(5x+1)^{3}}}$ → `correct`; original correct; full expression matched.

#### q-314194 / reciprocal_blank_braced / blank

Original field `69dfefe3-2eb8-5512-ab7d-eb2788925109`, key `field-1`, type `:answer-field.type/blank`.

- `cb26afef-455b-5297-b622-9e232fa102cc`: $-\frac{1}{\sqrt{(2x+7)^{3}}}$ → `correct`; original correct; full expression matched.

#### q-342680 / sqrt_quadratic_blank / blank

Original field `fd768cbb-f716-59e5-acc7-6f058b68d4ef`, key `field-1`, type `:answer-field.type/blank`.

- `c3cdb155-0bd1-58bc-961e-1bfa7707dad6`: $\frac{x-3}{\sqrt{{x}^{2}-6x}}$ → `correct`; original correct; full expression matched.

#### q-342683 / sqrt_linear_blank / blank

Original field `b7c696cc-7f33-5839-8d2a-38d27e70f63c`, key `field-1`, type `:answer-field.type/blank`.

- `8316ace3-a7b2-57fb-a2e0-d20a2908d622`: $\frac{3}{2\sqrt{3x+6}}$ → `correct`; original correct; full expression matched.

#### q-342802 / slope_reciprocal_blank / blank

Original field `4e7bce52-e2d7-50a5-a44d-84c8a8cc1d7d`, key `field-1`, type `:answer-field.type/blank`.

- `22c57943-65ff-5d5d-81f8-1002a59bb417`: $-\frac{1}{18}$ → `correct`; original correct; full expression matched.

## Stage 4: reusable templates and domain/sampling policies

The extracted scaffold is parameterized at mathematical-component boundaries, not by returning a source payload or selecting prewritten answers. `extract.py` freezes the prose and TeX block placement, and `blocks()` independently constructs every mathematical chunk from integer parameters. All eight existing solutions and nine existing prompts replay exactly at their source parameters; full value equivalence handles harmless bank notation differences. There is no seed-specific source branch or answer lookup table.

Explicit parameter dictionaries must have exactly a,b for linear templates; a,b,c for quadratic templates; and t for slope templates. Noninteger inputs, zero leading coefficients, invalid slope domains and colliding complete banks raise errors rather than silently resampling. For learner output the mathematical domain is u(x)>0; it is recorded outside content, not inserted into source prompt text. Positive domains ensure both square-root derivatives and reciprocal radicals exist. Numeric slopes require u(t)>0, a perfect-square radicand and u′(t)≠0, including explicit parameter calls. Quadratic templates require c=0 to preserve the observed two-term structure. Source c=0 remains valid and is the default quadratic structure.

Authored variation policy, not recovered source code:

- Linear derivative templates use signed leading coefficients with magnitude 2–8 and nonzero constants −12…12: 336 initial parameter combinations per layout, before whole-bank rejection. Both constant-first and x-first source styles remain available.
- Quadratic derivative blanks use a=1…5, b∈−12…12 excluding zero, c=0: 120 parameter combinations. This keeps the observed two-term quadratic and the source cancellation workload; no additional algebra branch is introduced.
- Linear square-root slope radios use |a|=2…8, t∈{−3,−2,−1,1,2,3}, and r=2…9, then b=r²−a*t: 672 initial combinations. Perfect-square radicands retain rational slope arithmetic as in the easy original.
- Quadratic reciprocal slope blanks sample the 114 enumerated tuples with a=1…6, |b|=1…24, c=0, |t|=1…4 and matching signs of b,t, restricted to u(t)=r² for integer r=2…12. Positive and negative t are coordinate reflections with the same rational arithmetic and chain-rule workload. The source tuple a=3,b=12,t=2 is included. Every default therefore retains the original perfect-square radicand and rational slope; no radical simplification branch is added. Both easy templates require one application of the chain rule and one evaluation, despite different source algebra.

All three levels are directly observed. No missing-level expansion or new function skill is required. The authored extensions consist of parameter bounds, moderate assignment/solution/designation for q-48846, and operation-derived default radio banks. All original empirical profiles remain retained and explicitly labeled.

Deterministic identity includes generator version, template, parameters, domain, profile, displayed prompt, complete sorted bank, fixed solution and field layout. UUIDv5 answers are owned by their field's question content. Seed and answer order are excluded. A separate parameter fingerprint uses canonical expanded radicand, outer exponent, evaluation point, response kind and positive domain, independent of layout/profile/difficulty, to deduplicate the same mathematical task across profiles and notation. Changing the displayed bank changes content identity.

## Source findings and repairs

q-48846 lacks difficulty, solution and correct ref in EDB. Authoritative captured widget confirms layout and choices but cannot recover the missing designation. Independent differentiation repairs it; validation reports 8/8 existing designation matches and 1 authored designation. It does not claim 9 original designations matched. No source mathematical errors were found. Source empirical distractor intent remains unresolved, explicitly constrained to replay profiles. This is an interpretation limit, not a hidden missing bank.

## Validation and review

`validate.py` parses displayed TeX through an independent recursive grammar, differentiates the displayed polynomial mathematically, and verifies all answer values and every displayed derivative/product/substitution stage. It tests full-bank one-to-one source correspondence, exact prompt/solution scaffolds, all template/default combinations, collisions, invalid explicit inputs, stable UUID/content identity and variation counts. `engine-input.json` sends all reviewed radios through every choice and all blanks through canonical, equivalent, independently unreduced/expanded-cubic-radical, wrong-sign, omitted-half and zero entries. A separate domain-equivalent fractional-power probe is reported as a failed acceptance capability, not counted as a supported equivalent success or wrong-answer rejection. The mathematical equivalence holds on the positive-radicand question domain; the native grader currently lacks that context. `engine-report.json` uses the real native grade_field. `review.md` and `review.json` show every raw original plus source replay, two variants of every original template/bank and two defaults per template. `validation.json` separates fidelity, mathematical correctness, source repairs and native grading.
