# Newer capture correction review

Preparation only. Nothing in this migration has been transacted. All original Math Academy content must be committed first with `:org/Math-Academy` as source. Corrections follow on the same question entities, with the assistant source entity that will be created later. Jake is not the correction source.

The saved mathematical-correction archive contains 83 affected entities and 88 distinct verified correction events, including earlier versions. Each event is bound to its reviewed content and old transaction by the saved verification hashes. Old transactions contain old entity IDs and are evidence, not files to replay.

## Changes to canonical answer values

These are exact string comparisons. Unit and notation changes are included; this count is not a count of mathematical errors.

### q-104058 — old basis 2238

Original MA: `{"selection": "\\operatorname{ln}⁡|y|-y={x}^{2}-2"}`

Reviewed correction: `{"selection": "No differentiable classical solution exists."}`

The initial point makes the original differential equation require 0*yprime(1)=2. Retain its equation and initial data, clarify classical existence, replace the erroneous solution and add the correct no-solution choice with a new field version while preserving all source fields, answers, IDs and history.

[Review](/home/jake/Developer/Course_Academy/reference/mathacademy/mathematical-corrections/q-104058/review.json) · [Old transaction](/home/jake/Developer/Course_Academy/reference/mathacademy/mathematical-corrections/q-104058/transaction.edn) · [Verification](/home/jake/Developer/Course_Academy/reference/mathacademy/mathematical-corrections/q-104058/verification.json)

### q-124871 — old basis 1883

Original MA: `{"selection": "{\\int }_{1}^{3}6{t}^{2}\\,dt"}`

Reviewed correction: `{"selection": "\\displaystyle \\int_{1}^{3}6t^{3}\\,dt"}`

The original source correctly substitutes 3t^2*(2t), then incorrectly simplifies it to6t^2. Correct pullback is6t^3 and integral120. Preserve the original prompt and four current distractor answer identities, replace the defective study alternative with the already stored correct exponent, new field identity with existing mathematically correct answer identity retained, preserve raw source and actual Correct probe grade as evidence.

[Review](/home/jake/Developer/Course_Academy/reference/mathacademy/mathematical-corrections/q-124871/review.json) · [Old transaction](/home/jake/Developer/Course_Academy/reference/mathacademy/mathematical-corrections/q-124871/transaction.edn) · [Verification](/home/jake/Developer/Course_Academy/reference/mathacademy/mathematical-corrections/q-124871/verification.json)

### q-125485 — old basis 1940

Original MA: `{"selection": "8\\pi "}`

Reviewed correction: `{"selection": "8π"}`

Supply the omitted convergent improper-integral convention. Four independently convergent quadrant integrals yield 8pi; ordinary original circulation remains undefined.

[Review](/home/jake/Developer/Course_Academy/reference/mathacademy/mathematical-corrections/q-125485/review.json) · [Old transaction](/home/jake/Developer/Course_Academy/reference/mathacademy/mathematical-corrections/q-125485/transaction.edn) · [Verification](/home/jake/Developer/Course_Academy/reference/mathacademy/mathematical-corrections/q-125485/verification.json)

### q-161134 — old basis 2165

Original MA: `{"selection": "\\sqrt{8}\\,{u}^{5}{v}^{4}"}`

Reviewed correction: `{"selection": "\\sqrt{8}\\,{u}^{4}{v}^{4}|u|"}`

The Euclidean norm requires an absolute value of the parameter. Keep the original general domain, correct its area factor and derivation, and add the absolute-value answer with a new field version, retaining the old field, choices, key and history. q161286 uses sqrt8|v|; q161134 uses sqrt8|u|.

[Review](/home/jake/Developer/Course_Academy/reference/mathacademy/mathematical-corrections/q-161134/review.json) · [Old transaction](/home/jake/Developer/Course_Academy/reference/mathacademy/mathematical-corrections/q-161134/transaction.edn) · [Verification](/home/jake/Developer/Course_Academy/reference/mathacademy/mathematical-corrections/q-161134/verification.json)

### q-161286 — old basis 2164

Original MA: `{"selection": "({u}^{2}-{v}^{2}-2u)\\sqrt{8}v"}`

Reviewed correction: `{"selection": "({u}^{2}-{v}^{2}-2u)\\sqrt{8}|v|"}`

