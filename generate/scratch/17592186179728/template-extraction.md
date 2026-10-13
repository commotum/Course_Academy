# Template extraction

Captured math basis 1356; source.json preserves every source record, field, choice ID/value, prose and mathematical stage. The nine templates remain distinct. No source row or field is excluded.

## 1. Specific source descriptions

Each observed source has a `selection` radio field with five delimiter-free scalar math answers. All directed endpoints have small integer coordinates. All values are exact. Classification.md gives the nine one-forms, endpoint tuples and actual RHS row counts. Original question/field/choice IDs and complete raw mathematical rows remain in source.json.

- q-124654: signed endpoint interpolation, y dx−x dy; show product substitution, cancel variable terms to a constant, primitive and 4(1−0), final scalar. Seven integration RHS rows.
- q-81096: origin in x but shifted y, x² dx−y dy; square/product substitution, distributed quadratic/linear/constant terms, primitive and unevaluated endpoint powers, final scalar. Seven RHS rows.
- q-124652: two shifted coordinates and negative y′; xy dx+dy; retain the common factor 2 before distributing the xy product, primitive inside factor 2, endpoint sum, one extra precollection row, final scalar. Nine RHS rows.
- q-124658: origin-based interpolation, two different positive slopes; exponential shared in both terms; factor e^(x+y) before substitution, show e^(4t+2t)(4−2), then combine exponent and prefactor, primitive, exponent endpoint inputs 6(1),6(0), evaluation and collection. Eight RHS rows.
- q-124663: both shifted coordinates, equal positive slopes; two squares; keep common factor 2, expand squares separately, collect inside factor 2, refactor to 4, integrate inside that factor, evaluate endpoints and collect. Nine RHS rows. Endpoint +10 is a typo; +1 is the minimal supported repair.
- q-39345: positive shifted endpoints, x dx+y dy; two affine products, collected linear function, primitive, endpoint inputs and final scalar. Seven RHS rows.
- q-81102: shifted y and zero x origin; e^x dx−π sin(πy/2)dy; retain exponential/sinusoidal substitution products, expanded angle, primitive, symbolic endpoint inputs, familiar-angle evaluation, zero trig contributions and collection. Nine RHS rows.
- q-124660: origin to unit endpoint, sin(πy)dx−cos(πx)dy; show unit derivative products, simplify unit factors, primitive, factored endpoint combination, evaluated familiar-angle values and final scalar. Eight RHS rows.
- q-90714: shifted x and zero y origin; x dx−xy dy; show linear and coupled product substitution before distribution, collected quadratic, primitive, unevaluated endpoint powers and final scalar. Seven RHS rows.

None uses a plot, a rounded approximation or multiple fields. Shared prose remains fixed verbatim. Notation includes source `r(t)`, i/j vectors, dx/dy, derivative fractions and aligned equals rows. The generator does not replace these with another solution method.

## 2. Generalized pattern

Given a directed segment A→B and one-form P dx+Q dy, use r(t)=A+t(B−A), 0≤t≤1. Compute x′ and y′, substitute the affine coordinate functions into BOTH complete differential terms, distribute only after showing substitution/products, integrate the function of t and evaluate both endpoints. Select one exact scalar from a complete five-option bank. The worked solution is fixed independently of the chosen error.

## 3. Components and complete bank mapping

Observed scalar distractor intent is underdetermined. Each captured scalar vᵢ is an explicit coefficient in a uniform multiplier replay recipe k·vᵢ, where k multiplies the entire one-form. This is a narrow replay profile with **unresolved error interpretation**, never promoted as a recovered general error model. Original coefficients are evidence, not guessed operation errors. All generated mathematical values are verified against the actual multiplied one-form; original correct designation is compared separately. The appended mapping includes all 45 options, IDs and designations.

### Authored complete method banks

Write A=∫₀¹P(x(t),y(t))x′dt, B=∫₀¹Q(x(t),y(t))y′dt and C=A+B. The usual complete bank is `[C,A,B,A−B,−C]`: correct, omit dy, omit dx, reverse dy sign, reverse traversal. Derive all five from correct intermediates; reject the WHOLE sampled instance on any equivalence. Signed operands are grouped in display masks. Recipes remain author metadata, without invented learner-facing diagnosis.

For q-124658, B=−C would duplicate reverse traversal. Select its complete family bank `[C,A,B,A−B,k e⁶/3]`, with the last option omitting the lower endpoint of its actual primitive. This is a separate complete profile, not a partial replacement pool.

For q-124660, B=0 makes omission recipes ambiguous. Select `[C,−C,2k,2kπ,k/π]`: reverse traversal, omit chain π divisor, multiply rather than divide by π, omit lower primitive endpoint. These follow the displayed primitive and familiar-angle endpoints.

