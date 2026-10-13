# Template extraction

## 1. Describe each source before generalizing

Each source below keeps its exact prompt, bank and ordered solution in `source.json` and `source-replays.json`. Integer exponents range from 1 through 5, coefficients are 1 or 2 (and negative signs), angle symbols are x, theta and the literal Greek theta. All operations are products and sums of sin/cos of a single real angle. There are no denominators or branch restrictions. A complete simplified expression is selected from five delimiter-free mathematical choices.

### q-65163

Simplify the trigonometric expression $\cos^{3} θ + \cos θ\sin^{2} θ$.

Difficulty: unrated. Field: selection/radio; five choices. Worked solution absent.

### q-65193

Simplify the trigonometric expression $\sin^{2} x\cos^{3} x + \sin^{4} x\cos x$.

Difficulty: unrated. Field: selection/radio; five choices. Worked solution absent.

### q-119362

Simplify the trigonometric expression ${cos}^{3}⁡\theta {sin}^{2}⁡\theta +{cos}^{5}⁡\theta .$

Difficulty: easy. Field: selection/radio; five choices. Worked solution present; 5 ordered equality rows including the stated identity.

### q-119367

Simplify the trigonometric expression $2\operatorname{sin}⁡\theta -{cos}^{3}⁡\theta -\operatorname{cos}⁡\theta {sin}^{2}⁡\theta .$

Difficulty: moderate. Field: selection/radio; five choices. Worked solution present; 5 ordered equality rows including the stated identity.

### q-119371

Simplify the trigonometric expression ${sin}^{3}⁡\theta +\operatorname{sin}⁡\theta {cos}^{2}⁡\theta +\operatorname{sin}⁡\theta .$

Difficulty: moderate. Field: selection/radio; five choices. Worked solution present; 6 ordered equality rows including the stated identity.

### q-65229

Simplify the trigonometric expression $\operatorname{sin}⁡\theta {cos}^{2}⁡\theta +{sin}^{3}⁡\theta .$

Difficulty: easy. Field: selection/radio; five choices. Worked solution present; 5 ordered equality rows including the stated identity.

### q-65241

Simplify the trigonometric expression $\operatorname{sin}⁡x{cos}^{3}⁡x+{sin}^{3}⁡x\operatorname{cos}⁡x.$

Difficulty: easy. Field: selection/radio; five choices. Worked solution present; 5 ordered equality rows including the stated identity.

### q-65242

Simplify the trigonometric expression ${sin}^{5}⁡x+{cos}^{2}⁡x{sin}^{3}⁡x.$

Difficulty: easy. Field: selection/radio; five choices. Worked solution present; 5 ordered equality rows including the stated identity.

### q-65243

Simplify the trigonometric expression ${sin}^{2}⁡x{cos}^{2}⁡x+{cos}^{4}⁡x+{sin}^{2}⁡x.$

Difficulty: moderate. Field: selection/radio; five choices. Worked solution present; 6 ordered equality rows including the stated identity.

### q-72711

Simplify the trigonometric expression $\operatorname{sin}⁡x+2{cos}^{3}⁡x+2{sin}^{2}⁡x\operatorname{cos}⁡x.$

Difficulty: moderate. Field: selection/radio; five choices. Worked solution present; 5 ordered equality rows including the stated identity.

## 2. Generalize the common method

Factor a common monomial in sin(angle) and cos(angle) so the remaining sum is sin²(angle)+cos²(angle). Replace that sum by 1. A third residual term can then be collected or combined by the same identity. Source replay masks retain original sum order and fixed prose; authored hard performs this operation independently on two pairs.

## 3. Map every component and complete bank

The observed banks are expression patterns with unresolved error intentions. Their parameterized recipe is simultaneous substitution of complete sin/cos function names and complete angle arguments. For swap=false, S=sin(angle), C=cos(angle); for swap=true, S=cos(angle), C=sin(angle). The expression below is parsed from the whole owned choice, not fitted to its numerical value. All choices in a bank are rendered together; none are pooled.

