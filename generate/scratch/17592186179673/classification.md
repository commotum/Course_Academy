# Classification

Captured database `math`, basis **1356**, lineage `01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1`; raw wrapper preserved in `source.json`. Eleven practice questions: six easy, five moderate, no hard. All are a single `selection` radio field with five whole math expressions; no field anomalies, blanks or practice plots. The canonical example is separate from these counts.

| Template / source profile | Level | Assessed response | Complete bank count | Integral arithmetic rows | Plot |
|---|---|---|---:|---:|---|
| q-124597 | easy | Circle cubic trig integral setup | 1 | 5 | none |
| q-124656 | easy | Circle quartic trig integral setup | 1 | 5 | none |
| q-124657 | easy | Ellipse reciprocal/exponential setup | 1 | 4 | none |
| q-124651 | easy | Ellipse combined cubic setup | 1 | 5 | none |
| q-124653 | easy | Circle exponential/constant setup | 1 | 6 | none |
| q-124655 | easy | Ellipse linear-form setup | 1 | 5 | none |
| q-81192 | moderate | Circle rational-form evaluated value | 1 | 10 | none |
| q-124661 | moderate | Ellipse linear-form evaluated value | 1 | 11 | none |
| q-124665 | moderate | Ellipse reciprocal-form evaluated value | 1 | 8 | none |
| q-81186 | moderate | Circle double-angle evaluated value | 1 | 10 | none |
| q-90895 | moderate | Circle constant integrand evaluated value | 1 | 8 | none |

These eleven source masks remain separate because their distributed terms, simplification rows, endpoint rows and shared prose differ. A change of source numbers would not be counted as another recovered mathematical skill. Each source bank is an explicit `observed_q-...` replay profile; all 55 choices are mapped in `source-map.json` and extraction below. Scalar distractor intent is not determined from one bank. Normal generators therefore use one separately labeled authored complete operation bank at each level.

The lesson route was traversed through `activity/first-step` and `step/next`: Introduction (17592186180392), Segments (17592186180475), Cartesian curves (17592186180393), Circles and ellipses (17592186180391). This KP uses x=a cos t, y=b sin t and tangent derivatives. Its siblings own segments and Cartesian paths. The key prerequisites are scalar line integrals over circles (3688) and ellipses (3690); the latter explicitly teaches unequal semiaxis parametrizations and tangent derivatives. No Green theorem, potentials, fundamental theorem for line integrals, flux or Cartesian-curve task is introduced.

The missing hard level is an **authored scope claim**, not an observed label: evaluate polynomial one-forms on unequal-axis quarter/half ellipses, with both cubic components nonzero, by exactly this route. Source easy q-124656 already displays the sin²t cos²t product. Source moderate q-81186 and q-124661 explicitly use double-angle identities before integrating. Hard evaluates that already-observed product using one further familiar identity sin²t cos²t=(1-cos4t)/8, plus the constant produced by the two linear terms. This bounded trigonometric reduction is the additional workload; it does not require a new integration branch. Prerequisite snapshots do not independently establish an observed hard label or an observed fourth-angle teaching row; those are explicitly authored. All questions within each level are unordered repetitions of that level's method, with no progression.

Normal easy: P=m x², Q=n xy, setup only. Normal moderate: P=m x-n y, Q=n x+h y, evaluate. Normal hard: P=m x²y-n y, Q=n x+h xy², evaluate. Integer axes 1..4; easy |m|,|n|=1..3; moderate/hard |m|,|n|=1..4; |h|=1..3; all defining coefficients nonzero. Quarter-axis starting points, CCW one or two quarter arcs. Hard axes must differ and h b²-m a² must be nonzero. These guards apply equally to sampled and explicit parameters. The whole five-choice bank must remain pairwise inequivalent; invalid instances are rejected as a unit. Source radii 1,2,sqrt(2),sqrt(3) and observed reciprocal/exponential variants remain accessible through their replay masks rather than inflated into unsupported default recipes.

Two captured statements omit endpoint regularity qualifications: q-124657 has 2/y at the starting endpoint, q-124665 has 2/x at the ending endpoint. Their displayed values are valid as **one-sided improper path integrals**, equivalently by the continuous extension of the composed tangent integrand. The one-form itself has no continuous extension there. Captured problem/solution strings are preserved exactly with this interpretation recorded outside learner content. Normal defaults are regular polynomial one-forms. Interior one-form poles are rejected even if a symbolic product might cancel them.

## Complete-integral source ambiguity and supported repair

An independent audit of every easy source option as a **whole definite integral** found one defective bank: q-124656's correct `4 int_0^pi cos²t(1-4sin²t) dt` and its wrong `4 int_0^pi sin²t(1-4cos²t) dt` both equal zero. Structural transformed-integrand fidelity does not make those unequal mathematical answers. The other polynomial options evaluate to pi/2, pi and -2pi. Raw exact source replay remains accessible only as the explicitly ambiguous `observed_q-124656` evidence profile, with its original native ID designation preserved for fidelity tests. It is not claimed mathematically unambiguous.

The minimal `repaired_q-124656` bank changes only that wrong zero-valued option to the defensible omitted-dx-contribution integral `4 int_0^pi cos²t dt = 2pi`. All other four choices, prompt, designation and full worked-solution prose/stages are unchanged. Its five values are pi/2, pi, -2pi, 2pi and 0; global c scaling preserves uniqueness. Explicit q-124656 generation defaults to this repaired bank unless its observed evidence profile is requested. Normal authored E banks also reject the whole bank on any equal definite-integral values, even if their integrands differ.

Exact whole-integral quadrature checks the polynomial source banks. Independent 70-digit quadrature checks every exponential source-bank option and finds no collisions (reported values and tolerance in source-bank audit). Raw fidelity counts are 11/11 complete banks and 55/55 choices; raw mathematical uniqueness is 10/11 banks. Repaired uniqueness is 11/11, with q-124656 preserving 4/5 raw choices. Native ID grading counts are separate and do not override the source mathematical defect.