The Euclidean norm requires an absolute value of the parameter. Keep the original general domain, correct its area factor and derivation, and add the absolute-value answer with a new field version, retaining the old field, choices, key and history. q161286 uses sqrt8|v|; q161134 uses sqrt8|u|.

[Review](/home/jake/Developer/Course_Academy/reference/mathacademy/mathematical-corrections/q-161286/review.json) · [Old transaction](/home/jake/Developer/Course_Academy/reference/mathacademy/mathematical-corrections/q-161286/transaction.edn) · [Verification](/home/jake/Developer/Course_Academy/reference/mathacademy/mathematical-corrections/q-161286/verification.json)

### q-161481 — old basis 2265

Original MA: `{"selection": "\\pi -\\frac{{\\pi }^{3}}{6}"}`

Reviewed correction: `{"selection": "0"}`

Retain original inequalities, graph and field literally. They force projection{(0,0)}, area0 and flux0 under the zero-area convention; graph is degenerate, not regular2D. Source accepted b is only the formal reversed-bound integral. New field version appends0 and retains original fields/answers/history without inferring replacement bounds.

[Review](/home/jake/Developer/Course_Academy/reference/mathacademy/mathematical-corrections/q-161481/review.json) · [Old transaction](/home/jake/Developer/Course_Academy/reference/mathacademy/mathematical-corrections/q-161481/transaction.edn) · [Verification](/home/jake/Developer/Course_Academy/reference/mathacademy/mathematical-corrections/q-161481/verification.json)

### q-161496 — old basis 2020

Original MA: `{"selection": "5"}`

Reviewed correction: `{"selection": "\\frac{11}{3}"}`

Retain original R exactly, require its full actual nonempty projection, enforce ordered fibers, and distinguish source printed interval/accepted key from study mathematics. q161496 projection [1,8/3], answer11/3; q161495 projection[-2,4], answer2 with cap split at-1.

[Review](/home/jake/Developer/Course_Academy/reference/mathacademy/mathematical-corrections/q-161496/review.json) · [Old transaction](/home/jake/Developer/Course_Academy/reference/mathacademy/mathematical-corrections/q-161496/transaction.edn) · [Verification](/home/jake/Developer/Course_Academy/reference/mathacademy/mathematical-corrections/q-161496/verification.json)

### q-161659 — old basis 2095

Original MA: `{"selection": "\\frac{8}{3}"}`

Reviewed correction: `{"selection": "\\frac{8\\sqrt{2}}{3}"}`

Retain the original R inequalities, require their real domain, and distinguish actual volume8sqrt2/3 from the independently authorized signed polynomial recovery8/3. Add the missing mathematical answer with new field/answer identities; preserve source accepted8/3 and all historical fields.

[Review](/home/jake/Developer/Course_Academy/reference/mathacademy/mathematical-corrections/q-161659/review.json) · [Old transaction](/home/jake/Developer/Course_Academy/reference/mathacademy/mathematical-corrections/q-161659/transaction.edn) · [Verification](/home/jake/Developer/Course_Academy/reference/mathacademy/mathematical-corrections/q-161659/verification.json)

### q-161729 — old basis 2080

Original MA: `{"selection": "0"}`

Reviewed correction: `{"selection": "2"}`

Retain exact S; source nominal key0 differs from actual nonempty fiber product2. Replace only the changed field component, keeping existing answer2 and all other answer identities.

[Review](/home/jake/Developer/Course_Academy/reference/mathacademy/mathematical-corrections/q-161729/review.json) · [Old transaction](/home/jake/Developer/Course_Academy/reference/mathacademy/mathematical-corrections/q-161729/transaction.edn) · [Verification](/home/jake/Developer/Course_Academy/reference/mathacademy/mathematical-corrections/q-161729/verification.json)

### q-31671 — old basis 2041

Original MA: `{"selection": "6\\sqrt{2}\\,{\\text{m/s}}^{2}"}`

Reviewed correction: `{"selection": "6\\sqrt{2}\\,\\text{m}/\\text{s}^{2}"}`

Authentic screenshots show meters per second squared: explicitly scope the exponent to seconds in this acceleration exercise; the captured grouped m/s atom squared is mathematically different. Also repair the isolated swapped acceleration vector and its norm radicand using the unchanged velocity derivative.

