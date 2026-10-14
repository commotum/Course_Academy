# Four-stage template extraction

## 1. Each original specifically

q-18051: image first; A(-4, 1), B(3, 0); legacy `AB^(→)` and `\mid` request. End-minus-start gives (7,-1), squares49,1, sum50, exact5√2. Five radio values in source order: 5√2,6,5√3,3√2,5. Missing correct ref, difficulty and worked solution. Blue position vectors, no displacement arrow.

q-18052: image first; P(-2, 2), Q(3, 3); legacy `PQ^(→)` and `\mid` request. Displacement (5,1), squares25,1, sum26, √26. Five radio values √27,√23,8,5,√26. Missing correct ref, difficulty and worked solution. Includes P→Q orange displacement.

q-125118: moderate, image first, P(1,2), Q(-2,1), `\overset{\to }{PQ}` magnitude, no answer fields. Displacement(-3,-1), squares9,1, sum10, √10. Three aligned blocks have2/4/3 rows: both position vectors; formal OQ-OP then q-p then substituted vector difference then simplified components; signed squares then evaluated squares then radical. Shared sentences and compact formatting remain parameterized.

q-18049: moderate, image first, C(-1,3), D(1,-2), CD magnitude, no fields. Displacement(2,-5), squares4,25, sum29, √29. Same2/4/3 row backbone, different names and positive-base grouping. No displacement arrow.

q-18055: moderate, image first, picture supplies P/Q coordinates; no fields. Native grid reading independently establishes P(1,1), Q(2,3). Intro explicitly obtains those coordinates before position vectors. Displacement(1,2), squares1,4, sum5, √5. Same2/4/3 block backbone, no arrows in its source plot. Both axes carry signed tick labels; their source pixel units differ.

## 2. Shared mathematical pattern

Supply two actual 2D point positions. Obtain directed displacement by subtracting the first point's position vector from the second. Apply the nonnegative Euclidean norm by squaring both signed components, adding squares and taking the square root. A coordinate prompt and a graph-only prompt retain distinct supplied-information demand. Answer is a scalar magnitude, not a vector or direction.

## 3. Component and complete-bank mapping

`templates.json` records every original answer ID, source field ID/key, exact value, mathematical correct status, profile and parameterized evidence recipe. There are10 values/8 mathematically incorrect values in2 complete banks. Neither original stored a correct designation, so mathematical inference never counts as matched designation. Every original choice remains in its bank. Historical distractor author intent is underdetermined. The only supported evidence extension is homogeneous positive source scaling: endpoints and each complete value become t times their source quantity, t∈{1,2,3,4}. At t=1 the source unsimplified spelling is exact. This is explicitly opaque evidence, never a normal default or recovered error interpretation.

The normal method-derived bank is chosen as a complete profile before sampling. Its five values are: correct √(dx²+dy²); length of the sum of position vectors √((qx+px)²+(qy+py)²); |dx|+|dy| (omit squares/root); dx²+dy² (omit root); √(|dx|+|dy|) (omit squares). All ten pairs are compared under the actual exact scalar response criterion. A collision rejects the whole point pair. Reverse displacement has the SAME norm and is therefore never an incorrect magnitude distractor. No partial pool selection, unrelated numeric fit or learner-facing diagnosis is used.

## 4. Reusable masks and slots

Fixed: supplied endpoints and directed first→second role, 2D Cartesian position subtraction, both nonzero unequal displacement components, scalar magnitude request, source-shaped five-choice radio for authored normal completions, one response-independent worked solution, shared source sentences and ordered formal/substituted/component/square/sum/root stages. Fieldless/raw profiles retain fieldlessness. Source evidence retains exact original notation/spacing/absence; normal records use the same shared sentence masks, with an explicitly authored signed coordinate-subtraction sentence added for reviewable sign arithmetic.

Variable: complete endpoint tuples, dependent position-vector expressions, directed displacement components, individual squares, summed radicand, final exact radical; labels remain fixed by family because changing letters adds no assessed variety. Graph axes/bounds/ticks, marker positions, position-vector arrows and displacement direction derive from those same endpoint slots. Source masks replace complete vector and square components, never partial variables in prose/commands. Graph intro coordinates change with actual plotted points. There is no learner-error-dependent solution.

Allowed slots are in script `DOMAINS`; they apply on public explicit calls. Easy printed endpoints0..6, component differences1..6; moderate signed coordinates-5..5/differences1..8 or graph positive1..4/unit ticks; hard signed graph coordinates-8..8/differences1..12/two-unit ticks and odd intermediate coordinate. Within every band, every task uses the same two mathematical stages. Hard reading is a conservative same-method authored distinction supported by existing graph source and signed-coordinate prerequisite; it is not an observed MA hard label.

Canonical fingerprints retain signed directed displacement, zero/positive/negative subtraction operand categories, level and actual graph-reading tick demand. Common translations that preserve assessed displacement and subtraction signs do not create a new mathematical task. Cosmetic letters, answer order and profile aliases are excluded. Full content identity separately includes actual prompt, fixed solution and complete displayed bank; seed/choice shuffle cannot create identity. SHA256/UUID identities use canonical content, and every answer UUID is owned by its field.

Changed parameters retain the explicit collected radicand `\sqrt{dx²+dy²}` after individually evaluated squares. A conditional terminal simplification row is added only when the exact radical reduces (already required by the source bank 5√2); original three-row norm blocks remain exact at their anchors. This prevents CAS simplification from hiding the square-sum stage.
