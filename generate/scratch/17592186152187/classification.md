# Classification

Snapshot: math basis 1356, lineage `01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1`. `source.json` copies the entire capture wrapper. No database operations.

| Captured level | Practice questions | Assessment/layout | Families | Plot requirement |
|---|---:|---|---:|---|
| easy | 5 | one five-option radio | 1: graph → parametrization/locus | heavy: the graph supplies the radii |
| moderate | 7 | five five-option radios; two questions with two component blanks | 2: supplied radii + traversal radio; supplied radii + traversal construction | moderate: point/direction are illustrated; radii are also in prose |
| absent | 1 | five-option radio with absent correct designation and absent worked solution | graph family | heavy |
| hard | 0 | authored radio or original two-component blank layout | graph reading + traversal | heavy |

All 13 practice questions are included. Source masks and complete field-owned banks are in `recipes.json`; source-to-profile routing is in `source-cases.json`. There are 16 captured fields: 12 complete radio banks (60 choices) and four component blanks (four values). q-15856 contains two legacy-equivalent radio fields with the same key. Its first field has no correct ref. The original lesson widget (`/home/jake/Developer/MA/DATA/Lessons/2746/Source/2746.json`, question_id 15856) shows exactly one five-choice widget. Normal output therefore uses the authoritative second field; public `observed:q-15856` preserves both original fields and correct-ref presence.

q-15803 has no difficulty, solution or correct ref. Public raw replay omits all three attributes; normal completion assigns easy and derives the correct `x=3 cos θ, y=5 sin θ` from its inspected graph. That inference is not a matched captured designation. q-106701's last wrong pair has `x=4 cos θ, y=8 sin θ` even though a=7,b=4. Its pattern `b,a+1` is an opaque replay operation, not a recovered learner error. That complete historical bank is evidence-only; normal graph generation uses the separate fully method-derived banks from the other graph sources.

The owning lesson route is Introduction → this KP → translated-ellipse parametrization → partial-ellipse parametrization → Cartesian conversion, following first-step/next links (not collection order). This generator stops within the first KP. Prerequisites are Introduction to Ellipses and Parametric Equations of Circles.

Authored hard asks for the same complete origin-centered ellipse and the same [0,2π), rightmost start and counterclockwise traversal. It additionally requires reading unlabeled intercepts against half-unit ticks with even integers labeled, rather than copying prose radii. At least one semiaxis must be a noninteger half-integer; both lie in [2,9]. Easy uses labeled integer graph intercepts; moderate provides integer radii in prose. These different information and graph-reading workloads prevent identical easy/moderate/hard defaults. No Cartesian elimination, translation, subarc-domain calculation or new angular/frequency branch is introduced.

Repeated-practice domains contain 56 ordered unequal integer radius pairs each for easy and moderate, and 154 ordered half-unit pairs for hard after excluding all-integer pairs. Point-label aliases, bank profiles and field layouts do not inflate those counts. Both sampling and explicit generation enforce the same bounds. All normal banks are selected before parameters; a collision/ambiguous instance rejects the entire bank rather than replacing an option.

## Current-source reconciliation, basis 2733

The live pool now has 17 source practice questions: six rated easy, ten rated moderate, and one unrated. Native fresh inventory is 6 easy, 9 moderate, 0 hard; validated fresh inventory differs from the full source pool. Four later imports extend the existing families without adding a mathematical operation or response shape. All sources are captured together in `source.json` at basis 2733; the original basis-1356 wrapper remains in `reference/source-basis-1356.json`.

- q-326264: construct, a=6, b=5, marked rightmost H(6,0); two component blanks.
- q-326265: construct, a=10, b=4, marked rightmost I(10,0); two component blanks. Raw replay accepts radius 10. Normal sampling remains bounded to 2..9; this narrower policy is explicit.
- q-6890: graph, a=2, b=3; one five-option radio. Full bank: (a,b), (b,a), (a²,b²), (b²,a²), (2a,2b), all in cos/sin order. The doubled pair is distinct from the squared and swapped pairs throughout the unequal-axis sampling domain.
- q-79283: traversal, a=3, b=5, A(3,0); one five-option radio. Full bank: b sin/a cos; a sin/b cos; a cos/b sin (correct); b cos/a sin; a² sin/b² cos.

The four source plots were inspected at their stored image paths. H and I are cosmetic aliases of the same rightmost start, and the whole alias is substituted with the numerical coordinates. These aliases do not expand the meaningful variant count. No live source questions, fields, answers, or historical learner data are repaired or overwritten. Complete source banks and prompt/solution formatting are replayed before output can be committed.

`origin-ellipse-v8` adds these four raw profiles and normal complete banks. The replay validator now covers 22 fields/banks and 78 values, including the preserved legacy duplicate and absent designations. The authored hard level retains the existing bounded half-unit graph-reading workload and has no captured rated hard example. Its support is based on the documented same-method derivation, exact independent mathematics, actual learner grading, and rendered-plot checks.