### raw:q-65163 / repaired:q-65163

| Owned source answer UUID | Exact source value | Parameterized whole expression | Original designation |
|---|---|---|---|
| d69d271a-f3c8-56b0-b7dc-fa6812034519 | `\cos θ` | `C` | not designated |
| dbb0c832-08fd-5312-b076-070a25b4c05e | `2\cos θ` | `2*C` | not designated |
| dc885703-f19c-55bc-ad37-2bc6f538bea0 | `-2\cos^{2} θ` | `-2*C**2` | not designated |
| 2f36f807-8f0d-5398-8106-de28bd21a7c7 | `\cos^{2} θ` | `C**2` | not designated |
| 6333aba8-e989-5bc9-8dbb-dadf2674e638 | `-\cos θ` | `-C` | not designated |

### raw:q-65193 / repaired:q-65193

| Owned source answer UUID | Exact source value | Parameterized whole expression | Original designation |
|---|---|---|---|
| 9fe791fb-8776-5ba1-8486-38d056683c9b | `\sin^{2} x + \cos x` | `C + S**2` | not designated |
| faccc32f-ae33-5998-bb5a-6570e83270fc | `\sin x\cos x` | `C*S` | not designated |
| 103c9732-bb99-58c1-9613-b12af96f683b | `\sin^{2} x + 1` | `S**2 + 1` | not designated |
| 2a905bac-2fef-54e4-9da4-e8ea9d88ade8 | `\sin x - \cos x` | `-C + S` | not designated |
| 7fdf1e03-82f0-5ee9-ad44-06497b685aec | `\sin^{2} x\cos x` | `C*S**2` | not designated |

### raw:q-119362 / repaired:q-119362

| Owned source answer UUID | Exact source value | Parameterized whole expression | Original designation |
|---|---|---|---|
| 1666eb4d-d4a7-5e6b-9ab8-611863630400 | `2{cos}^{3}⁡\theta ` | `2*C**3` | incorrect |
| 671b51fc-531d-5b84-807b-36d54aed2521 | `-{cos}^{3}⁡\theta ` | `-C**3` | incorrect |
| 8919a4b0-5234-55e6-83d8-2a41e35d8daa | `2+{cos}^{3}⁡\theta ` | `C**3 + 2` | incorrect |
| cdf0fa52-e133-5bc9-a22b-a492f6ef6b68 | `{cos}^{3}⁡\theta +1` | `C**3 + 1` | incorrect |
| dea9e82c-1cb6-5360-b9bd-65af00f2d2da | `{cos}^{3}⁡\theta ` | `C**3` | correct |

### raw:q-119367 / repaired:q-119367

| Owned source answer UUID | Exact source value | Parameterized whole expression | Original designation |
|---|---|---|---|
| 2d3c858f-72cf-59c5-a71e-bf205cf9510e | `2\operatorname{sin}⁡\theta -1` | `2*S - 1` | incorrect |
| 674ed942-0d10-52be-8508-29405e26bf5c | `2\operatorname{sin}⁡\theta \operatorname{cos}⁡\theta ` | `2*C*S` | incorrect |
| 7f7196a7-2009-5537-a45f-466fd8a11ba0 | `\operatorname{sin}⁡\theta -\operatorname{cos}⁡\theta ` | `-C + S` | incorrect |
| 960d1f39-be40-5913-817e-76c42bfe84e4 | `2\operatorname{sin}⁡\theta -\operatorname{cos}⁡\theta ` | `-C + 2*S` | correct |
| aec279ea-8dda-5b03-ae58-55db46c2cede | `2\operatorname{sin}⁡\theta +\operatorname{cos}⁡\theta ` | `C + 2*S` | incorrect |

### raw:q-119371 / repaired:q-119371

