# Classification

Database `math`, basis **1356**, lineage `01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1`. `source.json` is the captured wrapper, unchanged. Owning topic is 17592186050482 / MA4132, “Computing Double Integrals Using a Change of Variables”. The linked lesson route is Introduction → Performing a Change of Variables → this KP → Cases When the Transformation Is Inferred From the Integrand, reconstructed from activity/first-step and step/next. This KP must infer coordinates from inequalities; it neither supplies the substitution (previous KP) nor reconstructs a quadrilateral from integrand/vertices (next KP).

| Source | Rating | Template | Field layout | Complete banks | Plot rating |
|---|---|---|---|---|---|
| q-38377 / 17592186198951 | moderate | arctan | two legacy same-key five-option radios, one missing correct | 2 | none |
| q-82916 / 17592186199007 | absent | gaussian | one five-option radio, missing correct and solution | 1 | none |
| q-160911 / 17592186373930 | moderate | linear_exp | one five-option radio | 1 | none |
| q-160919 / 17592186373937 | moderate | radical | one five-option radio | 1 | none |
| q-160920 / 17592186373944 | moderate | quadratic_exp | one five-option radio | 1 | none |
| q-83651 / 17592186375516 | moderate | sine | one five-option radio | 1 | none |

Five observed moderate templates plus one unrated family: six mathematical/prompt/solution families, seven captured field banks, 35 displayed choice occurrences. All six sources are retained in public API source replay. q82916 is explicitly assigned moderate only in authored normal completion; raw replay preserves the absent rating, correct ref and solution.

Canonical e12327 uses u=y−x,v=x+y, a nonunit Jacobian, rectangle bounds, separated polynomial/log integration. The curriculum presupposes partial derivatives, determinants, inverse transformations and elementary one-variable integration. Easy is an authored reduction: unit triangular linear map, zero lower limits, and a linear transformed integrand. Hard is an authored equal-method extension: nonunit triangular map with four nonzero endpoint evaluations; nonlinear radical hard uses asymmetric positive endpoints rather than the observed symmetry shortcut. These are design claims, not recovered MA difficulty labels. Every hard family stays in domain-inferred rectangularization and uses the same elementary primitive as its moderate family. No integration by parts, new branches, singular domains, multivalued maps, or vertex reconstruction.

All observed banks are retained as explicit **ineligible evidence** profiles. Single observed scalar wrong values often underdetermine their origin. Homogeneous integrand scaling k∈{1,2,3} scales the complete historical bank and solution equality sides; it reproduces evidence without claiming historical error intent. Default questions use separately authored complete method banks. Their errors operate on actual missing Jacobian factors, incorrect primitive inputs, omitted/reversed endpoints, dropped quartic terms, or upper-rectangle evaluation. An entire instance is rejected on any bank equivalence.

Source-format findings: q38377's authoritative MA4132 captured widget is one five-option radio, confirming the first EDB field is a duplicate legacy artifact. q82916 is likewise one five-option radio. The mathematical correct value is e−1, independently derived; missing designation is not counted as matched. q160911 has two stale outer `dv` differentials where `du` is required; normal output corrects them, raw evidence remains exact. No practice question contains plots. The canonical's two full-resolution raster images show only forward/inverse column-map notation and require no plotting.
