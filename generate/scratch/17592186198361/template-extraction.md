# Template extraction

Frozen math snapshot basis 1356, owning topic MA 4132. `source.json` retains all captured fields and raw strings. `templates.json` holds complete expression/bound slots; `build-evidence.py` derives those slots from source strings. No global short-number or variable replacement is used. `source-cases.json` assigns every practice source to its original complete bank and original parameters. `source-analysis.json` records every printed original option and its full scalar value, independently parsed from displayed integrals.

## 1. Specific originals

- **q-38129 / difference:** u=x+y, v=y−x; 0≤u≤3, 0≤v≤2; rewrite y²−x² as a complete iterated integral, order dvdu. Five options; no difficulty, solution or correct designation. The mathematically correct option is (1/2)∫∫uv, whose full value is9/2. The other source full values are−10,9,18,5. The original MA capture confirms the same widget and no captured key. Normal output explicitly authors the missing four-step solution and correct ref at easy.
- **q-38371 / sum_product_evidence:** supplied nonlinear u=xy,v=y+x; evaluate |y−x|e^{xy} over1≤xy≤4,1≤x+y≤10. Five exponential scalar options, no solution/difficulty/key. The image is **not** the rectangle: v²≥4u and v>0. The map has two preimages exchanged by x↔y; the diagonal is critical. The true integral is2∫₁⁴(10−2√u)e^u du, and no displayed option is correct. Its exact value is12e⁴−16e+2√π(erfi2−erfi1). Since the domain width is at least6 and both branches contribute, the true integral exceeds12(e⁴−e), which already exceeds the largest bank option10(e⁴−1); e>2 gives a direct strict inequality. This erroneous historical bank remains public evidence only. Inferring its intended key would be unjustified.
- **ratio_product (rated moderate):** supplied u=y/x²,v=xy; x²≤y≤4x²,1≤xy≤5 implies x,y>0. The inverse map is unique on the positive quadrant. Rewrite xy asv; forward determinant−3y/x², inverse determinant−1/(3u), absolute measure1/(3u); integrate v/u on the rectangle. Full source chain has ten rows, ending8ln2. Five scalar options9/2,11/4,3ln2,6,8ln2. Wrong scalar intentions are underdetermined and not promoted to normal sampling.
- **triangular_quadratic (rated easy):** supplied u=2x+y,v=y; rectangle[0,5]×[0,1]. Solve x=(u−v)/2,y=v. First substitute **both** factors in2xy+x²; then retain the expanded square as uv−v²+(u²−2uv+v²)/4; collect (2uv−3v²+u²)/8. Three operative rows. Source bank's complete values in captured order are−55/4,295/48,1555/96,55/48,−175/16. Each option is mapped in source-analysis.json; no option is silently omitted. Source wrong formulas are captured patterns without confidently recovered intent.
- **product (rated easy):** supplied u=y−x,v=x+y; rectangle[−1,1]×[0,1]. Forward determinant−2, inverse−1/2. Preserve the conjugate product8((v−u)/2)((v+u)/2), reduction2(v²−u²), explicit absolute inverse factor, then iterated integral. Four rows. The correct ∫∫(v²−u²) and the doubled option both have full value0. They are ambiguous answers even though their integrands differ; raw exact replay is ineligible. Other full values32/15,8/3,2/3.
- **exponential (rated easy):** supplied u=2x+5y,v=x+3y; rectangle[0,2]×[0,4]. Forward/inverse determinants1. Solve x=3u−5v,y=2v−u. Keep the uncollected exponent3u−5v+2v−u, collect2u−3v, explicitly substitute|1|, then give du dv bounds. Four rows, five complete integral options.
- **sum_square (rated easy):** supplied u=x+y,v=y−x; rectangle[−1,3]×[−4,−1]. The integrand3(x+y)² becomes3u² directly; preserve omission of redundant x,y inverse-solving rows. Three rows. Source banks contain forward Jacobian, wrong combinedu+v, extra half of that wrong expression, correct, and repeated integrand coefficient. Full values168,78,39,42,126 respectively.

The canonical sine example is scope evidence, not an eighth practice question or recovered practice bank. It requires the same supplied-map, region, determinant, inverse and substitution steps.

## 2. Shared pattern and intended skill

The supplied transformation sends each displayed pair of region inequalities to rectangular u,v bounds. Compute the forward Jacobian, invert it, take its absolute value in the measure, and substitute the integrand. Easy asks for a transformed integral; moderate evaluates a separable nonlinear transformed integral using a logarithm and quadratic primitive. The source's four named steps are retained across normal generation. Adjacent KPs infer transformations, so every authored variant here supplies its map explicitly.

## 3. Components and complete banks

