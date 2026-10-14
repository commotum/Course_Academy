# Template extraction

## 1. Specific source evidence

All prompts ask for the exact scalar line integral, not an integral setup. Each bank has five math radio options. Moderate prompts supply F and a counterclockwise origin-centered circle equation. Hard and unrated prompts supply Pdx+Qdy and an oriented boundary diagram. Univariate nuisances disappear under the held-coordinate cross partial; their nonzero derivatives with respect to their own coordinates are not substituted into the curl.

| ID | Original P; Q | Polar bounds | Curl | Result |
|---|---|---|---|---|
|q109119|x²y−cosx;4−xy²|0≤r≤2,0≤θ≤2π|−(x²+y²)|−8π|
|q126733|2−x²y;1+xy²|0≤r≤5,0≤θ≤2π|x²+y²|625π/2|
|q126736|sinx−2x²y;√(y+3)+2xy²|0≤r≤1,0≤θ≤2π|2(x²+y²)|π|
|q126755|4ˣ−y³+2;2/(y²+1)+x³|0≤r≤√2,0≤θ≤2π|3(x²+y²)|6π|
|q126759|(√(x+5)−y³)/3;(√(y+5)+x³)/3|0≤r≤2,0≤θ≤2π|x²+y²|8π|
|q126753|sin³x−y³;y⁴+x³|0≤r≤3,0≤θ≤2π|3(x²+y²)|243π/2|
|q126747|3ˣ+x²y;2ʸ+xy²|0≤r≤4,0≤θ≤π/3|y²−x²|−16√3|
|q126756|eˣ−2x²y;eʸ+2xy²|0≤r≤3,π/2≤θ≤π|2(x²+y²)|81π/4|
|q126758|√(5+x)−3x²y;e^(−y²)+3xy²|2≤r≤4,0≤θ≤π/2|3(x²+y²)|90π|
|q125717|√x−4x²y;eʸ+4xy²|0≤r≤2,0≤θ≤π/2|4(x²+y²)|8π, inferred|

The canonical e9550 has P=e^(−x²)−y³ and Q=e^(−y²)+x³ on the upper semicircle of radius2. The MA3627 JSON supplies readable mathematics for all canonical SVGs. It evaluates to12π. The source's first final double-integral LHS says3x²+y² instead of3(x²+y²); retain raw evidence and repair the teaching chain.

## 2. Shared pattern

Compute Qx−Py, apply Green's theorem on the positively oriented boundary, describe the region in polar coordinates, include the Jacobian r, simplify cos²θ+sin²θ=1 or cos²θ−sin²θ=cos2θ, integrate in r and then θ. One fixed worked solution is independent of which option is selected. No diagnosis is added to learner options.

## 3. Components and complete banks

bank-map.json maps every option to its original field and exact mathematical value, source-designation presence, and opaque expression recipe. HISTORICAL in the script independently transcribes the values; raw option bytes are retained in source.json and public observed:<ID> profiles. Source difficulty enums, all five options and every existing designation are preserved. A scalar alone cannot establish a wrong operation. Every historical bank remains explicitly evidence-only, with unresolved wrong-operation intentions. No arbitrary polynomial fit or scalar perturbation is promoted to learner generation.

Public raw profiles parameterize a complete nuisance component (noise1..6), whose cross partial is zero. The q126733 slot is the entire 2−x²y component, becoming(n+1)−x²y; powers are protected. Other slots multiply the complete univariate function with a visible multiplication mark. All repeated definitions and integral occurrences are masked; original values use the unit coefficient spelling. Original geometry remains fixed in these evidence profiles, so their scalar bank correctly remains fixed and nuisance changes do not count as mathematical-task variety. Correct results are derived from independently read prompt components and polar integration, not source answer lookups. Coefficient/radius/angle variation belongs to normal source-family recipes.

Normal authored bank is selected as a complete eligible operation set before sampling:

