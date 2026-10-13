# Four extraction stages

## 1. Specific sources

Every raw question, all original fields/UUIDs/choices, captured labels, full worked-solution prose and value-by-value mappings are retained in source.json, source-cases.json and source-components.json. q-1079 has zero diagonal product (1*0) and determinant -6. q-1080 has 40-(-3)=43; q-11646 has 12-(-10)=22 and reversed off-diagonal substitution order. q-127578 has 35-27=8; q-127580 has -5-20=-25. Blank sources give 32+15=47, 6-4=2 and 42+10=52. q-11648 asks for determinant of [2,-4;-2,7], giving 14-8=6; no observed correct label or solution exists.

## 2. Generalized pattern

Evaluate a supplied integer 2x2 determinant by the same ad-bc operation: locate the ordered diagonal entries, substitute both products, evaluate the two integer products, then subtract. Named forms include a separate determinant-to-matrix row; bare forms combine the matrix and substitution row. Radio responses are one exact integer from five; blank responses are a delimiter-free exact integer and retain their field-1 placeholder. No response-dependent solution or distractor feedback is added.

## 3. Components and full banks

source-components.json maps every original option to its field, exact value, profile and parameterized numerical covariance coefficient. All 33 source options (six 5-choice radios and three blanks), including 24 radio distractors, remain covered. One choice is correct mathematically in every complete bank. Eight designations are captured; the missing ninth is separately inferred.

The scalars alone do not recover mistake operations. An observed profile multiplies its documented scalar coefficient by the newly computed determinant, restricted to common nonzero integral matrix scaling, so both determinant and every replay option scale by t² and remain integers. At original parameters this matches the entire observed bank. This is an explicitly opaque numerical covariance extension, not a theory of the learner error. No arbitrary scalar fitting enters default banks. Original bank records are never returned as literal payloads or answer lookups; prompts/solutions/answers follow the same parameterized generation path.

The default authored 5-choice bank is one complete operation set: ad-bc (correct), ad+bc (add instead of subtract), bc-ad (reverse subtraction), ad (omit the other product), and ab-cd (multiply rows). Generate the complete bank and reject the whole instance if any pair coincides. No pooled first-valid distractors. Blank defaults compute only ad-bc. A profile's numerical reproduction is checked separately from the defensibility of authored default distractors.

## 4. Reusable templates, domains and scope

Fixed: complete source opening formula, transition sentence and paragraph/math layout. Slots: four ordered integer matrix entries, matrix name, both substitution factors, two products and final determinant. Conditional slots group negative factors after multiplication/subtraction; parenthesized blank templates turn subtraction of a negative product into addition. Source c*b ordering and first-row omissions are structural template attributes, never CAS simplifications. Full prose and every original stage are compared byte-for-byte on replay. No TeX repair is needed.

Easy default bounds: |entry|<=9, at most one zero and at most one negative, at least one product magnitude >=2; support source easy signed and zero cases without collapsing both products into zero. Moderate default bounds: nonzero |entry|<=10, at least one negative and at least one product magnitude >=10, matching observed signed arithmetic. Observed easy and moderate ratings overlap; these bounds are authored variation policies, not claims of recovered authoring code. Hard (absent from sources) bounds: each |entry| in 6..15, two or three negatives, both product magnitudes >=50 and at least one magnitude >=11. Thus hard always retains two nonunit products and signed integer subtraction. Arithmetic size/sign management is the only authored extra demand; no new algebraic skill. Every instance in a level has the same direct ad-bc workload, with no internal progression. All bounds apply to explicit authored inputs. Observed covariance replay has its separate finite scaling domain (all |entry|<=40); it is never used by default and is not counted as authored level variety.

Content UUIDs depend on actual printed prompt, full fixed solution, field layout and sorted complete bank. The mathematical fingerprint depends only on the ordered matrix; names, layout, profile, option order and seed cannot inflate assessed task counts. Choice shuffling is seeded after correct identity recording. Different banks on an identical matrix get different content IDs. Harmless profile aliases with identical learner output do not change IDs.

Plot extraction/spec: none. No assessed image references or parameter-dependent visual objects; no image renderer is needed at steps 5/7.
