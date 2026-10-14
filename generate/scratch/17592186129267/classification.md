# Classification

Capture: database `math`, basis **1356**, lineage `01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1`. Raw wrapper is `source.json`; owning topic 17592186050343 (MA 2059) is `topic.json`; lesson wrapper is `lesson.json`. All eight practice sources are covered. Canonical e-11470 is context, not a ninth practice question.

| Level | Templates | Sources | Fields | Plot requirement |
|---|---:|---|---|---|
| easy observed | 4 | q-39481, q-161605, q-161607, q-161604 | radio, five choices (q-39481 has two legacy fields) | moderate: projection recreated with parameters |
| moderate observed | 3 | q-161611, q-161612, q-161613 | radio, five choices | moderate |
| unrated | 1 | q-161520 | radio, five choices; missing correct and solution | moderate; authored moderate placement |
| hard authored | 1 | quarter_zdifference | radio, five choices | moderate |

Different integrands, region restrictions and operative chains retain separate templates. These are independent questions within a level, not a staged progression. Every observed field/bank is preserved in public `observed:<source-id>` profiles, including duplicate-key fields and absent attributes. Their evidence-only flag prevents treating malformed records as normal practice.

`route.json` follows `:activity/first-step` and `:step/next`: Introduction → this KP → shifted cylindrical solid → evaluation by conversion → Cartesian volume element → cylindrical volume element. Pull array order was not used. Prerequisites are double integrals in plane polar coordinates (2030) and cylindrical coordinates (1981). Sibling KP boundaries exclude shifted cylinders and integral evaluation. Hard is an authored workload claim: quadrant bookkeeping, a z-weighted difference-square identity, and conversion of two nonconstant heights together, using only the already observed operations. Moderate has either the difference identity/half disk or quadrant with unchanged integrand; hard guards preserve its extra combined demands. q-161520 is authored moderate because half-disk angular bounds, xz substitution and a sloping height match the canonical workload.

Source anomalies: q-161520 lacks rating, solution and correct ref and has flattened superscripts; q-39481 has duplicate `selection` fields, a legacy field without correct ref and flattened superscripts; q-161607 begins its final aligned chain with 1/sqrt(z) although the prompt is 1/sqrt(1+z); q-161612 includes an extra r in its expanded middle row. Several source region-set braces are literal unescaped braces; normal output minimally escapes them. None is silently normalized in raw replay. Exact source-bank strings, mathematical interpretation and repaired normal presentation have separate validation denominators.