| Owned source answer UUID | Exact source value | Parameterized whole expression | Original designation |
|---|---|---|---|
| 1815e8ee-c289-5f64-9f4d-5df43b4aab39 | `\operatorname{sin}⁡\theta +1` | `S + 1` | incorrect |
| 25423e87-2e31-52ea-9bed-9680a8ad4d75 | `1-\operatorname{sin}⁡\theta ` | `1 - S` | incorrect |
| 380b2f49-3850-505e-a125-48611fc7669a | `2\operatorname{sin}⁡\theta ` | `2*S` | correct |
| b6fc9b1c-0a28-54c2-82c9-b8ff1ad7eae4 | `\operatorname{sin}⁡\theta ` | `S` | incorrect |
| bb0ddaa2-dc14-5f83-8293-f70b43e52381 | `2\operatorname{sin}⁡\theta +1` | `2*S + 1` | incorrect |

### raw:q-65229 / repaired:q-65229

| Owned source answer UUID | Exact source value | Parameterized whole expression | Original designation |
|---|---|---|---|
| 02d7371b-7e5b-5f51-a575-5e52d878b5c8 | `2\operatorname{sin}⁡\theta ` | `2*S` | incorrect |
| 193108c5-931f-564f-b252-07665477dc34 | `\operatorname{sin}⁡\theta -1` | `S - 1` | incorrect |
| 7b56426e-1884-51ec-a725-95996978cb19 | `\operatorname{sin}⁡\theta +1` | `S + 1` | incorrect |
| 89516c4f-55c0-5b8f-9955-e18423108512 | `-\operatorname{sin}⁡\theta ` | `-S` | incorrect |
| e12e3070-6a78-5139-96fa-51a9722de3bb | `\operatorname{sin}⁡\theta ` | `S` | correct |

### raw:q-65241 / repaired:q-65241

| Owned source answer UUID | Exact source value | Parameterized whole expression | Original designation |
|---|---|---|---|
| 1332c368-ca92-598a-b017-c6a38e37515b | `2\operatorname{sin}⁡x\operatorname{cos}⁡x` | `2*C*S` | incorrect |
| 3b440461-a311-58f9-97a9-e236f18955f3 | `2\operatorname{sin}⁡x\operatorname{cos}⁡x-1` | `2*C*S - 1` | incorrect |
| 3d865c4f-b7d6-59c6-af49-bc32692c8d3d | `-\operatorname{sin}⁡x\operatorname{cos}⁡x` | `-C*S` | incorrect |
| ccf29d01-df1f-5592-a1cc-d38d9953cc72 | `-2\operatorname{sin}⁡x\operatorname{cos}⁡x+1` | `-2*C*S + 1` | incorrect |
| ed815fda-1d0c-57d0-91b5-495efb2c04b8 | `\operatorname{sin}⁡x\operatorname{cos}⁡x` | `C*S` | correct |

### raw:q-65242 / repaired:q-65242

| Owned source answer UUID | Exact source value | Parameterized whole expression | Original designation |
|---|---|---|---|
| 157552b8-e765-5d61-8346-1aa10683fec6 | `{sin}^{3}⁡x` | `S**3` | correct |
| 5c79992e-1408-559a-98eb-3bff3199b138 | `-{sin}^{3}⁡x` | `-S**3` | incorrect |
| 8a04e9e1-60b9-510a-ae62-f44c851f7b22 | `{sin}^{2}⁡x` | `S**2` | incorrect |
| 9a74ba8f-3ef7-5e80-912c-e2627d41fec7 | `-{sin}^{2}⁡x` | `-S**2` | incorrect |
| fc1b2500-f9ab-5d8c-94e6-018b91064fad | `\operatorname{sin}⁡x` | `S` | incorrect |

### raw:q-65243 / repaired:q-65243