[Review](/home/jake/Developer/Course_Academy/reference/mathacademy/mathematical-corrections/q-31671/review.json) · [Old transaction](/home/jake/Developer/Course_Academy/reference/mathacademy/mathematical-corrections/q-31671/transaction.edn) · [Verification](/home/jake/Developer/Course_Academy/reference/mathacademy/mathematical-corrections/q-31671/verification.json)

### q-31674 — old basis 2041

Original MA: `{"selection": "2\\,{\\text{m/s}}^{2}"}`

Reviewed correction: `{"selection": "2\\,\\text{m}/\\text{s}^{2}"}`

Authentic screenshots show meters per second squared: explicitly scope the exponent to seconds in this acceleration exercise; the captured grouped m/s atom squared is mathematically different. Retain every numerical coefficient and accepted magnitude.

[Review](/home/jake/Developer/Course_Academy/reference/mathacademy/mathematical-corrections/q-31674/review.json) · [Old transaction](/home/jake/Developer/Course_Academy/reference/mathacademy/mathematical-corrections/q-31674/transaction.edn) · [Verification](/home/jake/Developer/Course_Academy/reference/mathacademy/mathematical-corrections/q-31674/verification.json)

### q-31683 — old basis 2041

Original MA: `{"selection": "5\\sqrt{5}\\,\\text{m}/\\text{s}^{2}"}`

Reviewed correction: `{"selection": "5\\sqrt{5}m/s^{2}"}`

Authentic screenshots show meters per second squared: explicitly scope the exponent to seconds in this acceleration exercise; the captured grouped m/s atom squared is mathematically different. Retain every numerical coefficient and accepted magnitude.

[Review](/home/jake/Developer/Course_Academy/reference/mathacademy/mathematical-corrections/q-31683/review.json) · [Old transaction](/home/jake/Developer/Course_Academy/reference/mathacademy/mathematical-corrections/q-31683/transaction.edn) · [Verification](/home/jake/Developer/Course_Academy/reference/mathacademy/mathematical-corrections/q-31683/verification.json)

### q-332547 — old basis 1354

Original MA: `{"field-1": "Ae^{-6x}-5"}`

Reviewed correction: `{"field-1": "Ae^{-6x/5}-5"}`

The equation 5y′+6y=-30 requires exponent -6x/5. The original supplied complementary solution, worked solution and accepted answer omit /5. The user explicitly authorized correcting the study question, hint, worked solution and answer key.

[Review](/home/jake/Developer/Course_Academy/reference/mathacademy/mathematical-corrections/q-332547/review.json) · [Old transaction](/home/jake/Developer/Course_Academy/reference/mathacademy/mathematical-corrections/q-332547/transaction.edn) · [Verification](/home/jake/Developer/Course_Academy/reference/mathacademy/mathematical-corrections/q-332547/verification.json)

### q-339239 — old basis 1694

Original MA: `{"selection": "12\\,547"}`

Reviewed correction: `{"selection": "12\\,546"}`

The source lesson rounds the initial constant to three decimal places, then rounds the resulting later population to 12,547. That is its documented approximation method, confirmed by the revealed source solution. The study prompt now explicitly requires final-only nearest-whole rounding, whose mathematically correct value is 12,546. Preserve original source content and its 12,547 key in historical question content and immutable old answer fields; create new study field and answer identities with matching prompt, solution, choice and key.

[Review](/home/jake/Developer/Course_Academy/reference/mathacademy/mathematical-corrections/q-339239/review.json) · [Old transaction](/home/jake/Developer/Course_Academy/reference/mathacademy/mathematical-corrections/q-339239/transaction.edn) · [Verification](/home/jake/Developer/Course_Academy/reference/mathacademy/mathematical-corrections/q-339239/verification.json)

### q-342644 — old basis 1996

Original MA: `{"field-1": "an ordinary", "field-2": "an irregular singular", "field-3": "an irregular singular", "field-4": "a regular singular"}`

Reviewed correction: `{"field-1": "an ordinary", "field-2": "outside the real coefficient domain", "field-3": "an irregular singular", "field-4": "a regular singular"}`