For q-81102, B=0 likewise precludes the usual omission bank. Select `[C,−C,k e²,C/2,k(e−1)]`: reverse traversal, omit lower exponential endpoint, omit dx multiplier, halve exponential argument. All options are checked as complete unequal scalars.

## 4. Reusable masks, constraints and calculations

Observed prompt masks isolate only the final complete integral component and scale it by k as a whole. Endpoint prose/blocks stay fixed. The final aligned block is extracted as one complete LHS plus an ordered list of complete RHS rows; scale each full expression, preserving every original substitution, distribution, antiderivative and endpoint stage. At k=1 masks naturally reproduce original strings, without a branch returning a literal source question. The sole q-124663 correction touches only its endpoint component. Raw erroneous evidence is retained and separately evaluated in raw-source-reconstruction.json; this raw record is ineligible normal mathematics. Full prompt/full solution fidelity is tested byte-for-byte, with 8/9 raw solution and 9/9 repaired solution denominators.

Observed replay constraints: captured fixed path and integer 1≤|k|≤9. These 18 complete-one-form multipliers form a finite replay domain; fixed endpoint geometry never counts as recovered endpoint diversity. Normal defaults use method banks. Broader practice uses endpoint-varied authored templates.

Authored easy templates have six integer inputs x₀,y₀,x₁,y₁,a,b. Moderate uses canonical x²y/xy with shifted coordinates; hard uses x²y/xy². Both require nonzero coordinate slopes and nonzero a,b, with a surviving degree-three pullback. Moderate performs one cubic plus one quadratic coupled substitution; hard performs two cubic coupled substitutions. Both integrate a degree-three polynomial using the same elementary primitive method. This is an authored workload distinction, not an observed MA label or coefficient-size distinction. Explicit inputs obey the same signed magnitude/shift/cancellation guards as samplers. Bounds and curriculum anchors are in classification.md.

Authored masks show symbolic change of variables, grouped unevaluated substitution products, separately distributed differential components, collected polynomial, primitive, unevaluated endpoint inputs, evaluated endpoint values and final collection. SymPy simplifies at collection/evaluation stages only. Five integral RHS rows precede the primitive; three endpoint/scalar rows follow it. Tests read each actual row back and compare both its value and its integrand/primitive structure, with a deliberate distribution-sign mutation to prove detection.

Content identity hashes version plus actual prompt/full fixed solution/sorted complete bank. Seed, shuffle order, profile aliases and unused metadata do not affect UUIDs. Mathematical fingerprints hash actual directed endpoints, canonical complete P/Q and [0,1] traversal limits, excluding bank/profile/level. The validator reconstructs these fingerprints from printed mathematics.

Plot rating none; no image in any practice prompt, bank or solution. No renderer or database preparation is required. Stop after step 7.

## Complete observed source-choice component mapping
### q-124654_observed

Question UUID `bccb8e18-5ece-5d84-8a75-003e818045de`; field UUID `ce8f3449-3ae9-55ef-ba7f-735d655fcb1f`; field key `selection`. Complete five-value bank.

| Answer UUID | Original vᵢ | Uniform multiplier recipe | Source designation |

|---|---|---|---|

| `5cd60488-a0dc-5fbe-ad61-99ef09f53fd8` | $2$ | $k\left(2\right)$ | wrong: intent unresolved |

| `7d18e2c3-2a49-58ba-9262-8615f99ff198` | $\frac{11}{6}$ | $k\left(\frac{11}{6}\right)$ | wrong: intent unresolved |

| `7df658bc-3949-564c-8f0a-ff4d65a8122c` | $\frac{4}{3}$ | $k\left(\frac{4}{3}\right)$ | wrong: intent unresolved |

| `9647de0b-9ead-58ae-98b3-078246de2961` | $4$ | $k\left(4\right)$ | correct |

| `f9d41240-8070-5238-af02-d0421b2f2cb8` | $3$ | $k\left(3\right)$ | wrong: intent unresolved |

### q-81096_observed

Question UUID `5d8fdb2d-e684-54ed-a57b-9028bda74ea1`; field UUID `c7c6a695-a9f0-5e4f-ad87-ac5134afda03`; field key `selection`. Complete five-value bank.

| Answer UUID | Original vᵢ | Uniform multiplier recipe | Source designation |

|---|---|---|---|

| `37eefa34-5c7b-5c18-b8ed-71a775d5e074` | $5$ | $k\left(5\right)$ | correct |

| `3de4c8b4-1db8-5fc8-a86d-71a5c61c7d18` | $10$ | $k\left(10\right)$ | wrong: intent unresolved |