| Owned source answer UUID | Exact source value | Parameterized whole expression | Original designation |
|---|---|---|---|
| 2cd57dd3-a194-5b56-84d6-87e4444afb9c | `2` | `2` | incorrect |
| 3d8cf897-ea6b-5f51-9afd-8aaa5d08aa48 | `0` | `0` | incorrect |
| 549211cd-01a7-542a-b47e-d75d6a3097fa | `1` | `1` | correct |
| 63d89e8b-ca8c-57b3-9147-34899f169960 | `-1` | `-1` | incorrect |
| d2dec1a9-1dd1-5a2f-bcda-419921628be9 | `-2` | `-2` | incorrect |

### raw:q-72711 / repaired:q-72711

| Owned source answer UUID | Exact source value | Parameterized whole expression | Original designation |
|---|---|---|---|
| 733d9013-5828-5e8a-a6ca-98d0ee84db3d | `-2\operatorname{sin}⁡x+\operatorname{cos}⁡x` | `C - 2*S` | incorrect |
| 9e08cb06-fa94-559a-b45f-0247593ae993 | `\operatorname{sin}⁡x-\operatorname{cos}⁡x` | `-C + S` | incorrect |
| ce427bad-7fbf-553d-94e7-4eac1f2a458e | `\operatorname{sin}⁡x+3\operatorname{cos}⁡x` | `3*C + S` | incorrect |
| d512d53f-d1ef-5fcf-a459-a5ecee4d6396 | `\operatorname{sin}⁡x+2\operatorname{cos}⁡x` | `2*C + S` | correct |
| ddb559b7-bf25-5a4d-8461-b1784d7b4dd7 | `-\operatorname{sin}⁡x+\operatorname{cos}⁡x` | `C - S` | incorrect |

## 4. Extract reusable masks and constraints

Source masks consist of literal Markdown/prose plus complete trigonometric function-name and angle slots. Exact exponents, coefficients, source spacing, argument omissions and solution sequence remain original. The public raw API reconstructs these masks through the same slot renderer; it never returns the literal capture record or looks up a final answer. Complete choice values come from these same expression patterns, with correct designation mapped from original owned answer UUID. Sine/cosine symmetry provides a valid same-method parameterization; source bank intentions remain unresolved and are not promoted to authored default distractor operations.

Repaired masks normalize complete function atoms to standard LaTeX and make exactly the two documented solution repairs. The unrated profiles add mathematically derived correct refs, an authored easy label and a parameterized five-row authored solution. No repaired designation is counted as an observed designation where it was absent. Raw missing-key parity is checked individually.

For authored generation let F=a*S^p*C^q. Easy displays F*S²+F*C² and factors F. Moderate adds residual R: opposite or same linear monomial, or a complementary square with matching coefficient. Hard adds G=b*C^n, displaying F*S²+F*C²+G*S²+G*C² and factoring each pair. Ordered solution stages are prompt → factored expression → identity substitution → optional collection → final simplified expression → conclusion. Separate unevaluated masks preserve factoring and multiplication by 1.

| Authored family | Whole five-choice operation bank (chosen together) |
|---|---|
| easy | F, 2F, -F, F*(S²+C²-1), F*(S²-C²) |
| moderate opposite | F+R, F-R, -F+R, F*(S²-C²)+R, 2F+R |
| moderate same | F+R, F-R, -(F+R), F*(S²-C²)+R, F+2R |
| moderate complement | a, 2a, -a, 0, F-R |
| hard | F+G, F-G, -F+G, F*(S²-C²)+G, F+G*(S²-C²) |

These are authored error operations (doubled factors, wrong signs, the wrong squared relation, omitted identity value), not recovered source intent. They produce no learner-facing diagnosis. Complete banks reject any two equivalent values modulo S²+C²-1. Workload ranges and the exact 598-task domain are in `classification.md`; source original parameters are not forced into those authored bounds. Angle aliases and bank/layout spelling do not affect mathematical fingerprints. Content identities include actual prompt, fixed solution and complete bank; seed-based shuffling preserves identity.

## Plots (steps 5 and 7)

Rating: none for every template/profile/layout. Captured learner content contains no plot references. No renderer or generated plot assets are needed.