Retain the original real ln(x) equation. Source categorizes-1as irregular despite lacking any real local coefficient domain there. Explicitly add the truthful outside-real-domain response and clarify boundary analyticity at0; keep source keys and raw captures unchanged. ln|x| remains only a separate reviewed recovery alternative, not asserted source intent. The field-2 prompt is phrased as a classification or real-domain status so the added outside-domain response forms a grammatical sentence.

[Review](/home/jake/Developer/Course_Academy/reference/mathacademy/mathematical-corrections/q-342644/review.json) · [Old transaction](/home/jake/Developer/Course_Academy/reference/mathacademy/mathematical-corrections/q-342644/transaction.edn) · [Verification](/home/jake/Developer/Course_Academy/reference/mathacademy/mathematical-corrections/q-342644/verification.json)

### q-37131 — old basis 2290

Original MA: `{"selection": "z=\\operatorname{cos}⁡xy"}`

Reviewed correction: `{"selection": "z=\\cos(xy),\\quad 0\\le xy\\le\\pi"}`

Keep original f and point. Principal arcsine gives the exact level set z=cos(xy),0≤xy≤π. The unrestricted source relation includes extra points. Append a complete choice in a new field version, preserving original source a and historical component identities.

[Review](/home/jake/Developer/Course_Academy/reference/mathacademy/mathematical-corrections/q-37131/review.json) · [Old transaction](/home/jake/Developer/Course_Academy/reference/mathacademy/mathematical-corrections/q-37131/transaction.edn) · [Verification](/home/jake/Developer/Course_Academy/reference/mathacademy/mathematical-corrections/q-37131/verification.json)

### q-72175 — old basis 1728

Original MA: `{"selection": "I and II only"}`

Reviewed correction: `{"selection": "I, II, and III"}`

The integrand is symmetric under exchange of coordinates, so the repeated integral on the transposed rectangle has the same value even though its bounds are assigned to opposite variables. Keep the original equality-truth request and correct the study solution to all three true equalities. The practice item receives a new all-three choice, key, field and answer identities; preserve original source choices, revealed key, actual Incorrect grade, uncertain solver decision, canonical source content and historical EDB versions.

[Review](/home/jake/Developer/Course_Academy/reference/mathacademy/mathematical-corrections/q-72175/review.json) · [Old transaction](/home/jake/Developer/Course_Academy/reference/mathacademy/mathematical-corrections/q-72175/transaction.edn) · [Verification](/home/jake/Developer/Course_Academy/reference/mathacademy/mathematical-corrections/q-72175/verification.json)

### q-82336 — old basis 2041

Original MA: `{"selection": "10\\,{\\text{m/s}}^{2}"}`

Reviewed correction: `{"selection": "10\\,\\text{m}/\\text{s}^{2}"}`

Authentic screenshots show meters per second squared: explicitly scope the exponent to seconds in this acceleration exercise; the captured grouped m/s atom squared is mathematically different. Retain every numerical coefficient and accepted magnitude.

[Review](/home/jake/Developer/Course_Academy/reference/mathacademy/mathematical-corrections/q-82336/review.json) · [Old transaction](/home/jake/Developer/Course_Academy/reference/mathacademy/mathematical-corrections/q-82336/transaction.edn) · [Verification](/home/jake/Developer/Course_Academy/reference/mathacademy/mathematical-corrections/q-82336/verification.json)

### q-82337 — old basis 2041

Original MA: `{"selection": "\\sqrt{5}\\,{\\text{m/s}}^{2}"}`

Reviewed correction: `{"selection": "\\sqrt{5}\\,\\text{m}/\\text{s}^{2}"}`

Authentic screenshots show meters per second squared: explicitly scope the exponent to seconds in this acceleration exercise; the captured grouped m/s atom squared is mathematically different. Retain every numerical coefficient and accepted magnitude.

[Review](/home/jake/Developer/Course_Academy/reference/mathacademy/mathematical-corrections/q-82337/review.json) · [Old transaction](/home/jake/Developer/Course_Academy/reference/mathacademy/mathematical-corrections/q-82337/transaction.edn) · [Verification](/home/jake/Developer/Course_Academy/reference/mathacademy/mathematical-corrections/q-82337/verification.json)

### q-88686 — old basis 2073

Original MA: `{"selection": "II only"}`

