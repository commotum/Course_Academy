# Classification

Snapshot: database **math**, basis **1356**, lineage `01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1`. `source.json` copies the complete captured wrapper, including all original fields and answer UUIDs. The authoritative `/home/jake/Developer/MA/DATA/Lessons/1104/Source/1104.json` confirms five-choice multiple-choice widgets for both questions, with no solution, correct label or rating in their captured widgets.

| Observed source | Prompt/value template | Field | Complete bank | Rating | Plot |
|---|---|---|---|---|---|
| q-11376 | named abstract vector, supplied integer magnitude 5 | radio, key selection, five mathematical choices | raw_named | absent | none |
| q-12202 | directed abstract vector AB, supplied integer magnitude 7 | radio, key selection, five mathematical choices | raw_directed | absent | none |

These are two observed wording/notation templates with one bank each; number changes do not create templates. Both lack `:answer-field/correct`, `:question/worked-solution`, and `:question/difficulty`. The raw API reproduces those omissions, and sets `evidence_only=true`, `eligible_for_learning=false` outside the question. It does not fabricate observed labels. Both sources are assigned an **authored easy replay context**, because their supplied positive integer magnitudes require exactly the canonical example's reciprocal scaling operation.

Every normal level is authored, rather than inferred from an observed rating. All use the original radio response layout and five complete choices. The two source wording templates remain supported at every level. The normal whole banks `normalization` and `direction_errors` are authored operation banks; no mixed first-valid distractor pools are used.

## Curriculum scope and level rationale

Follow `:activity/first-step` and `:step/next`: 17592186097737 (Introduction) → 17592186097738 (this KP) → 17592186097739 (unit vector from a diagram) → 17592186097740 (unit vector parallel to a sum). The introduction gives **u=a/|a|** and a magnitude-2 example. This KP's canonical magnitude-3 example divides an already supplied magnitude. Prerequisites are **The Magnitude of a Vector**, topic 1101, and **Parallel Vectors**, topic 1103. The next topic is component form, topic 1165. Accordingly, no generated question asks for coordinates, component calculation, reading a diagram, Pythagorean magnitude calculation, or a vector sum.

| Authored level | Workload at every instance | Exact finite magnitude domain | Meaningful task count |
|---|---|---|---|
| easy | Recognize supplied magnitude and scale by its integer reciprocal | integers 2…30 | 29 |
| moderate | Same normalization, with a reduced noninteger rational magnitude; reciprocal swaps numerator and denominator | p/q, 3≤p≤20, 2≤q≤9, p>q, gcd(p,q)=1 | 72 |
| hard | Same normalization, with supplied noninteger squarefree-radical magnitude; recognize the exact reciprocal, including its equivalent rationalized expression | k√d, k=1…5; d∈{2,3,5,6,7,10,11,13,14,15,17,19} | 60 |

These are bounded arithmetic extensions of the same formal normalization rule, not additional vector skills. Hard does not require the learner to calculate the magnitude or demand a particular rationalized form. The displayed solution shows the supplied magnitude in a reciprocal before simplifying it. There is no ordered progression inside a level. Names and endpoint-letter aliases do not increase mathematical task counts. Banks, layout and random choice ordering also do not increase those counts.

## Source anomalies and correctness

Raw `AB^(→)` is retained in evidence replay, while normal learner output uses `\overrightarrow{AB}`. This is a supported notation presentation repair; the directed endpoints and reversal relation are retained. Raw named `a` becomes canonical bold vector notation in normal output. Decoded canonical strings have zero adjacent backslash pairs; JSON/tool serialization escaping does not establish a TeX escape anomaly. No backslash repair is made or claimed.

Parallel unit vectors can have either orientation: both ±v/m are mathematically eligible under the actual source prompt. The validator checks that full criterion. Each observed and authored bank contains exactly one eligible unit vector when m>1, so no same-direction restriction is needed. `BA=-AB` is accounted for in the entire directed source bank. Missing original correct designations cannot count as matched designations. The unique mathematically inferred value is tracked as metadata, not an original answer key.

The scalar `1/5` option is faithfully preserved as a scalar (not a vector). The observed `a/(2m)` and `a/(4m)` masks in q-11376 reproduce values exactly, but their intended mistakes are underdetermined. They are exposed only in explicitly evidence-only replay profiles. Normal operation banks are separately authored and labeled. No observed teaching prose is invented, no source mathematical option is silently removed, and no raw replay is eligible for learning.
