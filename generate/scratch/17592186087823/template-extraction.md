# Four extraction stages

## 1. Describe each source

q-26910 asks which image is y=4(6^x)-2. All five images have black arrow axes, blue curves, filled marked points; four use labelled dashed horizontal asymptotes. It is unrated, with no solution or correct reference. Complete original bank order is retained in `source-geometry.json`; original MA widget evidence is `q-26910-authoritative-widget.json`.

q-7121 asks which image is y=2(3^x)-4, easy. Correct graph is increasing, marked (0,-2), with asymptote y=-4. Wrong graphs include decreasing with the same intercept/asymptote; increasing with intercept -3; decreasing with intercept -2/asymptote 4; increasing with marked (2,-2)/asymptote -4. Its three-paragraph solution plots the base, stretch, then shift. The image choices are not interchangeable assets.

q-30270 uses integer k=5,b=6,c=2; intercept (0,7). q-170594 uses k=1.5,b=4,c=1; intercept (0,2.5), a comma before the final inline-math close. q-30269 uses k=2.5,b=1.5,c=8; intercept (0,10.5), and `$y-$axis` in the prompt. q-30873 uses k=1.5,b=10,c=-8.5; intercept (0,-7), same axis punctuation. All are moderate. Their worked sequences are exact, including Method 1's bullets and two separate displays, Method 2's four aligned rows, and the full conclusion.

Decoded TeX strings use ordinary single command backslashes and double row separators; JSON display escaping is not an anomaly. No TeX or mathematical repair is asserted. Full raw records are retained; all practice sources are replayed.

## 2. Generalize the assessed pattern

For y=k(b^x)+c with b>1 and k>1, the curve is increasing, has horizontal asymptote y=c, and y-intercept (0,k+c). Graph identification selects the image with these features. The intercept variant substitutes x=0 or applies the two transformations to (0,1). The given base is incidental to x=0 arithmetic and to marked-feature discrimination in an ungridded bank; it does not inflate task counts.

## 3. Map every original component and complete bank

The complete banks below are ordered exactly as captured. Parenthesized entries denote coordinate answers, while curves describe their labelled features and an explicit rendering recipe. Historical scalar recipes are algebraic replay hypotheses, not recovered error intent; their opacity is retained and none is selected as an authored default.

| Profile/source | Parameters k,b,c | Five complete parameterized recipes, in original order | Exact values/features |
|---|---|---|---|
| intercept_base / q-30270 | 5,6,2 | (0,b+k); (b+k,0); (0,bc); (0,k+c); (k+c,0) | (0,11); (11,0); (0,12); **(0,7)**; (7,0) |
| intercept_components / q-170594 | 1.5,4,1 | (0,c); (0,k); (0,b); (0,k+c); (0,2(k+c)) | (0,1); (0,1.5); (0,4); **(0,2.5)**; (0,5) |
| intercept_swap / q-30269 | 2.5,1.5,8 | (0,k+c+1); (k+c,0); (0,k+c); (0,c-k); (c-k,0) | (0,11.5); (10.5,0); **(0,10.5)**; (0,5.5); (5.5,0) |
| intercept_signed / q-30873 | 1.5,10,-8.5 | (0,-b); (0,-(k+c)); (0,k+c); (0,k+c+1); (0,b) | (0,-10); (0,7); **(0,-7)**; (0,-6); (0,10) |
| graph_observed / q-7121 | 2,3,-4 | k b^-x+c; b^x+c; (k+2c)b^x-c; k b^x+c; k b^(x-k)+c, marked at x=k | decreasing (0,-2), asym -4; increasing (0,-3), asym -4; decreasing (0,-2), asym 4; **increasing (0,-2), asym -4**; increasing (2,-2), asym -4 |
| graph_unrated / q-26910 | 4,6,-2 | (k+c)b^x; k b^-x+c; (k+c)b^x-c; (c-k)b^x+k; k b^x+c | increasing (0,2), unlabelled zero asymptote; decreasing (0,2), asym -2; increasing (0,4), asym 2; decreasing (0,-2), asym 4; **inferred increasing (0,2), asym -2** |

Each image recipe specifies the geometry needed for recognition; the numerical bases of historical distractor images cannot be established from their ungridded rasters. The above uses the prompt base as a documented normalization for changed-parameter plots, not an asserted recovered source equation. Source-parameter replay reuses exact original PNGs only after verifying each recipe's marked point/asymptote against the extracted asset registry. Equality of raster hashes is recorded separately from feature fidelity and numerical-base uncertainty.

Authored intercept bank: correct (0,k+c), transpose (k+c,0), omit shift (0,k), omit stretch/exponential contribution (0,c), reverse shift (0,k-c). Authored graph bank keeps the source-shaped five-member feature bank: correct; reverse input sign; omit stretch; reverse the asymptote while preserving the marked intercept; move the marked intercept horizontally to x=k. These are explicit operations on the assessed features. A nonzero curve coefficient and five inequivalent complete curves are mandatory. No first-valid distractor pool or replacement option is used.

## 4. Reusable masks, constraints and sequence

Slots are complete k,b,c values in y=k({b}^{x})±|c|, the corresponding x=0 substitution, individual product/sum displays, signed shift wording, all coordinate tuples, asymptote equations, and conclusion formula. They are constructed as components; no blind global replacement of short source strings occurs. Source-specific comma/axis layouts are conditional. Math remains independent of which option is chosen.

Graph solution: (1) base curve and plot, (2) stretching sentence with (0,1)→(0,k), unchanged zero asymptote and plot, (3) signed shift sentence with (0,k)→(0,k+c), asymptote 0→c and plot. Intercept solution: Method 1 base intercept bullet, stretch bullet/product display, shift bullet/sum display; Method 2 introduction, substitute x=0, evaluate b^0, evaluate multiplication, collect sum; full equation and intercept conclusion. Exact source prose is replay-tested in its entirety.

Normal bounds: bases {1.5,2,3,4,6,10}; easy integer k=2..8 and nonzero integer c=-8..8; moderate k=1.5..8 and nonzero c=-8.5..8.5 in half steps; hard k∈{1.5,2.5,3.5,4.5,5.5,6.5}, c∈{±0.5,±1.5,…,±8.5}. Every explicit call obeys the same level guard as sampling. Every member is computed before whole-instance collision/domain rejection. The finite meaningful task counts are easy 108, moderate 441, hard 108, excluding base aliases, layouts and banks. Graph fingerprints include marked-feature transformation parameters and actual difficulty; intercept fingerprints include the scale/shift arithmetic even where sums coincide. Banks/profile spellings belong only to content identity. Seed/order changes do not alter identity.

The sole missing observed designation is q-26910. Independent mathematics gives intercept (0,2), asymptote -2 and growth, matching its fifth captured image. Raw replay deliberately omits its original missing attributes and is ungraded/ineligible; inferred correctness is metadata, not a counted observed designation. No source values are excluded.

Normal presentation masks are served by default as `intercept`, `intercept_comma`, and `intercept_axis`, all with the full authored operation bank. They are selected before numerical sampling. Public default coverage is exercised across 36 seeds; each explicit mask has seed-independent content identity at fixed parameters and the same task fingerprint as its aliases. These are presentation variants, not new methods or inflated task counts.