Each source keeps one five-choice bank profile `observed`, with displayed values in `templates.json` and the complete per-option mathematical evaluation in `source-analysis.json`. Bounds are the only source-template parameters: each is a complete inequality/integral-bound slot, and every corresponding region/limit/primitive/end-evaluation occurrence changes consistently. Linear maps and source integrands remain fixed so the original algebraic workload is preserved. Constant wrong scalar patterns in the moderate observed bank stay constant when rectangle bounds vary; their interpretation is opaque, and all observed-profile records carry evidence_only=true, eligible_for_learning=false. This does not claim recovered original error code.

Normal banks are selected as one complete family before parameters are sampled. Recipes:

| Family | Correct transformed integrand | Four wrong transformed integrands / operations |
|---|---|---|
| difference |uv/2|uv (omit inverse determinant),2uv (forward determinant),−uv/2 (reverse the two determinant products and omit the absolute value), (u²−v²)/2 (difference instead of product)|
| triangular_quadratic |(u²+2uv−3v²)/8|(u²+2uv−3v²)/4 (omit determinant), (u²+2uv−3v²)/2 (forward determinant), [2((u+v)/2)v+((u+v)/2)²]/2 (inverse sign error), [(u−v)v]/2 (omit x²)|
| product |v²−u²|2(v²−u²),4(v²−u²),(v−u)²,(v+u)²; omit/invert determinant and replace conjugate factors by repeated factors|
| exponential |e^{2u−3v}|2e^{3u−2v},e^{2u−v},e^{u+v},(1/2)e^{3u−2v}; complete source patterns, coefficient swaps/drop/naive-variable substitution, leading-coefficient factor misuse. Intentions remain inferred|
| sum_square |(3/2)u²|6u²,(3/2)(u+v)²,(3/4)(u+v)²,(9/2)u²; complete source patterns, forward determinant/wrong sum/extra half/repeated integrand coefficient|
| ratio_product |v/(3u)|v/u,−v/(3u),1/(3u),v²/(3u): omit determinant3, retain signed determinant, omit integrandv, add extrav|
| ratio_product_squared (authored hard) |v²/(3u)|v²/u,−v²/(3u),1/(3u),v³/(3u); same operations on the actual supplied map/integrand|

All choices at easy are **complete definite integrals**. Equality of full scalar values rejects the entire normal instance; nonidentical setups do not override this rule. There is no replacement from a distractor pool. Moderate/hard banks evaluate the listed wrong integrands directly, not an unrelated correct-answer perturbation. One fixed worked solution is independent of the selected wrong choice.

The evidence-only sum/product bank retains observed scalar forms with width(v), upper(v), half-upper(v), upper(u) and width(u) slots. Their authorial interpretation is unresolved; no invented missing designation is emitted and they never participate in normal practice.

## 4. Reusable templates, domains and variation

`templates.json` preserves full source prose, math blocks, answer shapes and exact source spelling. Easy changes only inequality/integral bounds; determinant, inverse, distributed-square, conjugate-product and exponent-collection stages stay structurally intact. The moderate ten-row chain is reconstructed by ordered primitive/evaluation components, reproducing its source bytes at the original bounds. Both individual logarithm endpoints and both individually evaluated quadratic/cubic endpoints precede the final collection row. No CAS-simplified duplicate rows replace these operations.

Normal easy bounds are integers−4 through 8 with widths1 through5, reflecting source signed rectangles and largest observed width5. These parameters change the assessed u,v integral limits and therefore belong in task fingerprints. The finite family has50 intervals per axis,2500 candidate rectangles per family before exact whole-bank collisions. Moderate uses u∈[1,4|9|16],v endpoints1 through 8:3×28=84 candidate tasks. Authored hard uses the same u bounds,v endpoints1 through 6:3×15=45 candidate tasks, with cubic endpoint integers through 216. Guards apply equally to explicit normal parameters and random sampling. Historical evidence may exceed normal easy width limits, but remains ineligible.

Hard is missing-source authorship: replace xy by(xy)² under the already-supplied nonlinear map, preserve the same logarithmic inner integral and four Jacobian steps, change the outer primitive to v³/3 and evaluate the two cubic components. This adds substantive power/end-evaluation bookkeeping at fixed method. No transformation inference, nonrectangular domain branch, or new integration technique is added. The unrated difference completion is authored easy; the malformed sum/product original receives only an authored replay label in metadata, with its question difficulty still absent.

Formatting normalization is limited to the moderate source double colon “as follows::” in normal output; raw observed replay preserves it. There are no proven TeX escape-byte anomalies. Natural logs retain source operator notation in the integration chain or standard \ln in answer values. Content UUIDs depend on actual prompt, fixed solution, difficulty presence, complete displayed bank and designation; seeds/order do not alter them. Mathematical fingerprints exclude bank/profile/notation aliases.
