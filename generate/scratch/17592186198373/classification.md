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

Bounded variety: authored easy uses u∈[0,b],v∈[0,d] with b≤8,d≤6 and a single linear primitive. Familiar squares are at most36, followed by one width product; the complete method-bank eligibility leaves30 mathematical tasks. Hard radical uses u lower endpoints1 or2, upper endpoints through5, and asymmetric v intervals [1,2], [1,3], [2,3], with R∈{9,16,25} and R>d²; this supplies49 eligible tasks, all with the same quartic expansion and cubic/quintic primitive operations. Moderate sampling includes observed R=4, u upper1, Gaussian x upper5 and signed exponential bounds. These bounds are authored same-method policies, not recovered source-generator code.

The captured topic predecessor (`:topic/_next`) is MA1998, “Computing Areas Using a Change of Variables” (db17592186050705), providing the transformation/Jacobian prerequisite anchor; the lesson introduction explicitly extends its area formula by inserting the transformed integrand.

## Current inventory audit, basis 2589

`reference/replenishment/initial/kp.edn` captures all 12 current practice questions at one basis. The original six have since received format/field/completion repairs in the database; this package preserves both its original basis-1356 evidence and the new capture. `initial/source-audit.json` retains every current prompt, full worked solution, complete five-value bank, designation, independently computed integral, and mathematical task identity. All 12 current fields are moderate, single-key five-option math radios; none requires plots. Eleven mathematical keys are correct; nine questions pass the conservative source-solution eligibility audit. Actual native grading is checked again during preparation. No source repair is part of this job.

Six additional moderate templates are now visible:

| Source / database ID | Backbone | Plot rating | Generator capability |
|---|---|---|---|
| q-83653 / 17592186481389 | Infer u=y−2x,v=y; separate ln(u)/u, square-log primitive and v width | none | Evidence only; not sampled |
| q-38309 / 17592186481418 | Infer u=y−x,v=y; v cos²(u), half-angle identity then two primitives | none | Evidence only; Step 1 sign typo excludes source from usable count |
| q-160918 / 17592186481432 | Infer u=x+y,v=x−y; factor square then u² exp(v), determinant −2 | none | Evidence only; not sampled |
| q-160916 / 17592186481434 | Infer u=y−x,v=x+y; cos(u) sin(v), determinant −2, two trig primitives | none | Evidence only; not sampled |
| q-160917 / 17592186495059 | Infer u=y−2x,v=y+2x; u/v, determinant −4, positive-denominator logarithm | none | Evidence only; not sampled |
| q-160915 / 17592186495100 | Infer u=xy,v=y/x; two region branches, v sin(πu)/2 per branch | none | Unsupported source key: actual full-domain integral −24/π; source gives −12/π |

These remain separate Markdown/value templates and separate observed bank profiles. Their 30 current choice occurrences are recorded exactly and normalized mathematically in the source audit; no inferred wrong-answer recipes are claimed. This job reuses the already validated normal generator's six families plus authored easy reduction and authored hard bookkeeping policies. It does not declare coverage of the six newly observed families. This bounded template scope leaves all three difficulty bands supported, and sufficient distinct validated variants exist for the current shortage. A future request for these extra families requires extraction and full bank replay before sampling them.

The current q-160911 source still has two stale outer differentials; it is conservatively excluded from the count. q-38309 has a wrong lower endpoint in Step 1; q-160915 is noninjective on its full stated domain and omits a branch. All three remain unchanged in EDB. The original generator's corrected, one-to-one normal families are unaffected by these source defects.
