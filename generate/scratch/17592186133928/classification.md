# Classification — frozen math basis 1356

Provenance: math, basis 1356, lineage `01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1`. `source.json` is the unmodified capture wrapper. Lesson order was followed from `:activity/first-step` through `:step/next`: introduction → circulation over space curves → Green's theorem review → induced orientations → Stokes' theorem → this KP → using Stokes to evaluate line integrals → the sibling line-integral KP. Pull collection order was not used.

This KP converts a supplied surface integral of curl to the boundary circulation. It is not the later sibling task of choosing a surface and integrating over it. The supplied parameterization fixes positive boundary orientation; its induced normal need not point upward. Curl/normal calculations in validation are independent checks, not additional learner tasks.

There are 11 practice prompts with distinct boundary/field/stage structures and 12 complete five-option radio banks, including one duplicate legacy field. Five are observed moderate, five observed hard, and one unrated. No observed easy questions. The unrated trigonometric question gets a separately authored hard assignment for normal generation (π chain factor, three nonzero tangent coordinates). All templates have plot rating **none**: no practice prompt, option, or solution includes an image. Tutorial diagrams belong to the ordered lesson context, not this KP's template assets.

| Template/source | Observed level | Curve/field structure | Banks |
|---|---|---|---:|
| q-161928 | moderate | quadratic/cubic boundary, F=(y,0,x) | 2, duplicate legacy |
| q-162377 | unrated | sin(πt), cos(πt), sin(πt); F=(x,0,y) | 1, missing designation |
| q-162316 | moderate | signed cubic/quadratic boundary, F=(z,0,y) | 1 |
| q-162324 | hard | cos(πt), sin(πt), cos(πt); F=(y,0,x) | 1 |
| q-162886 | moderate | polynomial boundary, cyclic linear field | 1 |
| q-162887 | moderate | polynomial boundary, one bilinear yz component | 1 |
| q-162892 | hard | tilted circle, exp(z−2y) reduces to 1 | 1 |
| q-162889 | hard | horizontal circle, constant and square field components | 1 |
| q-162891 | hard | tilted circle, three coordinate-difference field components | 1 |
| q-162999 | moderate | polynomial boundary, scaled z/y field components | 1 |
| q-162314 | hard | signed polynomial boundary on [−1,0) | 1 |

The canonical example supplies the Stokes-to-circulation route and polynomial expansion. Prerequisites are flux in 3D, Green's theorem, and curl. Authored easy retains exactly the same conversion but uses a horizontal ellipse and F=(−cy,cx,0), two nonzero tangent components and immediate sin²+cos² reduction. Moderate/hard variations retain each source family's workload; no within-level progression or new integration technique is introduced.

## Reclassification at basis 2620

`source-basis-2620.json` retains the current 12 practice questions and 13 radio fields at lineage `01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1`. The original basis-1356 capture is retained unchanged. Five current questions are moderate and seven are hard; there are no observed easy sources. All 12 Markdown/value templates have plot rating **none**. The old q-162377 now has an observed hard label, worked solution and key π; its existing mathematical backbone and bank values are unchanged. Its historical missing-key replay remains an explicitly historical fixture. Source UUID changes and delimiter normalization do not define new mathematical variants.

New template q-162890 is hard: r=(cos t,2 sin t,2 cos t), F=(2z,x,3y), t∈[0,2π). Its five-option bank is {3π/2,2π,−6π,−π/3,−10π}, with −10π correct. All three tangent coordinates and all three linear field components are nonzero. Its cosine/sine dot product has a mixed term and unequal squared terms, followed by double-angle reduction, antiderivative and both endpoint evaluations. This differs from the older two-component field templates. The exact source and full bank are retained in the new capture and raw mask; distractor intent remains opaque. `current-source-validation.json` records each current field, complete bank and independently computed integral. The incomplete first q-161928 duplicate field and four erroneous source solutions are preserved but excluded from validated inventory counts.
