# Four extraction stages

## 1. Specific source descriptions

The exhaustive source components are in source.json, source-cases.json, bank-map.json and source-geometry.json. q-43310 uses AB=3, angle30°, area21/4 cm², unknown AC=7. q-43343 uses AB=5, AC=6, area15√3/2 cm², acute angle60°. Both omit rated difficulty, correct designation and worked solution. The owning original MA1275 Markdown confirms these omissions and complete five-option banks.

q-161107: AB=5,60°, area5√3, unknown AC=4; five scalar cm options, whole-radical cancellation. q-161109: AB=6,45°, area21√2/2, AC=7; five cm options, separate radical/denominator cancellation then 3b=21. q-280279: AB=10,120°, area25√3/2, AC=5; field-1 scalar blank, known sine factored before cancellation. q-280282: AB=√3,AC=4, area3 mm²,60°; scalar degree fragment, rationalization with duplicated direction of sine equality. q-365424: AB=8,AC=10, area20√2,45°; scalar degree fragment, no redundant reduced fraction row. q-43328: AB=√2,AC=√6, area√6/2,45°; radio angles, common b/2 cancellation then 1/√2 rationalization. q-43339: AB=5,AC=12, area15,30°; radio angles, product30 then fraction15/30.

Decoded strings contain adjacent ord92 values only for aligned row breaks (maximum run2). Commands have a single decoded slash. No TeX escape repair is claimed from serialized output.

## 2. Generalized shared pattern

Read the two sides adjoining marked A. Use A=½bc sin A. If b is unknown, evaluate the supplied special angle, form the side coefficient and isolate b. If A is unknown, divide twice the area by bc and recognize the acute special angle. The angle branch is limited to30°,45°,60°. Source geometry is schematic; only the included angle A is described as acute in normal prose, rather than making a global triangle claim. Side families also include obtuse120°.

## 3. Components and complete banks

source_chain implements each observed ordered arithmetic mask independently. Formal operator, Here component definitions, sine evaluation (side families), substitution, individual coefficient multiplication, cancellation/reduction, final unit and conclusion remain separate stages. Blocks replace complete mathematical components inside unchanged source prose; no short numeric replacement crosses variable labels or prose. At original parameters all seven present solutions are byte exact.

bank-map.json lists all 33 original values, field ownership, original correct state and raw replay recipe. Raw side profiles apply common geometric dilation s to all side options and s² to area; raw angle profiles keep exact angles fixed while sides/area dilate. This is an evidence parameterization, **not a recovery of historical wrong operations**. Permitted s is½,1,2,3. Raw profiles retain missing metadata and are always ineligible for learning. Missing correct values (7 cm and60°) are independently derived only in completed normal variants, and never counted as matched observed designations.

The authored default side bank is chosen whole before sampling: [b, b/2, bc², c, b/c]. Its four wrong operations are omitting½; multiplying by known c instead of dividing; isolating the already supplied side instead of requested b; dividing by c twice. All are derived directly from ½bc sin A. The special-angle recognition bank is [30°,45°,60°,120°,135°], representing familiar-angle lookup and supplementary-branch errors. The requested acute branch makes only one option eligible. Entire instances are rejected on duplicate/invalid values. Blanks have no distractors.

## 4. Reusable masks and bounds

Public API is generate(level,seed,template,field_type,parameters,profile), with three level entrypoints. Parameters are exactly {b,c,theta,unit}. Explicit invalid parameters are rejected. Completed questions use owned UUID answers and lookup refs; source IDs/provenance and recipe eligibility stay outside learner content. Identity derives from actual prompt, solution, sorted whole bank, level and shape. Seed/option order do not change identity. Mathematical task fingerprints omit unit-letter changes and bank profiles.

Easy authored supplies sin30°=½ in the prompt; positive integral side values2..12 leave one linear isolation. Moderate integer families use sides2..12 and their observed special angle, preserving their exact operation sequence. Radical families independently vary half/integer side multipliers through8 subject to both lengths≤12: q-280282 has28 meaningful side combinations, q-43328 has45. Hard authored keeps the same side-isolation method but both side lengths are reduced nonintegral rationals in[1,12], denominators2,3,4; familiar45°,60°,120°,135° preserve exact trig evaluation. Both the given side and recovered answer are genuinely nonintegral, so no explicit parameter choice can collapse hard to moderate. No branch or progression occurs within any level.

variety.json enumerates actual eligible arithmetic tasks per family, ignoring unit aliases, seed and bank aliases: easy radio108/blank121; moderate families28–121 each; hard radio11792/blank12100. Layout variants are not new mathematics and are not summed as distinct task counts. Scope follows linked lesson order17592186106917 introduction→06918 area KP→06919 this inverse KP→06920 quadrilateral→06921 difference areas→06922 derivation, and the Special Trigonometric Ratios prerequisite. Authored hard expands number forms, not the lesson method. Cross-product topic1299 is the succeeding topic and is excluded.

Normal angle prose specifies the acute included angle only; original public raw prompts remain unchanged. A source prose error occurs in q-280282: “acute triangle” is false as a whole-triangle classification, since cos B has numerator √3−4cos60°=√3−2<0. The intended included angle is acute. Raw evidence is exact; normal prompts specify only acute ∠A, a minimal supported branch clarification. The two omitted designations remain unknown source attributes despite independently identifiable answers.
