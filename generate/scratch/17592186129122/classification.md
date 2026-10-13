# Step 3 — classification, frozen basis 1356

Database `math`, lineage `01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1`. The capture wrappers are retained unchanged in source.json, topic.json and lesson.json. There are eight practice questions, seven labeled easy and one unrated. Canonical e-15610 is context, not a practice question.

| Source | Template | Original layout | Original label | Angular scale | Bank |
|---|---|---|---|---|---|
| q-43404 | rad_sine_fraction | radio, 5 choices | easy | radians | opaque complete bank |
| q-53457 | rad_cos_fraction | radio, 5 choices, missing key | absent | radians | opaque complete bank |
| q-117580 | rad_cos_integer | answer-fields attribute absent | easy | radians | absent |
| q-117583 | degree_sine_fraction | answer-fields attribute absent | easy | degrees | absent |
| q-117578 | rad_sine_scaled_fraction | radio, 5 choices | easy | radians | opaque complete bank |
| q-117579 | degree_sine_scaled_fraction | radio, 5 choices | easy | degrees | opaque complete bank |
| q-43411 | degree_cos_integer | radio, 5 choices | easy | degrees | opaque complete bank |
| q-81513 | degree_sine_integer | radio, 5 choices | easy | degrees | opaque complete bank |

Eight masks preserve the distinct prompt/function notation and complete solution prose. These are not eight different skills: all identify B and divide the appropriate base period by B. Six complete historical bank profiles remain separate, with all 30 choices retained. Their unrelated scalars do not identify unique underlying error operations. No plots occur in any practice record, prompt, bank or solution; plot rating **none**. Lesson introduction assets do not form part of this assessed algebraic question.

The lesson route follows activity/first-step 17592186129953 and step/next, in order: Introduction → amplitude KP → this period KP → midline KP → range tutorial → range KP. Prerequisite is Horizontal Stretches of Trigonometric Functions (784). The introduction provides the full affine sinusoidal form and demonstrates factoring a coefficient in the argument. The canonical example computes 2π/2. Neighboring KPs assess amplitude, midline and range separately, so generated records request period only and never ask for those properties, graphing, zeros or extrema.

No moderate/hard practice label is present. Authored moderate uses a negative reduced rational B, requiring the positive period 2π/|B| or 360°/|B|; authored hard recovers B from one factored affine argument before applying the same formula. These are design claims, not recovered difficulty ratings. Every question in each level has the same stated reasoning workload, with no instructional progression or mathematical case branching inside a level.

# Anomalies and exclusions from default eligibility

* q-53457 has no difficulty, worked solution or correct designation. Original MA widget in authoritative-widgets.json confirms five-choice multiple choice and the same complete values; it does not supply a stored correct key. Mathematics independently gives B=1/3, T=6π. Public raw replay preserves all three omissions. Normal completion adds a radio key, a worked solution and an explicitly authored easy label.
* q-117580 and q-117583 have no answer-fields attribute. They are absent from the older authoritative MA JSON; this is not evidence of an original widget layout. Raw replay omits the attribute, whereas normal output adds an authored five-option radio bank.
* q-43411's opening says the period of A cos(Bx+C)+D is 360°, omitting division by B. Its subsequent B=8 computation and keyed 45° answer are correct. Raw replay is exact, flagged evidence-only. Normal output makes the minimal opening correction to 360°/B.
* Decoded-string-evidence.json records actual ordinal-92 slash runs. Every present source string has maximum adjacent run 1; absent solution evidence has maximum 0. There is no decoded doubled-slash anomaly and no TeX repair is claimed.
* All six historical banks are evidence-only, including those with complete keys. Their scalar observations alone cannot justify a recovered distractor operation. Normal output uses a separately authored complete bank derived from the period method.
