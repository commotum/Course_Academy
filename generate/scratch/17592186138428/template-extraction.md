# Four-stage template extraction

## 1. Specific source descriptions

q-171700 begins with a 360×310 PNG, then the shared introduction, a system with two standard equations x+y=1 and 2x+y=4, the request to use the diagram, and “The solution is” followed by two free entries in one coordinate tuple. Both slopes are negative, -1 and -2; the graph crosses at (3,-2). Each numbered blank expects one scalar integer, x then y. The source has no answer bank or solution text.

q-238014 has the same image-first prose/tuple structure, with 4x-y=12 and y=-3x+9. Its first line rises steeply, second falls steeply, and they cross at (3,0) on the x-axis. Its Pull field order is reversed but widget numbered-entry order is unchanged. The second row retains slope-intercept form. No bank or solution text exists.

Canonical e-13129 instead puts its diagram after the request. x+2y=8 and 2x-y=6 meet at (4,2). The fixed solution has the intersection sentence, annotated graph, and the point/therefore sentence. It has no practice blank widget and is not counted as practice coverage.

## 2. Shared pattern

Read a unique intersection of two straight lines on a Cartesian unit grid and supply its ordered pair, using two scalar blanks. The displayed equations identify the drawn lines; algebraic solution is not requested or taught by this question template. Primitive line coefficients and bounds must match the plot, entries, and coordinate sentence.

## 3. Component mapping

| Component | q-171700 | q-238014 | Reusable operation |
|---|---|---|---|
| coordinates | x=3, y=-2 | x=3, y=0 | finite integer coordinate pair |
| slope 1 / slope 2 | -1 / -2 | 4 / -3 | distinct familiar rational slopes |
| first row | x+y=1 | 4x-y=12 | primitive standard form from m1, x, y |
| second row | 2x+y=4 | y=-3x+9 | standard or slope-intercept layout from m2, x, y |
| field-1 | source blank; value absent | source blank; value absent | exact x fragment, independently derived |
| field-2 | source blank; value absent | source blank; value absent | exact y fragment, independently derived |
| full bank | none supplied | none supplied | no distractors; one owned correct answer per blank |
| prompt graphic | af8654…png | 7035e6…png | same row coefficients and unit scales |
| worked solution | absent | absent | canonical complete prose + coordinate guides/marker |

Independent derivations: q-171700 gives (2x+y)-(x+y)=4-1, hence x=3 and y=-2; substitutions yield 3-2=1 and 6-2=4. q-238014 gives 4x-(-3x+9)=12, hence x=3 and y=0; substitutions yield 12-0=12 and 0=-9+9. This derivation is validation evidence, not learner solution content.

## 4. Reusable template

Fixed image-first introduction/request and two-entry tuple reproduce the authoritative practice structure; variable equation rows use complete components. Never blindly replace coefficients across strings. Standard rows use primitive integer coefficients with positive x coefficient; mixed second rows use an integer slope and exact intercept. Source-like spacing is preserved, including `y =-3x + 9`. Optional components are solely the second equation layout. Level bounds apply to explicit parameters and seeded sampling. Invalid inputs raise ValueError; whole instances are never silently changed.

Source replay follows `generate(level, template=..., parameters=..., profile='observed_layout')`, the same renderer and parameter calculations as normal generation. There is no source-return branch or answer table. Profile aliases do not change display or identity. The canonical's entire fixed solution sequence is instantiated; there are no invented distractor diagnoses or grading-dependent explanations. Mathematical metadata, derived-answer origin, difficulty origin and plot data stay outside learner prose.

Parameter fingerprint: unordered primitive standard equations representing both lines plus numbered-major-tick increment and unit-minor-grid increment. These scale conventions determine whether intermediate coordinate reading is required. Content fingerprint: version plus actual displayed prompt, fixed solution and complete two-fragment bank. Question/field/answer UUIDs are stable and field-owned. A source's missing original correct designation never counts as matched.
