# Classification at math basis 1356

KP 17592186152189, `6d82541c-40ca-5df9-aa17-c20b201fadd4`, **The Parametric Equations of an Ellipse Centered at a General Point**. Topic 17592186049672 / MA 2746. Snapshot lineage `01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1` is preserved in source.json.

The source has **15 practice questions: 5 moderate, 9 hard, 1 unrated**. There are 19 captured fields, including the duplicate historical field at q-78680. Plot rating is **heavy** for graph recognition at moderate and **moderate** for the supplied-data hard questions. No plotted answer options occur. Easy is absent and is an authored extension with plot rating none.

| Level | Assessment family | Fields | Sources / masks |
|---|---|---|---|
| Unrated | Read center/radii from graph; choose ellipse locus | One radio, no correct ref | q-78679; public replay omits difficulty and worked solution |
| Moderate | Read center/radii from graph; choose ellipse locus | One five-choice radio | q-106704, q-106706, q-79285, q-79286, q-79287 |
| Hard | Given center/radii, choose rightmost-start CCW parametrization | One five-choice radio, except q-78680 duplicate legacy layout | q-78680, q-106398, q-106399, q-79289, q-79290, q-79292 |
| Hard | Given center/radii, construct rightmost-start CCW parametrization | Two expression blanks, keyed field-1=x and field-2=y; source collection order preserved | q-274862, q-327171, q-327172 |
| Easy authored | Given center/radii, choose ellipse locus | One five-choice radio | Supplied-data direct substitution, without traversal criterion |

Three broad mathematical families have small presentation variants: source Unicode versus TeX theta; unit coefficient omission; zero horizontal shift and trailing whitespace; spaces/newlines around blank placeholders. `specs.json` preserves one exact mask per source so these variations are independently replayed. Each radio source has a complete five-operation bank; the duplicate q-78680 has two independent banks. Every observed choice is mapped in template-extraction.md and specs.json.

## Scope and curriculum

The linked lesson route is 17592186153102 (introduction) → 17592186153103 (origin ellipse) → 17592186153105 (**this KP**) → 17592186153106 (parts of an ellipse) → 17592186153104 (Cartesian equation). This follows first-step/next, not collection order. The introduction explicitly gives origin-centered $x=a\cos\theta,y=b\sin\theta$ and rightmost-start counterclockwise traversal. The current canonical e-6816 adds the two center coordinates. Topic predecessors are general-center Cartesian ellipses and parametric circles. Their supplied-center/radius recognition and translation bookkeeping anchor the authored easy workload.

All levels use positive integer semiaxes 1–8, distinct horizontal/vertical radii, integer center coordinates −6–6 with center not at the origin. The source has these same integer number forms, one unit semiaxis, both signs of shifts, and a zero horizontal shift. Broadening center values only preserves addition/subtraction; no radicals, rotations, frequency multipliers, phase offsets, restricted domains, or Cartesian elimination are introduced. The same radius/center arithmetic ceiling applies to explicit and sampled normal inputs. Easy needs supplied-parameter substitution; moderate additionally reads four quantities from axes/guides; hard additionally applies the starting-point and traversal criterion (and constructs two expressions in the blank layout). Hard's stated information does not force graph reconstruction; this follows the observed labels rather than inventing a numerical progression.

Normal easy and moderate use the same locus bank operations but have different assessed information. Normal hard supports both observed response layouts and a bank with sine/cosine interchanges that preserve the Cartesian locus but violate rightmost-start/CCW requirements. Correctness therefore cannot be tested by Cartesian locus equality alone.

## Source anomalies

q-78679 omits difficulty, correct designation, and worked solution. Its raster identifies center (2,1), a=4,b=2, so the unique eligible option is x=4cosθ+2,y=2sinθ+1. This is an independently derived answer, **not** a matched captured designation. It is assigned moderate only as an authored analysis/design claim; public raw replay omits the original absent attributes.

q-78680 has two fields with the same selection key. The first is ungraded legacy data; the second contains the correct ref and matches the authoritative captured MA widget. The original lesson JSON `.../Lessons/2746/Source/2746.json`, question_id 78680, shows one five-choice widget, not two simultaneous assessment demands. Raw public replay preserves both historical fields and the first field's absent correct ref. Normal output has one field. The two missing designations are excluded from the exact-designation denominator, not counted as matched. Raw profiles are explicitly evidence-only and never default sampling candidates.

The source strings have ordinary single backslashes after JSON decoding; no escape anomaly or repair is claimed. No mathematical source error was found. Fourteen worked solutions and all source prompt strings replay byte-for-byte. Native trig-shift equivalences remain unresolved in the engine and are reported separately.