| `ab99d944-7135-5a96-8ebe-a930f4912b68` | $25$ | $k\left(25\right)$ | wrong: intent unresolved |

| `be137474-0788-5e5a-961f-c0c550ca9ef5` | $15$ | $k\left(15\right)$ | wrong: intent unresolved |

| `ec9c8ba2-744b-59f6-8a7e-28308457b79d` | $20$ | $k\left(20\right)$ | wrong: intent unresolved |

### q-124652_observed

Question UUID `c9d024fb-1731-5e0e-8fd1-3a79afb84b21`; field UUID `b256fecd-a217-5f81-b776-bf372703f7c4`; field key `selection`. Complete five-value bank.

| Answer UUID | Original vᵢ | Uniform multiplier recipe | Source designation |

|---|---|---|---|

| `2061316d-1856-583b-a012-175c95e1c965` | $-\frac{3}{2}$ | $k\left(-\frac{3}{2}\right)$ | wrong: intent unresolved |

| `563f3b75-047f-5df7-8de7-9221c43542f0` | $2$ | $k\left(2\right)$ | wrong: intent unresolved |

| `721d5e3a-d79f-55f9-9018-78465894af00` | $-1$ | $k\left(-1\right)$ | wrong: intent unresolved |

| `78eb821b-6c70-554e-972c-afc5237e47d2` | $\frac{3}{4}$ | $k\left(\frac{3}{4}\right)$ | wrong: intent unresolved |

| `a6fda23d-0a63-5c16-8aa0-61bd7f16d537` | $-\frac{8}{3}$ | $k\left(-\frac{8}{3}\right)$ | correct |

### q-124658_observed

Question UUID `d143a12d-610a-5ab9-bde5-0709d25859cb`; field UUID `ac77208e-6c5b-5fce-9439-9602678d59af`; field key `selection`. Complete five-value bank.

| Answer UUID | Original vᵢ | Uniform multiplier recipe | Source designation |

|---|---|---|---|

| `518dc48b-166a-5cab-b682-ceb513ca018f` | $\frac{3{e}^{4}-1}{2}$ | $k\left(\frac{3{e}^{4}-1}{2}\right)$ | wrong: intent unresolved |

| `5514bb7f-2242-59f6-a527-7a456fa434c0` | $\frac{{e}^{4}-2}{3}$ | $k\left(\frac{{e}^{4}-2}{3}\right)$ | wrong: intent unresolved |

| `72ddc658-03d6-5c6d-9682-1d117f5448cb` | $\frac{{e}^{6}-3}{2}$ | $k\left(\frac{{e}^{6}-3}{2}\right)$ | wrong: intent unresolved |

| `d551764d-1496-5882-b891-2f87604939f5` | $\frac{2{e}^{6}-1}{3}$ | $k\left(\frac{2{e}^{6}-1}{3}\right)$ | wrong: intent unresolved |

| `ef05dfcc-4837-55ea-a44c-b1bc4977ee48` | $\frac{{e}^{6}-1}{3}$ | $k\left(\frac{{e}^{6}-1}{3}\right)$ | correct |

### q-124663_observed

Question UUID `06d9e7d7-47d1-54b7-9b9c-2dd2d48786ed`; field UUID `ed846ac5-800c-5ebb-aa61-1cb4d2210b07`; field key `selection`. Complete five-value bank.

| Answer UUID | Original vᵢ | Uniform multiplier recipe | Source designation |

|---|---|---|---|

| `08792d36-b712-50c1-b364-d2539ef8bc5d` | $\frac{28}{3}$ | $k\left(\frac{28}{3}\right)$ | correct |

| `10c49561-a693-5a9e-8fe4-f237ac8c02dc` | $\frac{25}{2}$ | $k\left(\frac{25}{2}\right)$ | wrong: intent unresolved |

| `26adfe2c-c9e9-5b3f-a5e0-1481d5b90994` | $\frac{20}{3}$ | $k\left(\frac{20}{3}\right)$ | wrong: intent unresolved |

| `6c787fa5-b320-5415-99de-06c8e742d4f5` | $9$ | $k\left(9\right)$ | wrong: intent unresolved |

| `6e385de7-39aa-5450-a0e9-ee6c4afd30d2` | $7$ | $k\left(7\right)$ | wrong: intent unresolved |

### q-39345_observed

Question UUID `e4234b69-bc6e-5b88-b148-08ea10478920`; field UUID `a0b9a63a-36ef-528c-ae36-20b4778b17db`; field key `selection`. Complete five-value bank.

| Answer UUID | Original vᵢ | Uniform multiplier recipe | Source designation |

