# Four-stage extraction

## 1. Specific source descriptions

All prompts ask for the units of a **first** derivative from a verbal declaration of function output and input units, with no numeric function or calculation. Each is a single response demand. Derivative notation is retained exactly at original replay, including `\frac{dw}{dp}`, `\frac{dV}{dt}`, and the seven `\frac{\text{d}…}{\text{d}…}` sources. Neither constants nor incidental numbers serve as artificial variation parameters.

- **q-48557 farmer:** output `w(p)` metric tons; input `p` dollars per ton. No source rating/solution/correct designation. Five text choices exactly documented below. Compound input makes the requested units tons²/dollar. Both the EDB prompt and authoritative widget agree, so there is no support for silently interpreting `p` as dollars. Raw profile is invalid evidence; normal output retains prompt and four wrong options and replaces its missing correct option.
- **q-48613 pail:** `V(t)` cubic centimeters and `t` seconds; five text choices with output-length versus volume distinctions. No source rating/solution/correct ref. Original widget confirms the full bank. Authored easy assignment; correct value independently inferred as cubic centimeters per second.
- **q-110040 website:** `v(h)` visits and `h` hours, captured easy with no fields. Source solution declares time before output, refers to visitors, uses `v` rather than `v(h)` in the change explanation and concludes `visitors per hour ` with a trailing space. All of those source-specific text features replay exactly. Normal output repairs visitors → visits; the radio bank is authored because neither EDB nor available older widget provides one.
- **q-72091 reward:** `R(p)` dollars for average `p` exam points, easy; no fields. Source explanation uses full function `R(p)`, output before input, “In other words” conclusion. Five-text radio is an authored missing-field repair.
- **q-110037 cupcake:** `f(c)` grams of flour for `c` cupcakes, easy; five text choices, grams/kilograms as distinct requested scales, and `squared kilograms`. Source solution output/input table uses cupcakes plural; quotient denominator uses cupcake singular; “Therefore” conclusion.
- **q-110038 milk:** `p(v)` dollars and input `v` liters; easy, five text choices with milliliters as an alternate declared scale and cubic dollars/squared liters. “In other words” conclusion. One derivative unit demand; no milk price rate differentiation.
- **q-110042 battery:** `L(t)` hours of battery duration versus `t` minutes of charging, easy. These are named time units with a nontrivial exact unit scale; hours/minute and minutes/hour are unequal complete unit expressions even though both are dimensionless in physical-dimensional analysis. Source quotient uses minute singular. Five text choices.
- **q-72092 currency:** exchange output `E(D)` euros versus input `D` dollars, easy, five text choices. Currency values remain symbolic named units because no exchange conversion rate is supplied. No numerical currency conversion.
- **q-48611 coffee:** temperature `F(t)` degrees Fahrenheit and `t` minutes; easy. Bank starts each choice with a capital letter, while solution is lowercase. “Degrees Fahrenheit squared per minute” is retained exactly as a squared-temperature distractor; no Celsius conversion. Five text choices.

No practice plot appears in prompt, bank, or solution. Plot extraction and generation are none.

## 2. Shared generalized pattern

Identify the units of the function output and its independent variable. The derivative measures change in output over change in input, so divide the **complete** declared output unit by the **complete** declared input unit. Match a named-unit text option, preserving output/input orientation, unit powers and exact scale. The context and solution prose variants remain separate templates, while this assessed operation is common to all.

The lesson's common solution stages are preserved structurally: declarations in prose → two-row unit-label block → fixed change-ratio sentence and unit-quotient block → prose unit conclusion. Authoring the missing solutions uses all of those stages, not just a final units lookup. There is one fixed solution per instance and no option-dependent feedback/diagnosis.

## 3. Components and complete observed banks

