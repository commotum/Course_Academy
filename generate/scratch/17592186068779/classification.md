# Classification at math basis 1356

Provenance: database `math`, basis `1356`, lineage `01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1`. `source.json` is the complete unchanged capture wrapper.

| Captured level | Questions | Response | Presentation templates | Plot rating |
|---|---:|---|---:|---|
| easy | 0 | Authored five-image radio | 2 authored translation orientations | heavy |
| moderate | 4 | Five-image radio | 2: scaling then vertical translation, either three solution images or final image only | heavy |
| hard | 4 | Five-image radio | 1: horizontal translation then scaling, three solution images | heavy |
| unrated | 2 | Five-image radio; missing correct designation and solution | 2: horizontal shifted negative integer reciprocal and vertically shifted negative fractional reciprocal | heavy |

The API exposes two mathematical family names, `horizontal_then_scale` and `scale_then_vertical`. Full presentation masks and banks are selected by profile; it does not conflate the final-only source layout with the three-image layout. Each of the ten observed banks has a public `raw:q-N` profile. Nine geometrically defensible banks also have normal `normal:q-N` profiles. The remaining opaque bank is evidence-only. All source radio fields use `selection` and image answers, with five choices; no feedback is present.

Source IDs and exact parameters, including the authored routing assignment for unrated questions, are in `source-cases.json`. The horizontal unrated source is assigned hard for dispatch because it has the same denominator-translation-plus-scale demand as the four rated hard questions. The vertical unrated source is assigned moderate for the corresponding two-stage vertical demand. Those assignments never create a difficulty attribute in raw replay.

## Scope and missing-level design

The lesson route, reconstructed from first-step/next links, is introduction → stretch below one → stretched reciprocal KP → negative stretch tutorial → stretched negative reciprocal KP → this transformed-reciprocal KP → solving unknowns from a graph. The prerequisite is Graph Transformations of Reciprocal Functions (topic3735). The canonical example combines a negative unit curve, horizontal translation, scale2, and vertical translation. The next sibling asks for unknown coefficients from a given graph; this generator never asks that question.

Authored easy questions use a signed **unit** reciprocal and exactly one nonzero integer translation. Positive/negative sign recognition is assumed from the prerequisite and earlier lesson route. They assess one transformation rather than the observed moderate/hard two transformations. Both horizontal and vertical orientations have equal workload; neither requires solving unknown parameters. Easy excludes all nonunit scales; moderate requires a nonunit familiar reduced scale and a vertical translation; hard requires the same scale workload and a horizontal translation. All shifts have magnitude1–4. Scale magnitudes are the distinct reduced n/q with 1≤n,q≤5 and n≠q, with either sign. These bounds retain the observed integer and familiar fraction number forms and yield 32 easy, 288 moderate, and 288 hard substantive tasks. Bank profiles, source IDs, sign spelling, option order, and seeds do not inflate these counts.

## Anomalies

Two unrated records omit difficulty, correct references, and worked solutions. Raw replay retains all three omissions. Completed normal records infer the unique correct graph from the printed equation and visible asymptotes/points and provide an explicitly authored worked solution. For q-16508 this is original option4 (x=-1, marked(-2,2),(0,-2)); for q-98003 this is original option1 (y=1, marked(-1,1.5),(1,0.5)). These are new mathematical designations, not matched original designations.

q-113372 and q-113369 have stale opening formulas ending +1 while prompts/final stages end +3 and +2, respectively. These strings remain raw-exact evidence. Normal output corrects the complete opening equation. q-98017 has “1 units”; normal output uses the singular.

q-113372's fifth graph has vertical asymptote x=-3 and no marked horizontal asymptote. Its source marker labels (-2.2,3),(-3.8,-7) imply a horizontal asymptote -2 within the reciprocal family; the actual curve/markers are symmetric about the drawn y=0 axis. The y labels and curve disagree. A y=4/(x+3) geometric model fits the raster when choosing a y-scale, but the coefficient/y-scale are not uniquely recoverable from coherent visible data. We do not claim that formula as recovered source truth. It is certainly incorrect for the prompt's x=0 vertical asymptote, and distinct from every other choice by its x=-3 asymptote. The complete bank remains public exact raw evidence; its parameterized geometric continuation remains ineligible. Normal q-113372-style questions use the separately authored method bank.