|---|---|---|---|

| `346fd834-9f4b-5298-99e8-684dece5b13b` | $12$ | $k\left(12\right)$ | wrong: intent unresolved |

| `40fc053f-efcc-59ec-af1c-fef223bf76b5` | $9$ | $k\left(9\right)$ | wrong: intent unresolved |

| `c90f25cc-5183-51bc-8ea0-dfe66b0a8547` | $16$ | $k\left(16\right)$ | wrong: intent unresolved |

| `cd18a5c9-22f8-510d-b764-46c7b3cf4a87` | $10$ | $k\left(10\right)$ | correct |

| `f57bcf97-908f-5723-a9d1-77a0ae528e17` | $18$ | $k\left(18\right)$ | wrong: intent unresolved |

### q-81102_observed

Question UUID `88864edb-1c9c-588d-bdc6-1eef5e251f66`; field UUID `7a5f8fc5-bd8c-52a6-b3a1-caea03d05cdf`; field key `selection`. Complete five-value bank.

| Answer UUID | Original vᵢ | Uniform multiplier recipe | Source designation |

|---|---|---|---|

| `499b11ec-b714-5e35-93a8-a00dd90bd487` | ${e}^{2}-\frac{\pi }{2}$ | $k\left({e}^{2}-\frac{\pi }{2}\right)$ | wrong: intent unresolved |

| `4b3d1df7-d187-5a76-9ff2-d586354e93f0` | ${e}^{2}-1$ | $k\left({e}^{2}-1\right)$ | correct |

| `a07e3936-f719-59ae-bec5-b46ca80359cb` | $e+1$ | $k\left(e+1\right)$ | wrong: intent unresolved |

| `ce5f8cad-b0d3-57e8-8823-669fc1f82f6e` | $e-\frac{\pi }{2}$ | $k\left(e-\frac{\pi }{2}\right)$ | wrong: intent unresolved |

| `dc675675-601c-5a06-9c0d-83e3763e65c4` | ${e}^{2}$ | $k\left({e}^{2}\right)$ | wrong: intent unresolved |

### q-124660_observed

Question UUID `36f8b820-02e2-5d5e-8155-bd2e7c9da1db`; field UUID `79e92368-7b49-5e53-95cb-a87e9c528421`; field key `selection`. Complete five-value bank.

| Answer UUID | Original vᵢ | Uniform multiplier recipe | Source designation |

|---|---|---|---|

| `2f77ceb7-6be8-5d0b-93e7-60790b6d14db` | $\frac{2}{\pi }$ | $k\left(\frac{2}{\pi }\right)$ | correct |

| `488a4e09-5667-54f6-ad88-5c61e9a4ef4c` | $\frac{1}{\pi }$ | $k\left(\frac{1}{\pi }\right)$ | wrong: intent unresolved |

| `65db0f0e-cfd6-52b8-9117-b967fb489769` | $2\pi $ | $k\left(2\pi \right)$ | wrong: intent unresolved |

| `8b52cac3-7234-5848-87cf-921935519eb4` | $\pi $ | $k\left(\pi \right)$ | wrong: intent unresolved |

| `9b98bb58-d459-5b8d-8729-a3f1ab440861` | $\frac{\pi }{2}$ | $k\left(\frac{\pi }{2}\right)$ | wrong: intent unresolved |

### q-90714_observed

Question UUID `b73ad7ec-dc24-5c99-a917-9ce5919adbcd`; field UUID `b523b71f-1a4d-563c-8ba4-de711d207cf0`; field key `selection`. Complete five-value bank.

| Answer UUID | Original vᵢ | Uniform multiplier recipe | Source designation |

|---|---|---|---|

| `29488f70-3dff-5945-99fa-114e41ce2085` | $-8$ | $k\left(-8\right)$ | wrong: intent unresolved |

| `38c233c1-8522-530d-9bbc-48e152799452` | $-6$ | $k\left(-6\right)$ | correct |

| `794f752f-1659-5318-a69d-58c5a353960e` | $6$ | $k\left(6\right)$ | wrong: intent unresolved |

| `d6e2e962-8b22-57c7-9fde-b02c03d0533e` | $-9$ | $k\left(-9\right)$ | wrong: intent unresolved |

| `e3ac4b86-8657-5c33-ab2c-ac749e9ddbc9` | $5$ | $k\left(5\right)$ | wrong: intent unresolved |

Authored endpoint evaluation retains each separately evaluated primitive term, including zero terms at the starting endpoint, as an unevaluated component sum before the final scalar collection. The validator checks the ordered component masks and rejects a same-value collapsed endpoint row.