- Radial: correct; reversed curl; omitted polar Jacobian (integrate r²); omitted /4 in radial primitive; omitted one of the two equal cross-partial contributions.
- Anisotropic: correct; reversed curl; omitted chain-rule /2 in ∫cos2θ; omitted Jacobian; used sum-of-squares identity instead of the difference.

Each option is computed by its displayed method operation. Whole instances are rejected on any scalar equivalence; no first-valid replacement pool is used. Full scalar integral values establish bank validity. q126758's90π/4 and45π/2 are equivalent wrong options: raw replay retains both, normal bank replaces the historical bank wholesale with the labeled method bank.

## 4. Reusable masks, stages and bounds

Normal parameters are c (positive integer derivative magnitude1..6), s (squared outer radius1..25), inner integer radius, and θ bounds given in units ofπ. Easy narrows c1..4 and s∈{1,4,9,16,25}; supplied bounds, full disk only. Moderate full disk s∈{1,2,4,9,16,25}, with strict radius<3 for√(y+3) and radius<5 for√(x+5),√(y+5). Hard uses integral radii2..5; quarter/half sectors, first-quadrant quarter annuli, or anisotropic θ upperπ/6,π/3,2π/3. Arbitrary trig evaluation angles, holes requiring extending Green's theorem, and new integrands/methods are not introduced. An annular-sector boundary encloses a simply connected strip. Same workload bounds apply to explicit calls.

Coefficient slots cover full monomial components, quotient numerators and every complete conclusion. Normal solutions retain source common sentences and stages, including F·dr rewriting only for moderate; distinct numerator/cross derivatives; grouped Qx−Py; radial trig substitution and identity reduction; anisotropic minus/cos2θ transformation; per-family coefficient-inside/outside convention; primitive evaluation, angular bracket and arithmetic. q126755 retains its evaluated-radial integral row with an implicit integrand1 when its radial value equals1; changed radii display the actual nonunit radial value; q126736 retains its abbreviated last arithmetic. One explicitly added radial row shows individually evaluated upper and lower primitive components before their collection; it supplements the source sequence. Expressions are kept as ordered unevaluated text masks until final scalar collection.

### Source errors and minimal normal repairs

1. q126736 writes √(y+3)−2xy² instead of +2xy² in the opening rewritten integral and the Green-chain first line. The prompt/components/partials imply plus. Both normal rows use the actual prompt's Q.
2. q126758 omits3 from xy² only in the Green-chain first line. The prompt/components/partials all imply3. Normal row uses the actual prompt's Q.
3. q125717 lacks difficulty, correct ref and solution. Raw replay preserves all omissions; normal inference is8π, supported by independent integration. Its √x lacks C1 on an open neighborhood at x=0; normal changes only this irrelevant-to-curl nuisance to√(x+1), which is smooth on a neighborhood of the displayed first-quadrant sector.
4. e9550 canonical first final LHS coefficient error is retained in captured evidence and documented above; normal output uses correct factored curl.
5. Historical scalar answer values contain decoded double backslashes (verified as characters, not inferred from JSON serialization). Raw profiles retain bytes; normal options use standard single-command TeX. Raw region set braces and malformed ∮_(C) notation are preserved in evidence; normal uses escaped visible set braces and standard \oint_C.

Fidelity denominators are reported separately:10/10 raw prompts and bank shapes,50/50 option strings,9/9 present designations,9/9 present worked solutions,10/10 key-presence parity. Mathematical source validity:9/9 designated results valid;1/1 missing result inferred,9/10 unique banks,7/9 present worked solutions without errors. Normal corrected source solution count2/2, plus the authored missing solution; normal exact source prose/mathematical notation bytes are not claimed. Canonical is excluded from practice denominators.

The complete bounded domain has20 distinct easy tasks,108 moderate tasks and204 hard tasks after algebraically equivalent assessed components are deduplicated. Template noise choices and bank aliases do not inflate these counts. Every whole bank is mathematically distinct across that enumerated domain. The outer-radius sampler and explicit guard use the same documented finite sets; quarter-annulus inner radii range from1 through outer-radius−1 (maximum4).
