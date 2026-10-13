# Classification — circle center/radius extraction

Captured database `math`, basis **1356**, lineage `01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1`; `source.json` is the unchanged wrapper/record. Eight practice questions are included; canonical e-3226 is context, not counted as practice.

| Level | Observed practice | Fields | Template family | Complete banks | Plot rating |
|---|---:|---|---|---:|---|
| Easy | 7 | one `selection` radio, five text choices | standard-form extraction, with zero-offset and article variants | 7 | none |
| Unrated | 1 (q-7527) | same five-choice radio, missing correct ref | spaced standard form; source omits solution and difficulty | 1 | none |
| Moderate | 0 | authored same radio layout | one fractional coordinate offset | authored whole sign/root bank | none |
| Hard | 0 | authored same radio layout | two fractional offsets plus familiar square-root reduction | authored whole sign/root bank | none |

There is one observed complete instructional template family: compare the circle's standard equation with `(x-a)^2+(y-b)^2=r^2`, interpret both shifts, and take the positive radius. Seven supplied solutions share exactly two displays and a three-row aligned comparison followed by substitution/conclusion prose. The zero-offset family q-117087 conditionally restores `(y-0)^2` in the final comparison row and encloses its radical square with the captured extra grouping braces. q-117084/086 say “and the radius” in the prompt/answers. These are documented rendering variants, not new skills. The separate legacy q-7527 rendering omits the worked solution, difficulty attribute, and correct ref; its raw API output is evidence-only.

All eight complete banks differ; `bank-map.json` maps all 40 values to whole-bank operations. q-7527's extra `S^2` radius is retained, not merged into another profile. The source questions have no plot references anywhere in prompts, banks, or worked solutions, so no plot extraction or renderer is required. Plots in other KPs in the lesson do not imply plot requirements here.

## Curriculum and boundaries

Following `:activity/first-step` and `:step/next` gives tutorial 17592186088461 → construction from center/radius KP 17592186087655 → this extraction KP 17592186087656 → construction from center/point KP 17592186087768 → construction from diameter endpoints KP 17592186087657. Pull array order differs and was not used. The tutorial supplies the generic shifted-circle equation and justifies it by the distance formula. The preceding topic is Equations of Circles Centered at the Origin (842). Completing the square (666), intercepts (844), and circle-line intersections (845) are later topics, as are ellipse and parametric extensions.

This generator only extracts a center and positive radius from an already standard-form circle equation. It supplies no center-point construction, distance/midpoint task, expansion/rearrangement, completing-square task, ellipse coefficient, intercept, or diagram reading.

## Authored difficulty policy

These are design claims, not recovered source difficulty labels. Easy retains the observed integer shifts and square/square-free RHS number forms. All seven observed labels remain easy, including nonsquare examples. Moderate requires exactly one noninteger rational shift and one nonzero integer shift, with a square-free RHS: the extra demand is interpreting a signed fractional center coordinate. Hard requires two noninteger rational shifts and a familiar reducible nonsquare RHS: both coordinates require that interpretation and the radius requires familiar factor extraction. Every instance inside each authored level has these same numerical bookkeeping demands. The supplied source and tutorial equation continue to be the sole method; neither authored level changes the assessed geometric task.

Integer shifts range from -10 to 10, including axis-centered examples but excluding the origin-only prerequisite. Rational shifts are the finite reduced values `n/d` with `d` in {2,3}, `-9 <= n <= 9`, `n != 0`, and `n % d != 0` (22 distinct values, |shift| <= 9/2). Moderate's integer shift is nonzero. Easy RHS values are {2,3,5,6,7,10,11,13} or integer squares from 4 through 100. Moderate uses those eight square-free integers. Hard uses {8,12,18,20,24,27,28,32,45,48,50,63,72,75,80,98}. These are familiar small prime factors and the same radius extraction, extending the lesson's exact square-root number forms. Explicit parameters must satisfy the same reduced-value domains.

There are **7,480** eligible easy mathematical tasks, **7,040** moderate tasks, and **7,744** hard tasks; the counts exclude notation, profile and seed aliases. None of the authored moderate/hard parameter sets overlap each other or easy. The finite domains are intentionally bounded to familiar arithmetic, not claimed infinite.