Reviewed correction: `{"selection": "None of I, II, III"}`

Ordinary improper integration requires convergent one-sided limits at every tangent pole. Preserve all three integrals and make that definition explicit; add the missing mathematically correct sixth choice. The separately retained principal-value recovery and actual MA grade establish the source key without changing ordinary-integral mathematics.

[Review](/home/jake/Developer/Course_Academy/reference/mathacademy/mathematical-corrections/q-88686/review.json) · [Old transaction](/home/jake/Developer/Course_Academy/reference/mathacademy/mathematical-corrections/q-88686/transaction.edn) · [Verification](/home/jake/Developer/Course_Academy/reference/mathacademy/mathematical-corrections/q-88686/verification.json)

## All reviewed correction events

| Entity | Old basis | Changed content | Evidence |
|---|---:|---|---|
| q-332547 | 1354 | problem, worked_solution, answer_fields | [review](/home/jake/Developer/Course_Academy/reference/mathacademy/mathematical-corrections/q-332547/review.json) |
| q-128452 | 1411 | problem, worked_solution, answer_fields | [review](/home/jake/Developer/Course_Academy/reference/mathacademy/mathematical-corrections/q-128452/review.json) |
| q-280531 | 1428 | problem, worked_solution, answer_fields | [review](/home/jake/Developer/Course_Academy/reference/mathacademy/mathematical-corrections/q-280531/review.json) |
| e-21715 | 1506 | worked_solution | [review](/home/jake/Developer/Course_Academy/reference/mathacademy/mathematical-corrections/e-21715/review.json) |
| q-127043 | 1539 | problem, worked_solution | [review](/home/jake/Developer/Course_Academy/reference/mathacademy/mathematical-corrections/q-127043/review.json) |
| q-72005 | 1629 | problem, worked_solution | [review](/home/jake/Developer/Course_Academy/reference/mathacademy/mathematical-corrections/q-72005/prior-correction-basis-1629/review.json) |
| q-72005 | 1633 | problem, worked_solution | [review](/home/jake/Developer/Course_Academy/reference/mathacademy/mathematical-corrections/q-72005/review.json) |
| q-36371 | 1643 | worked_solution | [review](/home/jake/Developer/Course_Academy/reference/mathacademy/mathematical-corrections/q-36371/review.json) |
| q-339239 | 1694 | problem, worked_solution, answer_fields | [review](/home/jake/Developer/Course_Academy/reference/mathacademy/mathematical-corrections/q-339239/review.json) |
| q-128339 | 1720 | problem, worked_solution, answer_fields | [review](/home/jake/Developer/Course_Academy/reference/mathacademy/mathematical-corrections/q-128339/review.json) |
| q-128340 | 1721 | problem, worked_solution | [review](/home/jake/Developer/Course_Academy/reference/mathacademy/mathematical-corrections/q-128340/review.json) |
| q-72175 | 1728 | worked_solution, answer_fields | [review](/home/jake/Developer/Course_Academy/reference/mathacademy/mathematical-corrections/q-72175/review.json) |
| e-6099 | 1729 | worked_solution | [review](/home/jake/Developer/Course_Academy/reference/mathacademy/mathematical-corrections/e-6099/review.json) |
| e-10897 | 1733 | worked_solution | [review](/home/jake/Developer/Course_Academy/reference/mathacademy/mathematical-corrections/e-10897/versions/v1/review.json) |
| e-10911 | 1735 | worked_solution | [review](/home/jake/Developer/Course_Academy/reference/mathacademy/mathematical-corrections/e-10911/versions/v1/review.json) |
| e-10897 | 1737 | worked_solution | [review](/home/jake/Developer/Course_Academy/reference/mathacademy/mathematical-corrections/e-10897/review.json) |
| e-10911 | 1739 | worked_solution | [review](/home/jake/Developer/Course_Academy/reference/mathacademy/mathematical-corrections/e-10911/review.json) |
| e-6996 | 1745 | problem, worked_solution | [review](/home/jake/Developer/Course_Academy/reference/mathacademy/mathematical-corrections/e-6996/review.json) |
| q-80266 | 1745 | problem, worked_solution | [review](/home/jake/Developer/Course_Academy/reference/mathacademy/mathematical-corrections/q-80266/review.json) |
| q-86860 | 1745 | problem, worked_solution | [review](/home/jake/Developer/Course_Academy/reference/mathacademy/mathematical-corrections/q-86860/review.json) |
| q-86861 | 1745 | problem, worked_solution | [review](/home/jake/Developer/Course_Academy/reference/mathacademy/mathematical-corrections/q-86861/review.json) |
| q-129658 | 1799 | problem, worked_solution | [review](/home/jake/Developer/Course_Academy/reference/mathacademy/mathematical-corrections/q-129658/prior-correction-basis-1799/review.json) |
| q-129662 | 1799 | problem, worked_solution | [review](/home/jake/Developer/Course_Academy/reference/mathacademy/mathematical-corrections/q-129662/review.json) |
| q-129666 | 1799 | problem, worked_solution | [review](/home/jake/Developer/Course_Academy/reference/mathacademy/mathematical-corrections/q-129666/review.json) |
| q-80430 | 1799 | problem, worked_solution | [review](/home/jake/Developer/Course_Academy/reference/mathacademy/mathematical-corrections/q-80430/review.json) |
| q-80503 | 1799 | problem, worked_solution | [review](/home/jake/Developer/Course_Academy/reference/mathacademy/mathematical-corrections/q-80503/review.json) |
| q-129658 | 1801 | problem, worked_solution | [review](/home/jake/Developer/Course_Academy/reference/mathacademy/mathematical-corrections/q-129658/review.json) |
| q-334452 | 1806 | problem, worked_solution | [review](/home/jake/Developer/Course_Academy/reference/mathacademy/mathematical-corrections/q-334452/review.json) |
| q-334265 | 1808 | worked_solution | [review](/home/jake/Developer/Course_Academy/reference/mathacademy/mathematical-corrections/q-334265/review.json) |
| q-124871 | 1883 | worked_solution, answer_fields | [review](/home/jake/Developer/Course_Academy/reference/mathacademy/mathematical-corrections/q-124871/review.json) |
| q-140043 | 1920 | worked_solution | [review](/home/jake/Developer/Course_Academy/reference/mathacademy/mathematical-corrections/q-140043/review.json) |
| q-337721 | 1925 | problem, worked_solution | [review](/home/jake/Developer/Course_Academy/reference/mathacademy/mathematical-corrections/q-337721/review.json) |
| e-21717 | 1926 | problem, worked_solution | [review](/home/jake/Developer/Course_Academy/reference/mathacademy/mathematical-corrections/e-21717/review.json) |
| q-125585 | 1937 | problem, worked_solution | [review](/home/jake/Developer/Course_Academy/reference/mathacademy/mathematical-corrections/q-125585/review.json) |
| q-125457 | 1938 | problem, worked_solution | [review](/home/jake/Developer/Course_Academy/reference/mathacademy/mathematical-corrections/q-125457/review.json) |
| q-125485 | 1940 | problem, worked_solution, answer_fields | [review](/home/jake/Developer/Course_Academy/reference/mathacademy/mathematical-corrections/q-125485/review.json) |
| q-41811 | 1969 | problem, worked_solution | [review](/home/jake/Developer/Course_Academy/reference/mathacademy/mathematical-corrections/q-41811/review.json) |
| e-21849 | 1994 | problem, worked_solution | [review](/home/jake/Developer/Course_Academy/reference/mathacademy/mathematical-corrections/e-21849/review.json) |
| q-342644 | 1995 | problem, worked_solution, answer_fields | [review](/home/jake/Developer/Course_Academy/reference/mathacademy/mathematical-corrections/q-342644/version-1/review.json) |
| q-342644 | 1996 | problem, worked_solution, answer_fields | [review](/home/jake/Developer/Course_Academy/reference/mathacademy/mathematical-corrections/q-342644/review.json) |
| q-161496 | 2020 | problem, worked_solution, answer_fields | [review](/home/jake/Developer/Course_Academy/reference/mathacademy/mathematical-corrections/q-161496/review.json) |
| q-161495 | 2021 | problem, worked_solution | [review](/home/jake/Developer/Course_Academy/reference/mathacademy/mathematical-corrections/q-161495/review.json) |
| q-161490 | 2022 | worked_solution | [review](/home/jake/Developer/Course_Academy/reference/mathacademy/mathematical-corrections/q-161490/review.json) |
| q-161516 | 2023 | worked_solution | [review](/home/jake/Developer/Course_Academy/reference/mathacademy/mathematical-corrections/q-161516/review.json) |
| e-7224 | 2041 | worked_solution | [review](/home/jake/Developer/Course_Academy/reference/mathacademy/mathematical-corrections/e-7224/review.json) |
| e-7225 | 2041 | worked_solution | [review](/home/jake/Developer/Course_Academy/reference/mathacademy/mathematical-corrections/e-7225/review.json) |
| q-31671 | 2041 | worked_solution, answer_fields | [review](/home/jake/Developer/Course_Academy/reference/mathacademy/mathematical-corrections/q-31671/review.json) |
| q-31674 | 2041 | worked_solution, answer_fields | [review](/home/jake/Developer/Course_Academy/reference/mathacademy/mathematical-corrections/q-31674/review.json) |
| q-31683 | 2041 | worked_solution, answer_fields | [review](/home/jake/Developer/Course_Academy/reference/mathacademy/mathematical-corrections/q-31683/review.json) |
| q-351408 | 2041 | problem, worked_solution | [review](/home/jake/Developer/Course_Academy/reference/mathacademy/mathematical-corrections/q-351408/review.json) |
| q-82336 | 2041 | worked_solution, answer_fields | [review](/home/jake/Developer/Course_Academy/reference/mathacademy/mathematical-corrections/q-82336/review.json) |
| q-82337 | 2041 | worked_solution, answer_fields | [review](/home/jake/Developer/Course_Academy/reference/mathacademy/mathematical-corrections/q-82337/review.json) |
| q-88686 | 2073 | problem, worked_solution, answer_fields | [review](/home/jake/Developer/Course_Academy/reference/mathacademy/mathematical-corrections/q-88686/review.json) |
| q-115278 | 2075 | problem, worked_solution | [review](/home/jake/Developer/Course_Academy/reference/mathacademy/mathematical-corrections/q-115278/review.json) |
| e-10898 | 2079 | problem, worked_solution | [review](/home/jake/Developer/Course_Academy/reference/mathacademy/mathematical-corrections/e-10898/review.json) |
| q-161729 | 2080 | problem, worked_solution, answer_fields | [review](/home/jake/Developer/Course_Academy/reference/mathacademy/mathematical-corrections/q-161729/review.json) |
| e-11507 | 2081 | worked_solution | [review](/home/jake/Developer/Course_Academy/reference/mathacademy/mathematical-corrections/e-11507/review.json) |
| q-161712 | 2082 | problem, worked_solution | [review](/home/jake/Developer/Course_Academy/reference/mathacademy/mathematical-corrections/q-161712/review.json) |
| q-40503 | 2083 | worked_solution, answer_fields | [review](/home/jake/Developer/Course_Academy/reference/mathacademy/mathematical-corrections/q-40503/review.json) |
| q-40437 | 2084 | problem, worked_solution | [review](/home/jake/Developer/Course_Academy/reference/mathacademy/mathematical-corrections/q-40437/review.json) |
| q-161836 | 2085 | worked_solution | [review](/home/jake/Developer/Course_Academy/reference/mathacademy/mathematical-corrections/q-161836/review.json) |
| q-161659 | 2095 | problem, worked_solution, answer_fields | [review](/home/jake/Developer/Course_Academy/reference/mathacademy/mathematical-corrections/q-161659/review.json) |
| q-161653 | 2097 | worked_solution | [review](/home/jake/Developer/Course_Academy/reference/mathacademy/mathematical-corrections/q-161653/review.json) |
| q-125460 | 2155 | problem, worked_solution | [review](/home/jake/Developer/Course_Academy/reference/mathacademy/mathematical-corrections/q-125460/review.json) |
| q-161286 | 2164 | problem, worked_solution, answer_fields | [review](/home/jake/Developer/Course_Academy/reference/mathacademy/mathematical-corrections/q-161286/review.json) |
| q-161134 | 2165 | problem, worked_solution, answer_fields | [review](/home/jake/Developer/Course_Academy/reference/mathacademy/mathematical-corrections/q-161134/review.json) |
| q-104058 | 2238 | problem, worked_solution, answer_fields | [review](/home/jake/Developer/Course_Academy/reference/mathacademy/mathematical-corrections/q-104058/review.json) |
| q-79710 | 2241 | problem, worked_solution | [review](/home/jake/Developer/Course_Academy/reference/mathacademy/mathematical-corrections/q-79710/review.json) |
| q-161481 | 2265 | problem, worked_solution, answer_fields | [review](/home/jake/Developer/Course_Academy/reference/mathacademy/mathematical-corrections/q-161481/review.json) |
| q-37131 | 2290 | problem, worked_solution, answer_fields | [review](/home/jake/Developer/Course_Academy/reference/mathacademy/mathematical-corrections/q-37131/review.json) |
| q-139969 | 2302 | problem, worked_solution | [review](/home/jake/Developer/Course_Academy/reference/mathacademy/mathematical-corrections/q-139969/review.json) |
| q-125075 | 2331 | problem, worked_solution | [review](/home/jake/Developer/Course_Academy/reference/mathacademy/mathematical-corrections/q-125075/review.json) |
| q-95114 | 2342 | problem, worked_solution | [review](/home/jake/Developer/Course_Academy/reference/mathacademy/mathematical-corrections/q-95114/review.json) |
| q-335465 | 2346 | problem, worked_solution | [review](/home/jake/Developer/Course_Academy/reference/mathacademy/mathematical-corrections/q-335465/review.json) |
| q-132984 | 2368 | problem, worked_solution | [review](/home/jake/Developer/Course_Academy/reference/mathacademy/mathematical-corrections/q-132984/review.json) |
| q-160888 | 2391 | problem, worked_solution | [review](/home/jake/Developer/Course_Academy/reference/mathacademy/mathematical-corrections/q-160888/review.json) |
| q-37083 | 2395 | problem, worked_solution | [review](/home/jake/Developer/Course_Academy/reference/mathacademy/mathematical-corrections/q-37083/review.json) |
| q-36300 | 2396 | problem, worked_solution | [review](/home/jake/Developer/Course_Academy/reference/mathacademy/mathematical-corrections/q-36300/review.json) |
| q-84607 | 2420 | problem, worked_solution | [review](/home/jake/Developer/Course_Academy/reference/mathacademy/mathematical-corrections/q-84607/review.json) |
| q-130486 | 2431 | problem, worked_solution | [review](/home/jake/Developer/Course_Academy/reference/mathacademy/mathematical-corrections/q-130486/review.json) |
| q-332355 | 2432 | problem, worked_solution | [review](/home/jake/Developer/Course_Academy/reference/mathacademy/mathematical-corrections/q-332355/review.json) |
| q-103792 | 2446 | problem, worked_solution | [review](/home/jake/Developer/Course_Academy/reference/mathacademy/mathematical-corrections/q-103792/review.json) |
| q-338921 | 2615 | problem, worked_solution | [review](/home/jake/Developer/Course_Academy/reference/mathacademy/mathematical-corrections/q-338921/review.json) |
| q-335252 | 2693 | problem, worked_solution | [review](/home/jake/Developer/Course_Academy/reference/mathacademy/mathematical-corrections/q-335252/review.json) |
| q-330826 | 2700 | problem, worked_solution | [review](/home/jake/Developer/Course_Academy/reference/mathacademy/mathematical-corrections/q-330826/review.json) |
| q-38980 | 2716 | worked_solution | [review](/home/jake/Developer/Course_Academy/reference/mathacademy/mathematical-corrections/q-38980/review.json) |
| q-340850 | 2740 | problem | [review](/home/jake/Developer/Course_Academy/reference/mathacademy/mathematical-corrections/q-340850/review.json) |
| q-164576 | 2813 | problem, worked_solution | [review](/home/jake/Developer/Course_Academy/reference/mathacademy/mathematical-corrections/q-164576/review.json) |

## Answer-source reconciliations

198 saved replacement decisions for `answer-field/correct` are recorded separately in `answer-reconciliations.json`. These include replacement of locally interpreted or differently formatted answers with MA evidence. They must not all be treated as our mathematical corrections.

The full original and corrected content, rationales, old transaction paths and verification paths are in `correction-events.json`. The mathematical-corrections directory will be preserved alongside this review.