`U` is the dependent named unit; `V` is the input named unit (farmer's input is the **compound** `V/U`); `A` is a neighboring named scale unit. A choice recipe records a complete numerator/denominator, exponent, singular/plural form and prefix/suffix power spelling in templates.json. The interpretations below describe explicit unit-pattern transformations and do not claim recovery of the original author's distractor algorithm.

| Source | Profile | Exact original choices, with generalized recipe |
| --- | --- | --- |
| q-48557 | raw_observed | `dollar per ton squared` = V/U²; `dollar per ton` = V/U; `tons` = U; `dollars` = V; `tons per dollar` = U/V |
| q-48613 | observed | `seconds` = V; `centimeters per second` = U/V; `centimeters` = U; `cubic centimeters per second` = U³/V (correct); `seconds per cubic centimeter` = V/U³ |
| q-110037 | observed | `squared kilograms per cupcake` = A²/V; `cupcakes per kilogram` = V/A; `kilograms per cupcake` = A/V; `grams per cupcake` = U/V (correct); `cupcakes per gram` = V/U |
| q-110038 | observed | `milliliters per squared dollar` = A/U²; `dollars per liter` = U/V (correct); `liters per dollar` = V/U; `dollars per milliliter` = U/A; `cubic dollars per squared liters` = U³/V² |
| q-110042 | observed | `squared hours` = U²; `hours per minute` = U/V (correct); `minutes` = V; `hours` = U; `minutes per hour` = V/U |
| q-72092 | observed | `dollars` = V; `euros per dollar` = U/V (correct); `dollars per euro squared` = V/U²; `dollars per euro` = V/U; `euros` = U |
| q-48611 | observed | `Degrees Fahrenheit per minute` = U/V (correct); `Degrees Fahrenheit` = U; `Minutes per degrees Fahrenheit` = V/U; `Minutes` = V; `Degrees Fahrenheit squared per minute` = U²/V |

Every one of 35 original choice strings is mapped one-to-one. Five original correct designations exist and all five match their complete unit expressions. Missing correct refs in the two older sources are not counted as matched designations. The corrected farmer bank replaces U/V with U²/V, preserving the four other options and the five-choice count. Original raw bank remains replayable via the public generate API, without inventing a correct selection.

Website/reward each have a labeled authored full bank: U/V, U, V, V/U, U²/V. Website U is visits for the field; its observed replay preserves only the incorrect raw solution's visitor wording. None of those ten authored options counts toward original bank fidelity.

Authored moderate bank: Uᵏ/V (correct), V/Uᵏ, U/V, Uᵏ, V, k∈{2,3}. Authored hard bank: U²/V (correct), U/V, V/U², V/U, U. The complete bank is chosen as a unit; equality/ambiguity invalidates the whole instance. No first-valid recipe pooling occurs.

## 4. Reusable masks, calculations and domains

build_evidence.py produces slot masks in templates.json from captured strings. Longest **complete unit phrases** are masked before shorter singular/plural phrases. Function symbols, TeX command names, quoted punctuation, solution ordering and all unrelated prose are fixed. The script fills those unit slots and constructs every answer from term recipes through the normal API; it never returns a literal source question payload.

For original contexts the exact observed unit labels are legal explicit parameters. Approved finite samplers are:

- Farmer: output ton/kilogram, input dollar/euro per output unit; unit ratio U/(V/U). Source remains labeled unrated in evidence, with an authored hard replay rating.
- Pail: cubic centimeter/meter output; second/minute/hour input.
- Website: visits output; hour/minute/second input; visitors retained only in raw teaching prose.
- Reward: dollar/euro output; point input.
- Cupcake: gram/kilogram output; cupcake input; alternate A must be the other mass unit.
- Milk: dollar/euro output; liter/milliliter input; alternate A must be the other volume unit.
- Battery: hour output; minute/second input; never an equal pair.
- Currency: euro output; dollar input. This observed bank has one meaningful domain pair, honestly counted.
- Coffee: degrees Fahrenheit output; minute/second/hour input.

Authored moderate has one output length label raised to power 2/3 and one non-time count input; sixteen tasks. Authored hard has one quantity output and one currency-per-same-quantity input; sixteen tasks, including the same units operation as farmer. Entry point sections and guards document those workload bounds; all explicit parameters obey the same bounds. Seeds merely choose eligible units and option order, not new mathematical difficulty.

Exact SymPy expressions include declared scale: kilogram=1000 grams, ton=1,000,000 grams, minute=60 seconds, hour=3600 seconds, centimeter=1/100 meter, liter=1/1000 cubic meter, milliliter=1/1,000,000 cubic meter. This is internal equality QA, **not a conversion exercise**. Independent validator asserts liter=1000 cm³ and mL=cm³ and parses the units from the actual printed prompt and choices. A wrong kg/cupcake option remains wrong for a grams/cupcake request.

Mathematical fingerprints include the exact dependent/input unit objects and exclude context, symbols, bank/profile and option order. Content identities include actual prompt, fixed solution, sorted complete bank, correct designation and generator version. Field/answer UUIDs are stable and field-owned. Raw profile aliases do not create new identities when actual content is unchanged. The finite domains are exhausted and deduplicated globally by level in validation.json; farmer and authored price-rate duplicates do not inflate hard task counts.

Source fidelity checks compare **whole source prompt and worked solution strings**, not a few shared phrases, and all bank strings ignoring option order. Normal output mathematics/formatting and native radio grading are separate checks. Website raw prose and farmer raw invalid bank are intentionally excluded from normal learner eligibility and documented rather than marked mathematically correct. All normal declared unit tables, displayed quotient stages and final text are independently verified. No EDB transactions or registration follow this draft.
