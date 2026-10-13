# Writing first-order linear ODEs in standard form

Source capture: `reference/source.json`, database math, lineage `01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1`, basis 2006. All nine practice questions, both fields of q-16400, and the canonical example were pulled together. Available inventory at that basis: easy 6, hard 1, moderate 0. Canonical examples never count as available practice.

| Difficulty | Practice sources | Complete field layout | Templates | New plots |
| --- | --- | --- | --- | --- |
| Easy | q-16400, q-8359, q-103349, q-103354, q-16396, q-79697, q-79699, q-8360 | One radio `selection`, five mathematical equations | 8 | none, each template |
| Hard | q-16401 | One radio `selection`, five mathematical equations | 1 | none |
| Moderate | None | No observed field/layout | 0 | none |

Every template has its own complete source bank profile, named by source ID. q-16400 additionally has a duplicate `selection` field without a correct reference. Its values are retained as evidence and checked against the complete profile, but this malformed field is not reproduced in gradable output. No source field, question, or learner record is changed.

Easy templates respectively require rearranging a trig equation and dividing a constant, collecting a rational coefficient, dividing an exponential coefficient, dividing a trig coefficient and simplifying sin(2x), canceling a nonzero dependent factor, clearing a rational derivative coefficient, canceling a nonzero dependent factor and exponential coefficient, and rearranging cotangent terms. Hard expands a square, cancels the quadratic terms, and collects the remaining linear term. These different solution sequences remain separate templates even where the resulting normalized equations overlap.

The canonical example rearranges y' + y sin(x) - cos(x) = 0. The captured lesson narrative (`generate/runs/current/lessons/17592186050608.json`, historical basis 1356) teaches division by the derivative coefficient and recognition of P(x), Q(x). The prerequisite is Introduction to Differential Equations. Generated questions do not solve the ODE or introduce integrating factors.

Moderate is unsupported by this frozen package: the nine rated practice sources and the canonical example do not establish a separate moderate workload or response layout. The bounded classification examines all current source practice questions and the captured lesson context; it does not prove that no moderate template could ever be authored. New source evidence reopens classification. Moderate availability remains zero and is not called filled.

All observed easy and hard templates are implemented. Positive integer coefficient/frequency bounds are documented sampling extensions, preserving the source algebra and workload rather than claiming recovered sampling rules. No negative source parameters were observed. Changing frequency inside a trig or exponential function creates a different mathematical coefficient. Common equation/dependent scaling, choice order, seeds, UUIDs and alternative rearrangements are excluded by semantic deduplication.
